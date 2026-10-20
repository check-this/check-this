# V2 - Test A

## Input

> When was the Gutenberg Bible printed, and how many copies were made?

## What the system receives

- The student's question (text).
- [MOCKED] One model answer and two resampled answers to the same question.
- [MOCKED] Results from the source search for each sentence.

## What it does

1. [MOCKED] Model writes an answer with 3 sentences and is asked the same question 2 more times.
2. [IMPLEMENTED] Consistency check: compare the numbers in each sentence with the same sentence in the 2 resamples.
3. [MOCKED] Source search: look for sources that match each sentence.
4. [IMPLEMENTED] Sentence type check: reference / number-date / general.
5. [IMPLEMENTED] Validation v2: a reference must match a real paper record by title; a number must appear in a found source.
6. [IMPLEMENTED] Flag rule v2: highlight if NOT consistent OR NOT verified. If the search is down, every reference/number is marked 'Not checked'.

### Sentence check table

| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |
|---|---|---|---|---|---|---|
| 1 | The Gutenberg Bible was printed in Mainz, Germany, around 1455. | number/date | yes | S1, S2 | yes | - |
| 2 | Gutenberg printed about 500 copies. | number/date | no | none | no | YELLOW |
| 3 | It was one of the first books in Europe printed with metal movable type. | general | yes | S3 | - | - |

## Response shown to the student

> The Gutenberg Bible was printed in Mainz, Germany, around 1455. `[Checked: S1, S2]`
> ==Gutenberg printed about 500 copies.== `[Check this]`
>   - Why? the numbers changed when the model answered again (also said 180).
> It was one of the first books in Europe printed with metal movable type.

## Next action for the student

- For each yellow sentence: read the reason, then check it, fix it, remove it or keep it.
