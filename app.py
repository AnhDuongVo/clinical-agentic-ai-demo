"""Clinical Agentic AI, an interactive demo of four healthcare agents.

Run locally:   streamlit run app.py
Deploy:        Hugging Face Spaces (SDK: Streamlit) or Streamlit Community Cloud.

The demo runs each project's deterministic VERIFICATION logic live (the part that catches wrong numbers,
refuses to guess, and ranks candidates). The generated clinical text shown is a bundled sample; set an
NVIDIA_API_KEY and install the full project to produce it with the real models.
"""

from __future__ import annotations

import streamlit as st

import samples
from core import check_number, eval_threshold, rank_candidates

st.set_page_config(page_title="Clinical Agentic AI, demo", page_icon="🩺", layout="centered")

st.title("Clinical Agentic AI")
st.caption(
    "Four open examples of agentic AI for healthcare, on the open NVIDIA stack. "
    "One idea runs through all of them: a fluent wrong answer is the real risk, so the model cites its "
    "evidence, code checks every number, and a human signs off."
)
st.info(
    "Offline demo. The verification logic below runs live in your browser session. The generated text is a "
    "bundled sample; the real pipelines run Nemotron, NeMo Agent Toolkit, Guardrails and BioNeMo on the "
    "NVIDIA stack.",
    icon="ℹ️",
)

tabs = st.tabs(["consult-to-note", "trial-matcher", "csr-assistant", "ai-scientist"])

# ---------------------------------------------------------------- consult-to-note
with tabs[0]:
    st.subheader("Ambient clinical documentation")
    st.write("A consultation transcript becomes a structured note. Every sentence cites a transcript line, "
             "and every number is verified against it in code.")
    with st.expander("Transcript (source)"):
        for sid, line in samples.CONSULT_TRANSCRIPT:
            st.markdown(f"`{sid}`  {line}")

    inject = st.checkbox("Inject a dose error (claim 250 mg instead of 25 mg)", value=False, key="c2n_inject")
    st.markdown("**Generated note** (sample), with live checks:")
    for sentence, sid, claimed in samples.CONSULT_NOTE:
        if claimed is None:
            st.markdown(f"- {sentence}  \n  <span style='color:gray'>cite {sid}</span>", unsafe_allow_html=True)
            continue
        shown = claimed
        if inject and sid == "t11":
            shown = 250.0
            sentence = sentence.replace("25 mg", "250 mg")
        chk = check_number(sentence, shown, sid, samples.CONSULT_SOURCES)
        if chk.ok:
            st.markdown(f"- ✅ {sentence}  \n  <span style='color:gray'>cite {sid}, matches {chk.source_value:g}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"- 🚩 {sentence}  \n  <span style='color:#b4561e'>flagged: claims {chk.claimed:g}, source says {chk.source_value:g} (cite {sid})</span>", unsafe_allow_html=True)
    st.caption("The checker reads the cited transcript line and compares the number. A wrong dose is caught before a human ever sees the note.")

# ---------------------------------------------------------------- trial-matcher
with tabs[1]:
    st.subheader("Clinical-trial screening")
    st.write("A patient record is checked against a trial's criteria. Thresholds are decided in code. "
             "A missing or stale value returns **unknown**, never a guess.")
    col1, col2, col3 = st.columns(3)
    age = col1.number_input("Age", value=54.0, step=1.0)
    hba1c = col2.number_input("HbA1c (%)", value=7.2, step=0.1)
    has_egfr = col3.checkbox("eGFR on record", value=False)
    egfr = col3.number_input("eGFR", value=60.0, step=1.0) if has_egfr else None

    values = {"age": age, "hba1c": hba1c, "egfr": egfr}
    st.markdown("**Per-criterion verdicts:**")
    for crit, key, op, bound in samples.TRIAL_CRITERIA:
        v = eval_threshold(crit, values[key], op, bound, key)
        icon = {"met": "✅", "not met": "⛔", "unknown": "❓"}[v.status]
        st.markdown(f"- {icon} **{crit}**: {v.status}  \n  <span style='color:gray'>{v.basis}, confidence {v.confidence:.2f}</span>", unsafe_allow_html=True)
    st.caption("Uncheck 'eGFR on record' to see the criterion return 'unknown' rather than a false decision.")

# ---------------------------------------------------------------- csr-assistant
with tabs[2]:
    st.subheader("Regulatory writing (ICH E3)")
    st.write("A drafted study report is checked sentence by sentence: every number is verified in code "
             "against the cited source table row.")
    with st.expander("Source table (cited rows)"):
        for rid, val in samples.CSR_TABLE.items():
            st.markdown(f"`{rid}`  value = {val:g}")
    st.markdown("**Drafted report** (sample), with live checks:")
    for sentence, rid, claimed in samples.CSR_DRAFT:
        chk = check_number(sentence, claimed, rid, samples.CSR_TABLE)
        if chk.ok:
            st.markdown(f"- ✅ {sentence}  \n  <span style='color:gray'>cite {rid}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"- 🚩 {sentence}  \n  <span style='color:#b4561e'>flagged: claims {chk.claimed:g}, source row {rid} says {chk.source_value:g}</span>", unsafe_allow_html=True)
    st.caption("A reported -1.4 is caught against the table's -1.21. A wrong number in a clinical study report is a regulatory finding, not a typo.")

# ---------------------------------------------------------------- ai-scientist
with tabs[3]:
    st.subheader("Protein binder design on BioNeMo")
    st.write("For a target protein, the agent chains the BioNeMo models (RFdiffusion, ProteinMPNN, Boltz-2) "
             "and ranks the candidates. This tab runs a **deterministic simulator** live, so no GPU or key is needed.")
    target = st.text_input("Target protein", value=samples.AI_TARGET)
    n = st.slider("Number of candidates", 3, 10, 5)
    ranked = rank_candidates(target, n=n)
    st.table(ranked)
    st.caption("Scores are simulated and meaningless; this shows the orchestration and ranking, not the biology. "
               "The real pipeline folds each binder WITH the target and scores the complex. One flag switches the "
               "simulator to the real BioNeMo NIMs.")

st.divider()
st.markdown(
    "Source: [consult-to-note](https://github.com/AnhDuongVo/consult-to-note) · "
    "[trial-matcher](https://github.com/AnhDuongVo/trial-matcher) · "
    "[csr-assistant](https://github.com/AnhDuongVo/csr-assistant) · "
    "[ai-scientist](https://github.com/AnhDuongVo/ai-scientist)"
)
