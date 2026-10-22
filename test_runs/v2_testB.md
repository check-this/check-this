# Test B on v2 (problem input)

## Input
"can u give me a source about AI in school for my essay"

## What the system receives
- The question, and an answer with 2 sentences. [MOCKED]
- The same question answered 2 more times. [MOCKED]
- Source search results for each sentence. [MOCKED]

## What it does
- Sentence 1: same in all 3 answers; related sources: R1, R2; no record of this paper -> YELLOW
- Sentence 2: changed when asked again; related sources: R1 -> YELLOW
- Rule v2: highlight if the sentence changed OR a paper reference has no real record.

## Response (what the student sees, ! = yellow)
> ! Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60. [NOT VERIFIED]  
>   Why? no record of this paper was found in the paper search, so it may not exist.  
>   [Find real papers] [Remove this reference] [I will check it myself]  
> ! It shows that AI tutors improved test scores by 20%. [Check this]  
>   Why? the number changed when the model answered again (it also said 35).  

## Next action
- The student can click the button on each yellow sentence, then check, fix, remove or keep it.
