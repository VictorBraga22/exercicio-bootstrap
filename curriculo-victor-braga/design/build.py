"""Gera as duas versões de design do CV (HTML -> PDF via Chromium headless).

    python3 build.py

Saída (na pasta acima): Victor_Braga_CV_Typographic.pdf e Victor_Braga_CV_Modernist.pdf
Fontes: Inter (TTF estático em fonts/) — evita fontes Type 3 no PDF.
O build falha se o PDF passar de 1 página ou se a margem inferior real do texto
ficar abaixo de MIN_MARGIN_MM.
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


def link(text, href, wbr=False):
    shown = html.escape(text)
    if wbr:  # permite quebrar o endereço depois da barra, nunca no meio do nome
        shown = shown.replace("/", "/<wbr>")
    return f'<a href="{html.escape(href)}">{shown}</a>' if href else shown


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

# Base comum: A4, Inter (grotesca suíça contemporânea), travessão como marcador.
BASE_CSS = FONT_FACES + """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #fff; }
body {
  font-family: "CV Inter", sans-serif;
  font-feature-settings: "cv11" 1;
  -webkit-font-smoothing: antialiased;
  color: #111;
  text-wrap: pretty;
}
.page { width: 210mm; height: 297mm; padding: var(--mt) var(--mx) var(--mb); }
.grid { display: grid; grid-template-columns: repeat(12, 1fr); column-gap: var(--gutter); }
ul { list-style: none; }
li { position: relative; padding-left: 3mm; }
li::before { content: "–"; position: absolute; left: 0; color: var(--muted); }
strong { font-weight: 600; }
a { color: inherit; text-decoration: none; }
.date, .tnum { font-variant-numeric: tabular-nums; }
.nw { white-space: nowrap; }
.muted { color: var(--muted); }
h1, h2, h3 { font-weight: inherit; font-size: inherit; }
address { font-style: normal; }
"""


# ---------------------------------------------------------------------------
# Versão 1 — Tipográfica: só texto, sem cor, sem linhas. Hierarquia apenas por
# tamanho, peso, tom (preto/cinza) e espaço. Grid de 12 colunas: rótulos em
# 3/12, conteúdo em 9/12, subdividido em terços (contato, idiomas).
# Rótulos e conteúdo alinhados pela primeira linha de base.
# ---------------------------------------------------------------------------
def typographic():
    css = BASE_CSS + """
:root { --mt: 14mm; --mb: 12mm; --mx: 15mm; --gutter: 4.5mm; --muted: #737373; }
body { font-size: 8pt; line-height: 1.33; }
.name { font-weight: 600; font-size: 29pt; line-height: 1; letter-spacing: -0.03em; }
.roles { margin-top: 2.2mm; font-size: 9.8pt; color: var(--muted); letter-spacing: -0.005em; }
section { margin-top: 4.2mm; align-items: baseline; }
section.contact { margin-top: 5.6mm; }
.label { grid-column: 1 / 4; font-size: 6.8pt; font-weight: 600; letter-spacing: 0.1em;
         text-transform: uppercase; }
.body { grid-column: 4 / 13; }
.thirds { display: grid; grid-template-columns: repeat(3, 1fr); column-gap: var(--gutter); }
.lead { font-size: 8.6pt; line-height: 1.38; letter-spacing: -0.005em; }
.lead + .lead { margin-top: 1.6mm; }
.job + .job { margin-top: 2.3mm; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.job-title { font-weight: 600; font-size: 8.8pt; }
.date { color: var(--muted); white-space: nowrap; font-size: 7.8pt; }
.org { color: var(--muted); margin: 0.2mm 0 0.9mm; }
li + li { margin-top: 0.5mm; }
.edu + .edu { margin-top: 1.4mm; }
"""

    def job(t, org, loc, date, items):
        return f"""<div class="job">
  <div class="job-head"><span class="job-title">{e(t)}</span><span class="date">{e(date)}</span></div>
  <div class="org">{e(org)}, {e(loc)}</div>
  {bullets(items)}
</div>"""

    def section(label, body, cls=""):
        return (f'<section class="grid {cls}"><h2 class="label">{e(label)}</h2>'
                f'<div class="body">{body}</div></section>')

    (_, loc, _), (_, phone, phone_href), (_, mail, mail_href), (_, folio, folio_href) = C.CONTACT
    contact = (f'<address class="thirds"><div>{e(loc)}&nbsp;·&nbsp;{link(phone, phone_href)}</div>'
               f'<div>{link(mail, mail_href)}</div><div>{link(folio, folio_href)}</div></address>')
    profile = "".join(f'<p class="lead">{e(p)}</p>' for p in C.PROFILE)
    edu = "".join(
        f'<div class="edu"><div class="job-head"><span class="job-title">{e(s)}</span>'
        f'<span class="date">{e(d)}</span></div>'
        f'<div>{e(x)}&nbsp;<span class="muted">·&nbsp;{e(loc)}</span></div></div>'
        for s, loc, d, x in C.EDUCATION)
    langs = "".join(f"<div><strong>{e(l)}</strong> <span class='muted'>{e(v)}</span></div>"
                    for l, v in C.LANGUAGES)

    body = f"""
<header>
  <h1 class="name">{e(C.NAME_FIRST)} {e(C.NAME_LAST)}</h1>
  <div class="roles">{" / ".join(e(r) for r in C.ROLES)}</div>
</header>
{section("Contact", contact, "contact")}
{section("Profile", profile)}
{section("Australian Experience", "".join(job(*j) for j in C.AUSTRALIA))}
{section("Design Experience", "".join(job(*j) for j in C.DESIGN))}
{section("Skills", e(", ".join(C.SKILLS)) + ".")}
{section("Education", edu)}
{section("Languages", f'<div class="thirds">{langs}</div>')}
"""
    return page(css, body)


# ---------------------------------------------------------------------------
# Versão 2 — Modernista: International Typographic Style (Müller-Brockmann,
# Vignelli). Composição assimétrica: coluna lateral num painel cinza que sangra
# a página (contato, idiomas, skills, educação) e coluna principal com o nome em
# display, seções numeradas em vermelho suíço e réguas finas. O vermelho é o
# único acento: faixa no topo do painel e numeração.
# ---------------------------------------------------------------------------
def modernist():
    css = BASE_CSS + """
:root { --mt: 16mm; --mb: 12mm; --mx: 15mm; --side: 40mm; --gap: 12mm;
        --muted: #6b6b6b; --red: #E3241B; --panel: #F2F2F0; }
body { font-size: 8pt; line-height: 1.36; }
.page { position: relative; display: grid; grid-template-columns: var(--side) 1fr;
        grid-template-rows: auto auto 1fr; column-gap: var(--gap); row-gap: 6.2mm;
        align-items: start; }
/* painel: sangra topo, base e esquerda; termina 5mm depois do texto lateral */
.page::before { content: ""; position: absolute; top: 0; bottom: 0; left: 0;
                width: calc(var(--mx) + var(--side) + 5mm); background: var(--panel);
                border-top: 5mm solid var(--red); }
/* cada bloco lateral pendura na mesma linha horizontal da seção principal */
.page > * { position: relative; }
.m { grid-column: 2; } .s { grid-column: 1; }
.r1 { grid-row: 1; } .r2 { grid-row: 2; } .r3 { grid-row: 3; }
.s.r1 { padding-top: 1mm; }
.rule { border-top: 0.75pt solid #111; padding-top: 1.6mm; }

.name { font-weight: 700; font-size: 44pt; line-height: 0.9; letter-spacing: -0.045em;
        word-spacing: 0.14em;
        margin-left: -0.6mm; }
.roles { margin-top: 3.6mm; font-size: 9.4pt; font-weight: 500; letter-spacing: -0.005em; }
.roles span { color: var(--red); margin: 0 1.6mm; font-weight: 400; }

section.first { margin-top: 8.4mm; }
.sec-head { display: flex; gap: 3mm; align-items: baseline; margin-bottom: 2.8mm; font-size: 7pt; font-weight: 600;
            letter-spacing: 0.1em; text-transform: uppercase; }
.sec-head, .block h2 { line-height: 1.36; }
.sec-head .n { color: var(--red); letter-spacing: 0; font-variant-numeric: tabular-nums; }
.lead { font-size: 8.8pt; line-height: 1.42; letter-spacing: -0.005em; }
.lead + .lead { margin-top: 1.6mm; }
.job + .job { margin-top: 2.8mm; }
.job-head { display: flex; justify-content: space-between; align-items: baseline; gap: 4mm; }
.job-title { font-weight: 600; font-size: 9pt; }
.date { color: var(--muted); white-space: nowrap; font-size: 7.8pt; }
.org { color: var(--muted); margin: 0.2mm 0 1mm; }
li + li { margin-top: 0.5mm; }

.block + .block { margin-top: 7mm; }
.block h2 { font-size: 7pt; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase;
            margin-bottom: 2.6mm; }
.block dl dt { color: var(--muted); font-size: 7pt; }
.block dl dd + dt { margin-top: 1.6mm; }
.langs div { display: flex; justify-content: space-between; }
.langs div + div { margin-top: 0.6mm; }
.s li { padding-left: 0; } .s li::before { content: none; }
.s li + li { margin-top: 0.6mm; }
.edu + .edu { margin-top: 2.4mm; }
"""

    def job(t, org, loc, date, items):
        return f"""<div class="job">
  <div class="job-head"><span class="job-title">{e(t)}</span><span class="date">{e(date)}</span></div>
  <div class="org">{e(org)}, {e(loc)}</div>
  {bullets(items)}
</div>"""

    def sec_rule(n, title, body, cls):
        return (f'<section class="rule {cls}"><h2 class="sec-head"><span class="n">{n:02d}</span>'
                f'{e(title)}</h2>{body}</section>')

    contact = "".join(f"<dt>{e(k)}</dt><dd>{link(v, h, wbr=True)}</dd>" for k, v, h in C.CONTACT)
    langs = "".join(f"<div><span>{e(l)}</span><span class='muted'>{e(v)}</span></div>"
                    for l, v in C.LANGUAGES)
    skills = "".join(f"<li>{e(s[:1].upper() + s[1:])}</li>" for s in C.SKILLS)
    edu = "".join(
        f'<div class="edu"><strong>{e(s)}</strong><div class="muted tnum">{e(d)}<br>{e(loc)}</div>'
        f'<div>{e(x)}</div></div>' for s, loc, d, x in C.EDUCATION)
    profile = "".join(f'<p class="lead">{e(p)}</p>' for p in C.PROFILE)
    roles = '<span>/</span>'.join(e(r) for r in C.ROLES)

    body = f"""
<div class="m r1">
  <header>
    <h1 class="name">{e(C.NAME_FIRST)} {e(C.NAME_LAST)}</h1>
    <div class="roles">{roles}</div>
  </header>
  <section class="rule first"><h2 class="sec-head"><span class="n">01</span>Profile</h2>{profile}</section>
</div>
<div class="s r1 block"><h2>Contact</h2><address><dl>{contact}</dl></address></div>
{sec_rule(2, "Australian Experience", "".join(job(*j) for j in C.AUSTRALIA), "m r2")}
<div class="s r2 rule"><div class="block langs"><h2>Languages</h2>{langs}</div>
  <div class="block"><h2>Skills</h2><ul>{skills}</ul></div></div>
{sec_rule(3, "Design Experience", "".join(job(*j) for j in C.DESIGN), "m r3")}
<div class="s r3 rule block"><h2>Education</h2>{edu}</div>
"""
    return page(css, body)


def page(css, body):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Victor Braga – CV</title>
<meta name="author" content="Victor Braga">
<style>{css}</style></head>
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
    which = sys.argv[1:] or ["typographic", "modernist"]
    if "typographic" in which:
        render("Victor_Braga_CV_Typographic", typographic())
    if "modernist" in which:
        render("Victor_Braga_CV_Modernist", modernist())
