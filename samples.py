"""Sample inputs and sample generated text for the demo. Everything here is synthetic."""

# ---------------------------------------------------------------- consult-to-note
# Each case: transcript lines, the numeric facts the transcript supports, the generated note
# (sentence, cited line, number or None), and one plantable error (line, wrong value, text before, text after).
CONSULT_CASES = {
    "Chest pain visit, two new prescriptions": {
        "transcript": [
            ("t3", "Doctor: how long has the chest pain been going on?  Patient: about two days."),
            ("t5", "Patient: no allergies that I know of."),
            ("t8", "Nurse: blood pressure is 148 over 92."),
            ("t11", "Doctor: I'll start you on metoprolol 25 milligrams once a day."),
            ("t14", "Doctor: and atorvastatin 20 at night."),
        ],
        "sources": {"t8": 148.0, "t11": 25.0, "t14": 20.0},
        "note": [
            ("Chest pain for two days.", "t3", None),
            ("Blood pressure 148/92.", "t8", 148.0),
            ("Start metoprolol 25 mg once daily.", "t11", 25.0),
            ("Start atorvastatin 20 mg nightly.", "t14", 20.0),
        ],
        "error": ("t11", 250.0, "25 mg", "250 mg"),
        "error_label": "Plant an error: write 250 mg instead of the 25 mg in the transcript",
    },
    "Diabetes follow-up, insulin adjustment": {
        "transcript": [
            ("t2", "Doctor: the HbA1c from last week came back at 7.2 percent."),
            ("t4", "Patient: I've been having some low readings in the morning."),
            ("t6", "Doctor: let's reduce the evening insulin by 2.5 units and see."),
            ("t9", "Doctor: keep the metformin as it is, 1000 milligrams twice a day."),
            ("t12", "Doctor: I'd like to see you again in three months."),
        ],
        "sources": {"t2": 7.2, "t6": 2.5, "t9": 1000.0},
        "note": [
            ("HbA1c 7.2%.", "t2", 7.2),
            ("Morning hypoglycaemia reported.", "t4", None),
            ("Reduce evening insulin by 2.5 units.", "t6", 2.5),
            ("Continue metformin 1000 mg twice daily.", "t9", 1000.0),
            ("Follow-up in three months.", "t12", None),
        ],
        "error": ("t6", 25.0, "2.5 units", "25 units"),
        "error_label": "Plant an error: write 25 units instead of the 2.5 units in the transcript",
    },
}

# ---------------------------------------------------------------- trial-matcher
TRIAL_CRITERIA = [
    ("Age 18 or older", "age", ">=", 18.0),
    ("HbA1c of at least 7.0%", "hba1c", ">=", 7.0),
    ("eGFR of at least 45", "egfr", ">=", 45.0),
]
TRIAL_PATIENTS = {
    "Patient A: 54 years, HbA1c 7.2, no eGFR on record": {"age": 54.0, "hba1c": 7.2, "egfr": None},
    "Patient B: 61 years, HbA1c 6.5, eGFR 38": {"age": 61.0, "hba1c": 6.5, "egfr": 38.0},
}

# ---------------------------------------------------------------- csr-assistant
# Each section: the source table rows, the drafted sentences (sentence, cited row, number),
# and which sentence the demo lets you edit (index, label).
CSR_SECTIONS = {
    "Efficacy: change in HbA1c": {
        "discrete_rows": {"r2"},
        "table": {"r1": -1.21, "r2": 240.0, "r3": -0.35},
        "draft": [
            ("Mean change in HbA1c was -1.21 in the treatment arm.", "r1", -1.21),
            ("A total of 240 patients were randomised.", "r2", 240.0),
            ("Mean change in the placebo arm was -1.4.", "r3", -1.4),
        ],
        "editable": (2, "Placebo-arm change as written in the draft"),
    },
    "Safety: adverse events": {
        "discrete_rows": {"s1", "s2", "s4"},
        "table": {"s1": 12.0, "s2": 240.0, "s3": 5.0, "s4": 2.0},
        "draft": [
            ("Nausea was reported by 12 of 240 patients.", "s1", 12.0),
            ("That corresponds to 5.0 percent of the safety population.", "s3", 5.0),
            ("3 patients discontinued because of adverse events.", "s4", 3.0),
        ],
        "editable": (2, "Discontinuations as written in the draft"),
    },
}

# ---------------------------------------------------------------- ai-scientist
AI_TARGETS = ["PD-L1", "EGFR", "IL-6"]
