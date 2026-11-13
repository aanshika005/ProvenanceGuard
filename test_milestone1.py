"""Milestone 1 regression checks; no model download required."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app
import audit
import config
import detector


class MilestoneOneTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.paths = patch.multiple(config, LOG_DIR=Path(self.tmp.name),
                                    AUDIT_LOG=Path(self.tmp.name) / 'audit.jsonl')
        self.paths.start()
        self.addCleanup(self.paths.stop)
        app.limiter.reset()
        self.client = app.app.test_client()

    @patch.object(detector, 'model_signal', return_value=0.4)
    def test_flood_and_creator_isolation(self, model):
        codes = [self.client.post('/submit', json={
            'text': 'Several sentences of writing.',
            'creator_id': ' writer ' if i % 2 else 'writer',
        }).status_code for i in range(15)]
        self.assertEqual(codes, [201] * 10 + [429] * 5)
        self.assertEqual(model.call_count, 10)
        self.assertEqual(sum(e.get('reason') == 'rate_limited'
                             for e in audit.read_entries()), 5)
        self.assertEqual(self.client.post('/submit', json={
            'text': 'Another writer.', 'creator_id': 'other',
        }).status_code, 201)
        self.assertTrue(self.client.get('/health').json['rate_limiting'])

    @patch.object(detector, 'model_signal', return_value=0.4)
    def test_three_decisions_read_back(self, model):
        responses = [self.client.post('/submit', json={
            'text': text, 'creator_id': 'log_writer',
        }).json for text in ['First piece.', 'Second piece.', 'Third piece.']]
        entries = self.client.get('/log').json['entries']
        self.assertEqual(len(entries), 3)
        required = {'timestamp', 'content_id', 'creator_id', 'guess',
                    'model_score', 'style_score', 'combined_score', 'label', 'status'}
        for response, entry in zip(responses, entries):
            self.assertTrue(required <= entry.keys())
            self.assertTrue(all(entry[k] is not None for k in required))
            self.assertEqual(response['content_id'], entry['content_id'])
            self.assertEqual(response['confidence'], entry['combined_score'])

    def test_route_rejections_are_logged(self):
        cases = [({'data': 'plain'}, 415),
                 ({'data': '{', 'content_type': 'application/json'}, 400),
                 ({'json': []}, 400),
                 ({'json': {'creator_id': 'writer'}}, 400),
                 ({'json': {'text': 'x' * 20001, 'creator_id': 'writer'}}, 400),
                 ({'json': {'text': 'A piece.', 'creator_id': ''}}, 400)]
        for kwargs, expected in cases:
            self.assertEqual(self.client.post('/submit', **kwargs).status_code, expected)
        for exc, expected in [(ValueError(), 400), (detector.DetectorUnavailable(), 503)]:
            with patch.object(detector, 'model_signal', side_effect=exc):
                self.assertEqual(self.client.post('/submit', json={
                    'text': 'Some writing.', 'creator_id': 'errors',
                }).status_code, expected)
        entries = self.client.get('/log').json['entries']
        self.assertEqual(len(entries), 8)
        self.assertTrue(all(e['status'] == 'rejected' for e in entries))
        self.assertEqual([e['http_status'] for e in entries], [415] + [400] * 6 + [503])

    @patch.object(detector, 'model_signal', return_value=0.4)
    def test_daily_limit_survives_minute_window(self, model):
        # Advance the storage clock between batches without waiting in real time.
        import time
        base = time.time()
        for batch in range(10):
            with patch('time.time', return_value=base + batch * 61):
                for _ in range(10):
                    self.assertEqual(self.client.post('/submit', json={
                        'text': 'Daily submission.', 'creator_id': 'daily',
                    }).status_code, 201)
        with patch('time.time', return_value=base + 610):
            self.assertEqual(self.client.post('/submit', json={
                'text': 'Over daily allowance.', 'creator_id': 'daily',
            }).status_code, 429)


if __name__ == '__main__':
    unittest.main()
