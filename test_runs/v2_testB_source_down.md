# Test B on v2: problem input (vague request for a source), source search down

Screen: `test_screens/testB_search_down.png` (v1 left, v2 right)

## 1. Input
The student types: **"can u give me a source about AI in school for my essay"**

## 2. What the system receives
- The question above.
- An answer with 2 sentences, plus the same question answered 2 more times. [MOCKED: mock_data.json]
- Source search results for each sentence. [MOCKED] **In this run the search fails.**

## 3. What it does
1. Checks the request: it asks for a source, but the topic is only "ai school", so it is **too vague**.
2. Checks each sentence:
   - Sentence 1: "Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60." → same in all 3 answers; search failed; paper not checked → **YELLOW**
   - Sentence 2: "It shows that AI tutors improved test scores by 20%." → **changed** when asked again; search failed → **YELLOW**
3. Rule v2: highlight if it changed **or** it could not be verified. If the search fails, mark facts as "Not checked".

## 4. Response and next action
What the student sees (⚠ = yellow highlight):

> **Notice:** I could not reach the source search, so references, numbers and dates are marked Not checked.  
> **Your request is broad.** Which part of "AI in school" is your essay about? [AI tutors] [AI and exams] [Teachers using AI] [Type my own topic]  
> ⚠ Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. **[Not checked]**  
>   Why? the source search was unavailable, so this fact could not be checked.  
>   [Try the search again] [Remove this reference] [I will check it myself]  
> ⚠ It shows that AI tutors improved test scores by 20%. **[Not checked]**  
>   Why? the numbers changed when the model answered again (also said 35); the source search was unavailable, so this fact could not be checked.  

Next action:
- Pick a narrower topic.
- Read the reason on each yellow sentence, then check, fix, remove or keep it.
- Try again later, or check the "Not checked" facts by hand.

**Result:** OK: the student is told the search failed.
