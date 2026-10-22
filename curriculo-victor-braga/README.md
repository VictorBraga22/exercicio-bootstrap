# Currículo – Victor Braga (Austrália)

Pasta separada do resto do repositório.

## Para enviar
- `Victor_Braga_CV_Typographic.pdf` – versão só texto: hierarquia por tamanho, peso e espaço; grid de 12 colunas (rótulos 3 / conteúdo 9).
- `Victor_Braga_CV_Modernist.pdf` – versão modernista (Estilo Tipográfico Internacional – Müller-Brockmann, Vignelli): nome em display, régua com acento vermelho, seções numeradas, coluna de datas.
- `Victor_Braga_CV.pdf` / `.docx` – versão simples para sites/ATS que pedem Word.

Antes de enviar: trocar `[ADD PORTFOLIO LINK]` (em `design/content.py`, e em `gerar_cv.py` para o DOCX).

## Como gerar de novo
- Versões de design: `cd design && python3 build.py` (edite o texto em `design/content.py`).
  O build falha se o PDF passar de 1 página ou se a margem inferior real ficar abaixo de 10 mm.
- Versão DOCX: `python3 gerar_cv.py` e depois `soffice --headless --convert-to pdf Victor_Braga_CV.docx`.

Fonte: Inter (SIL Open Font License), em `design/fonts/`.
