"""Interactive demo of four clinical AI agents.

Run locally:   streamlit run app.py
Deploy:        Hugging Face Spaces (SDK: Streamlit) or Streamlit Community Cloud.

The page runs each project's verification logic (citation checks, number checks, eligibility rules,
candidate ranking). The generated clinical text is a bundled sample. To produce it with the real models,
install the full project and set an NVIDIA_API_KEY.
"""

from __future__ import annotations

import streamlit as st

import samples
from core import check_number, eval_threshold, rank_candidates
from ui import check_card, hero, info, inject_css, rank_table, section, source_card

st.set_page_config(page_title="Clinical AI agents, demo", page_icon="🩺", layout="centered")
inject_css()

hero(
    "Demo",
    "Four clinical AI agents",
    "One agent per tab. The citation and number checks run in this page; the generated text is a bundled sample. "
    "No API key is needed.",
)
info("Built with the NVIDIA NeMo stack (NeMo Agent Toolkit, NIM, Nemotron, Guardrails, BioNeMo). "
     "Change the inputs to see how the checks respond.")

tabs = st.tabs(["consult-to-note", "trial-matcher", "csr-assistant", "ai-scientist"])

# ---------------------------------------------------------------- consult-to-note
with tabs[0]:
    hero("consult-to-note", "Ambient clinical documentation",
         "Turns a consultation transcript into a structured note. Each sentence cites a transcript line, "
         "and the numbers in it are checked against that line.")
    case_name = st.selectbox("Consultation", list(samples.CONSULT_CASES), key="c2n_case")
    case = samples.CONSULT_CASES[case_name]
    section("Transcript")
    source_card(case["transcript"])
    plant = st.checkbox(case["error_label"], value=False, key=f"c2n_err_{case_name}")
    err_sid, err_val, err_from, err_to = case["error"]
    section("Generated note")
    for sentence, sid, claimed in case["note"]:
        if claimed is None:
            check_card(sentence, "neutral", "no number to check", cite=sid)
            continue
        shown = claimed
        if plant and sid == err_sid:
            shown = err_val
            sentence = sentence.replace(err_from, err_to)
        chk = check_number(sentence, shown, sid, case["sources"])
        if chk.ok:
            check_card(sentence, "ok", f"{chk.claimed:g} matches the transcript", cite=sid)
        else:
            check_card(sentence, "flag", f"the note says {chk.claimed:g}, the transcript says {chk.source_value:g}", cite=sid)
    st.markdown('<div class="note">Flagged sentences go back to the clinician for review before the note is signed.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- trial-matcher
with tabs[1]:
    hero("trial-matcher", "Clinical-trial screening",
         "Checks a patient record against a trial's eligibility criteria. Thresholds are evaluated in code; "
         "a missing value is reported as unknown rather than decided.")
    patient_name = st.selectbox("Patient", list(samples.TRIAL_PATIENTS), key="tm_patient")
    preset = samples.TRIAL_PATIENTS[patient_name]
    k = patient_name[:9]
    section("Record (editable)")
    c1, c2, c3 = st.columns(3)
    age = c1.number_input("Age", value=preset["age"], step=1.0, key=f"age_{k}")
    hba1c = c2.number_input("HbA1c (%)", value=preset["hba1c"], step=0.1, key=f"hba1c_{k}")
    has_egfr = c3.checkbox("eGFR on record", value=preset["egfr"] is not None, key=f"has_egfr_{k}")
    egfr = c3.number_input("eGFR", value=preset["egfr"] if preset["egfr"] is not None else 60.0, step=1.0, key=f"egfr_{k}") if has_egfr else None
    values = {"age": age, "hba1c": hba1c, "egfr": egfr}
    section("Criteria")
    for crit, key, op, bound in samples.TRIAL_CRITERIA:
        v = eval_threshold(crit, values[key], op, bound, key)
        status = {"met": "ok", "not met": "flag", "unknown": "unknown"}[v.status]
        check_card(crit, status, f"{v.basis}, confidence {v.confidence:.2f}", label=v.status)
    st.markdown('<div class="note">A study coordinator reviews the result before the patient is contacted. Criteria that need reading rather than a threshold are handled by the model in the full project.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- csr-assistant
with tabs[2]:
    hero("csr-assistant", "Clinical study report review",
         "Checks the sentences of a drafted report against the source table rows they cite.")
    sec_name = st.selectbox("Section", list(samples.CSR_SECTIONS), key="csr_section")
    sec = samples.CSR_SECTIONS[sec_name]
    section("Source table")
    source_card([(rid, f"value = {val:g}") for rid, val in sec["table"].items()])
    edit_idx, edit_label = sec["editable"]
    default_val = sec["draft"][edit_idx][2]
    edited = st.number_input(edit_label, value=float(default_val), step=0.01, format="%.2f", key=f"csr_edit_{sec_name}")
    section("Drafted sentences")
    for i, (sentence, rid, claimed) in enumerate(sec["draft"]):
        val = edited if i == edit_idx else claimed
        shown = sentence
        if i == edit_idx and abs(val - claimed) > 1e-9:
            shown = sentence.replace(f"{claimed:g}", f"{val:g}")
        chk = check_number(shown, val, rid, sec["table"])
        if chk.ok:
            check_card(shown, "ok", f"{chk.claimed:g} matches row {rid}", cite=rid)
        else:
            check_card(shown, "flag", f"the draft says {chk.claimed:g}, row {rid} says {chk.source_value:g}", cite=rid)
    st.markdown('<div class="note">Whole counts have to match exactly; percentages may be rounded. Flagged sentences are listed in the review report for the medical writer.</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------- ai-scientist
with tabs[3]:
    hero("ai-scientist", "Protein binder design",
         "Chains RFdiffusion, ProteinMPNN and Boltz-2 and ranks the candidates. This demo uses a built-in "
         "simulator instead of the real models, so the scores are placeholders.")
    section("Run settings")
    c1, c2, c3 = st.columns([2, 1, 1])
    target = c1.selectbox("Target protein", samples.AI_TARGETS, key="sci_target")
    n = c2.slider("Candidates", 3, 10, 5, key="sci_n")
    seed = c3.slider("Seed", 0, 5, 0, key="sci_seed")
    section("Ranked candidates")
    rank_table(rank_candidates(target, n=n, seed=seed))
    st.markdown('<div class="note">In the full project each binder is folded together with the target and the complex is scored; one flag switches the simulator to the real BioNeMo NIMs.</div>', unsafe_allow_html=True)

st.divider()
st.markdown(
    "Source: [consult-to-note](https://github.com/AnhDuongVo/consult-to-note) · "
    "[trial-matcher](https://github.com/AnhDuongVo/trial-matcher) · "
    "[csr-assistant](https://github.com/AnhDuongVo/csr-assistant) · "
    "[ai-scientist](https://github.com/AnhDuongVo/ai-scientist)"
)
