# Test A on v1: standard input

Screen: `test_screens/testA.png` (v1 left, v2 right)

## 1. Input
The student types: **"When was the Gutenberg Bible printed, and how many copies were made?"**

## 2. What the system receives
- The question above.
- An answer with 3 sentences, plus the same question answered 2 more times. [MOCKED: mock_data.json]
- Source search results for each sentence. [MOCKED]

## 3. What it does
1. Checks each sentence:
   - Sentence 1: "The Gutenberg Bible was printed in Mainz, Germany, around 1455." → same in all 3 answers; related sources found: S1, S2 → no highlight
   - Sentence 2: "Gutenberg printed about 500 copies." → **changed** when asked again; no source found → **YELLOW**
   - Sentence 3: "It was one of the first books in Europe printed with metal movable type." → same in all 3 answers; related sources found: S3 → no highlight
2. Rule v1: highlight only the sentences that changed. (The sources do not change the decision.)

## 4. Response and next action
What the student sees (⚠ = yellow highlight):

> The Gutenberg Bible was printed in Mainz, Germany, around 1455.  
> ⚠ Gutenberg printed about 500 copies. **[Check this]**  
> It was one of the first books in Europe printed with metal movable type.  

Next action:
- The student can click "Check this" on sentence 2.

**Result:** OK: the wrong number is highlighted.
