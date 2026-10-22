# Test B on v2: problem input (vague request for a source)

Screen: `test_screens/testB.png` (v1 left, v2 right)

## 1. Input
The student types: **"can u give me a source about AI in school for my essay"**

## 2. What the system receives
- The question above.
- An answer with 2 sentences, plus the same question answered 2 more times. [MOCKED: mock_data.json]
- Source search results for each sentence. [MOCKED]

## 3. What it does
1. Checks the request: it asks for a source, but the topic is only "ai school", so it is **too vague**.
2. Checks each sentence:
   - Sentence 1: "Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60." → same in all 3 answers; related sources found: R1, R2; **no record of this paper** → **YELLOW**
   - Sentence 2: "It shows that AI tutors improved test scores by 20%." → **changed** when asked again; related sources found: R1; number not found in a source → **YELLOW**
3. Rule v2: highlight if it changed **or** it could not be verified. If the search fails, mark facts as "Not checked".

## 4. Response and next action
What the student sees (⚠ = yellow highlight):

> **Your request is broad.** Which part of "AI in school" is your essay about? [AI tutors] [AI and exams] [Teachers using AI] [Type my own topic]  
> ⚠ Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. **[NOT VERIFIED]**  
>   Why? no matching record for this paper was found in the paper search, so it may not exist.  
>   [Find real papers] [Remove this reference] [I will check it myself]  
> ⚠ It shows that AI tutors improved test scores by 20%. **[Check this]**  
>   Why? the numbers changed when the model answered again (also said 35).  
> Real papers found in the search: R1 AI tutoring systems and student learning: a review (placeholder record, 2020); R2 Generative AI in secondary classrooms (placeholder record, 2024)  

Next action:
- Pick a narrower topic.
- Read the reason on each yellow sentence, then check, fix, remove or keep it.
- Use a real paper from the search instead of the unverified one.

**Result:** OK: the made-up paper is caught, each flag has a reason, and the system asks before guessing.
