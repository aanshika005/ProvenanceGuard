# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does
Provenance Guard is a local web service that assesses text using two signals: predictability under a language model and measurable writing-style patterns.
<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->
### Submission Path
A submission follows this path:

1. **Receive the request — `app.py::submit`.** Accept the writer’s text and creator ID through `POST /submit`.
2. **Validate the input.** Check that the body is a JSON object, the text is a nonempty string, and the creator ID is valid. Return a clear error for invalid input.
3. **Assign a content ID.** Generate a unique identifier that connects the submission, its decision, and any later appeal.
4. **Calculate both signals.** Use `detector.py::model_signal` to measure predictability and `stylometry.py::style_signal` to measure textual shape.
5. **Combine the signals — `scoring.py::combine_signals`.** Calculate one combined score. Higher scores indicate more AI-like patterns.
6. **Choose a label — `scoring.py::score_to_label`.** Map the score to `human`, `unsure`, or `ai`, accompanied by a reader-facing explanation.
7. **Log and return the decision.** Record the timestamp, content ID, creator ID, both signal scores, combined score, guess, label, and status. Return the decision to the caller.

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

**Why that might differ between human and AI writing:**
AI-generated prose may have more uniform sentence lengths and recurring stylistic patterns. Human writing may vary more in sentence structure, vocabulary, and punctuation.

**What it can't see:**
Style measurements do not understand meaning or establish authorship. Typos, sentence splitting, and inserted quotations can change the measurements without changing who wrote the text. Vocabulary ratios also depend on text length.

### The combining rule
The current combining rule in `scoring.py::combine_signals` uses equal weights:

    combined_score = 0.5 * model_score + 0.5 * style_score

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**
**The rule:** Take the average of the model signal and the style signal, giving each equal influence. Both scores range from 0 to 1, with higher scores indicating more AI-like patterns. When the signals strongly disagree, their average moves toward the unsure range.

**The numbers:**
combined_score = 0.5 * model_score + 0.5 * style_score

- Model signal weight: **50%**
- Style signal weight: **50%**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
In a hypothetical example, the model signal gives a submission 0.9 because its wording is highly predictable, while the style signal gives it 0.1 because its sentence lengths and vocabulary appear varied.

With equal weights:

    combined_score = 0.5 * 0.9 + 0.5 * 0.1 = 0.5

The combined score falls in the `unsure` range. This treats strong disagreement as uncertainty rather than allowing either signal to decide alone.

---

### Tracing a False Positive

The following scenario is hypothetical and describes the planned behavior, not an actual test result.

A student submits a paragraph they wrote themselves using simple vocabulary and regular sentence structures. The model signal gives it **0.85** because its wording is predictable. Suppose the completed style signal gives it **0.55**.

With equal weights:

```text
combined_score = 0.5 * 0.85 + 0.5 * 0.55
               = 0.70
```

Because the combined score exceeds the configured AI threshold of **0.65**, the system incorrectly classifies the student's work as AI.

The proposed label says:

> This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.

The student can challenge the decision through `/appeal`, providing the submission's `content_id` and an explanation. The service records the appeal and marks the item as `under_review`, preserving the original decision.

This scenario guides my threshold choices. I would prioritize reducing false accusations against genuine writers, accepting that a wider unsure range could allow more AI-generated text to avoid a confident AI label. Actual threshold changes will need evidence from testing.

### Planned Endpoint Contracts

These contracts describe the intended behavior.

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
| `text` | string | Required; must contain non-whitespace text. Proposed maximum: 20,000 characters. |
| `creator_id` | string | Required; must contain non-whitespace text. Proposed maximum: 100 characters. |

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
| 429 | `rate_limited` | The submission limit has been exceeded, once limiting is enabled. |
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
| `reasoning` | string | Required; must contain non-whitespace text. Proposed maximum: 5,000 characters. |

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

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 ≤ score ≤ 0.35 | This text appears likely to have been written by a person. This assessment is not proof of authorship. |
| unsure | 0.35 < score < 0.65 | We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use. |
| high-confidence AI | 0.65 ≤ score ≤ 1.00 | This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review. |

**Why I worded the "unsure" one this way:**

The wording communicates uncertainty without accusing the writer. Weak or conflicting signals do not establish AI use, and a genuine writer may receive this result.


## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->
Request: 

```bash
$ curl -i -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text":"Yesterday I went to the library to finish my assignment. I spent most of the afternoon reviewing my notes. Before leaving, I checked out a book for next week.","creator_id":"writer_123"}'
```

Response: HTTP/1.1 201 CREATED

```json
{
  "confidence": null,
  "content_id": "4d471ed0-fe57-46cc-8f71-171e5d01452d",
  "guess": "pending",
  "label": "Model signal calculated; final assessment is not available yet.",
  "model_score": 0.8272,
  "status": "decided",
  "style_score": null
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**
Request:

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

Response: 

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": null,
      "content_id": "2ea4912d-158e-45da-980f-15e3c895477e",
      "creator_id": "writer_123",
      "guess": "pending",
      "label": "Model signal calculated; final assessment is not available yet.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-03T04:04:01+00:00"
    },
    {
      "combined_score": null,
      "content_id": "4d471ed0-fe57-46cc-8f71-171e5d01452d",
      "creator_id": "writer_123",
      "guess": "pending",
      "label": "Model signal calculated; final assessment is not available yet.",
      "model_score": 0.8272,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-03T04:52:42+00:00"
    }
  ]
}
```

### Standalone Detector Tests

| Input | Perplexity | Model score |
|---|---|---|
| Unedited AI-generated paragraph | 27.2 | 0.6910 |
| My own human-written paragraph | 44.5 | 0.5044 |
| AI-generated paragraph I edited | 18.5 | 0.8056 |

These scores measure predictability and do not establish authorship.

### Illustrative Signal Comparison

| Test input | Model score | Style score | Combined score | Observation |
|---|---:|---:|---:|---|
| Clearly AI-generated text | 0.90 | 0.80 | 0.85 | Both signals indicate AI-like patterns. |
| Clearly human-written text | 0.20 | 0.30 | 0.25 | Both signals indicate human-like patterns. |
| Formal human writing | 0.30 | 0.80 | 0.55 | Signals disagree; averaging places the score in the unsure range. |
| Lightly-edited AI text | 0.80 | 0.40 | 0.60 | Editing changes stylistic patterns; the combined score falls in the unsure range. |

Combined score = 0.5 × model score + 0.5 × style score.

## Sample Run

### A Submission

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

This exceeds the AI threshold of 0.65, producing the `ai` guess. The `confidence` field contains the combined AI-like score, not a calibrated probability of authorship. This test paragraph was supplied by an AI assistant and is not evidence of a false positive on human writing.

### An Appeal

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

### What the Log Shows Afterwards

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


## Sample Run

### A Submission

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

The score falls within the unsure range: 0.35 < score < 0.65. The `confidence` field contains the combined AI-like score, not a calibrated probability of authorship.

### An Appeal

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

### What the Log Shows Afterwards

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

### Sample Run: Human Label and Appeal

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


<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
