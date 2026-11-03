# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Limit false positives on genuine human writing

Of 10 paragraphs I wrote myself, at most 1 may receive the `ai` guess in each trial. At least 5 must receive `human`, so returning `unsure` for everything does not satisfy this criterion.

**Why this target:** A false accusation can harm a genuine writer. I prioritize avoiding that harm while still requiring the service to recognize some human writing confidently.

---

## 2. Separate clearly human and clearly AI-generated writing

Using a fixed set of 10 human-written paragraphs and 10 unedited AI-generated paragraphs, the mean combined score for the AI set must exceed the mean for the human set by at least 0.15 in each trial. Paragraphs will contain 100–200 words and cover comparable topics.

**Why this target:** The scores should provide meaningful separation between these groups. Keeping length and topics comparable reduces obvious confounding, although this small test cannot establish general detection accuracy.

---

## 3. Make all three labels reachable

A fixed set of 12 calibration paragraphs must produce at least one `human`, one `unsure`, and one `ai` guess in every trial. Every response must contain a nonempty reader-facing label without placeholder text.

The score boundaries must also map correctly:

- Scores at or below 0.35 map to `human`.
- Scores strictly between 0.35 and 0.65 map to `unsure`.
- Scores at or above 0.65 map to `ai`.

**Why this target:** Three configured labels are useful only if real submissions can reach them. Checking the boundaries separately ensures that the implementation matches the documented ranges.

---

## 4. Record appeals and preserve the original decision

For each of 3 valid submissions in each trial, an appeal using its returned `content_id` must:

- Return HTTP 200 with the same `content_id` and status `under_review`.
- Append an appeal event containing the content ID, creator ID, reasoning, timestamp, and status.
- Preserve the original decision entry and its scores.

An appeal for a nonexistent content ID must return HTTP 404 and must not create an under-review event.

**Why this target:** Writers need a reliable way to challenge a decision. Preserving the original entry makes both the assessment and the challenge visible in the audit history.

---

## 5. Reject invalid text without crashing

Each of these requests must return HTTP 400 with a JSON response containing `error: "invalid_input"` and a nonempty `message`:

1. Missing `text`.
2. `text` set to an empty string.
3. `text` containing only whitespace.
4. `text` set to `null`.
5. `text` set to a number.
6. `text` containing 20,001 characters, exceeding the proposed 20,000-character limit.

Use a valid `creator_id` for every case. None may return HTTP 500 or create a classification decision. After these requests, `GET /health` must still return HTTP 200.

**Why this target:** Invalid submissions should receive understandable errors without disrupting the service. The length limit also bounds accepted input size, although it does not by itself provide complete resource protection.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
