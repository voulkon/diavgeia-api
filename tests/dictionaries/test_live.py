import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_dictionary_live(specific_dictionarys_result):
    # dictionary_result now performed a real call
    assert specific_dictionarys_result.name == "FEKTYPES"
    assert len(specific_dictionarys_result.items) > 5
