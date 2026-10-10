import samples


def test_editable_csr_sentences_contain_the_numeric_value():
    for section in samples.CSR_SECTIONS.values():
        index, _ = section["editable"]
        sentence, _, claimed = section["draft"][index]
        assert f"{claimed:g}" in sentence
