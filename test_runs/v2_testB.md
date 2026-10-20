# V2 - Test B

## Input

> can u give me a source about AI in school for my essay

## What the system receives

- The student's question (text).
- [MOCKED] One model answer and two resampled answers to the same question.
- [MOCKED] Results from the source search for each sentence.

## What it does

1. [IMPLEMENTED] Request check: this asks for a source, but the topic is only ['ai', 'school']. Marked as vague.
2. [MOCKED] Model writes an answer with 2 sentences and is asked the same question 2 more times.
3. [IMPLEMENTED] Consistency check: compare the numbers in each sentence with the same sentence in the 2 resamples.
4. [MOCKED] Source search: look for sources that match each sentence.
5. [IMPLEMENTED] Sentence type check: reference / number-date / general.
6. [IMPLEMENTED] Validation v2: a reference must match a real paper record by title; a number must appear in a found source.
7. [IMPLEMENTED] Flag rule v2: highlight if NOT consistent OR NOT verified. If the search is down, every reference/number is marked 'Not checked'.

### Sentence check table

| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |
|---|---|---|---|---|---|---|
| 1 | Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. | reference | yes | R1, R2 | no | YELLOW |
| 2 | It shows that AI tutors improved test scores by 20%. | number/date | no | R1 | no | YELLOW |

## Response shown to the student

> **Your request is broad.** Which part of "AI in school" is your essay about?  `[AI tutors]` `[AI and exams]` `[Teachers using AI]` `[Type my own topic]`

> ==Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60.== `[NOT VERIFIED]`
>   - Why? no matching record for this paper was found in the paper search, so it may not exist.
>   - `[Find real papers]` `[Remove this reference]` `[I will check it myself]`
> ==It shows that AI tutors improved test scores by 20%.== `[Check this]`
>   - Why? the numbers changed when the model answered again (also said 35).
>
> **Real papers found in the paper search** (open them before you use them):
>   - R1: AI tutoring systems and student learning: a review (placeholder record, 2020)
>   - R2: Generative AI in secondary classrooms (placeholder record, 2024)

## Next action for the student

- Pick a narrower topic, so the system can search again.
- For each yellow sentence: read the reason, then check it, fix it, remove it or keep it.
- Open one of the real papers from the search instead of the unverified one.
