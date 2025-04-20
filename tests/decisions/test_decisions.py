import pytest


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_a_decision_live(one_decisions_fetched_result, decisions_uid):
    # dictionary_result now performed a real call
    assert one_decisions_fetched_result.ada == decisions_uid


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_a_decisions_version_live(
    one_decisions_version_fetched_result, decisions_version_id
):
    ...
    # dictionary_result now performed a real call
    assert one_decisions_version_fetched_result.versionId == decisions_version_id


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_a_decisions_version_log_live(
    one_decisions_version_log_fetched_result, decisions_uid
):
    ...
    # dictionary_result now performed a real call
    assert one_decisions_version_log_fetched_result.ada == decisions_uid
