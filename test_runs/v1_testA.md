# V1 - Test A

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
4. [IMPLEMENTED] Flag rule v1: highlight a sentence only if it was NOT consistent. Sources are shown but do not change the flag.

### Sentence check table

| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |
|---|---|---|---|---|---|---|
| 1 | The Gutenberg Bible was printed in Mainz, Germany, around 1455. | (not used in v1) | yes | S1, S2 | (not checked in v1) | - |
| 2 | Gutenberg printed about 500 copies. | (not used in v1) | no | none | (not checked in v1) | YELLOW |
| 3 | It was one of the first books in Europe printed with metal movable type. | (not used in v1) | yes | S3 | (not checked in v1) | - |

## Response shown to the student

> The Gutenberg Bible was printed in Mainz, Germany, around 1455.
> ==Gutenberg printed about 500 copies.== `[Check this]`
> It was one of the first books in Europe printed with metal movable type.

## Next action for the student

- The student sees 1 yellow sentence(s): [2]. They can click "Check this" on those.
