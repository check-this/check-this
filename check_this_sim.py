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
  python check_this_sim.py --html       # writes compare_view.html: v1 and v2 side by side, as the student sees them
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
def analyse(version, question, item, source_down=False):
    """Runs the checks and the flag rule. Returns (clarify, results, search_ok)."""
    clarify = None
    if version == "v2":
        vague, topic = vague_source_request(question)
        if vague:
            clarify = topic

    answer, resamples = item["answer"], item["resamples"]

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

    return clarify, results, search_ok


def run(version, test, source_down=False):
    """Run one test and return a short, readable test record (Markdown)."""
    question = TESTS[test]
    kind = "standard input" if test == "A" else "problem input (vague request for a source)"
    out = []
    p = out.append
    title = f"Test {test} on {version}: {kind}" + (", source search down" if source_down else "")
    p(f"# {title}\n")
    p(f"Screen: `test_screens/test{test}{'_search_down' if source_down else ''}.png` (v1 left, v2 right)\n")

    p("## 1. Input")
    p(f"The student types: **\"{question}\"**\n")

    key, item = pick_mock_answer(question)
    if item is None:
        p("## 2. What the system receives\n- Only the question. There is no answer for it in this prototype. [MOCKED]\n")
        p("## 3. What it does\n- Stops.\n")
        p("## 4. Response and next action\n> Sorry, this prototype cannot answer that question.\n\nThe student can ask one of the test questions.\n")
        return "\n".join(out)

    clarify, results, search_ok = analyse(version, question, item, source_down)

    p("## 2. What the system receives")
    p(f"- The question above.")
    p(f"- An answer with {len(results)} sentences, plus the same question answered 2 more times. [MOCKED: mock_data.json]")
    p("- Source search results for each sentence. [MOCKED]" + (" **In this run the search fails.**" if source_down else "") + "\n")

    p("## 3. What it does")
    n = 1
    if version == "v2":
        p(f"{n}. Checks the request: " + (f"it asks for a source, but the topic is only \"{' '.join(clarify)}\", so it is **too vague**." if clarify else "it is clear enough.")); n += 1
    p(f"{n}. Checks each sentence:"); n += 1
    for i, r in enumerate(results, 1):
        bits = []
        bits.append("same in all 3 answers" if r["consistent"] else "**changed** when asked again")
        if not search_ok:
            bits.append("search failed")
        elif r["sources"]:
            bits.append("related sources found: " + ", ".join(s["id"] for s in r["sources"]))
        else:
            bits.append("no source found")
        if version == "v2":
            if r["type"] == "reference":
                bits.append({True: "paper record found", False: "**no record of this paper**", None: "paper not checked"}[r["verified"]])
            elif r["type"] == "number/date" and r["verified"] is not None:
                bits.append("number found in a source" if r["verified"] else "number not found in a source")
        verdict = "**YELLOW**" if r["flag"] else "no highlight"
        p(f"   - Sentence {i}: \"{r['text']}\" → {'; '.join(bits)} → {verdict}")
    if version == "v1":
        p(f"{n}. Rule v1: highlight only the sentences that changed. (The sources do not change the decision.)\n")
    else:
        p(f"{n}. Rule v2: highlight if it changed **or** it could not be verified. If the search fails, mark facts as \"Not checked\".\n")

    p("## 4. Response and next action")
    p("What the student sees (⚠ = yellow highlight):\n")
    if version == "v2" and not search_ok:
        p("> **Notice:** I could not reach the source search, so references, numbers and dates are marked Not checked.")
    if clarify:
        p("> **Your request is broad.** Which part of \"AI in school\" is your essay about? [AI tutors] [AI and exams] [Teachers using AI] [Type my own topic]")
    for r in results:
        if r["flag"]:
            if version == "v2" and not search_ok:
                lab = "Not checked"
            elif version == "v2" and r["type"] == "reference" and r["verified"] is False:
                lab = "NOT VERIFIED"
            else:
                lab = "Check this"
            p(f"> ⚠ {r['text']} **[{lab}]**")
            if version == "v2":
                p(f">   Why? {'; '.join(r['reasons'])}.")
                if r["type"] == "reference":
                    p(">   [" + ("Find real papers" if search_ok else "Try the search again") + "] [Remove this reference] [I will check it myself]")
        else:
            mark = " **[Checked]**" if (version == "v2" and r["verified"]) else ""
            p(f"> {r['text']}{mark}")
    if version == "v2" and clarify and search_ok:
        p("> Real papers found in the search: " + "; ".join(f"{s['id']} {s['title']}" for s in DATA["source_index"] if s["type"] == "paper"))
    p("")

    p("Next action:")
    if version == "v1":
        flagged = [i for i, r in enumerate(results, 1) if r["flag"]]
        p(f"- The student can click \"Check this\" on sentence {', '.join(map(str, flagged))}.")
        hidden = [i for i, r in enumerate(results, 1) if not r["flag"] and r["type"] == "reference"]
        if hidden:
            p(f"- Sentence {', '.join(map(str, hidden))} (the paper) has no highlight, so it looks safe. The student would probably copy it.")
        if source_down:
            p("- Nothing tells the student that the search failed.")
    else:
        if clarify:
            p("- Pick a narrower topic.")
        p("- Read the reason on each yellow sentence, then check, fix, remove or keep it.")
        if clarify and search_ok:
            p("- Use a real paper from the search instead of the unverified one.")
        if not search_ok:
            p("- Try again later, or check the \"Not checked\" facts by hand.")
    p("")

    # one-line result, the same idea as the verdict in compare_view.html
    hidden = [r for r in results if r["type"] == "reference" and not r["flag"]]
    if hidden:
        res = "PROBLEM: the made-up paper is not highlighted."
    elif version == "v1" and source_down:
        res = "PROBLEM: the search failed, but the student is not told."
    elif version == "v2" and not search_ok:
        res = "OK: the student is told the search failed."
    elif version == "v2" and clarify:
        res = "OK: the made-up paper is caught, each flag has a reason, and the system asks before guessing."
    else:
        res = "OK: the wrong number is highlighted."
    p(f"**Result:** {res}\n")
    # keep each quoted line on its own line in Markdown viewers
    return "\n".join(l + "  " if l.startswith(">") else l for l in out)


# ---------- visual view (HTML) ----------
CSS = """
*{box-sizing:border-box}body{margin:0;background:#f6f8fa;font-family:Helvetica,Arial,sans-serif;color:#1f2328}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px}
h1{margin:0 0 6px;font-size:26px}.sub{color:#59636e;margin:0 0 22px}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
.tabs button{border:1px solid #d0d7de;background:#fff;border-radius:20px;padding:8px 16px;font-size:14px;cursor:pointer}
.tabs button.on{background:#1f2328;color:#fff;border-color:#1f2328}
.case{display:none}.case.on{display:block}
.q{background:#2f6feb;color:#fff;border-radius:16px 16px 4px 16px;padding:10px 14px;display:inline-block;margin:0 0 6px}
.qlab{font-size:13px;color:#59636e;margin-bottom:16px}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:820px){.cols{grid-template-columns:1fr}}
.col{background:#fff;border:2px solid #d0d7de;border-radius:12px;overflow:hidden}
.col.v2{border-color:#6639ba}
.ch{padding:10px 14px;font-weight:700;background:#eaeef2}.col.v2 .ch{background:#efe6ff;color:#4b2a91}
.chat{padding:14px}
.bot{background:#fff;border:1px solid #d0d7de;border-radius:14px 14px 14px 4px;padding:10px 12px;line-height:1.6;font-size:14.5px}
.s{display:block;margin:2px 0;padding:2px 4px;border-radius:4px}
.s.y{background:#ffe066}.s.g{background:#e6f6ea}
.tag{display:inline-block;font-size:11px;font-weight:700;color:#fff;border-radius:10px;padding:1px 8px;margin-left:6px;vertical-align:middle}
.t-chk{background:#9a6700}.t-nv{background:#cf222e}.t-ok{background:#1a7f37}.t-nc{background:#59636e}
.why{font-size:13px;color:#4b2a91;margin:2px 0 6px 6px}
.btns{margin:2px 0 8px 6px}.btns span{display:inline-block;border:1px solid #8c959f;border-radius:6px;padding:2px 8px;font-size:12px;margin:2px 4px 2px 0;background:#fff}
.note{border-radius:10px;padding:9px 12px;font-size:14px;margin-bottom:10px}
.n-clar{background:#efe6ff;border:1px solid #6639ba}.n-down{background:#fff1e5;border:1px solid #bc4c00}
.real{font-size:13px;margin-top:10px;padding-top:8px;border-top:1px dashed #d0d7de}
.risk{margin:12px 14px 14px;border-radius:10px;padding:9px 12px;font-size:13.5px}
.risk.bad{background:#ffebe9;border:1px solid #cf222e}.risk.good{background:#dafbe1;border:1px solid #1a7f37}
details{margin:0 14px 14px;font-size:13px}summary{cursor:pointer;color:#59636e}
table{border-collapse:collapse;width:100%;margin-top:8px}td,th{border:1px solid #d0d7de;padding:4px 6px;text-align:left;vertical-align:top}th{background:#f6f8fa}
.legend{margin-top:20px;font-size:13px;color:#59636e}
"""


def _esc(t):
    return (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def _panel(version, test, source_down):
    question = TESTS[test]
    key, item = pick_mock_answer(question)
    clarify, results, search_ok = analyse(version, question, item, source_down)
    h = []
    if version == "v2" and not search_ok:
        h.append('<div class="note n-down"><b>Notice:</b> I could not reach the source search, so references, numbers and dates are marked <b>Not checked</b>.</div>')
    if clarify:
        h.append('<div class="note n-clar"><b>Your request is broad.</b> Which part of "AI in school" is your essay about?'
                 '<div class="btns"><span>AI tutors</span><span>AI and exams</span><span>Teachers using AI</span><span>Type my own topic</span></div></div>')
    h.append('<div class="bot">')
    for r in results:
        if r["flag"]:
            if version == "v2" and not search_ok:
                tag = '<span class="tag t-nc">Not checked</span>'
            elif version == "v2" and r["type"] == "reference" and r["verified"] is False:
                tag = '<span class="tag t-nv">NOT VERIFIED</span>'
            else:
                tag = '<span class="tag t-chk">Check this</span>'
            h.append(f'<span class="s y">{_esc(r["text"])}{tag}</span>')
            if version == "v2":
                h.append(f'<div class="why">Why? {_esc("; ".join(r["reasons"]))}.</div>')
                if r["type"] == "reference":
                    first = "Find real papers" if search_ok else "Try the search again"
                    h.append(f'<div class="btns"><span>{first}</span><span>Remove this reference</span><span>I will check it myself</span></div>')
        else:
            ok = version == "v2" and r["verified"]
            tag = '<span class="tag t-ok">Checked</span>' if ok else ""
            h.append(f'<span class="s{" g" if ok else ""}">{_esc(r["text"])}{tag}</span>')
    if version == "v2" and clarify and search_ok:
        h.append('<div class="real"><b>Real papers found in the paper search</b> (open them before you use them):<br>'
                 + "<br>".join(f'{s["id"]}: {_esc(s["title"])}' for s in DATA["source_index"] if s["type"] == "paper") + "</div>")
    h.append("</div>")
    chat = "".join(h)

    # one-line verdict for the person reading the comparison
    hidden_ref = [r for r in results if r["type"] == "reference" and not r["flag"]]
    if hidden_ref:
        risk = '<div class="risk bad">✗ The made-up reference has <b>no highlight</b>, so it looks safe to copy.</div>'
    elif version == "v1" and source_down:
        risk = '<div class="risk bad">✗ The source search failed, but nothing tells the student.</div>'
    elif version == "v2" and not search_ok:
        risk = '<div class="risk good">✓ The student is told the search failed, and the facts are marked Not checked.</div>'
    elif version == "v2" and clarify:
        risk = '<div class="risk good">✓ The fake reference is caught, each flag has a reason, and the system asks before guessing.</div>'
    else:
        n = sum(r["flag"] for r in results)
        risk = f'<div class="risk good">✓ {n} sentence(s) flagged for checking.' + (" Each flag shows a reason." if version == "v2" else "") + "</div>"

    rows = "".join(
        f'<tr><td>{i}</td><td>{"yes" if r["consistent"] else "<b>no</b>"}</td>'
        f'<td>{", ".join(s["id"] for s in r["sources"]) or ("search down" if not search_ok else "none")}</td>'
        f'<td>{({None: "-", True: "yes", False: "<b>no</b>"}[r["verified"]]) if version == "v2" else "not checked"}</td>'
        f'<td>{"YELLOW" if r["flag"] else "-"}</td></tr>' for i, r in enumerate(results, 1))
    table = ('<details><summary>What the system checked (sentence by sentence)</summary><table>'
             '<tr><th>#</th><th>Same when asked again?</th><th>Sources found</th><th>Verified</th><th>Flag</th></tr>'
             + rows + "</table></details>")
    title = "v1 — before revision" if version == "v1" else "v2 — after revision"
    return f'<div class="col {version}"><div class="ch">{title}</div><div class="chat">{chat}</div>{risk}{table}</div>'


def render_html():
    cases = [("A", False, "Test A · standard input"), ("B", False, "Test B · problem input"),
             ("B", True, "Test B · source search down")]
    tabs, bodies = [], []
    for n, (t, down, label) in enumerate(cases):
        on = " on" if n == 0 else ""
        tabs.append(f'<button class="{on.strip()}" onclick="show({n})">{label}</button>')
        lab = "The student types this question." + (" In this run the source search is unavailable (mocked failure)." if down else "")
        bodies.append(f'<div class="case{on}" id="c{n}"><div class="q">{_esc(TESTS[t])}</div><div class="qlab">{lab}</div>'
                      f'<div class="cols">{_panel("v1", t, down)}{_panel("v2", t, down)}</div></div>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Check-this comparison</title><style>{CSS}</style></head><body><div class="wrap">
<h1>Check-this prototype: v1 vs v2</h1>
<p class="sub">What the student would see in the chat. Generated by <code>python check_this_sim.py --html</code>. The model answers and the source search are mocked (mock_data.json).</p>
<div class="tabs">{"".join(tabs)}</div>{"".join(bodies)}
<p class="legend">Yellow = the system thinks this may be unreliable · Green = checked against a found source · Purple border = changed in v2 · Names and papers are placeholders.</p>
</div><script>function show(i){{document.querySelectorAll('.case').forEach((c,j)=>c.classList.toggle('on',i===j));document.querySelectorAll('.tabs button').forEach((b,j)=>b.classList.toggle('on',i===j));}}</script></body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", choices=["v1", "v2"], default="v2")
    ap.add_argument("--test", choices=list(TESTS), default="A")
    ap.add_argument("--source-down", action="store_true")
    ap.add_argument("--all", action="store_true", help="run every case and save to test_runs/")
    ap.add_argument("--html", action="store_true", help="write compare_view.html (v1 and v2 side by side)")
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
    if a.all or a.html:
        (HERE / "compare_view.html").write_text(render_html(), encoding="utf-8")
        print("wrote", HERE / "compare_view.html")
    if not (a.all or a.html):
        print(run(a.version, a.test, a.source_down))


if __name__ == "__main__":
    main()
