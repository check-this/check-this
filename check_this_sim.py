"""Check-this simulation for Lab 3.

A student asks a study chatbot a question. The system checks each sentence
of the answer and highlights the ones that may be unreliable.

What is real and what is mocked:
  [MOCKED]       the language model answers (mock_data.json)
  [MOCKED]       the source / paper search (a small index in mock_data.json)
  [IMPLEMENTED]  the checks, the highlight rule and the response text

Usage:
  python check_this_sim.py --version v1 --test A
  python check_this_sim.py --version v1 --test B
  python check_this_sim.py --version v2 --test B
  python check_this_sim.py --all     # runs the three cases and saves them in test_runs/
"""
import argparse
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "mock_data.json").read_text(encoding="utf-8"))

TESTS = {
    "A": "When was the Gutenberg Bible printed, and how many copies were made?",
    "B": "can u give me a source about AI in school for my essay",
}


def numbers(text):
    return sorted(re.findall(r"\d+", text))


def is_reference(text):
    """A sentence that looks like a paper reference, e.g. 'Smith, J. (2021). Title. Journal, 12(3)'."""
    return bool(re.search(r"\(\d{4}\)", text) and re.search(r"\d+\(\d+\)", text))


def get_answer(question):
    """[MOCKED] stands in for the language model."""
    q = question.lower()
    for item in DATA["model_answers"].values():
        if all(t in q for t in item["triggers"]):
            return item
    return None


def search_sources(sentence):
    """[MOCKED] stands in for a web search: pages that share a keyword with the sentence."""
    s = sentence.lower()
    return [r["id"] for r in DATA["source_index"] if any(k in s for k in r["keywords"])]


def paper_exists(sentence):
    """[IMPLEMENTED, v2] validation step: the paper title must match a real record."""
    m = re.search(r"\(\d{4}\)\.\s*(.+?)\.", sentence)
    title = m.group(1).lower() if m else ""
    return any(r["type"] == "paper" and title in r["title"].lower() for r in DATA["source_index"]) if title else False


def check(version, question):
    """Runs the checks and the highlight rule for every sentence."""
    item = get_answer(question)
    if item is None:
        return None
    results = []
    for i, sentence in enumerate(item["answer"]):
        r = {"text": sentence, "why": []}
        # consistency check: do the numbers stay the same when the model answers again?
        r["same"] = all(numbers(sentence) == numbers(other[i]) for other in item["resamples"])
        if not r["same"]:
            other_nums = sorted({n for o in item["resamples"] for n in numbers(o[i])} - set(numbers(sentence)))
            r["why"].append(f"the number changed when the model answered again (it also said {', '.join(other_nums)})")
        r["sources"] = search_sources(sentence)
        r["paper_found"] = None
        if version == "v2" and is_reference(sentence):
            r["paper_found"] = paper_exists(sentence)
            if not r["paper_found"]:
                r["why"].append("no record of this paper was found in the paper search, so it may not exist")
        # highlight rule
        if version == "v1":
            r["flag"] = not r["same"]
        else:
            r["flag"] = (not r["same"]) or (r["paper_found"] is False)
        results.append(r)
    return results


def record(version, test):
    """Returns a short test record in Markdown."""
    q = TESTS[test]
    kind = "standard input" if test == "A" else "problem input"
    out = [f"# Test {test} on {version} ({kind})\n", "## Input", f'"{q}"\n']
    results = check(version, q)
    if results is None:
        out += ["## Response", "> Sorry, this prototype cannot answer that question.\n"]
        return "\n".join(out)

    out += ["## What the system receives",
            f"- The question, and an answer with {len(results)} sentences. [MOCKED]",
            "- The same question answered 2 more times. [MOCKED]",
            "- Source search results for each sentence. [MOCKED]\n",
            "## What it does"]
    for i, r in enumerate(results, 1):
        steps = ["same in all 3 answers" if r["same"] else "changed when asked again"]
        steps.append("related sources: " + ", ".join(r["sources"]) if r["sources"] else "no source")
        if r["paper_found"] is not None:
            steps.append("paper record found" if r["paper_found"] else "no record of this paper")
        out.append(f"- Sentence {i}: {'; '.join(steps)} -> {'YELLOW' if r['flag'] else 'no highlight'}")
    rule = ("Rule v1: highlight only if the sentence changed when asked again." if version == "v1"
            else "Rule v2: highlight if the sentence changed OR a paper reference has no real record.")
    out += [f"- {rule}\n", "## Response (what the student sees, ! = yellow)"]
    for r in results:
        if r["flag"]:
            label = "NOT VERIFIED" if r["paper_found"] is False else "Check this"
            out.append(f"> ! {r['text']} [{label}]  ")
            if version == "v2":
                out.append(f">   Why? {'; '.join(r['why'])}.  ")
                if r["paper_found"] is False:
                    out.append(">   [Find real papers] [Remove this reference] [I will check it myself]  ")
        else:
            out.append(f"> {r['text']}  ")
    out.append("\n## Next action")
    if version == "v1" and any(is_reference(r["text"]) and not r["flag"] for r in results):
        out.append("- The paper has no highlight, so it looks safe. The student would probably copy it into the essay.")
    out.append("- The student can click the button on each yellow sentence, then check, fix, remove or keep it.\n")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", choices=["v1", "v2"], default="v1")
    ap.add_argument("--test", choices=["A", "B"], default="A")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    if a.all:
        folder = HERE / "test_runs"
        folder.mkdir(exist_ok=True)
        for v, t in [("v1", "A"), ("v1", "B"), ("v2", "B")]:
            (folder / f"{v}_test{t}.md").write_text(record(v, t), encoding="utf-8")
            print("wrote", folder / f"{v}_test{t}.md")
    else:
        print(record(a.version, a.test))


if __name__ == "__main__":
    main()
