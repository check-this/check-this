# Test A on v1 (standard input)

## Input
"When was the Gutenberg Bible printed, and how many copies were made?"

## What the system receives
- The question, and an answer with 3 sentences. [MOCKED]
- The same question answered 2 more times. [MOCKED]
- Source search results for each sentence. [MOCKED]

## What it does
- Sentence 1: same in all 3 answers; related sources: S1, S2 -> no highlight
- Sentence 2: changed when asked again; no source -> YELLOW
- Sentence 3: same in all 3 answers; related sources: S3 -> no highlight
- Rule v1: highlight only if the sentence changed when asked again.

## Response (what the student sees, ! = yellow)
> The Gutenberg Bible was printed in Mainz, Germany, around 1455.  
> ! Gutenberg printed about 500 copies. [Check this]  
> It was one of the first books in Europe printed with metal movable type.  

## Next action
- The student can click the button on each yellow sentence, then check, fix, remove or keep it.
