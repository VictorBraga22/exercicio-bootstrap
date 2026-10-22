"""Gera o CV de Victor Braga (HTML -> PDF via Chromium headless).

    python3 build.py

Saída (na pasta acima): Victor_Braga_CV_Modernist.pdf
Fontes: Inter (TTF estático em fonts/) — evita fontes Type 3 no PDF.
O build falha se o PDF passar de 1 página ou se a margem inferior real do texto
ficar abaixo de MIN_MARGIN_MM.

Layout — International Typographic Style (Müller-Brockmann, Vignelli):
composição assimétrica com painel lateral que sangra a página (contato, idiomas,
skills, educação) e coluna principal com o nome em display e seções numeradas.
Cada bloco lateral pendura na mesma régua horizontal da seção principal ao lado.
O vermelho suíço é o único acento: faixa do painel, numeração e marcadores.
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

FONT_FACES = "".join(
    f'@font-face {{ font-family: "CV Inter"; font-weight: {w}; '
    f'src: url("fonts/Inter-{w}.ttf") format("truetype"); }}\n'
    for w in (400, 500, 600, 700))

CSS = FONT_FACES + """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
:root {
  --mt: 15mm; --mb: 13mm;
  --ml: 12mm;        /* margem esquerda do texto lateral (painel sangra até a borda) */
  --side: 40mm;      /* coluna de texto lateral */
  --inset: 9mm;      /* respiro entre o texto lateral e a borda direita do painel */
  --gap: 10mm;       /* do painel até a coluna principal */
  --mr: 13mm;
  --muted: #6b6b6b; --red: #E3241B; --panel: #F1F1EE; --ink: #111;
}
body {
  font-family: "CV Inter", sans-serif;
  font-feature-settings: "cv11" 1;
  -webkit-font-smoothing: antialiased;
  color: var(--ink);
  font-size: 8pt; line-height: 1.42;
  text-wrap: pretty;
}
.page {
  position: relative; width: 210mm; height: 297mm;
  padding: var(--mt) var(--mr) var(--mb) var(--ml);
  display: grid; align-items: start;
  grid-template-columns: var(--side) 1fr;
  grid-template-rows: auto auto 1fr;
  column-gap: calc(var(--inset) + var(--gap));
  row-gap: 8.4mm;
}
/* painel: sangra topo, base e esquerda, com faixa vermelha no topo */
.page::before {
  content: ""; position: absolute; inset: 0 auto 0 0;
  width: calc(var(--ml) + var(--side) + var(--inset));
  background: var(--panel); border-top: 4mm solid var(--red);
}
.page > * { position: relative; }
.m { grid-column: 2; } .s { grid-column: 1; }
.r1 { grid-row: 1; } .r2 { grid-row: 2; } .r3 { grid-row: 3; }
.rule { border-top: 0.75pt solid var(--ink); padding-top: 2mm; }

ul { list-style: none; }
strong { font-weight: 600; }
a { color: inherit; text-decoration: none; }
h1, h2 { font-weight: inherit; font-size: inherit; }
address { font-style: normal; }
.nw { white-space: nowrap; }
.muted { color: var(--muted); }
.tnum { font-variant-numeric: tabular-nums; }

/* cabeçalho */
.name { font-weight: 700; font-size: 44pt; line-height: 0.9; letter-spacing: -0.045em;
        word-spacing: 0.14em; margin-left: -0.6mm; }
.roles { margin-top: 4mm; font-size: 9.4pt; font-weight: 500; letter-spacing: -0.005em; }
.roles span { color: var(--red); margin: 0 1.6mm; font-weight: 400; }

/* títulos de seção: mesmo sistema nas duas colunas */
.head { display: flex; gap: 2.6mm; align-items: baseline; margin-bottom: 3.2mm;
        font-size: 7pt; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
        line-height: 1.45; }
.head .n { color: var(--red); letter-spacing: 0; font-variant-numeric: tabular-nums; }
.head .dot { align-self: center; width: 1.5mm; height: 1.5mm; background: var(--red);
             flex: none; }

/* coluna principal */
.profile { margin-top: 8mm; }
.lead { font-size: 8.5pt; line-height: 1.48; letter-spacing: -0.005em; }
.lead + .lead { margin-top: 2mm; }
.job + .job { margin-top: 3.8mm; }
.job-title { font-weight: 600; font-size: 9pt; line-height: 1.35; }
.org { color: var(--muted); margin: 0.4mm 0 1.4mm; }
.org .date { color: var(--ink); font-variant-numeric: tabular-nums; }
.org .sep { margin: 0 1.4mm; }
.m li { position: relative; padding-left: 3.2mm; }
.m li::before { content: "–"; position: absolute; left: 0; color: var(--muted); }
.m li + li { margin-top: 0.8mm; }

/* coluna lateral */
.s .block + .block { margin-top: 7mm; }
.s dt { color: var(--muted); font-size: 7pt; }
.s dd + dt { margin-top: 2.2mm; }
.s dd { line-height: 1.35; }
.langs li { display: flex; justify-content: space-between; }
.s li + li { margin-top: 1mm; }
.edu + .edu { margin-top: 3.2mm; }
.edu strong { display: block; line-height: 1.35; }
.edu .tnum { margin: 0.4mm 0 0.8mm; }
.contact { padding-top: 1.4mm; }
"""


def e(text):
    """Escapa e impede quebras feias: 'point-of-sale', 'CCXP 2022'."""
    return NOBREAK.sub(lambda m: f'<span class="nw">{m.group(0)}</span>', html.escape(text))


def link(text, href):
    shown = html.escape(text).replace("/", "/<wbr>")  # quebra só depois da barra
    return f'<a href="{html.escape(href)}">{shown}</a>' if href else shown


def bullet(b):
    if isinstance(b, tuple):
        return f"<li><strong>{e(b[0])}</strong> {e(b[1])}</li>"
    return f"<li>{e(b)}</li>"


def job(title, org, loc, date, items):
    return (f'<div class="job"><div class="job-title">{e(title)}</div>'
            f'<div class="org">{e(org)}, {e(loc)}<span class="sep">·</span>'
            f'<span class="date nw">{html.escape(date)}</span></div>'
            f'<ul>{"".join(bullet(b) for b in items)}</ul></div>')


def main_head(n, title):
    return f'<h2 class="head"><span class="n">{n:02d}</span>{e(title)}</h2>'


def side_head(title):
    return f'<h2 class="head"><span class="dot"></span>{e(title)}</h2>'


def build():
    contact = "".join(f"<dt>{e(k)}</dt><dd>{link(v, h)}</dd>" for k, v, h in C.CONTACT)
    langs = "".join(f"<li><span>{e(l)}</span><span class='muted'>{e(v)}</span></li>"
                    for l, v in C.LANGUAGES)
    skills = "".join(f"<li>{e(s[:1].upper() + s[1:])}</li>" for s in C.SKILLS)
    edu = "".join(
        f'<div class="edu"><strong>{e(s)}</strong><div class="muted tnum">{e(d)}<br>{e(loc)}</div>'
        f'<div>{e(x)}</div></div>' for s, loc, d, x in C.EDUCATION)
    profile = "".join(f'<p class="lead">{e(p)}</p>' for p in C.PROFILE)
    roles = '<span>/</span>'.join(e(r) for r in C.ROLES)
    au = "".join(job(*j) for j in C.AUSTRALIA)
    design = "".join(job(*j) for j in C.DESIGN)

    body = f"""
<div class="m r1">
  <header>
    <h1 class="name">{e(C.NAME_FIRST)} {e(C.NAME_LAST)}</h1>
    <div class="roles">{roles}</div>
  </header>
  <section class="rule profile">{main_head(1, "Profile")}{profile}</section>
</div>
<div class="s r1 contact">{side_head("Contact")}<address><dl>{contact}</dl></address></div>
<section class="m r2 rule">{main_head(2, "Australian Experience")}{au}</section>
<div class="s r2 rule">
  <div class="block">{side_head("Languages")}<ul class="langs">{langs}</ul></div>
  <div class="block">{side_head("Skills")}<ul>{skills}</ul></div>
</div>
<section class="m r3 rule">{main_head(3, "Design Experience")}{design}</section>
<div class="s r3 rule">{side_head("Education")}{edu}</div>
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Victor Braga – CV</title>
<meta name="author" content="Victor Braga">
<style>{CSS}</style></head>
<body><div class="page">{body}</div></body></html>
"""


def render(name, html_text):
    src = HERE / f"{name}.html"
    out = HERE.parent / f"{name}.pdf"
    src.write_text(html_text, encoding="utf-8")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu",
                    "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={out}", src.as_uri()],
                   check=True, capture_output=True)
    info = subprocess.run(["pdfinfo", str(out)], capture_output=True, text=True).stdout
    n = int(next(l for l in info.splitlines() if l.startswith("Pages:")).split()[1])
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
    render("Victor_Braga_CV_Modernist", build())
