# Check This: marking unreliable sentences in a study chatbot

README prose word count: about 470 (code and commands not counted)

## Project status
- **What it is:** a design and simulated prototype. A study chatbot checks each sentence of its answer and marks the ones that may be unreliable, so students know what to check before using it in coursework.
- **Implemented** (`check_this_sim.py`): the consistency check (do the numbers stay the same when the model answers again?), the paper check (does a cited paper match a real record?), the highlight rule, and the response text with a "Why?" reason and buttons.
- **Simulated** (`mock_data.json`): the language model answers and the source / paper search. These are fixed, hand-written data, not live services.
- **Planned, not built:** a real LLM API, a real paper search (e.g. Crossref), a clickable chat interface, a clarifying question for vague requests, and a message when the search is unavailable.

## Technology stack
- Python 3 (standard library only). No API key or network is needed.
- Language model: simulated. A real LLM API is still undecided.
- Source search: simulated with a small local index. A real search API (e.g. Crossref) is planned.

## Running or inspecting the work
```
python3 check_this_sim.py --version v1 --test A   # Test A: clear fact question
python3 check_this_sim.py --version v1 --test B   # Test B: vague request for a source (v1 misses the fake paper)
python3 check_this_sim.py --version v2 --test B   # Test B again after the revision (v2 catches it)
python3 check_this_sim.py --all                   # writes all three runs to test_runs/
```
- `01_SPEC.md`: use case, system path, tests, review and revision
- `diagrams/`: system path before (v1) and after (v2) the revision
- `storyboard/`: storyboards from Week 2
- `test_runs/`: saved outputs of the three test runs

## Development record
- **Week 2 storyboard → Week 3 prototype.** I turned the storyboard into one system path: answer → check each sentence → highlight → student decides. (commit `f12c3aa`)
- **v1 → v2 after Test B.** In v1, a highlight only meant "the model changed its answer". Test B showed a made-up paper with no highlight, because the model repeated it every time. I added a paper check and a "Why?" reason. I checked it by running Test B again: the fake paper is now marked NOT VERIFIED. (commit `8199712`, spec and test records)
- **Cut back to the lab scope.** I removed extra parts (an HTML comparison page, screenshots, a clarifying question and a "search down" test) so I can explain every part. The clarifying question is now planned. (commit `70b5bd0`)

## AI assistance
- **Tool:** Claude (Anthropic), in the Claude app.
- **What I asked for:** help to write the simulation code, the mock data, the diagrams, `01_SPEC.md`, this README and a draft of my report, and to correct my English.
- **How I used or changed it:** I chose the use case and the scope. I asked for the test output to be made easier to read, and later asked to remove the extra features. Details are in `02_PROMPT_LOG.md`.
- **How I checked it:** I ran Test B on v1 and v2 in my own terminal and compared the output with `test_runs/`. I checked the references against the publisher pages.

## Additional files
None. Everything is in this repository.
