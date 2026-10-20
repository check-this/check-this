# V2 - Test B (source search down)

## Input

> can u give me a source about AI in school for my essay

## What the system receives

- The student's question (text).
- [MOCKED] One model answer and two resampled answers to the same question.
- [MOCKED] Results from the source search for each sentence. The search is DOWN in this run.

## What it does

1. [IMPLEMENTED] Request check: this asks for a source, but the topic is only ['ai', 'school']. Marked as vague.
2. [MOCKED] Model writes an answer with 2 sentences and is asked the same question 2 more times.
3. [IMPLEMENTED] Consistency check: compare the numbers in each sentence with the same sentence in the 2 resamples.
4. [MOCKED] Source search: FAILED (service unavailable). v2 reports it to the student.
5. [IMPLEMENTED] Sentence type check: reference / number-date / general.
6. [IMPLEMENTED] Validation v2: a reference must match a real paper record by title; a number must appear in a found source.
7. [IMPLEMENTED] Flag rule v2: highlight if NOT consistent OR NOT verified. If the search is down, every reference/number is marked 'Not checked'.

### Sentence check table

| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |
|---|---|---|---|---|---|---|
| 1 | Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. | reference | yes | search down | - | YELLOW |
| 2 | It shows that AI tutors improved test scores by 20%. | number/date | no | search down | - | YELLOW |

## Response shown to the student

> **Notice:** I could not reach the source search right now, so I could not check any facts. References, numbers and dates are marked **Not checked**. You can try again later or check them yourself.

> **Your request is broad.** Which part of "AI in school" is your essay about?  `[AI tutors]` `[AI and exams]` `[Teachers using AI]` `[Type my own topic]`

> ==Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60.== `[Not checked]`
>   - Why? the source search was unavailable, so this fact could not be checked.
>   - `[Try the search again]` `[Remove this reference]` `[I will check it myself]`
> ==It shows that AI tutors improved test scores by 20%.== `[Not checked]`
>   - Why? the numbers changed when the model answered again (also said 35); the source search was unavailable, so this fact could not be checked.

## Next action for the student

- Pick a narrower topic, so the system can search again.
- For each yellow sentence: read the reason, then check it, fix it, remove it or keep it.
- Try again later, or check the 'Not checked' facts by hand.
