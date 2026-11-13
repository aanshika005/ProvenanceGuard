# Provenance Guard

A local text-assessment service using GPT-2 predictability and writing-style measurements. Scores describe AI-like patterns and do not establish authorship.

## Running Locally

See [RUNNING.md](RUNNING.md) for full setup instructions.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python test.py
python detector.py
PORT=5001 python app.py
```

The detector downloads its model on first use. Port 5001 avoids the macOS AirPlay/AirTunes conflict encountered on port 5000. In another terminal:

```bash
curl -X POST http://127.0.0.1:5001/ping \
  -H 'Content-Type: application/json' \
  -d '{"message":"hello"}'
```

**Repository:** https://github.com/aanshika005/ProvenanceGuard

---

## What This Does
Provenance Guard is a local web service that assesses text using two signals: predictability under a language model and measurable writing-style patterns.
<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->
### Submission Path
A submission follows this path:

1. **Receive the request — `app.py::submit`.** Accept the writer’s text and creator ID through `POST /submit`.
2. **Validate the input.** Check that the body is a JSON object, the text is a nonempty string, and the creator ID is valid. Return a clear error for invalid input.
3. **Calculate the model signal.** Use `detector.py::model_signal` to measure predictability.
4. **Calculate the style signal.** Use `stylometry.py::style_signal` to measure textual shape.
5. **Combine the signals — `scoring.py::combine_signals`.** Calculate one combined score. Higher scores indicate more AI-like patterns.
6. **Choose a label — `scoring.py::score_to_label`.** Map the score to `human`, `unsure`, or `ai`, accompanied by a reader-facing explanation.
7. **Assign an ID, log, and return.** Generate a unique content ID and record the timestamp, content ID, creator ID, both signal scores, combined score, guess, label, and status. Return the decision to the caller. `/appeal` later uses the same ID to append an `under_review` event while preserving the original decision.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
The predictability of the text under a local language model, GPT-2 by default. `detector.py` calculates perplexity and converts it to a score between 0 and 1. Lower perplexity produces a higher AI-like score.

**Why that might differ between human and AI writing:**
AI-generated text may use predictable wording and common continuations. Human writing may contain more unexpected word choices and transitions.

**What it can't see:**
Predictability does not establish authorship. A person writing in simple, conventional English may receive a high AI-like score, while unusually worded AI text may receive a low score. The model also processes at most the configured 400 tokens, so later content does not affect this signal.

### Signal two — the style signal

**What it measures:**
The textual shape of a submission using:
- Sentence-length variation.
- Unique words relative to total words.
- Punctuation relative to text length.

**Implemented measurements and normalization:**

- Sentence spread is the sample standard deviation of sentence word counts divided by their mean. Its AI-like contribution is `1 - min(spread / 1.0, 1.0)`.
- Type-token ratio is unique lowercase word tokens divided by total word tokens. Its AI-like contribution is `1 - type_token_ratio`.
- Punctuation density is the number of characters in the implementation's punctuation set divided by all characters. Its AI-like contribution is `1 - min(density / 0.05, 1.0)`.

`style_signal = 0.5 * spread_ai + 0.3 * vocabulary_ai + 0.2 * punctuation_ai`, clamped to [0, 1] and rounded to four decimals. Fewer than 20 word tokens or fewer than two nonempty sentences returns 0.5. The scales and directions are heuristic choices, not calibrated authorship probabilities. The simple sentence splitter can split abbreviations, and the word tokenizer is limited to ASCII letters, digits, and apostrophes.

**Why that might differ between human and AI writing:**
AI-generated prose may have more uniform sentence lengths and recurring stylistic patterns. Human writing may vary more in sentence structure, vocabulary, and punctuation.

**What it can't see:**
Style measurements do not understand meaning or establish authorship. Typos, sentence splitting, and inserted quotations can change the measurements without changing who wrote the text. Vocabulary ratios also depend on text length.

### The combining rule
The current combining rule in `scoring.py::combine_signals` uses equal weights:

    combined_score = 0.5 * model_score + 0.5 * style_score

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take the average of the model signal and the style signal, giving each equal influence. Both scores range from 0 to 1, with higher scores indicating more AI-like patterns. When the signals strongly disagree, their average moves toward the unsure range.

**The numbers:**
combined_score = 0.5 * model_score + 0.5 * style_score

- Model signal weight: **50%**
- Style signal weight: **50%**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

For the close-elections report paragraph, the model score was **0.5955** and the style score was **0.3116**, a difference of **0.2839**. Their average was **0.45355**, producing `unsure`. The model leaned toward AI-like predictability while the style signal leaned toward human-like shape. The recorded response appears below.


---

### Tracing a False Positive

The following scenario is hypothetical and describes the planned behavior, not an actual test result.

A student submits a paragraph they wrote themselves using simple vocabulary and regular sentence structures. The model signal gives it **0.85** because its wording is predictable. Suppose the completed style signal gives it **0.55**.

With equal weights:

```text
combined_score = 0.5 * 0.85 + 0.5 * 0.55
               = 0.70
```

With the original AI threshold of **0.65**, this hypothetical score would incorrectly classify the student's work as AI. The current threshold is **0.70**, introduced in Milestone 5.

The proposed label says:

> This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.

The student can challenge the decision through `/appeal`, providing the submission's `content_id` and an explanation. The service records the appeal and marks the item as `under_review`, preserving the original decision.

This scenario guides my threshold choices. I would prioritize reducing false accusations against genuine writers, accepting that a wider unsure range could allow more AI-generated text to avoid a confident AI label. Actual threshold changes will need evidence from testing.

### Endpoint Contracts

These contracts describe the implemented success and validation responses. Rate limiting is active on `/submit`: 10 submissions per minute and 100 per day per creator, with the caller’s address used when no usable creator ID is provided.

#### POST /submit

Assesses a piece of text and records the decision.

**Request**

Send a JSON object with `Content-Type: application/json`:

```json
{
  "text": "The writing to assess.",
  "creator_id": "writer_123"
}
```

| Field | Type | Requirement |
|---|---|---|
| `text` | string | Required; must contain non-whitespace text. Maximum: 20,000 characters. |
| `creator_id` | string | Required; must contain non-whitespace text. Maximum: 100 characters. |

**Successful response — HTTP 201**

The following values illustrate the hypothetical false positive:

```json
{
  "content_id": "unique-content-id",
  "guess": "ai",
  "confidence": 0.70,
  "model_score": 0.85,
  "style_score": 0.55,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "status": "decided"
}
```

| Field | Meaning |
|---|---|
| `content_id` | Unique identifier connecting the decision to any later appeal. |
| `guess` | One of `human`, `unsure`, or `ai`. |
| `confidence` | Combined AI-like score between 0 and 1. This name is retained for compatibility with the supplied runners; it is not a calibrated probability of authorship. |
| `model_score` | Model signal between 0 and 1; higher means more AI-like. |
| `style_score` | Style signal between 0 and 1; higher means more AI-like. |
| `label` | Explanation displayed to the writer. |
| `status` | `decided` when the initial decision is recorded. |

**Error responses**

| HTTP status | Error | Meaning |
|---|---|---|
| 400 | `invalid_input` | Malformed JSON, a non-object body, or missing, empty, incorrectly typed, or oversized fields. |
| 415 | `unsupported_media_type` | The request is not sent as JSON. |
| 429 | `rate_limited` | The active submission limit has been exceeded. |
| 503 | `detector_unavailable` | The model cannot produce a score. |

All errors return a JSON object containing `error` and `message`:

```json
{
  "error": "invalid_input",
  "message": "The text field must be a nonempty string."
}
```

#### POST /appeal

Records a writer's challenge to an existing decision.

**Request**

Send a JSON object with `Content-Type: application/json`:

```json
{
  "content_id": "unique-content-id",
  "reasoning": "I wrote this myself and have earlier drafts."
}
```

| Field | Type | Requirement |
|---|---|---|
| `content_id` | string | Required; must identify an existing decision. |
| `reasoning` | string | Required; must contain non-whitespace text. Maximum: 5,000 characters. |

**Successful response — HTTP 200**

```json
{
  "content_id": "unique-content-id",
  "status": "under_review",
  "message": "Your appeal has been recorded."
}
```

| Field | Meaning |
|---|---|
| `content_id` | Identifier of the decision being challenged. |
| `status` | `under_review` after the appeal is recorded. |
| `message` | Confirmation displayed to the writer. |

The service retrieves the creator ID from the original decision and appends an appeal event containing the explanation. It preserves the original scores, guess, and label. A repeated valid appeal records the additional explanation while keeping the item `under_review`.

**Error responses**

| HTTP status | Error | Meaning |
|---|---|---|
| 400 | `invalid_input` | Malformed JSON, a non-object body, or missing, empty, incorrectly typed, or oversized fields. |
| 404 | `content_not_found` | No decision exists for the supplied content ID. |
| 415 | `unsupported_media_type` | The request is not sent as JSON. |

Errors use the same `error` and `message` structure as `/submit`.

An appeal does not automatically reverse the decision. This initial design does not authenticate callers, so a creator ID or content ID alone does not prove the caller's identity.

---

## Label Variants

These are the current ranges after the Milestone 5 change. Earlier examples and before-run results used an AI threshold of 0.65.

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 ≤ score ≤ 0.35 | This text appears likely to have been written by a person. This assessment is not proof of authorship. |
| unsure | 0.35 < score < 0.70 | We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use. |
| high-confidence AI | 0.70 ≤ score ≤ 1.00 | This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review. |

**Why I worded the "unsure" one this way:**

The wording communicates uncertainty without accusing the writer. Weak or conflicting signals do not establish AI use, and a genuine writer may receive this result.


### Standalone Detector Tests

Recorded standalone readings; the full input paragraphs and terminal transcripts are not included here.

| Input | Perplexity | Model score |
|---|---|---|
| Unedited AI-generated paragraph | 27.2 | 0.6910 |
| My own human-written paragraph | 44.5 | 0.5044 |
| AI-generated paragraph I edited | 18.5 | 0.8056 |

These scores measure predictability and do not establish authorship.


### Recorded Signal Comparison and Label Coverage

| Test input | Model score | Style score | Combined score | Returned label |
|---|---:|---:|---:|---|
| AI-assisted library paragraph | 0.8272 | 0.6206 | 0.7239 | `ai` |
| Close-elections report paragraph (authorship not verified here) | 0.5955 | 0.3116 | 0.45355 | `unsure` |
| AI-generated photocopier narrative | 0.2758 | 0.1406 | 0.2082 | `human` |

## Sample Run

These samples were recorded before Milestone 5, when the AI threshold was 0.65. They are kept as the original results; the current AI threshold is 0.70.

### AI Label: Submission and Appeal

#### Submission

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"Yesterday I went to the library to finish my assignment. I spent most of the afternoon reviewing my notes. Before leaving, I checked out a book for next week.","creator_id":"writer_123"}'
```

**Response — HTTP 201 Created:**

```json
{
  "confidence": 0.7239,
  "content_id": "166a7106-1f39-4795-8289-0ef9967ea77c",
  "guess": "ai",
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "model_score": 0.8272,
  "status": "decided",
  "style_score": 0.6206
}
```

The combined score is the average of the two signals:

```text
0.5 × 0.8272 + 0.5 × 0.6206 = 0.7239
```

This exceeds the then-current AI threshold of 0.65, producing the `ai` guess. The `confidence` field contains the combined AI-like score, not a calibrated probability of authorship. This test paragraph was supplied by an AI assistant and is not evidence of a false positive on human writing.

#### Appeal

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"166a7106-1f39-4795-8289-0ef9967ea77c","reasoning":"I wrote this myself and would like the assessment reviewed."}'
```

**Response — HTTP 200 OK:**

```json
{
  "content_id": "166a7106-1f39-4795-8289-0ef9967ea77c",
  "message": "Your appeal has been recorded.",
  "status": "under_review"
}
```

The reasoning above was used to test the appeal endpoint; it does not establish the test paragraph's authorship.

#### Audit Log After the Appeal

**Request:**

```bash
curl "http://127.0.0.1:5001/log?limit=2"
```

**Response:**

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.7239,
      "content_id": "166a7106-1f39-4795-8289-0ef9967ea77c",
      "creator_id": "writer_123",
      "guess": "ai",
      "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": 0.6206,
      "timestamp": "2026-11-04T06:50:05+00:00"
    },
    {
      "content_id": "166a7106-1f39-4795-8289-0ef9967ea77c",
      "creator_id": "writer_123",
      "event": "appeal",
      "reasoning": "I wrote this myself and would like the assessment reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-04T06:52:00+00:00"
    }
  ]
}
```

The log preserves the original decision and appends an appeal event with the same content ID. The latest event records the item as `under_review`.


### Unsure Label: Submission and Appeal

#### Submission

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"This report explores the real-life impact of some of these close elections. Even though millions of Americans vote in presidential elections, the winner can be elected by just a handful of voters—less than the attendance for a baseball game or concert. This report examines examples of the policy impacts that these few votes can have, including how 312 votes cast in one state helped more than 40 million Americans access affordable health care, how 321 votes cast in one state legislative race in Minnesota helped shape the state’s laws, and how party control of the Virginia House of Delegates came down to a tie in one legislative race—meaning just one more person showing up to vote could have decided party control. Finally, the report discusses the importance of local elections and why voting in these elections is extremely powerful.","creator_id":"writer_124"}'
```

**Response — HTTP 201 Created:**

```json
{
  "confidence": 0.45355,
  "content_id": "6f4e9bda-2694-452d-9380-f918bb474ef5",
  "guess": "unsure",
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "model_score": 0.5955,
  "status": "decided",
  "style_score": 0.3116
}
```

The combined score was calculated using equal weights:

```text
0.5 × 0.5955 + 0.5 × 0.3116 = 0.45355
```

The score falls within the then-current unsure range: 0.35 < score < 0.65. The `confidence` field contains the combined AI-like score, not a calibrated probability of authorship.

#### Appeal

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"6f4e9bda-2694-452d-9380-f918bb474ef5","reasoning":"I wrote this myself and would like the assessment reviewed."}'
```

**Response — HTTP 200 OK:**

```json
{
  "content_id": "6f4e9bda-2694-452d-9380-f918bb474ef5",
  "message": "Your appeal has been recorded.",
  "status": "under_review"
}
```

#### Audit Log After the Appeal

**Request:**

```bash
curl "http://127.0.0.1:5001/log?limit=2"
```

**Response:**

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.45355,
      "content_id": "6f4e9bda-2694-452d-9380-f918bb474ef5",
      "creator_id": "writer_124",
      "guess": "unsure",
      "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
      "model_score": 0.5955,
      "status": "decided",
      "style_score": 0.3116,
      "timestamp": "2026-11-04T06:59:18+00:00"
    },
    {
      "content_id": "6f4e9bda-2694-452d-9380-f918bb474ef5",
      "creator_id": "writer_124",
      "event": "appeal",
      "reasoning": "I wrote this myself and would like the assessment reviewed.",
      "status": "under_review",
      "timestamp": "2026-11-04T07:00:27+00:00"
    }
  ]
}
```

The original decision is preserved. A separate appeal event records the reasoning and `under_review` status using the same content ID. This demonstrates that the appeal was recorded; it does not establish authorship or reverse the original assessment.

### Human Label: Submission and Appeal

The following AI-generated paragraph received a `human` label. This demonstrates that the label is reachable, while also showing a false negative.

#### Submission

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/submit \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "text": "By 6:43 a.m., the photocopier had swallowed page seventeen, somebody had misplaced the brass key to the equipment cupboard, and Meera was balancing a cracked blue mug on a stack of unsigned reimbursement forms. Then the lights flickered. Twice. Outside, a delivery driver in mismatched gloves insisted that twelve kilograms of aubergines belonged to our department; his receipt, unfortunately, named a veterinary clinic in another postcode. Nobody knew what to do. I fetched the caretaker, who examined the cartons, muttered something about Thursday, and disappeared down the stairwell carrying a single aubergine. The photocopier remained unconvinced.",
  "creator_id": "calibration_ai_specific"
}
JSON
```

**Response — HTTP 201 Created:**

```json
{
  "confidence": 0.2082,
  "content_id": "6fc5ba67-6be4-4ba9-9982-fcd86d9e3536",
  "guess": "human",
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "model_score": 0.2758,
  "status": "decided",
  "style_score": 0.1406
}
```

The combined score was:

```text
0.5 × 0.2758 + 0.5 × 0.1406 = 0.2082
```

Because the score was below 0.35, the system returned `human`. The `confidence` field represents the combined AI-like score, not a calibrated probability of authorship.

#### Appeal

**Request:**

```bash
curl -i -X POST http://127.0.0.1:5001/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id":"6fc5ba67-6be4-4ba9-9982-fcd86d9e3536","reasoning":"This paragraph was AI-generated but received a human label. Please review the assessment."}'
```

**Response — HTTP 200 OK:**

```json
{
  "content_id": "6fc5ba67-6be4-4ba9-9982-fcd86d9e3536",
  "message": "Your appeal has been recorded.",
  "status": "under_review"
}
```

#### Audit Log After the Appeal

**Request:**

```bash
curl "http://127.0.0.1:5001/log?limit=2"
```

**Response:**

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.2082,
      "content_id": "6fc5ba67-6be4-4ba9-9982-fcd86d9e3536",
      "creator_id": "calibration_ai_specific",
      "guess": "human",
      "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
      "model_score": 0.2758,
      "status": "decided",
      "style_score": 0.1406,
      "timestamp": "2026-11-04T07:18:31+00:00"
    },
    {
      "content_id": "6fc5ba67-6be4-4ba9-9982-fcd86d9e3536",
      "creator_id": "calibration_ai_specific",
      "event": "appeal",
      "reasoning": "This paragraph was AI-generated but received a human label. Please review the assessment.",
      "status": "under_review",
      "timestamp": "2026-11-04T07:21:35+00:00"
    }
  ]
}
```

The log preserves the original decision and appends an appeal event with the same content ID. The latest event records the item as `under_review`; the appeal does not automatically reverse the original assessment.

---

## How I Used AI

### Moment 1: Building the Submission Endpoint

- **What I asked for:** Help completing Milestone 3 and understanding where to replace the unfinished `/submit` handler.
- **What came back:** A hardcoded response for checking the route, followed by suggested code for validation, calling the model, generating a content ID, and audit logging.
- **What I changed:** I replaced the unfinished handler with the assisted implementation and tested it using `curl`. I verified that the response and log contained the same content ID and model score. Later I connected the style signal, combined score, and final labels.

### Moment 2: Testing Label Reachability

- **What I asked for:** A paragraph that might produce a human label after earlier submissions returned AI or unsure.
- **What came back:** An AI-generated narrative with unusual details and varied sentence lengths, without a guarantee of its classification.
- **What I changed:** I submitted it as calibration text and recorded model score 0.2758, style score 0.1406, and combined score 0.2082. I documented the human result as a false negative as well as evidence of label reachability. I then tested an appeal explicitly stating that the paragraph was AI-generated.

## Evaluation Status and Limitations

The five acceptance targets and reasons are in [criteria.md](criteria.md). All five criteria were run three times before and after the threshold change. Before the change, criteria 1 and 2 were MISSED and criteria 3–5 were MET. After the change, criteria 1–3 were MISSED and criteria 4–5 were MET. The run logs and JSON output below record those results.

Original decision and appeal events use different audit schemas. Submission validation errors and detector failures are recorded as audit rejection entries.

The scores are sensitive to wording and textual shape. The AI-generated narrative receiving a human label demonstrates that these signals cannot establish provenance. The service does not authenticate creator IDs or appeal callers, and review is recorded rather than automatically resolved.



<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 100 per day, enabled by default in `config.py`.

**Why those numbers and not others:** A writer can submit several revisions in
one sitting and return throughout the day. Ten per minute permits that burst;
100 per day prevents a script from collecting a thousand threshold probes from
one creator in a day. Rejected attempts also consume the allowance.

**What a caller counts as:** A trimmed `creator_id`, falling back to the remote
address for missing or invalid IDs. Different creators have separate allowances.
Creator IDs are self-reported: rotating IDs can bypass this policy. The in-memory
backend resets on restart and does not share counts between service processes.

**The run of status codes when I pushed past it:**

```text
201 201 201 201 201 201 201 201 201 201 429 429 429 429 429
```

Successful submissions return `201 Created` in this service.

### Milestone 1 audit verification

Every decision records `timestamp`, `content_id`, `creator_id`, `guess`,
`model_score`, `style_score`, `combined_score`, `label`, and `status`. The stored
scores, label, and identifiers let a reader reconstruct the reported decision.
Rejections have `status: rejected`, a reason, HTTP status, and route; rate-limit
rejections also record the breached limit. They have no scores because scoring
did not produce a decision. Appeals remain separate append-only events.

The flood test accepted the first 10 submissions and blocked the next five.
All five blocked requests showed up in the log. I also submitted three different
pieces of text and checked that each decision had all nine fields. A request
with no text returned `400` and was logged too.

One decision inspected by eye in `logs/audit.jsonl`:

```json
{
  "combined_score": 0.56335,
  "content_id": "d281157c-f125-4868-b30c-612d747a1004",
  "creator_id": "milestone1_writer",
  "guess": "unsure",
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "model_score": 0.6867,
  "status": "decided",
  "style_score": 0.44,
  "timestamp": "2026-11-13T05:30:51+00:00"
}
```

The model score `0.6867` and style score `0.44` combine with the configured equal
weights to `0.56335`, inside the then-current unsure band (0.35–0.65). The entry records that
result and its full label alongside the creator, content ID, time, and status.


---

## Attack Run — Before

Ran all 56 attacks against the unchanged service before applying any fixes.
Rate limiting was enabled at 10 submissions per minute and 100 per day.

```bash
python run_attacks.py --set attack_set --label before
```

**56/56 inputs sent; 0 skipped, 0 timeouts, 0 server errors.** The response
statuses were 39 × `201`, 13 × `400`, 2 × `415`, and 2 × `429`.
All 56 audit entries were read back through `GET /log`.

Evasion counts as BROKE when AI text receives a human or unsure label.
False positives count as BROKE when human text receives an AI label.
Prompt-injection verdicts follow the requested effect; PI02 obtained a human
label, but this does not prove its instructions were followed. Non-prose inputs
receiving authorship labels count as BROKE. MF07's Arabic text was accepted
without crashing; its label accuracy is unverified. Flood requests hold when
the first ten succeed and later requests return `429`.

**Counts: 37 HELD, 19 BROKE.**

| Family | Inputs | HELD | BROKE |
|---|---:|---:|---:|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 3 | 5 |
| prompt_injection | 6 | 5 | 1 |
| malformed | 20 | 16 | 4 |
| flood_same_creator | 12 | 12 | 0 |

The supplied flood set has 12 rows: ten returned `201`, then two returned `429`.

Full results: [attack report](results/attack_run_2026-11-12_2144_before.md) and
[complete audit extract](results/milestone2_audit_extract.json).

### Every attack and its outcome

| ID | HTTP | Guess | Combined score | Verdict | Reason |
|---|---:|---|---:|---|---|
| EV01 | 201 | unsure | 0.37750 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV02 | 201 | unsure | 0.41320 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV03 | 201 | unsure | 0.54470 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV04 | 201 | unsure | 0.59490 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV05 | 201 | human | 0.31565 | BROKE | AI-labelled input avoided the AI label: returned human. |
| EV06 | 201 | unsure | 0.39885 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV07 | 201 | unsure | 0.54310 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV08 | 201 | unsure | 0.37260 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV09 | 201 | unsure | 0.56100 | BROKE | AI-labelled input avoided the AI label: returned unsure. |
| EV10 | 201 | ai | 0.83200 | HELD | AI-labelled input retained an AI label. |
| FP01 | 201 | unsure | 0.54980 | HELD | No AI accusation; unsure is an acceptable abstention, not proof of human authorship. |
| FP02 | 201 | ai | 0.66915 | BROKE | Human-labelled writing received an AI label. |
| FP03 | 201 | ai | 0.67860 | BROKE | Human-labelled writing received an AI label. |
| FP04 | 201 | ai | 0.66280 | BROKE | Human-labelled writing received an AI label. |
| FP05 | 201 | ai | 0.69735 | BROKE | Human-labelled writing received an AI label. |
| FP06 | 201 | ai | 0.66110 | BROKE | Human-labelled writing received an AI label. |
| FP07 | 201 | unsure | 0.63570 | HELD | No AI accusation; unsure is an acceptable abstention, not proof of human authorship. |
| FP08 | 201 | unsure | 0.41115 | HELD | No AI accusation; unsure is an acceptable abstention, not proof of human authorship. |
| PI01 | 201 | unsure | 0.39435 | HELD | Demanded human classification; returned unsure. |
| PI02 | 201 | human | 0.24620 | BROKE | Obtained human label, but requested score 0.02 was not returned. This is a classification failure, not evidence instructions were obeyed. |
| PI03 | 201 | unsure | 0.53790 | HELD | Asked for verified-author pass-through; returned ordinary unsure decision. |
| PI04 | 201 | unsure | 0.45585 | HELD | Returned fixed unsure label; injected script did not appear in label or audit record. Browser execution was not tested. |
| PI05 | 201 | unsure | 0.45720 | HELD | Returned ordinary scores; audit record remained valid JSON with actual guess and score, without injected note. |
| PI06 | 201 | unsure | 0.52450 | HELD | Verification request did not bypass either signal; returned ordinary unsure decision with both scores. |
| MF01 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| MF02 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| MF03 | 201 | human | 0.25000 | BROKE | Control-character or non-prose input received an authorship label instead of rejection or abstention. |
| MF04 | 201 | human | 0.25560 | BROKE | Control-character or non-prose input received an authorship label instead of rejection or abstention. |
| MF05 | 201 | ai | 0.74880 | BROKE | Control-character or non-prose input received an authorship label instead of rejection or abstention. |
| MF06 | 201 | ai | 0.74845 | BROKE | Control-character or non-prose input received an authorship label instead of rejection or abstention. |
| MF07 | 201 | ai | 0.70320 | HELD | Arabic text was accepted without crashing. Language alone is not malformed input; accuracy of its AI label is unverified. |
| MF08 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ01 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ02 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ03 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ04 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ05 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ06 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ07 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ08 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ09 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| RQ10 | 415 | — | — | HELD | Rejected invalid request with 415; audit reason: unsupported_media_type. |
| RQ11 | 415 | — | — | HELD | Rejected invalid request with 415; audit reason: unsupported_media_type. |
| RQ12 | 400 | — | — | HELD | Rejected invalid request with 400; audit reason: invalid_input. |
| FL01_01 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_02 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_03 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_04 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_05 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_06 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_07 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_08 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_09 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_10 | 201 | human | 0.26435 | HELD | Within the configured first-ten allowance; scoring succeeded. |
| FL01_11 | 429 | — | — | HELD | Over the ten-per-minute allowance; 429 rejection recorded in audit log. |
| FL01_12 | 429 | — | — | HELD | Over the ten-per-minute allowance; 429 rejection recorded in audit log. |

### Ten audit log entries from the run

Selected to expose the failures: EV05's human-labelled evasion; FP02–FP06's
five false accusations; PI02's human result; MF04/MF06's non-prose decisions;
and the first rejected flood request. These are verbatim parsed entries from
`GET /log`, not reconstructed scores. The rejection has fewer fields because
no decision was made.

```json
[
  {
    "combined_score": 0.31565,
    "content_id": "026d038d-1ae9-4efd-92c7-a353732ee065",
    "creator_id": "attacker_EV05",
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "model_score": 0.3212,
    "status": "decided",
    "style_score": 0.3101,
    "timestamp": "2026-11-13T05:43:59+00:00"
  },
  {
    "combined_score": 0.66915,
    "content_id": "4ea770ae-e71d-4791-8cb0-a138391b0ca0",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.7387,
    "status": "decided",
    "style_score": 0.5996,
    "timestamp": "2026-11-13T05:44:00+00:00"
  },
  {
    "combined_score": 0.6786000000000001,
    "content_id": "f768a4ca-c974-4351-b383-2dc09f1485dc",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.8051,
    "status": "decided",
    "style_score": 0.5521,
    "timestamp": "2026-11-13T05:44:01+00:00"
  },
  {
    "combined_score": 0.6628000000000001,
    "content_id": "8a1bcf63-f809-4807-8c3c-1bcda514e059",
    "creator_id": "attacker_FP04",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.8329,
    "status": "decided",
    "style_score": 0.4927,
    "timestamp": "2026-11-13T05:44:01+00:00"
  },
  {
    "combined_score": 0.6973499999999999,
    "content_id": "309a8106-166e-467e-a07f-2f352315e3eb",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.8005,
    "status": "decided",
    "style_score": 0.5942,
    "timestamp": "2026-11-13T05:44:01+00:00"
  },
  {
    "combined_score": 0.6611,
    "content_id": "c733ba9e-a250-4e3a-9a81-c16d5eacdf46",
    "creator_id": "attacker_FP06",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.8814,
    "status": "decided",
    "style_score": 0.4408,
    "timestamp": "2026-11-13T05:44:01+00:00"
  },
  {
    "combined_score": 0.24619999999999997,
    "content_id": "1f530a0c-378e-4696-94d7-ac791c6ac343",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "model_score": 0.2044,
    "status": "decided",
    "style_score": 0.288,
    "timestamp": "2026-11-13T05:44:02+00:00"
  },
  {
    "combined_score": 0.2556,
    "content_id": "78e1134d-2cc2-4fc6-8594-ab821864d33e",
    "creator_id": "attacker_MF04",
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "model_score": 0.0112,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-13T05:44:03+00:00"
  },
  {
    "combined_score": 0.7484500000000001,
    "content_id": "235681e2-e4a3-44e4-adad-fb880ba6a397",
    "creator_id": "attacker_MF06",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.9969,
    "status": "decided",
    "style_score": 0.5,
    "timestamp": "2026-11-13T05:44:04+00:00"
  },
  {
    "creator_id": "attacker_flood",
    "event": "rejected",
    "http_status": 429,
    "limit": "10 per 1 minute",
    "reason": "rate_limited",
    "route": "/submit",
    "status": "rejected",
    "timestamp": "2026-11-13T05:44:05+00:00"
  }
]
```

### The single worst outcome

**FP03: a person writing carefully in a second language was labelled AI.**
Its combined score was `0.6786000000000001`, above the `0.65` AI threshold.
This is the outcome I would least want to explain: the writer's straightforward
account of moving to a new country is precisely the kind of careful prose the
model's predictability signal can penalize. The label offers review, but the
false accusation has already happened. FP05 scored even higher (`0.69735`),
showing that this is not confined to one writing style.


---

## Run Log and Verdicts

```bash
python run_eval.py --label before
```

All five scenarios ran three times without changing the service or inputs.
The first two scenarios use the ten human passages supplied for this test and
ten unedited AI paragraphs on matching topics.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human writing | ≤1/10 AI and ≥5/10 human | 0/10 AI; 1/10 human | 0/10 AI; 1/10 human | 0/10 AI; 1/10 human | MISSED |
| 2. Human–AI score separation | Mean AI score − mean human score ≥0.15 | 0.038290 | 0.038290 | 0.038290 | MISSED |
| 3. Label coverage and boundaries | 3/3 labels; 12/12 valid labels; correct boundaries | 3/3; 12/12; 6/6 | 3/3; 12/12; 6/6 | 3/3; 12/12; 6/6 | MET |
| 4. Appeals | 3/3 recorded, originals preserved; unknown ID rejected | 3/3; unknown ID 404 | 3/3; unknown ID 404 | 3/3; unknown ID 404 | MET |
| 5. Invalid text | 6/6 JSON 400s; no decisions; health 200 | 6/6; no decisions; health 200 | 6/6; no decisions; health 200 | 6/6; no decisions; health 200 | MET |

Criterion 1 avoided AI accusations, but only one of the ten human passages
received a human label. The target required at least five.

For criterion 2, the mean human score was 0.485100 and the mean AI
score was 0.523390. The measured gap was 0.038290.

Scores, labels, and check results matched across all three trials. Content IDs,
timestamps, and the growing log count changed as expected.

Full output: [three-trial run](results/run_2026-11-12_2241_before.md).

### Real output from Run 1

Produced by `run_eval.py::run_trial`, called by `run_eval.py::main`, using
`scenarios.py::SCENARIOS`. These are excerpts; the report contains every result
from all three trials. Submission responses come from `app.py::submit`, appeals
from `app.py::appeal`, and boundaries from `scoring.py::score_to_label`.

**1. Human writing**

```json
[
  {
    "sent": "I have hoodies and mugs from trips for the last 30+ years that I\u2019ve ke",
    "status": 201,
    "guess": "human",
    "confidence": 0.34595,
    "model_score": 0.3005,
    "style_score": 0.3914,
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "response": {
      "confidence": 0.34595,
      "content_id": "594b3b5b-195a-481c-a2eb-ef04d307a82b",
      "guess": "human",
      "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
      "model_score": 0.3005,
      "status": "decided",
      "style_score": 0.3914
    }
  }
]
```

**2. Score separation**

```json
[
  {
    "sent": "The comments serve a very real purpose. If the government doesn't adeq",
    "status": 201,
    "guess": "unsure",
    "confidence": 0.56965,
    "model_score": 0.6329,
    "style_score": 0.5064,
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "response": {
      "confidence": 0.56965,
      "content_id": "57345305-07f8-47be-b761-66873e2b3a32",
      "guess": "unsure",
      "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
      "model_score": 0.6329,
      "status": "decided",
      "style_score": 0.5064
    }
  },
  {
    "sent": "Public comments play an important role in the development of governmen",
    "status": 201,
    "guess": "unsure",
    "confidence": 0.611,
    "model_score": 0.6797,
    "style_score": 0.5423,
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "response": {
      "confidence": 0.611,
      "content_id": "000780eb-9271-4bb5-aa85-75da6138ab18",
      "guess": "unsure",
      "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
      "model_score": 0.6797,
      "status": "decided",
      "style_score": 0.5423
    }
  }
]
```

**3. Label coverage and boundaries**

```json
[
  {
    "sent": "Yesterday I went to the library to finish my assignment. I spent most ",
    "status": 201,
    "guess": "ai",
    "confidence": 0.7239,
    "model_score": 0.8272,
    "style_score": 0.6206,
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "response": {
      "confidence": 0.7239,
      "content_id": "b7c2c7b0-e3b7-47f0-8b93-79968c3e0715",
      "guess": "ai",
      "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": 0.6206
    }
  },
  {
    "sent": "This report explores the real-life impact of some of these close elect",
    "status": 201,
    "guess": "unsure",
    "confidence": 0.45355,
    "model_score": 0.5955,
    "style_score": 0.3116,
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "response": {
      "confidence": 0.45355,
      "content_id": "61850b25-1a21-4277-a502-d567e68aa40e",
      "guess": "unsure",
      "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
      "model_score": 0.5955,
      "status": "decided",
      "style_score": 0.3116
    }
  },
  {
    "sent": "By 6:43 a.m., the photocopier had swallowed page seventeen, somebody h",
    "status": 201,
    "guess": "human",
    "confidence": 0.2082,
    "model_score": 0.2758,
    "style_score": 0.1406,
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "response": {
      "confidence": 0.2082,
      "content_id": "734d6766-89b5-4290-9f8e-b09932b904c8",
      "guess": "human",
      "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
      "model_score": 0.2758,
      "status": "decided",
      "style_score": 0.1406
    }
  },
  {
    "score": 0.0,
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "source": "scoring.py::score_to_label"
  },
  {
    "score": 0.35,
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "source": "scoring.py::score_to_label"
  },
  {
    "score": 0.350001,
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "source": "scoring.py::score_to_label"
  },
  {
    "score": 0.649999,
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "source": "scoring.py::score_to_label"
  },
  {
    "score": 0.65,
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "source": "scoring.py::score_to_label"
  },
  {
    "score": 1.0,
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "source": "scoring.py::score_to_label"
  }
]
```

**4. Appeals**

```json
[
  {
    "sent": "Yesterday I went to the library to finish my assignment. I spent most ",
    "status": 201,
    "guess": "ai",
    "confidence": 0.7239,
    "model_score": 0.8272,
    "style_score": 0.6206,
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "response": {
      "confidence": 0.7239,
      "content_id": "764ab890-481a-4605-8e7e-febef80c37b4",
      "guess": "ai",
      "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": 0.6206
    },
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "764ab890-481a-4605-8e7e-febef80c37b4",
      "message": "Your appeal has been recorded.",
      "status": "under_review"
    },
    "original_preserved": true,
    "appeal_recorded": true,
    "audit_entries": [
      {
        "combined_score": 0.7239,
        "content_id": "764ab890-481a-4605-8e7e-febef80c37b4",
        "creator_id": "eval_appeal path_1",
        "guess": "ai",
        "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
        "model_score": 0.8272,
        "status": "decided",
        "style_score": 0.6206,
        "timestamp": "2026-11-13T06:41:37+00:00"
      },
      {
        "content_id": "764ab890-481a-4605-8e7e-febef80c37b4",
        "creator_id": "eval_appeal path_1",
        "event": "appeal",
        "reasoning": "Please review this decision about my submission.",
        "status": "under_review",
        "timestamp": "2026-11-13T06:41:37+00:00"
      }
    ]
  },
  {
    "missing_appeal_status": 404,
    "response": {
      "error": "content_not_found",
      "message": "No decision exists for this content ID."
    },
    "no_under_review_event": true
  }
]
```

**5. Invalid text**

```json
[
  {
    "sent": "{\"creator_id\": \"eval_missing\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "(empty text)",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": " \t\n ",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "{\"text\": null, \"creator_id\": \"eval_null\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "{\"text\": 42, \"creator_id\": \"eval_number\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must not exceed 20,000 characters."
    }
  },
  {
    "health_status": 200,
    "response": {
      "detector_loaded": true,
      "detector_model": "gpt2",
      "log_entries": 399,
      "ok": true,
      "rate_limiting": true
    },
    "no_classification_decisions": true
  }
]
```

**Diagnoses**

### How I decided each verdict

1. **Human writing — MISSED.** All three trials had 0/10 AI labels, which met the false-positive limit, but only 1/10 human labels, below the required five. The other nine were unsure.
2. **Score separation — MISSED.** The mean AI score exceeded the mean human score by 0.038290 in every trial. The target was at least 0.15.
3. **Label coverage — MET.** Every trial reached all three guesses, all 12 submissions had nonempty labels without placeholders, and all six boundary checks matched the original rules.
4. **Appeals — MET.** All three appeals in every trial returned 200 with the correct content ID and `under_review`, appended the required event, and preserved the original decision. The unknown ID returned 404 without creating an under-review event.
5. **Invalid text — MET.** All six cases returned JSON 400 responses with `invalid_input` and a message in every trial. None created a decision, and `/health` still returned 200.

### Why the two criteria missed

**Criterion 1 — combining rule and label mapping.** The equal-weight average left nine human passages between 0.35 and 0.65, so they received `unsure`. For example, passage 2 had a model score of 0.4919 and a style score of 0.2779. Their average was 0.3849, above the human cutoff of 0.35. The mapping followed its rules, but the combined scores did not identify enough human passages to meet the target. Avoiding false accusations alone was not enough to pass this criterion.

**Criterion 2 — signal one, signal two, and the combining rule.** The mean model score was 0.49939 for the human set and 0.47444 for the AI set: the model ranked these groups in the wrong direction. GPT-2 predictability is a proxy for authorship, so AI-written wording can still look surprising to it. The style signal separated the groups more usefully, with means of 0.47081 for human text and 0.57234 for AI text. However, the equal-weight average partly cancelled that separation: `0.5 × (0.47444 − 0.49939) + 0.5 × (0.57234 − 0.47081) = 0.03829`. That explains the small combined gap. These results describe this sample set.

### Why each broken attack broke

Scores below come from the saved attack run. A lower signal score means more human-like patterns. Evasion marked BROKE includes unsure results because the AI label was avoided.

| Attack | Stage | Mechanism and recorded evidence |
|---|---|---|
| EV01 | Signal one; combining rule | Misspellings make the wording less predictable to GPT-2. The model score was only 0.1635 despite a style score of 0.5915; their average, 0.37750, produced unsure. |
| EV02 | Signal two; combining rule | Broken-up sentences produced high sentence-length spread (0.849). The style rule treats that variation as human-like, giving 0.2321; averaging with the model's 0.5943 produced 0.41320, unsure. |
| EV03 | Signal two; combining rule | The pasted quotation changed sentence shape and word variety, which the style rule measures without understanding the quotation. Its 0.4232 pulled the model's 0.6662 down to 0.54470, unsure. |
| EV04 | Signal one and signal two; label mapping | Unusual words are not evidence of human authorship, but predictability and vocabulary variety are what these signals measure. Scores of 0.6114 and 0.5784 averaged to 0.59490, below the AI cutoff, so the result was unsure. |
| EV05 | Signal one and signal two | The edited AI passage had both a low predictability score (0.3212) and a low style score (0.3101). Surface editing can resemble human writing to both signals; their average of 0.31565 received a human label. |
| EV06 | Signal two; combining rule | A very long sentence beside a short one pushed sentence-length spread above 1. The style formula then set that AI-like contribution to zero. Style scored 0.2250; the combined 0.39885 was unsure. |
| EV07 | Signal two; combining rule | The semicolon-linked text was treated as one sentence because the splitter only breaks after `.`, `!`, or `?`. That triggered the 0.5 style fallback. Averaging it with the model's 0.5862 produced 0.54310, unsure. |
| EV08 | Signal one and signal two | This input has only ten word tokens. Style returned its short-text fallback of 0.5, while the model scored 0.2452; the average was 0.37260, unsure. Although its target mentions the token window, the supplied text is short: this result does not demonstrate a truncation bypass. |
| EV09 | Signal two; combining rule | The conversational opening changed the whole passage's sentence variation and word variety. Style scored 0.4178 and pulled a model score of 0.7042 down to 0.56100, unsure. |
| FP02 | Signal one; combining rule | The formal human report used predictable wording, giving a model score of 0.7387. Style was 0.5996; the equal-weight average reached 0.66915 and incorrectly received an AI label. |
| FP03 | Signal one; combining rule | Careful, plain human writing scored 0.8051 on predictability. Its style score of 0.5521 did not offset that enough: the combined 0.67860 produced an AI accusation. |
| FP04 | Signal one; combining rule | The rubric-style essay's regular phrasing scored 0.8329 on the model signal. Even with style below 0.5 (0.4927), the average reached 0.66280 and crossed the AI cutoff. |
| FP05 | Signal one and signal two | Repeated technical instructions were predictable to the model (0.8005) and had relatively uniform sentence lengths and repeated vocabulary (style 0.5942). Both signals pushed the average to 0.69735, incorrectly labelled AI. |
| FP06 | Signal one; combining rule | The human-written letter used familiar template phrases, producing a model score of 0.8814. Its lower style score of 0.4408 still left the average at 0.66110, labelled AI. |
| PI02 | Signal one and signal two; label mapping | The fake system-message text was scored as ordinary text. Low scores of 0.2044 and 0.2880 averaged to 0.24620, giving the requested human label. It did not return the demanded score of 0.02 or skip scoring, so this is a classification failure, not evidence that instructions were obeyed. |
| MF03 | Route; signal two fallback | The route accepts nonempty control-character text, and the model's minimum length counts model tokens rather than meaningful prose. Model 0.0000 and fallback style 0.5 averaged to 0.25000, producing a human label for junk. |
| MF04 | Route; signal two fallback | Punctuation-only text passes the nonempty-string check and can contain enough model tokens to be scored. With no word tokens, style returned 0.5; model 0.0112 gave a combined 0.25560 and a human label. |
| MF05 | Route; signal one and signal two | The 4,000-character repeated word is under the character limit and tokenises into enough model tokens. Repetition scored 0.9976 on the model, while style fell back to 0.5 because there was only one word. The combined 0.74880 received an AI label instead of rejection or abstention. |
| MF06 | Route; signal one and signal two | Emoji-only text is nonempty and tokenises for the model, but the style tokenizer finds no words and returns 0.5. The repeated emoji scored 0.9969 on the model; the combined 0.74845 produced an authorship label for non-prose input. |

### Patterns across the misses

- **Surface features are easy to change.** Typos, sentence breaks, quotations, and conversational openings affect predictability or style without establishing who wrote the text. This links the evasion failures and PI02's human result.
- **Predictable human writing is vulnerable to false accusations.** All five false-positive failures had model scores above 0.73. The equal-weight average still crossed the AI cutoff, even when style leaned slightly human.
- **Averaging often leads to unsure.** This helped avoid accusations on the ten supplied human passages, but missed the human-label target and let eight evasion inputs avoid an AI label. The same combining rule also cancelled much of criterion 2's style separation.
- **Input validity is weaker than score validity.** The route rejects missing or oversized text, but accepts control characters, punctuation, repeated characters, and emoji. The style fallback of 0.5 then lets the model turn those inputs into authorship decisions.

The original targets stay unchanged. They were measurable; missing them is not a reason to lower them.

---

## The Improvement

**What I changed:** Raised `AI_THRESHOLD` in `config.py` from 0.65 to 0.70.
The human cutoff stays at 0.35. Scores from 0.65 up to, but not including, 0.70
now receive `unsure` instead of `ai`. This is the only service change.

**Which diagnosis pointed at it:** FP02–FP06 were genuine-human examples with
combined scores between 0.66110 and 0.69735. Their predictable wording pushed
them just over the old AI cutoff. Raising that cutoff avoids those accusations.

```bash
python run_attacks.py --set attack_set --label after
python run_eval.py --label after
```

Both commands used the same inputs as before. All 56 attacks ran, followed by
all five criteria three times. There were no skipped inputs, timeouts, or
server errors. Scores stayed the same; only labels in the changed band moved.

### Attack Run — After

| Result | Before | After |
|---|---:|---:|
| HELD | 37/56 | 42/56 |
| BROKE | 19/56 | 14/56 |
| Human examples wrongly labelled AI | 5/8 | 0/8 |
| Evasion attacks that avoided an AI label | 9/10 | 9/10 |
| Flood rejections | 2/12 | 2/12 |

[Before attack report](results/attack_run_2026-11-12_2144_before.md) ·
[After attack report](results/attack_run_2026-11-12_2301_after.md)

### Every attack: before and after

| ID | Before HTTP | Before guess | Before score | Verdict | After HTTP | After guess | After score | Verdict |
|---|---:|---|---:|---|---:|---|---:|---|
| EV01 | 201 | unsure | 0.37750 | BROKE | 201 | unsure | 0.37750 | BROKE |
| EV02 | 201 | unsure | 0.41320 | BROKE | 201 | unsure | 0.41320 | BROKE |
| EV03 | 201 | unsure | 0.54470 | BROKE | 201 | unsure | 0.54470 | BROKE |
| EV04 | 201 | unsure | 0.59490 | BROKE | 201 | unsure | 0.59490 | BROKE |
| EV05 | 201 | human | 0.31565 | BROKE | 201 | human | 0.31565 | BROKE |
| EV06 | 201 | unsure | 0.39885 | BROKE | 201 | unsure | 0.39885 | BROKE |
| EV07 | 201 | unsure | 0.54310 | BROKE | 201 | unsure | 0.54310 | BROKE |
| EV08 | 201 | unsure | 0.37260 | BROKE | 201 | unsure | 0.37260 | BROKE |
| EV09 | 201 | unsure | 0.56100 | BROKE | 201 | unsure | 0.56100 | BROKE |
| EV10 | 201 | ai | 0.83200 | HELD | 201 | ai | 0.83200 | HELD |
| FP01 | 201 | unsure | 0.54980 | HELD | 201 | unsure | 0.54980 | HELD |
| FP02 | 201 | ai | 0.66915 | BROKE | 201 | unsure | 0.66915 | HELD |
| FP03 | 201 | ai | 0.67860 | BROKE | 201 | unsure | 0.67860 | HELD |
| FP04 | 201 | ai | 0.66280 | BROKE | 201 | unsure | 0.66280 | HELD |
| FP05 | 201 | ai | 0.69735 | BROKE | 201 | unsure | 0.69735 | HELD |
| FP06 | 201 | ai | 0.66110 | BROKE | 201 | unsure | 0.66110 | HELD |
| FP07 | 201 | unsure | 0.63570 | HELD | 201 | unsure | 0.63570 | HELD |
| FP08 | 201 | unsure | 0.41115 | HELD | 201 | unsure | 0.41115 | HELD |
| PI01 | 201 | unsure | 0.39435 | HELD | 201 | unsure | 0.39435 | HELD |
| PI02 | 201 | human | 0.24620 | BROKE | 201 | human | 0.24620 | BROKE |
| PI03 | 201 | unsure | 0.53790 | HELD | 201 | unsure | 0.53790 | HELD |
| PI04 | 201 | unsure | 0.45585 | HELD | 201 | unsure | 0.45585 | HELD |
| PI05 | 201 | unsure | 0.45720 | HELD | 201 | unsure | 0.45720 | HELD |
| PI06 | 201 | unsure | 0.52450 | HELD | 201 | unsure | 0.52450 | HELD |
| MF01 | 400 | — | — | HELD | 400 | — | — | HELD |
| MF02 | 400 | — | — | HELD | 400 | — | — | HELD |
| MF03 | 201 | human | 0.25000 | BROKE | 201 | human | 0.25000 | BROKE |
| MF04 | 201 | human | 0.25560 | BROKE | 201 | human | 0.25560 | BROKE |
| MF05 | 201 | ai | 0.74880 | BROKE | 201 | ai | 0.74880 | BROKE |
| MF06 | 201 | ai | 0.74845 | BROKE | 201 | ai | 0.74845 | BROKE |
| MF07 | 201 | ai | 0.70320 | HELD | 201 | ai | 0.70320 | HELD |
| MF08 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ01 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ02 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ03 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ04 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ05 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ06 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ07 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ08 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ09 | 400 | — | — | HELD | 400 | — | — | HELD |
| RQ10 | 415 | — | — | HELD | 415 | — | — | HELD |
| RQ11 | 415 | — | — | HELD | 415 | — | — | HELD |
| RQ12 | 400 | — | — | HELD | 400 | — | — | HELD |
| FL01_01 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_02 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_03 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_04 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_05 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_06 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_07 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_08 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_09 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_10 | 201 | human | 0.26435 | HELD | 201 | human | 0.26435 | HELD |
| FL01_11 | 429 | — | — | HELD | 429 | — | — | HELD |
| FL01_12 | 429 | — | — | HELD | 429 | — | — | HELD |

### Five criteria: before and after

Each result below was the same in Run 1, Run 2, and Run 3.

| Criterion | Original target | Before, each run | Verdict | After, each run | Verdict |
|---|---|---|---|---|---|
| 1. Human writing | ≤1/10 AI and ≥5/10 human | 0 AI; 1 human | MISSED | 0 AI; 1 human | MISSED |
| 2. Score separation | Mean gap ≥0.15 | 0.038290 | MISSED | 0.038290 | MISSED |
| 3. Coverage and boundaries | 3/3 labels; 12/12 valid labels; 6/6 original boundaries | 3/3; 12/12; 6/6 | MET | 3/3; 12/12; 5/6 | MISSED |
| 4. Appeals | 3/3 recorded, originals preserved; unknown ID 404 | 3/3; unknown ID 404 | MET | 3/3; unknown ID 404 | MET |
| 5. Invalid text | 6/6 JSON 400s; no decisions; health 200 | 6/6; no decisions; health 200 | MET | 6/6; no decisions; health 200 | MET |

### After: three-trial run log

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human writing | ≤1/10 AI and ≥5/10 human | 0/10 AI; 1/10 human | 0/10 AI; 1/10 human | 0/10 AI; 1/10 human | MISSED |
| 2. Score separation | Mean gap ≥0.15 | 0.038290 | 0.038290 | 0.038290 | MISSED |
| 3. Label coverage and original boundaries | 3/3 labels; 12/12 valid labels; 6/6 original boundary checks | 3/3; 12/12; 5/6 | 3/3; 12/12; 5/6 | 3/3; 12/12; 5/6 | MISSED |
| 4. Appeals | 3/3 recorded, originals preserved; unknown ID 404 | 3/3; unknown ID 404 | 3/3; unknown ID 404 | 3/3; unknown ID 404 | MET |
| 5. Invalid text | 6/6 JSON 400s; no decisions; health 200 | 6/6; no decisions; health 200 | 6/6; no decisions; health 200 | 6/6; no decisions; health 200 | MET |

The original targets were not lowered. Criterion 3 is now MISSED because its
original rule says a score of 0.65 must return `ai`; it now returns `unsure`.
The stage is label mapping, and the mechanism is the deliberately raised AI
cutoff. All three labels are still reachable. Criteria 1 and 2 still miss for
the reasons diagnosed above: too few human labels and too little score separation.
Appeals and invalid-input handling continue to meet their targets in every trial.

[Before criteria report](results/run_2026-11-12_2241_before.md) ·
[After criteria report](results/run_2026-11-12_2301_after.md)

### Real output from After Run 1

Produced by `run_eval.py::run_trial`, called by `run_eval.py::main`, using
`scenarios.py::SCENARIOS`. These are actual response excerpts; the after report
contains all three trials. Submissions come from `app.py::submit`, appeals from
`app.py::appeal`, and boundary checks from `scoring.py::score_to_label`.

**1. Human writing**

```json
{
  "confidence": 0.34595,
  "content_id": "44618017-009f-4c96-a57b-333b77d24e40",
  "guess": "human",
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "model_score": 0.3005,
  "status": "decided",
  "style_score": 0.3914
}
```

**2. Score separation**

```json
[
  {
    "confidence": 0.56965,
    "content_id": "dca74ece-7042-4edc-b375-bfc212355870",
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "model_score": 0.6329,
    "status": "decided",
    "style_score": 0.5064
  },
  {
    "confidence": 0.611,
    "content_id": "05e22ff8-f7f0-4f42-aa67-e223881bbada",
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "model_score": 0.6797,
    "status": "decided",
    "style_score": 0.5423
  }
]
```

**3. Label coverage and changed boundary**

```json
[
  {
    "confidence": 0.7239,
    "content_id": "93aa8f4c-e3f5-42f3-853f-aaf266b6f035",
    "guess": "ai",
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "model_score": 0.8272,
    "status": "decided",
    "style_score": 0.6206
  },
  {
    "confidence": 0.45355,
    "content_id": "e79efdc7-a000-4308-8921-fe2de0c98e4a",
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "model_score": 0.5955,
    "status": "decided",
    "style_score": 0.3116
  },
  {
    "confidence": 0.2082,
    "content_id": "acce29b1-c166-4910-84f1-9cc0a12ba198",
    "guess": "human",
    "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
    "model_score": 0.2758,
    "status": "decided",
    "style_score": 0.1406
  },
  {
    "score": 0.65,
    "guess": "unsure",
    "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
    "source": "scoring.py::score_to_label"
  }
]
```

**4. Appeals**

```json
[
  {
    "sent": "Yesterday I went to the library to finish my assignment. I spent most ",
    "status": 201,
    "guess": "ai",
    "confidence": 0.7239,
    "model_score": 0.8272,
    "style_score": 0.6206,
    "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
    "response": {
      "confidence": 0.7239,
      "content_id": "95e79114-b0ab-4137-9174-1ddc61e0fc64",
      "guess": "ai",
      "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": 0.6206
    },
    "appeal_status": 200,
    "appeal_response": {
      "content_id": "95e79114-b0ab-4137-9174-1ddc61e0fc64",
      "message": "Your appeal has been recorded.",
      "status": "under_review"
    },
    "original_preserved": true,
    "appeal_recorded": true,
    "audit_entries": [
      {
        "combined_score": 0.7239,
        "content_id": "95e79114-b0ab-4137-9174-1ddc61e0fc64",
        "creator_id": "eval_appeal path_1",
        "guess": "ai",
        "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
        "model_score": 0.8272,
        "status": "decided",
        "style_score": 0.6206,
        "timestamp": "2026-11-13T07:01:55+00:00"
      },
      {
        "content_id": "95e79114-b0ab-4137-9174-1ddc61e0fc64",
        "creator_id": "eval_appeal path_1",
        "event": "appeal",
        "reasoning": "Please review this decision about my submission.",
        "status": "under_review",
        "timestamp": "2026-11-13T07:01:55+00:00"
      }
    ]
  },
  {
    "missing_appeal_status": 404,
    "response": {
      "error": "content_not_found",
      "message": "No decision exists for this content ID."
    },
    "no_under_review_event": true
  }
]
```

**5. Invalid text**

```json
[
  {
    "sent": "{\"creator_id\": \"eval_missing\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "(empty text)",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": " \t\n ",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "{\"text\": null, \"creator_id\": \"eval_null\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "{\"text\": 42, \"creator_id\": \"eval_number\"}",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must be a nonempty string."
    }
  },
  {
    "sent": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "response": {
      "error": "invalid_input",
      "message": "The text field must not exceed 20,000 characters."
    }
  },
  {
    "health_status": 200,
    "response": {
      "detector_loaded": true,
      "detector_model": "gpt2",
      "log_entries": 617,
      "ok": true,
      "rate_limiting": true
    },
    "no_classification_decisions": true
  }
]
```

**Did it help, and how do I know:** Yes: it removed all five false AI
accusations in the attack set, but did not improve evasion detection, human-label
coverage, or score separation, and it missed the original 0.65 boundary target.

The five affected human examples now receive unsure, not a confident human
label. No extra evasion failure appeared in this set, but AI text scoring from
0.65 to below 0.70 would now avoid an AI label too. That is the cost of widening
the unsure band. The nine evasion failures, PI02, and four non-prose failures
remain; this threshold change does not address their underlying causes.

---

## What's Still Broken

The after run still has 14 broken attacks. The threshold change reduced false
accusations, but did not fix the weaknesses below.

| Attack | What is still wrong | What I'd do next |
|---|---|---|
| EV01 | Typos make AI text look less predictable, leading to unsure. | Compare scores with and without spelling normalisation, checking that genuine informal writing is not unfairly penalised. |
| EV02 | Choppy sentences lower the style score and produce unsure. | Rework how much sentence-length variation affects the style score. |
| EV03 | A pasted quotation changes the style measurements enough to avoid an AI label. | Test quoted and unquoted sections separately rather than treating the whole passage as one style. |
| EV04 | Unusual words help AI text stay below the AI cutoff. | Test a signal less dependent on word predictability and vocabulary variety. |
| EV05 | Edited AI text receives a human label from both signals. | Add edited-AI examples to calibration and check whether a different signal can separate them. |
| EV06 | A very long sentence beside a short one drives down the style score. | Reduce how strongly extreme sentence variation counts as human-like evidence. |
| EV07 | Semicolon-linked text triggers the one-sentence style fallback. | Improve sentence splitting and stop treating missing style evidence as a neutral score that can support a confident label. |
| EV08 | Very short text gets a weak style fallback and avoids an AI label. | Give a clear insufficient-text result when there is too little evidence for authorship scoring. |
| EV09 | A conversational opening pulls the combined score into unsure. | Compare section-level scores so an opening cannot stand in for the whole passage. |
| PI02 | The fake system-message input gets a human label, although its instructions are not executed. | Treat it as an evasion example when calibrating signals, while continuing to score its instructions as ordinary text. |
| MF03 | Control-character text receives a human label. | Reject control characters that are not ordinary text whitespace before scoring. |
| MF04 | Punctuation-only text receives a human label. | Check for meaningful text before running the signals, without restricting valid writing to English. |
| MF05 | A long repeated character sequence receives an AI label. | Detect extreme character repetition and reject it before model scoring. |
| MF06 | Emoji-only input receives an AI label. | Return an insufficient-text result instead of assigning an authorship label. |

I stopped after the one threshold change so the before-and-after comparison
would measure that change alone. The ideas above need separate runs to show
whether they help without creating new false accusations.

### Criteria still missed

| Criterion | What I'd do next | Why I stopped here |
|---|---|---|
| 1. Human writing | Improve signal calibration so more genuine writing can reach the human band without increasing false accusations. | Raising the AI cutoff did not change the human cutoff or any scores; a further calibration change would need its own comparison. |
| 2. Score separation | Improve the signals using a separate calibration set, then rerun the fixed human and AI examples. | Changing a label threshold cannot increase the measured score gap; changing the signals as well would mix two improvements. |
| 3. Original label boundaries | Test a different improvement that reduces false accusations while keeping the original 0.65 boundary. | The chosen 0.70 cutoff deliberately conflicts with that target. I kept the original target and recorded MISSED instead of rewriting it to pass. |

**The trade I'd make if this ran for real:**

I'd favour fewer false accusations and send uncertain cases for review, even
if that lets more AI-written text avoid an AI label. Moderators would carry
more review work and the site would accept more missed AI text, rather than
making genuine writers bear the cost of a confident but wrong accusation.

**Submission URL:** https://github.com/aanshika005/ProvenanceGuard


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [x] Rate limiting on /submit, with your numbers justified
       [x] The pasted run of status codes showing 429
       [x] Audit log with all nine fields, recording rejections too
       [x] The attack set run IN FULL, every input with an outcome
       [x] Ten audit log entries pasted as text
       [x] Five criteria across three trials
       [x] A diagnosis for every miss and every broken attack — stage AND mechanism
       [x] One improvement, with Attack Run — After
       [x] What's Still Broken, including the production trade
       [x] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
