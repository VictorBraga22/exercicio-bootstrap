"""Gera as duas versões de design do CV (HTML -> PDF via Chromium headless).

    python3 build.py

Saída (na pasta acima): Victor_Braga_CV_Typographic.pdf e Victor_Braga_CV_Modernist.pdf
Fontes: Inter (TTF estático em fonts/) — evita fontes Type 3 no PDF.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

import content as C

HERE = Path(__file__).resolve().parent
CHROME = "/opt/pw-browsers/chromium"
MIN_MARGIN_MM = 10
NOBREAK = re.compile(r"\w+(?:-\w+)+|[A-Z][A-Za-z]+ \d{4}")


def e(text):
    """Escapa e impede quebras feias: 'point-of-sale', 'CCXP 2022'."""
    return NOBREAK.sub(lambda m: f'<span class="nw">{m.group(0)}</span>', html.escape(text))


def bullet_html(b):
    if isinstance(b, tuple):
        return f"<li><strong>{e(b[0])}</strong> {e(b[1])}</li>"
    return f"<li>{e(b)}</li>"


def bullets(items):
    return "<ul>" + "".join(bullet_html(b) for b in items) + "</ul>"


FONT_FACES = "".join(
    f'@font-face {{ font-family: "CV Inter"; font-weight: {w}; '
    f'src: url("fonts/Inter-{w}.ttf") format("truetype"); }}\n'
    for w in (400, 500, 600, 700))

# Base comum: A4, grid de 12 colunas, Inter (grotesca suíça contemporânea).
BASE_CSS = FONT_FACES + """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
body {
  font-family: "CV Inter", sans-serif;
  font-feature-settings: "cv11" 1;
  -webkit-font-smoothing: antialiased;
  color: #111;
  hyphens: manual;
}
.page { width: 210mm; height: 297mm; padding: var(--mt) var(--mx) var(--mb); }
.grid { display: grid; grid-template-columns: repeat(12, 1fr); column-gap: var(--gutter); }
ul { list-style: none; }
li { position: relative; padding-left: 3mm; }
li::before { content: "–"; position: absolute; left: 0; color: var(--muted); }
strong { font-weight: 600; }
.date, .meta b { font-variant-numeric: tabular-nums; }
.nw { white-space: nowrap; }
h1, h2, h3 { font-weight: inherit; font-size: inherit; }
"""


# ---------------------------------------------------------------------------
# Versão 1 — Tipográfica: só texto, sem cor, sem linhas. Hierarquia apenas por
# tamanho, peso, tom (preto/cinza) e espaço. Rótulos em 3/12, conteúdo em 9/12.
# ---------------------------------------------------------------------------
def typographic():
    css = BASE_CSS + """
:root { --mt: 14mm; --mb: 12mm; --mx: 17mm; --gutter: 4.5mm; --muted: #737373; }
body { font-size: 8pt; line-height: 1.34; }
header { align-items: end; margin-bottom: 5.8mm; }
.name { grid-column: 1 / 10; font-weight: 600; font-size: 28pt; line-height: 1;
        letter-spacing: -0.03em; }
.roles { grid-column: 1 / 10; margin-top: 2.4mm; font-size: 9.6pt; color: var(--muted);
         letter-spacing: -0.005em; }
.contact { grid-column: 10 / 13; grid-row: 1 / 3; align-self: end; font-size: 7.8pt;
           line-height: 1.5; }
.contact span { display: block; }
section { margin-top: 4.2mm; }
.label { grid-column: 1 / 4; font-size: 6.8pt; font-weight: 600; letter-spacing: 0.1em;
         text-transform: uppercase; padding-top: 0.5mm; }
.body { grid-column: 4 / 13; }
.lead { font-size: 8.6pt; line-height: 1.38; letter-spacing: -0.005em; }
.lead + .lead { margin-top: 1.6mm; }
.job + .job { margin-top: 2.4mm; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.job-title { font-weight: 600; font-size: 8.8pt; }
.date { color: var(--muted); white-space: nowrap; font-size: 7.8pt; }
.org { color: var(--muted); margin: 0.2mm 0 0.9mm; }
li + li { margin-top: 0.5mm; }
.inline { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: var(--gutter); }
.edu + .edu { margin-top: 1.2mm; }
.muted { color: var(--muted); }
"""

    def job(t, org, loc, date, items):
        return f"""<div class="job">
  <div class="job-head"><span class="job-title">{e(t)}</span><span class="date">{e(date)}</span></div>
  <div class="org">{e(org)}, {e(loc)}</div>
  {bullets(items)}
</div>"""

    def section(label, body):
        return (f'<section class="grid"><h2 class="label">{e(label)}</h2>'
                f'<div class="body">{body}</div></section>')

    contact = "".join(f"<span>{e(v)}</span>" for _, v in C.CONTACT)
    profile = "".join(f'<p class="lead">{e(p)}</p>' for p in C.PROFILE)
    edu = "".join(
        f'<div class="edu"><div class="job-head"><span class="job-title">{e(s)}</span>'
        f'<span class="date">{e(d)}</span></div><div>{e(x)}&nbsp;<span class="muted">·&nbsp;{e(loc)}</span></div></div>'
        for s, loc, d, x in C.EDUCATION)
    langs = "".join(f"<div><strong>{e(l)}</strong> <span class='muted'>{e(v)}</span></div>"
                    for l, v in C.LANGUAGES)

    body = f"""
<header class="grid">
  <h1 class="name">{e(C.NAME_FIRST)} {e(C.NAME_LAST)}</h1>
  <div class="roles">{" / ".join(e(r) for r in C.ROLES)}</div>
  <address class="contact" style="font-style:normal">{contact}</address>
</header>
{section("Profile", profile)}
{section("Australian Experience", "".join(job(*j) for j in C.AUSTRALIA))}
{section("Design Experience", "".join(job(*j) for j in C.DESIGN))}
{section("Skills", e(", ".join(C.SKILLS)) + ".")}
{section("Education", edu)}
{section("Languages", f'<div class="inline">{langs}</div>')}
"""
    return page(css, body)


# ---------------------------------------------------------------------------
# Versão 2 — Modernista: International Typographic Style (Müller-Brockmann,
# Vignelli). Nome em display grande, régua preta forte, vermelho suíço como
# único acento, seções numeradas, coluna de datas (3/12) + conteúdo (9/12),
# rodapé em três colunas sobre o mesmo grid.
# ---------------------------------------------------------------------------
def modernist():
    css = BASE_CSS + """
:root { --mt: 14mm; --mb: 12mm; --mx: 15mm; --gutter: 4.5mm; --muted: #6b6b6b;
        --red: #E3241B; --rule: #111;
        /* 3 de 12 colunas + 2 gutters */
        --accent-w: calc((100% - 11 * var(--gutter)) / 12 * 3 + 2 * var(--gutter)); }
body { font-size: 7.8pt; line-height: 1.31; }

header { align-items: end; }
.name { grid-column: 1 / 9; grid-row: 1; font-weight: 700; font-size: 34pt; line-height: 0.92;
        letter-spacing: -0.04em; }
.contact { grid-column: 9 / 13; grid-row: 1; align-self: end; font-size: 7.6pt; line-height: 1.5; padding-bottom: 0.4mm; }
.contact dl { display: grid; grid-template-columns: 14mm 1fr; }
.contact dt { color: var(--muted); }
.rule { grid-column: 1 / 13; height: 2.4pt; margin-top: 4.5mm;
        background: linear-gradient(90deg, var(--red) var(--accent-w), var(--rule) var(--accent-w)); }
.roles { margin-top: 2.2mm; }
.roles div { grid-column: span 3; font-size: 8pt; font-weight: 500; }

section { margin-top: 4mm; }
.sec-head { grid-column: 1 / 13; display: grid; grid-template-columns: subgrid;
            border-top: 0.6pt solid var(--rule); padding-top: 1.3mm; margin-bottom: 2.2mm; }
.sec-num { grid-column: 1 / 4; color: var(--red); font-weight: 600; font-variant-numeric: tabular-nums; }
.sec-title { grid-column: 4 / 13; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }

.profile p { grid-column: 4 / 13; font-size: 8.4pt; line-height: 1.4; letter-spacing: -0.005em; }
.profile p + p { margin-top: 1.4mm; }

.job { grid-column: 1 / 13; display: grid; grid-template-columns: subgrid; }
.job + .job { margin-top: 2.1mm; }
.meta { grid-column: 1 / 4; color: var(--muted); font-size: 7.6pt; line-height: 1.42; padding-top: 0.3mm; }
.meta b { display: block; color: #111; font-weight: 500; }
.detail { grid-column: 4 / 13; }
.job-title { font-weight: 600; font-size: 8.8pt; line-height: 1.3; }
.org { color: var(--muted); margin-bottom: 0.8mm; }
li + li { margin-top: 0.3mm; }

.footer { margin-top: 4mm; }
.col { border-top: 0.6pt solid var(--rule); padding-top: 1.4mm; }
.col h3 { font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 2.4mm; }
.col h3 span { color: var(--red); margin-right: 2mm; font-variant-numeric: tabular-nums; }
.c1 { grid-column: 1 / 4; } .c2 { grid-column: 4 / 9; } .c3 { grid-column: 9 / 13; }
.edu + .edu { margin-top: 1.6mm; }
.muted { color: var(--muted); }
.langs div, .row { display: flex; justify-content: space-between; gap: 3mm; }
"""

    def job(t, org, loc, date, items):
        return f"""<div class="job">
  <div class="meta"><b>{e(date)}</b>{e(loc)}</div>
  <div class="detail"><div class="job-title">{e(t)}</div><div class="org">{e(org)}</div>{bullets(items)}</div>
</div>"""

    def sec_head(n, title):
        return (f'<div class="sec-head"><span class="sec-num">{n:02d}</span>'
                f'<h2 class="sec-title">{e(title)}</h2></div>')

    contact = "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in C.CONTACT)
    roles = "".join(f"<div>{e(r)}</div>" for r in C.ROLES)
    profile = "".join(f"<p>{e(p)}</p>" for p in C.PROFILE)
    skills = e(", ".join(C.SKILLS)) + "."
    edu = "".join(
        f'<div class="edu"><div class="row"><strong>{e(s)}</strong><span class="muted date">{e(d)}</span></div>'
        f'<div>{e(x)}&nbsp;<span class="muted">·&nbsp;{e(loc)}</span></div></div>' for s, loc, d, x in C.EDUCATION)
    langs = "".join(f"<div><span>{e(l)}</span><span class='muted'>{e(v)}</span></div>"
                    for l, v in C.LANGUAGES)

    body = f"""
<header class="grid">
  <h1 class="name">{e(C.NAME_FIRST)}<br>{e(C.NAME_LAST)}</h1>
  <div class="contact"><dl>{contact}</dl></div>
  <div class="rule" aria-hidden="true"></div>
</header>
<div class="grid roles">{roles}</div>
<section class="grid profile">{sec_head(1, "Profile")}{profile}</section>
<section class="grid">{sec_head(2, "Australian Experience")}{"".join(job(*j) for j in C.AUSTRALIA)}</section>
<section class="grid">{sec_head(3, "Design Experience")}{"".join(job(*j) for j in C.DESIGN)}</section>
<div class="grid footer">
  <div class="col c1 langs"><h3><span>04</span>Languages</h3>{langs}</div>
  <div class="col c2"><h3><span>05</span>Education</h3>{edu}</div>
  <div class="col c3"><h3><span>06</span>Skills</h3><p>{skills}</p></div>
</div>
"""
    return page(css, body)


def page(css, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Victor Braga – CV</title>
<meta name="author" content="Victor Braga">
<style>{css}</style></head>
<body><main class="page">{body}</main></body></html>
"""


def render(name, html_text):
    src = HERE / f"{name}.html"
    out = HERE.parent / f"{name}.pdf"
    src.write_text(html_text, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={out}", src.as_uri()],
                   check=True, capture_output=True)
    pages = subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout
    n = int(next(l for l in pages.splitlines() if l.startswith("Pages:")).split()[1])
    bbox = subprocess.run(["pdftotext", "-bbox", str(out), "-"], capture_output=True, text=True).stdout
    ys = [(float(a), float(b)) for a, b in re.findall(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)"', bbox)]
    top = min(a for a, _ in ys) * 25.4 / 72
    bottom = (841.92 - max(b for _, b in ys)) * 25.4 / 72
    print(f"wrote {out.name}: {n} page(s), text margins top {top:.1f}mm / bottom {bottom:.1f}mm")
    if n != 1:
        sys.exit(f"ERROR: {out.name} has {n} pages; content overflows A4")
    if bottom < MIN_MARGIN_MM:
        sys.exit(f"ERROR: {out.name} bottom margin {bottom:.1f}mm < {MIN_MARGIN_MM}mm")


if __name__ == "__main__":
    which = sys.argv[1:] or ["typographic", "modernist"]
    if "typographic" in which:
        render("Victor_Braga_CV_Typographic", typographic())
    if "modernist" in which:
        render("Victor_Braga_CV_Modernist", modernist())
