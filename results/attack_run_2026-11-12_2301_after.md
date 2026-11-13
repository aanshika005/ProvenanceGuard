# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-12 23:01
- Auto-marked BROKE (5xx, crash, no response): **0**
- Manually judged: **56**
- HELD: **42**; BROKE: **14**

Verdicts use the same rules as the before run. Only AI_THRESHOLD changed,
from 0.65 to 0.70. See README for the side-by-side comparison.

Text rows use `attacker_<id>`; request-file rows use their supplied creator IDs.
Flood rows share one creator. Decision content IDs match the audit log.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 201 | `fb959c91-9dc1-4bbb-a7c4-439d3281e131` | unsure | 0.378 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 201 | `cc4d130a-ad58-4890-9344-0c02710a94a8` | unsure | 0.413 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 201 | `6e9b81da-08f6-4fbf-b50b-b1c400557468` | unsure | 0.545 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 201 | `d74fb26a-960c-468e-9873-b57e4543f525` | unsure | 0.595 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 201 | `dd9cf3b3-b112-44ba-a43a-3eb0328dfa7e` | human | 0.316 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 201 | `4b315e4c-5516-4a0c-bf41-397c1d8ad64a` | unsure | 0.399 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 201 | `8da6532b-2d52-448b-9d6b-2ecdf46dbeeb` | unsure | 0.543 | BROKE |
| EV08 | evasion | signal one: text below the token window | 201 | `211a8dce-b2dc-414c-9ef1-bdf9a9316aa4` | unsure | 0.373 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 201 | `e9e44024-890f-4bfe-9014-e80f75a143e1` | unsure | 0.561 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 201 | `d3b0f48e-cd48-480a-94d6-bbb5574bb5f3` | ai | 0.832 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 201 | `41a9f79c-fb48-40a1-8759-fabca2a369c5` | unsure | 0.550 | HELD |
| FP02 | false_positive | human writing in a formal register | 201 | `721a0b92-9fa3-4dc2-a18d-beab3bd12db9` | unsure | 0.669 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 201 | `81e2026d-b2e2-4461-9c81-b8186d298547` | unsure | 0.679 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 201 | `2349a5b1-758a-4403-9223-f86363845442` | unsure | 0.663 | HELD |
| FP05 | false_positive | technical documentation written by a person | 201 | `ca65d653-d499-4c05-9f71-aaaf5f7aaec7` | unsure | 0.697 | HELD |
| FP06 | false_positive | a person imitating a formal template | 201 | `0e5965ee-bc73-4b3f-bad6-ff0017da5032` | unsure | 0.661 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 201 | `39425655-15f7-4832-bb73-e7b7f962668d` | unsure | 0.636 | HELD |
| FP08 | false_positive | very short genuine human submission | 201 | `0149e235-7485-4cec-9a91-383bd282f2e4` | unsure | 0.411 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 201 | `7098c925-a649-4e0b-9c2b-e1a43167c6b6` | unsure | 0.394 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 201 | `dc4a0ba8-5925-4241-b614-b401a9f52335` | human | 0.246 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 201 | `8159945c-2816-4c71-8b56-cf29ec35aaed` | unsure | 0.538 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 201 | `e7daec6f-e031-4494-9842-c863232747d1` | unsure | 0.456 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 201 | `3e6be739-9fa2-40e8-ae95-3ba37802a888` | unsure | 0.457 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 201 | `4f563ac1-5757-4e91-a033-aeac773526b1` | unsure | 0.524 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 201 | `1f0e0ed6-11a9-40fc-afb6-c9856fb62804` | human | 0.250 | BROKE |
| MF04 | malformed | text is only punctuation | 201 | `c3b5d53f-4eca-40b4-b777-2a29bbc63a56` | human | 0.256 | BROKE |
| MF05 | malformed | text is a very long single word | 201 | `f6c0bbf3-1100-45f4-89f3-3662413df4e9` | ai | 0.749 | BROKE |
| MF06 | malformed | text is emoji only | 201 | `78390bae-24fa-4d5a-81ef-eb97cca74283` | ai | 0.748 | BROKE |
| MF07 | malformed | text is right-to-left script | 201 | `9e46860e-d004-45a1-941b-e35a696fabc6` | ai | 0.703 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 201 | `a064c892-697c-45b0-ae19-2c7c7710ff2b` | human | 0.264 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 201 | `a2a720f3-149d-4f13-a94b-b4fdfde2e096` | human | 0.264 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 201 | `82894412-6796-4772-9030-0963e32bf85d` | human | 0.264 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 201 | `76d0c9b0-bdc6-49ec-aae0-4daab57624c3` | human | 0.264 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 201 | `9806aaef-723a-4c9f-8843-5a828dba3b6a` | human | 0.264 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 201 | `6f109b51-8dcc-4f0e-a1c9-03b98340ce89` | human | 0.264 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 201 | `ead0f152-f2b5-4c97-9243-66fa7d0ac2e9` | human | 0.264 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 201 | `a0015d6b-f4e7-4593-9d41-d7fa2be90c75` | human | 0.264 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 201 | `369c877f-096e-4b54-ad46-6d93a0e14208` | human | 0.264 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 201 | `9fd29ccf-7016-4e77-9421-40281f0687dc` | human | 0.264 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 8 | 0 |
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
  "content_id": "fb959c91-9dc1-4bbb-a7c4-439d3281e131",
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
  "content_id": "cc4d130a-ad58-4890-9344-0c02710a94a8",
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
  "content_id": "6e9b81da-08f6-4fbf-b50b-b1c400557468",
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
  "content_id": "d74fb26a-960c-468e-9873-b57e4543f525",
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
  "content_id": "dd9cf3b3-b112-44ba-a43a-3eb0328dfa7e",
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
  "content_id": "4b315e4c-5516-4a0c-bf41-397c1d8ad64a",
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
  "content_id": "8da6532b-2d52-448b-9d6b-2ecdf46dbeeb",
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
  "content_id": "211a8dce-b2dc-414c-9ef1-bdf9a9316aa4",
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
  "content_id": "e9e44024-890f-4bfe-9014-e80f75a143e1",
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
  "content_id": "d3b0f48e-cd48-480a-94d6-bbb5574bb5f3",
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
  "content_id": "41a9f79c-fb48-40a1-8759-fabca2a369c5",
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
  "content_id": "721a0b92-9fa3-4dc2-a18d-beab3bd12db9",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.66915,
  "model_score": 0.7387,
  "style_score": 0.5996,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "The unchanged score is below the new 0.70 AI threshold; this human example now receives unsure instead of an AI accusation."
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 201,
  "content_id": "81e2026d-b2e2-4461-9c81-b8186d298547",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6786000000000001,
  "model_score": 0.8051,
  "style_score": 0.5521,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "The unchanged score is below the new 0.70 AI threshold; this human example now receives unsure instead of an AI accusation."
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 201,
  "content_id": "2349a5b1-758a-4403-9223-f86363845442",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6628000000000001,
  "model_score": 0.8329,
  "style_score": 0.4927,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "The unchanged score is below the new 0.70 AI threshold; this human example now receives unsure instead of an AI accusation."
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 201,
  "content_id": "ca65d653-d499-4c05-9f71-aaaf5f7aaec7",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6973499999999999,
  "model_score": 0.8005,
  "style_score": 0.5942,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "The unchanged score is below the new 0.70 AI threshold; this human example now receives unsure instead of an AI accusation."
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 201,
  "content_id": "0e5965ee-bc73-4b3f-bad6-ff0017da5032",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6611,
  "model_score": 0.8814,
  "style_score": 0.4408,
  "label": "We cannot reliably determine how this text was written. This result should not be treated as an accusation of AI use.",
  "error": null,
  "verdict": "HELD",
  "note": "The unchanged score is below the new 0.70 AI threshold; this human example now receives unsure instead of an AI accusation."
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 201,
  "content_id": "39425655-15f7-4832-bb73-e7b7f962668d",
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
  "content_id": "0149e235-7485-4cec-9a91-383bd282f2e4",
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
  "content_id": "7098c925-a649-4e0b-9c2b-e1a43167c6b6",
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
  "content_id": "dc4a0ba8-5925-4241-b614-b401a9f52335",
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
  "content_id": "8159945c-2816-4c71-8b56-cf29ec35aaed",
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
  "content_id": "e7daec6f-e031-4494-9842-c863232747d1",
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
  "content_id": "3e6be739-9fa2-40e8-ae95-3ba37802a888",
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
  "content_id": "4f563ac1-5757-4e91-a033-aeac773526b1",
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
  "content_id": "1f0e0ed6-11a9-40fc-afb6-c9856fb62804",
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
  "content_id": "c3b5d53f-4eca-40b4-b777-2a29bbc63a56",
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
  "content_id": "f6c0bbf3-1100-45f4-89f3-3662413df4e9",
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
  "content_id": "78390bae-24fa-4d5a-81ef-eb97cca74283",
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
  "content_id": "9e46860e-d004-45a1-941b-e35a696fabc6",
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
  "content_id": "a064c892-697c-45b0-ae19-2c7c7710ff2b",
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
  "content_id": "a2a720f3-149d-4f13-a94b-b4fdfde2e096",
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
  "content_id": "82894412-6796-4772-9030-0963e32bf85d",
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
  "content_id": "76d0c9b0-bdc6-49ec-aae0-4daab57624c3",
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
  "content_id": "9806aaef-723a-4c9f-8843-5a828dba3b6a",
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
  "content_id": "6f109b51-8dcc-4f0e-a1c9-03b98340ce89",
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
  "content_id": "ead0f152-f2b5-4c97-9243-66fa7d0ac2e9",
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
  "content_id": "a0015d6b-f4e7-4593-9d41-d7fa2be90c75",
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
  "content_id": "369c877f-096e-4b54-ad46-6d93a0e14208",
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
  "content_id": "9fd29ccf-7016-4e77-9421-40281f0687dc",
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
