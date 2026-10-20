# 02_PROMPT_LOG.md

Use this file if you ask an AI assistant to help with the project. Name the tool, record the request or command, summarise what came back and explain what you kept, changed or rejected. If you did not use an assistant, you do not need to submit this file.

Note: the parts marked **(to complete)** must be written by me after I review the work. They record my own decisions, so the assistant did not fill them in.

## 2026-10-20 17:15  Plan the lab
Tool used: Claude (Anthropic) in the Claude app. It could read and write files in my Downloads folder and run Python and Git in its own workspace.
Request or command: I pasted the Lab 3 instructions and the submission rules. Earlier in the same chat, Claude had helped with my Lab 1 and Lab 2 work, so it had my problem sentence and my Week 2 storyboard ("Check this" highlights in a study chatbot).
What came back: A summary of the four phases and a plan: use one use case from the Week 2 storyboard (mark unreliable sentences), build a small Python simulation with a mocked model and a mocked source search, run Test A (fact question) and Test B (vague request for a source), draw a system path diagram, keep a Git history and zip the whole folder. It also said this log would name Claude as the tool.
What I decided to keep, change or reject, and why: **(to complete)**

## 2026-10-20 17:21  Build the simulation and run the tests
Tool used: Claude (Anthropic) in the Claude app, as above.
Request or command: I downloaded `lab3_pack.zip` and asked Claude to continue. Claude read the starter files (`01_SPEC.md`, `02_PROMPT_LOG.md`, `.gitignore`) and then ran these commands in its workspace:
- `git init`, then a first commit with the starter files unchanged
- `python check_this_sim.py --version v1 --test A` and `--test B`
- `python check_this_sim.py --version v2 --test B` and `--test B --source-down`
- `python check_this_sim.py --all` (writes every run to `test_runs/`)

What came back:
- `check_this_sim.py`: the system path with two versions. v1 flags a sentence only if the resampled answers disagree. v2 adds a request check, a sentence type check, a reference/number validation step and a "search down" fallback.
- `mock_data.json`: mocked model answers, resamples and a small mocked source index. The fake reference "Smith, J. (2021)" is a placeholder.
- `test_runs/*.md`: the outputs for v1 and v2.
- Results: in Test B the v1 path did **not** flag the fake reference, because the model repeated it every time. The v2 path flagged it as NOT VERIFIED and asked a clarifying question.

What I decided to keep, change or reject, and why: **(to complete)**

## 2026-10-20 17:30  Diagrams and specification
Tool used: Claude (Anthropic) in the Claude app, as above.
Request or command: Same request as above (complete the lab files).
What came back:
- `diagrams/system_path_v1.png` and `diagrams/system_path_v2.png`, with each box labelled implemented, simulated (mock) or planned. Changes in v2 are purple.
- `01_SPEC.md` filled in: use case, inputs, processing and technology table, fallback, Test A, Test B, review table (6 questions with evidence), one interaction change, one technology change, Test B again and why it helps.
- Copies of my Week 2 storyboard images in `storyboard/`.

What I decided to keep, change or reject, and why: **(to complete)**
