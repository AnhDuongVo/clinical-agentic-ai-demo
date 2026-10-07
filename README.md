---
title: Clinical Agentic AI Demo
emoji: 🩺
colorFrom: blue
colorTo: indigo
sdk: streamlit
app_file: app.py
pinned: false
license: apache-2.0
---

# Clinical Agentic AI, interactive demo

An interactive demo of four clinical AI agents built with the NVIDIA NeMo stack. In all four, the model
drafts, code checks numbers and citations, and a person reviews the result.

The demo runs each project's verification logic (number checks against a cited source, eligibility
thresholds, candidate ranking) on every input change. The generated clinical text is a bundled sample;
the full projects produce it with Nemotron, NeMo Agent Toolkit, NeMo Guardrails and BioNeMo.

## The four tabs

| consult-to-note | trial-matcher |
|---|---|
| ![consult-to-note](docs/consult-to-note.gif) | ![trial-matcher](docs/trial-matcher.gif) |
| **csr-assistant** | **ai-scientist** |
| ![csr-assistant](docs/csr-assistant.gif) | ![ai-scientist](docs/ai-scientist.gif) |

Full-quality videos are on [anhduongvo.github.io](https://anhduongvo.github.io/projects/clinical-agentic-ai/).

- **consult-to-note**: two consultations; the note's numbers are checked against the transcript, and an error can be planted to see it flagged.
- **trial-matcher**: two patients; thresholds are evaluated in code, a missing lab value is reported as unknown, and the record can be edited.
- **csr-assistant**: two report sections; each drafted sentence is checked against the table row it cites, and the flagged number can be corrected.
- **ai-scientist**: a simulated BioNeMo pipeline; change the target, seed and number of candidates to see the ranking update.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

- **Hugging Face Spaces**: create a new Space with SDK "Streamlit", push these files. The front matter above configures it. No secrets needed (offline demo).
- **Streamlit Community Cloud**: point it at this repo and `app.py`.

## Full projects

[consult-to-note](https://github.com/AnhDuongVo/consult-to-note) ·
[trial-matcher](https://github.com/AnhDuongVo/trial-matcher) ·
[csr-assistant](https://github.com/AnhDuongVo/csr-assistant) ·
[ai-scientist](https://github.com/AnhDuongVo/ai-scientist)

## License

Apache-2.0.
