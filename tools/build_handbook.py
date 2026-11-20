#!/usr/bin/env python3
"""Build a single readable handbook (Markdown, and HTML/PDF if pandoc + Chrome exist) from the skill files.
Usage: python3 tools/build_handbook.py [output_dir]   (run from the skill root)"""
import re, glob, os, sys, subprocess, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "handbook")
os.makedirs(OUT, exist_ok=True)
os.chdir(ROOT)

def body(p):
    t = open(p, encoding="utf-8").read()
    if t.startswith("---"):
        t = t.split("---", 2)[2]
    return t.strip() + "\n\n"

def demote(md, levels=1):
    out, code = [], False
    for line in md.splitlines():
        if line.startswith("```"):
            code = not code
        if not code and re.match(r"^#{1,5} ", line):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out) + "\n\n"

version = re.search(r"Project init · (v[\d.]+)", open("SKILL.md").read()).group(1)
n_practices = sum(len(re.findall(r"^## \d\d\.\d+", open(f).read(), re.M)) for f in glob.glob("practices/[0-9][0-9]-*.md"))
n_groups = len(glob.glob("practices/[0-9][0-9]-*.md"))

parts = [f"""# How to review this handbook

This is the full content of the **project-init** skill {version} in reading order: how it works, how it profiles a project, the {n_practices} practices in {n_groups} groups, and the guides. The skill reads the same files; this is a printable view.

**For each practice, ask:**

1. **Correct?** Is the rule right, and current?
2. **Applies at the right time?** Read the `applies:` tag. Would you want this rule in a prototype? In a solo project? Is anything switched on too early or too late?
3. **Actionable?** Could Claude (or a new developer) follow the rule without asking what it means?
4. **Right trade-off?** Where there are `alternatives:`, does the `choose-when:` pick the side you would pick?
5. **Missing?** Anything from your own experience that should be here?

**How to send feedback:** one line per remark, starting with the ID, e.g. `08.3: also mention passkeys`, `T19: default should be schema per tenant`, `Q7: confusing wording`. Rough notes are enough.

**Reading tips:** Parts 1 and 2 take about 15 minutes and make the rest easier. In Part 3 the groups can be read in any order.

"""]
skill = re.sub(r"^# .*\n", "", body("SKILL.md"), count=1)
parts.append("# Part 1 · How the skill works\n\n" + demote(skill))
parts.append("# Part 2 · Profile and questions\n\n" + demote(body("profile.md")) + demote(body("questions.md")))
parts.append(f"# Part 3 · Practices\n\nEach practice: ID and title, `applies` (when it is selected), `rule` (what gets written into the project), `why`, and for trade-offs `alternatives` and `choose-when`.\n\n")
for f in sorted(glob.glob("practices/[0-9][0-9]-*.md")):
    parts.append(demote(body(f)))
parts.append("# Part 4 · Guides\n\nThe tensions table is the decision layer; the other guides feed ADRs and rule files.\n\n")
order = ["principle-tensions", "architecture-styles", "testing-strategy", "database-selection",
         "repo-strategy", "branching", "tool-selection", "llm-evaluation"]
rest = sorted(os.path.basename(g)[:-3] for g in glob.glob("guides/*.md") if os.path.basename(g)[:-3] not in order)
for g in order + rest:
    if os.path.exists(f"guides/{g}.md"):
        parts.append(demote(body(f"guides/{g}.md")))
parts.append("# Appendix A · Detection rules\n\n" + demote(re.sub(r"^# .*\n", "", body("detection.md"), count=1)))
parts.append("# Appendix B · CLAUDE.md template\n\n```markdown\n" + open("templates/CLAUDE.md.tmpl").read() + "\n```\n\n")
parts.append("# Appendix C · Rule file template\n\n```markdown\n" + open("templates/rule-file.md.tmpl").read() + "\n```\n\n")
parts.append("# Appendix D · Proposed settings.json\n\n```json\n" + open("templates/settings.json.tmpl").read() + "\n```\n")

md_path = os.path.join(OUT, "project-init-handbook.md")
open(md_path, "w", encoding="utf-8").write("".join(parts))
print("markdown:", md_path)

css = os.path.join(OUT, "handbook.css")
open(css, "w").write("""
body{font-family:'DejaVu Sans',Arial,sans-serif;font-size:10.5pt;line-height:1.5;max-width:46em;margin:auto;color:#1d1d1f;padding:0 1em}
h1{font-size:20pt;border-bottom:2px solid #333;padding-bottom:.2em;page-break-before:always;margin-top:0}
h2{font-size:15pt;margin-top:1.6em;color:#222;border-bottom:1px solid #ccc}
h3{font-size:11.5pt;margin-top:1.3em;color:#0b4f8a}
table{border-collapse:collapse;font-size:8.5pt;margin:.6em 0;width:100%}
th,td{border:1px solid #bbb;padding:3px 5px;vertical-align:top;text-align:left}
th{background:#eef2f6}
code{font-size:9pt;background:#f3f3f3;padding:0 2px}
pre{background:#f6f6f6;padding:.6em;font-size:8pt;white-space:pre-wrap;page-break-inside:avoid}
li{margin:.15em 0}
#TOC{font-size:10pt} #TOC ul{list-style:none;padding-left:1.2em}
header h1.title{page-break-before:avoid;border:none;font-size:26pt;margin-top:3em}
nav#TOC{page-break-after:always}
""")
if shutil.which("pandoc"):
    html = os.path.join(OUT, "project-init-handbook.html")
    subprocess.run(["pandoc", md_path, "-s", "--toc", "--toc-depth=2", "--embed-resources", "--css", css,
                    "--metadata", f"title=project-init {version} · Handbook", "-o", html], check=True)
    print("html:", html)
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if chrome:
        pdf = os.path.join(OUT, "project-init-handbook.pdf")
        subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", "file://" + html], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("pdf:", pdf)
