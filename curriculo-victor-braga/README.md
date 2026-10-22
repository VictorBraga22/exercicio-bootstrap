# Currículo – Victor Braga (Austrália)

Pasta separada do resto do repositório.

## Para enviar
- `Victor_Braga_CV_Modernist.pdf` – versão principal (Estilo Tipográfico Internacional – Müller-Brockmann, Vignelli): composição assimétrica, painel lateral que sangra a página, nome em display, seções numeradas em vermelho; cada bloco lateral alinhado à régua da seção principal.
- `Victor_Braga_CV.pdf` / `.docx` – versão simples para sites/ATS que pedem Word.

Portfolio: https://www.behance.net/victorbragacsa (clicável no PDF).

## Como gerar de novo
- Versão de design: `cd design && python3 build.py` (edite o texto em `design/content.py`).
  O build falha se o PDF passar de 1 página ou se a margem inferior real ficar abaixo de 10 mm.
- Versão DOCX: `python3 gerar_cv.py` e depois `soffice --headless --convert-to pdf Victor_Braga_CV.docx`.

Fonte: Inter (SIL Open Font License), em `design/fonts/`.
