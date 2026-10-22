# Test B on v1: problem input (vague request for a source), source search down

Screen: `test_screens/testB_search_down.png` (v1 left, v2 right)

## 1. Input
The student types: **"can u give me a source about AI in school for my essay"**

## 2. What the system receives
- The question above.
- An answer with 2 sentences, plus the same question answered 2 more times. [MOCKED: mock_data.json]
- Source search results for each sentence. [MOCKED] **In this run the search fails.**

## 3. What it does
1. Checks each sentence:
   - Sentence 1: "Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60." → same in all 3 answers; search failed → no highlight
   - Sentence 2: "It shows that AI tutors improved test scores by 20%." → **changed** when asked again; search failed → **YELLOW**
2. Rule v1: highlight only the sentences that changed. (The sources do not change the decision.)

## 4. Response and next action
What the student sees (⚠ = yellow highlight):

> Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60.  
> ⚠ It shows that AI tutors improved test scores by 20%. **[Check this]**  

Next action:
- The student can click "Check this" on sentence 2.
- Sentence 1 (the paper) has no highlight, so it looks safe. The student would probably copy it.
- Nothing tells the student that the search failed.

**Result:** PROBLEM: the made-up paper is not highlighted.
