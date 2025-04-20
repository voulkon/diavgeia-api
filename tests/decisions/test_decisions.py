import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_a_decision_live(one_decisions_fetched_result, decisions_uid):
    # dictionary_result now performed a real call
    assert one_decisions_fetched_result.ada == decisions_uid
