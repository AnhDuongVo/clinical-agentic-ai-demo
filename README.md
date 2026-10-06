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

An interactive demo of four open examples of agentic AI for healthcare, built on the open NVIDIA stack.
One idea runs through all of them: in healthcare a fluent wrong answer is the real risk, so the model
cites its evidence, code checks every number, and a human signs off.

The demo runs each project's deterministic **verification logic live** (catching a wrong dose, refusing
to guess, flagging a mismatched number, ranking candidates). The generated clinical text is a bundled
sample; the real pipelines run Nemotron, NeMo Agent Toolkit, NeMo Guardrails and BioNeMo.

## The four tabs

- **consult-to-note**: a transcript becomes a cited note; toggle an injected dose error and watch it get caught.
- **trial-matcher**: per-criterion eligibility with thresholds in code; a missing value returns "unknown", not a guess.
- **csr-assistant**: a drafted study report checked number by number against the cited table row.
- **ai-scientist**: a deterministic simulated BioNeMo pipeline that ranks candidate binders.

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
