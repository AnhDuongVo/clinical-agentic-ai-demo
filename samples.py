"""Bundled sample inputs and sample generated text for the demo (offline, no key)."""

CONSULT_TRANSCRIPT = [
    ("t3", "Doctor: how long has the chest pain been going on?  Patient: about two days."),
    ("t5", "Patient: no allergies that I know of."),
    ("t8", "Nurse: blood pressure is 148 over 92."),
    ("t11", "Doctor: I'll start you on metoprolol 25 milligrams once a day."),
    ("t14", "Doctor: and atorvastatin 20 at night."),
]
# numeric facts the transcript actually supports (source_id -> value)
CONSULT_SOURCES = {"t8": 148.0, "t11": 25.0, "t14": 20.0}
# a generated note: (sentence, source_id, claimed_number_or_None)
CONSULT_NOTE = [
    ("Chest pain for two days.", "t3", None),
    ("Blood pressure 148/92.", "t8", 148.0),
    ("Start metoprolol 25 mg once daily.", "t11", 25.0),
    ("Start atorvastatin 20 mg nightly.", "t14", 20.0),
]

CSR_TABLE = {"r1": -1.21, "r2": 240.0, "r3": -1.21}   # r3 (placebo) is also -1.21 in the source
CSR_DRAFT = [
    ("Mean change in HbA1c was -1.21 in the treatment arm.", "r1", -1.21),
    ("A total of 240 patients were randomised.", "r2", 240.0),
    ("Mean change in the placebo arm was -1.4.", "r3", -1.4),   # planted error
]

TRIAL_CRITERIA = [
    ("Age >= 18", "age", ">=", 18.0),
    ("HbA1c between 7 and 10", "hba1c", ">=", 7.0),
    ("eGFR >= 45", "egfr", ">=", 45.0),
]

AI_TARGET = "PD-L1"
