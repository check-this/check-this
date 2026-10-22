# Test B on v1 (problem input)

## Input
"can u give me a source about AI in school for my essay"

## What the system receives
- The question, and an answer with 2 sentences. [MOCKED]
- The same question answered 2 more times. [MOCKED]
- Source search results for each sentence. [MOCKED]

## What it does
- Sentence 1: same in all 3 answers; related sources: R1, R2 -> no highlight
- Sentence 2: changed when asked again; related sources: R1 -> YELLOW
- Rule v1: highlight only if the sentence changed when asked again.

## Response (what the student sees, ! = yellow)
> Here is a useful paper: Smith, J. (2021). AI Tutors in Secondary Schools. Journal of Learning Technology, 12(3), 45-60.  
> ! It shows that AI tutors improved test scores by 20%. [Check this]  

## Next action
- The paper has no highlight, so it looks safe. The student would probably copy it into the essay.
- The student can click the button on each yellow sentence, then check, fix, remove or keep it.
