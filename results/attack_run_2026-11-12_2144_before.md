# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-12 21:44
- Auto-marked BROKE (5xx, crash, no response): **0**
- Manually judged: **56**
- HELD: **37**; BROKE: **19**

Verdicts were added after the complete unchanged-service run. See README's
Attack Run — Before section for the judging rules. Per-attack notes below
explain each mark; original measured scores and statuses are preserved.

Text attacks submit as `attacker_<id>`. Request-file rows use their supplied
creator IDs; flood rows share one ID. Decision content IDs below match the
complete run audit extract; rejected requests were matched in request order.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 201 | `589c8869-7625-4559-a355-b8944c891f37` | unsure | 0.378 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 201 | `9d881b13-5d8e-4c2d-916f-13cd4fa3077c` | unsure | 0.413 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 201 | `e56a9937-d477-483e-965e-a310acde94c0` | unsure | 0.545 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 201 | `535712bc-eeb4-4be9-8466-9d72df5cce3c` | unsure | 0.595 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 201 | `026d038d-1ae9-4efd-92c7-a353732ee065` | human | 0.316 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 201 | `e48ebd96-aee2-4b74-a512-8bc66f8104cf` | unsure | 0.399 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 201 | `6a54c82f-d5b8-46b7-8cf8-3d7b152f1b8e` | unsure | 0.543 | BROKE |
| EV08 | evasion | signal one: text below the token window | 201 | `7e3382ad-021b-45a9-8dd6-67ecb59b15c2` | unsure | 0.373 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 201 | `2476a42b-60bf-495e-8a93-056e04b38301` | unsure | 0.561 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 201 | `19782d3b-95cc-4c75-826e-b7c15394c247` | ai | 0.832 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 201 | `a86f6b9c-8afb-4dea-b77e-d9645e203881` | unsure | 0.550 | HELD |
| FP02 | false_positive | human writing in a formal register | 201 | `4ea770ae-e71d-4791-8cb0-a138391b0ca0` | ai | 0.669 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 201 | `f768a4ca-c974-4351-b383-2dc09f1485dc` | ai | 0.679 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 201 | `8a1bcf63-f809-4807-8c3c-1bcda514e059` | ai | 0.663 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 201 | `309a8106-166e-467e-a07f-2f352315e3eb` | ai | 0.697 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 201 | `c733ba9e-a250-4e3a-9a81-c16d5eacdf46` | ai | 0.661 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 201 | `2ed0e67b-e892-496c-b074-b52c3b41a67c` | unsure | 0.636 | HELD |
| FP08 | false_positive | very short genuine human submission | 201 | `26a8f01d-b5a6-4ea6-9164-ab43dd6b1bc0` | unsure | 0.411 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 201 | `140c87f2-4a2a-44b3-a84b-62c23665bde2` | unsure | 0.394 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 201 | `1f530a0c-378e-4696-94d7-ac791c6ac343` | human | 0.246 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 201 | `e913fe2d-8f9f-4ddb-8b7a-60ce155d5c1d` | unsure | 0.538 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 201 | `f6586bbc-3871-47ea-ac68-05979979e886` | unsure | 0.456 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 201 | `5022d613-a710-4777-a6f9-0eaf1716167f` | unsure | 0.457 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 201 | `edc67b78-5bcc-46df-835f-b0286d7822c0` | unsure | 0.524 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 201 | `8c03c4f0-a5d0-4246-90c9-416d1400dcd5` | human | 0.250 | BROKE |
| MF04 | malformed | text is only punctuation | 201 | `78e1134d-2cc2-4fc6-8594-ab821864d33e` | human | 0.256 | BROKE |
| MF05 | malformed | text is a very long single word | 201 | `b1656216-68f6-4a6d-bde2-4c76588907bf` | ai | 0.749 | BROKE |
| MF06 | malformed | text is emoji only | 201 | `235681e2-e4a3-44e4-adad-fb880ba6a397` | ai | 0.748 | BROKE |
| MF07 | malformed | text is right-to-left script | 201 | `fc794bc8-7be5-4256-8853-afaba075dc54` | ai | 0.703 | HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 415 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 415 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 201 | `f8ccf344-93f5-4809-ae8e-e0a385edce31` | human | 0.264 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 201 | `23c747c8-6339-4a14-96df-e290a80d6153` | human | 0.264 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 201 | `140cd0eb-729a-4d4d-a8fe-33d8ddbf9bbd` | human | 0.264 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 201 | `6cb91827-5874-4e7d-90fa-41731e57ea0c` | human | 0.264 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 201 | `ea2d7ade-8fbe-429b-ae85-c77cec8cf301` | human | 0.264 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 201 | `40a9f782-b6ed-4dc0-afeb-c51385d414f4` | human | 0.264 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 201 | `b00af7e5-9243-4c13-8098-9ab877d61ff0` | human | 0.264 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 201 | `dbc9dc22-3fb4-494e-98cb-55bdaa73b2a8` | human | 0.264 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 201 | `dc3ec589-ac89-4b0a-a208-c19f8f68746d` | human | 0.264 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 201 | `e1c0f659-a819-4b44-a69b-08696ff36463` | human | 0.264 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 3 | 5 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 16 | 4 |
| `prompt_injection` | 6 | 5 | 1 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 201,
  "content_id": "589c8869-7625-4559-a355-b8944c891f37",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3775,
  "model_score": 0.1635,
  "style_score": 0.5915,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 201,
  "content_id": "9d881b13-5d8e-4c2d-916f-13cd4fa3077c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4132,
  "model_score": 0.5943,
  "style_score": 0.2321,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 201,
  "content_id": "e56a9937-d477-483e-965e-a310acde94c0",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5447,
  "model_score": 0.6662,
  "style_score": 0.4232,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 201,
  "content_id": "535712bc-eeb4-4be9-8466-9d72df5cce3c",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5949,
  "model_score": 0.6114,
  "style_score": 0.5784,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 201,
  "content_id": "026d038d-1ae9-4efd-92c7-a353732ee065",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.31565,
  "model_score": 0.3212,
  "style_score": 0.3101,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned human."
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 201,
  "content_id": "e48ebd96-aee2-4b74-a512-8bc66f8104cf",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.39885,
  "model_score": 0.5727,
  "style_score": 0.225,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 201,
  "content_id": "6a54c82f-d5b8-46b7-8cf8-3d7b152f1b8e",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5431,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 201,
  "content_id": "7e3382ad-021b-45a9-8dd6-67ecb59b15c2",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3726,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 201,
  "content_id": "2476a42b-60bf-495e-8a93-056e04b38301",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.561,
  "model_score": 0.7042,
  "style_score": 0.4178,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "BROKE",
  "note": "AI-labelled input avoided the AI label: returned unsure."
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 201,
  "content_id": "19782d3b-95cc-4c75-826e-b7c15394c247",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.832,
  "model_score": 0.9792,
  "style_score": 0.6848,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "HELD",
  "note": "AI-labelled input retained an AI label."
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 201,
  "content_id": "a86f6b9c-8afb-4dea-b77e-d9645e203881",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5498000000000001,
  "model_score": 0.6175,
  "style_score": 0.4821,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "No AI accusation; unsure is an acceptable abstention, not proof of human authorship."
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 201,
  "content_id": "4ea770ae-e71d-4791-8cb0-a138391b0ca0",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.66915,
  "model_score": 0.7387,
  "style_score": 0.5996,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Human-labelled writing received an AI label."
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 201,
  "content_id": "f768a4ca-c974-4351-b383-2dc09f1485dc",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6786000000000001,
  "model_score": 0.8051,
  "style_score": 0.5521,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Human-labelled writing received an AI label."
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 201,
  "content_id": "8a1bcf63-f809-4807-8c3c-1bcda514e059",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6628000000000001,
  "model_score": 0.8329,
  "style_score": 0.4927,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Human-labelled writing received an AI label."
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 201,
  "content_id": "309a8106-166e-467e-a07f-2f352315e3eb",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6973499999999999,
  "model_score": 0.8005,
  "style_score": 0.5942,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Human-labelled writing received an AI label."
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 201,
  "content_id": "c733ba9e-a250-4e3a-9a81-c16d5eacdf46",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6611,
  "model_score": 0.8814,
  "style_score": 0.4408,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Human-labelled writing received an AI label."
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 201,
  "content_id": "2ed0e67b-e892-496c-b074-b52c3b41a67c",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6357,
  "model_score": 0.8816,
  "style_score": 0.3898,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "No AI accusation; unsure is an acceptable abstention, not proof of human authorship."
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 201,
  "content_id": "26a8f01d-b5a6-4ea6-9164-ab43dd6b1bc0",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.41115,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "No AI accusation; unsure is an acceptable abstention, not proof of human authorship."
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 201,
  "content_id": "140c87f2-4a2a-44b3-a84b-62c23665bde2",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.39435,
  "model_score": 0.4625,
  "style_score": 0.3262,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "Demanded human classification; returned unsure."
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 201,
  "content_id": "1f530a0c-378e-4696-94d7-ac791c6ac343",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.24619999999999997,
  "model_score": 0.2044,
  "style_score": 0.288,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "BROKE",
  "note": "Obtained human label, but requested score 0.02 was not returned. This is a classification failure, not evidence instructions were obeyed."
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 201,
  "content_id": "e913fe2d-8f9f-4ddb-8b7a-60ce155d5c1d",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5379,
  "model_score": 0.5943,
  "style_score": 0.4815,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "Asked for verified-author pass-through; returned ordinary unsure decision."
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 201,
  "content_id": "f6586bbc-3871-47ea-ac68-05979979e886",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.45585,
  "model_score": 0.4998,
  "style_score": 0.4119,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "Returned fixed unsure label; injected script did not appear in label or audit record. Browser execution was not tested."
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 201,
  "content_id": "5022d613-a710-4777-a6f9-0eaf1716167f",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4572,
  "model_score": 0.6401,
  "style_score": 0.2743,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "Returned ordinary scores; audit record remained valid JSON with actual guess and score, without injected note."
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 201,
  "content_id": "edc67b78-5bcc-46df-835f-b0286d7822c0",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5245,
  "model_score": 0.5583,
  "style_score": 0.4907,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "Verification request did not bypass either signal; returned ordinary unsure decision with both scores."
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 201,
  "content_id": "8c03c4f0-a5d0-4246-90c9-416d1400dcd5",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "BROKE",
  "note": "Control-character or non-prose input received an authorship label instead of rejection or abstention."
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 201,
  "content_id": "78e1134d-2cc2-4fc6-8594-ab821864d33e",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "BROKE",
  "note": "Control-character or non-prose input received an authorship label instead of rejection or abstention."
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 201,
  "content_id": "b1656216-68f6-4a6d-bde2-4c76588907bf",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7488,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Control-character or non-prose input received an authorship label instead of rejection or abstention."
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 201,
  "content_id": "235681e2-e4a3-44e4-adad-fb880ba6a397",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7484500000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "BROKE",
  "note": "Control-character or non-prose input received an authorship label instead of rejection or abstention."
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 201,
  "content_id": "fc794bc8-7be5-4256-8853-afaba075dc54",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text has patterns our system associates with AI-generated writing. This assessment can be wrong and does not establish who wrote it. You can request a review.",
  "error": null,
  "verdict": "HELD",
  "note": "Arabic text was accepted without crashing. Language alone is not malformed input; accuracy of its AI label is unverified."
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 415,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 415; audit reason: unsupported_media_type."
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 415,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 415; audit reason: unsupported_media_type."
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Rejected invalid request with 400; audit reason: invalid_input."
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 201,
  "content_id": "f8ccf344-93f5-4809-ae8e-e0a385edce31",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 201,
  "content_id": "23c747c8-6339-4a14-96df-e290a80d6153",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 201,
  "content_id": "140cd0eb-729a-4d4d-a8fe-33d8ddbf9bbd",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 201,
  "content_id": "6cb91827-5874-4e7d-90fa-41731e57ea0c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 201,
  "content_id": "ea2d7ade-8fbe-429b-ae85-c77cec8cf301",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 201,
  "content_id": "40a9f782-b6ed-4dc0-afeb-c51385d414f4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 201,
  "content_id": "b00af7e5-9243-4c13-8098-9ab877d61ff0",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 201,
  "content_id": "dbc9dc22-3fb4-494e-98cb-55bdaa73b2a8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 201,
  "content_id": "dc3ec589-ac89-4b0a-a208-c19f8f68746d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 201,
  "content_id": "e1c0f659-a819-4b44-a69b-08696ff36463",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.26435,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This text appears likely to have been written by a person. This assessment is not proof of authorship.",
  "error": null,
  "verdict": "HELD",
  "note": "Within the configured first-ten allowance; scoring succeeded."
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Over the ten-per-minute allowance; 429 rejection recorded in audit log."
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD",
  "note": "Over the ten-per-minute allowance; 429 rejection recorded in audit log."
}
```
