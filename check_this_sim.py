"""Check-this simulation for Lab 3.

Runs the system path from my Week 2 storyboard: a student asks a study
chatbot a question, the system checks each sentence of the answer and marks
the ones that may be unreliable.

What is real and what is mocked:
  [MOCKED]       the language model answer and the resamples (mock_data.json)
  [MOCKED]       the source / paper search (a small local index in mock_data.json)
  [IMPLEMENTED]  consistency check, sentence type check, source matching,
                 flag decision, vague-request check, response text

Usage:
  python check_this_sim.py --version v1 --test A
  python check_this_sim.py --version v2 --test B
  python check_this_sim.py --version v2 --test B --source-down
  python check_this_sim.py --all        # runs every case and writes test_runs/*.md
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

STOPWORDS = {"can", "u", "you", "give", "me", "a", "an", "the", "about", "for", "my",
             "essay", "in", "on", "of", "some", "source", "sources", "paper", "papers",
             "reference", "references", "article", "please", "find", "i", "need"}
SOURCE_WORDS = ("source", "paper", "reference", "article", "citation")


# ---------- small helpers ----------
def numbers(text):
    return sorted(re.findall(r"\d+", text))


def sentence_type(text):
    """[IMPLEMENTED in v2] rough type of a sentence, used to decide what must be verified."""
    if re.search(r"\(\d{4}\)", text) and re.search(r"\d+\(\d+\)", text):
        return "reference"
    if re.search(r"\d", text):
        return "number/date"
    return "general"


def pick_mock_answer(question):
    """[MOCKED] stands in for calling the language model."""
    q = question.lower()
    for key, item in DATA["model_answers"].items():
        if all(t in q for t in item["triggers"]):
            return key, item
    return None, None


def search_sources(sentence, source_down):
    """[MOCKED] stands in for a web / paper search API. Returns matching records."""
    if source_down:
        raise ConnectionError("source search unavailable")
    s = sentence.lower()
    return [r for r in DATA["source_index"] if any(k in s for k in r["keywords"])]


def exact_record(sentence, source_down):
    """[IMPLEMENTED in v2] validation step: a reference must match a real record by title."""
    if source_down:
        raise ConnectionError("source search unavailable")
    m = re.search(r"\(\d{4}\)\.\s*(.+?)\.", sentence)
    title = m.group(1).lower() if m else ""
    return [r for r in DATA["source_index"] if r["type"] == "paper" and title and title in r["title"].lower()]


def vague_source_request(question):
    """[IMPLEMENTED in v2] a source request with very few topic words is treated as vague."""
    q = question.lower()
    if not any(w in q for w in SOURCE_WORDS):
        return False, []
    topic = [w for w in re.findall(r"[a-z]+", q) if w not in STOPWORDS]
    return len(topic) <= 3, topic


# ---------- the system path ----------
def run(version, test, source_down=False):
    question = TESTS[test]
    out = []
    p = out.append
    title = f"{version.upper()} - Test {test}" + (" (source search down)" if source_down else "")
    p(f"# {title}\n")
    p("## Input\n")
    p(f"> {question}\n")

    p("## What the system receives\n")
    p("- The student's question (text).")
    p("- [MOCKED] One model answer and two resampled answers to the same question.")
    p("- [MOCKED] Results from the source search for each sentence." + (" The search is DOWN in this run." if source_down else "") + "\n")

    p("## What it does\n")
    steps = []
    key, item = pick_mock_answer(question)
    if item is None:
        p("1. [MOCKED] No canned model answer for this question. The simulation stops here.\n")
        return "\n".join(out)

    clarify = None
    if version == "v2":
        vague, topic = vague_source_request(question)
        if vague:
            clarify = topic
            steps.append(f"[IMPLEMENTED] Request check: this asks for a source, but the topic is only {topic}. Marked as vague.")

    answer, resamples = item["answer"], item["resamples"]
    steps.append(f"[MOCKED] Model writes an answer with {len(answer)} sentences and is asked the same question 2 more times.")

    search_ok = True
    results = []
    for i, sent in enumerate(answer):
        r = {"text": sent, "reasons": []}
        # consistency check (v1 and v2)
        same = all(numbers(sent) == numbers(rs[i]) for rs in resamples)
        r["consistent"] = same
        if not same:
            alt = sorted({n for rs in resamples for n in numbers(rs[i])} - set(numbers(sent)))
            r["reasons"].append(f"the numbers changed when the model answered again (also said {', '.join(alt)})")
        # source search
        try:
            r["sources"] = search_sources(sent, source_down)
        except ConnectionError:
            r["sources"], search_ok = [], False
        # v2 only: sentence type + validation
        r["type"] = sentence_type(sent)
        r["verified"] = None
        if version == "v2" and search_ok:
            try:
                if r["type"] == "reference":
                    rec = exact_record(sent, source_down)
                    r["verified"] = bool(rec)
                    if not rec:
                        r["reasons"].append("no matching record for this paper was found in the paper search, so it may not exist")
                elif r["type"] == "number/date":
                    supported = any(any(n in k for k in s["keywords"]) for s in r["sources"] for n in numbers(sent))
                    r["verified"] = supported
                    if not supported and r["consistent"]:
                        r["reasons"].append("no source found that gives this number")
            except ConnectionError:
                search_ok = False
                r["verified"] = None
        # flag decision
        if version == "v1":
            r["flag"] = not r["consistent"]                       # v1: consistency only
        else:
            if not search_ok:
                r["flag"] = r["type"] != "general" or not r["consistent"]
                if r["type"] != "general":
                    r["reasons"].append("the source search was unavailable, so this fact could not be checked")
            else:
                r["flag"] = (not r["consistent"]) or (r["verified"] is False)
        results.append(r)

    steps.append("[IMPLEMENTED] Consistency check: compare the numbers in each sentence with the same sentence in the 2 resamples.")
    if source_down:
        steps.append("[MOCKED] Source search: FAILED (service unavailable)." + (" v1 does not report this." if version == "v1" else " v2 reports it to the student."))
    else:
        steps.append("[MOCKED] Source search: look for sources that match each sentence.")
    if version == "v1":
        steps.append("[IMPLEMENTED] Flag rule v1: highlight a sentence only if it was NOT consistent. Sources are shown but do not change the flag.")
    else:
        steps.append("[IMPLEMENTED] Sentence type check: reference / number-date / general.")
        steps.append("[IMPLEMENTED] Validation v2: a reference must match a real paper record by title; a number must appear in a found source.")
        steps.append("[IMPLEMENTED] Flag rule v2: highlight if NOT consistent OR NOT verified. If the search is down, every reference/number is marked 'Not checked'.")
    for n, s in enumerate(steps, 1):
        p(f"{n}. {s}")
    p("")

    p("### Sentence check table\n")
    p("| # | Sentence | Type | Same in resamples? | Sources found | Verified | Flag |")
    p("|---|---|---|---|---|---|---|")
    for n, r in enumerate(results, 1):
        src = ", ".join(s["id"] for s in r["sources"]) or ("search down" if not search_ok else "none")
        ver = {None: "-", True: "yes", False: "no"}[r["verified"]] if version == "v2" else "(not checked in v1)"
        typ = r["type"] if version == "v2" else "(not used in v1)"
        p(f"| {n} | {r['text']} | {typ} | {'yes' if r['consistent'] else 'no'} | {src} | {ver} | {'YELLOW' if r['flag'] else '-'} |")
    p("")

    # ---------- response ----------
    p("## Response shown to the student\n")
    if version == "v2" and not search_ok:
        p("> **Notice:** I could not reach the source search right now, so I could not check any facts. "
          "References, numbers and dates are marked **Not checked**. You can try again later or check them yourself.\n")
    if clarify:
        p("> **Your request is broad.** Which part of \"AI in school\" is your essay about?  "
          "`[AI tutors]` `[AI and exams]` `[Teachers using AI]` `[Type my own topic]`\n")
    for r in results:
        if r["flag"]:
            label = "Not checked" if (version == "v2" and not search_ok) else ("NOT VERIFIED" if r["verified"] is False and r["type"] == "reference" else "Check this")
            p(f"> =={r['text']}== `[{label}]`")
            if version == "v2":
                p(f">   - Why? {'; '.join(r['reasons'])}.")
                if r["type"] == "reference":
                    if search_ok:
                        p(">   - `[Find real papers]` `[Remove this reference]` `[I will check it myself]`")
                    else:
                        p(">   - `[Try the search again]` `[Remove this reference]` `[I will check it myself]`")
        else:
            mark = " `[Checked: " + ", ".join(s['id'] for s in r['sources']) + "]`" if (version == "v2" and r["verified"]) else ""
            p(f"> {r['text']}{mark}")
    if version == "v2" and clarify and search_ok:
        real = [s for s in DATA["source_index"] if s["type"] == "paper"]
        p(">\n> **Real papers found in the paper search** (open them before you use them):")
        for s in real:
            p(f">   - {s['id']}: {s['title']}")
    p("")

    p("## Next action for the student\n")
    if version == "v1":
        flagged = [n for n, r in enumerate(results, 1) if r["flag"]]
        p(f"- The student sees {len(flagged)} yellow sentence(s): {flagged or 'none'}. They can click \"Check this\" on those.")
        unflagged_refs = [n for n, r in enumerate(results, 1) if not r["flag"] and sentence_type(r["text"]) == "reference"]
        if unflagged_refs:
            p(f"- Sentence(s) {unflagged_refs} look trusted (no highlight), so the student would probably copy them into the essay.")
        if source_down:
            p("- Nothing tells the student that the source search failed.")
    else:
        if clarify:
            p("- Pick a narrower topic, so the system can search again.")
        p("- For each yellow sentence: read the reason, then check it, fix it, remove it or keep it.")
        if search_ok and clarify:
            p("- Open one of the real papers from the search instead of the unverified one.")
        if not search_ok:
            p("- Try again later, or check the 'Not checked' facts by hand.")
    p("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", choices=["v1", "v2"], default="v2")
    ap.add_argument("--test", choices=list(TESTS), default="A")
    ap.add_argument("--source-down", action="store_true")
    ap.add_argument("--all", action="store_true", help="run every case and save to test_runs/")
    a = ap.parse_args()
    if a.all:
        d = HERE / "test_runs"
        d.mkdir(exist_ok=True)
        cases = [("v1", "A", False), ("v1", "B", False), ("v1", "B", True),
                 ("v2", "A", False), ("v2", "B", False), ("v2", "B", True)]
        for v, t, down in cases:
            name = f"{v}_test{t}{'_source_down' if down else ''}.md"
            (d / name).write_text(run(v, t, down), encoding="utf-8")
            print("wrote", d / name)
    else:
        print(run(a.version, a.test, a.source_down))


if __name__ == "__main__":
    main()
