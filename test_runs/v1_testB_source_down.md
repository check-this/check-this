# V1 - Test B (source search down)

## Input

> can u give me a source about AI in school for my essay

## What the system receives

- The student's question (text).
- [MOCKED] One model answer and two resampled answers to the same question.
- [MOCKED] Results from the source search for each sentence. The search is DOWN in this run.

## What it does

1. [MOCKED] Model writes an answer with 2 sentences and is asked the same question 2 more times.
2. [IMPLEMENTED] Consistency check: compare the numbers in each sentence with the same sentence in the 2 resamples.
3. [MOCKED] Source search: FAILED (service unavailable). v1 does not report this.
4. [IMPLEMENTED] Flag rule v1: highlight a sentence only if it was NOT consistent. Sources are shown but do not change the flag.

### Sentence check table

| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |
|---|---|---|---|---|---|---|
| 1 | Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. | (not used in v1) | yes | search down | (not checked in v1) | - |
| 2 | It shows that AI tutors improved test scores by 20%. | (not used in v1) | no | search down | (not checked in v1) | YELLOW |

## Response shown to the student

> Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60.
> ==It shows that AI tutors improved test scores by 20%.== `[Check this]`

## Next action for the student

- The student sees 1 yellow sentence(s): [2]. They can click "Check this" on those.
- Sentence(s) [1] look trusted (no highlight), so the student would probably copy them into the essay.
- Nothing tells the student that the source search failed.
