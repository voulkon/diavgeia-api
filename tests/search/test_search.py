import pytest
from diavgeia_api.models.search import SearchResponse, SearchInfo
from diavgeia_api.models.decisions import Decision
import datetime


# @pytest.mark.integration
# @pytest.mark.skipif(
#     "not config.getoption('--live')",
#     reason="Run with --live to hit the real API",
# )
# def test_simple_query(
#     simple_searches_fetched_result, simple_searches_expected_response
# ): ...


def test_search_response_structure(simple_searches_fetched_result):
    """Test that the search response has the expected structure."""
    assert isinstance(simple_searches_fetched_result, SearchResponse)
    assert hasattr(simple_searches_fetched_result, "decisions")
    assert hasattr(simple_searches_fetched_result, "info")
    assert isinstance(simple_searches_fetched_result.decisions, list)
    assert isinstance(simple_searches_fetched_result.info, SearchInfo)


def test_search_info_fields(simple_searches_fetched_result):
    """Test that the search info has the expected fields."""
    info = simple_searches_fetched_result.info
    assert hasattr(info, "query")
    assert hasattr(info, "page")
    assert hasattr(info, "size")
    assert hasattr(info, "actualSize")
    assert hasattr(info, "total")
    assert hasattr(info, "order")

    assert isinstance(info.query, str)
    assert isinstance(info.page, int)
    assert isinstance(info.size, int)
    assert isinstance(info.actualSize, int)
    assert isinstance(info.total, int)
    assert isinstance(info.order, str)


def test_decisions_list_content(simple_searches_fetched_result):
    """Test that the decisions list contains actual Decision objects."""
    decisions = simple_searches_fetched_result.decisions
    assert len(decisions) > 0
    for decision in decisions:
        assert isinstance(decision, Decision)
        assert hasattr(decision, "ada")
        assert hasattr(decision, "subject")
        assert hasattr(decision, "issueDate")
        assert isinstance(decision.ada, str)
        assert isinstance(decision.subject, str)
        assert isinstance(decision.issueDate, datetime.datetime)


def test_decisions_count_matches_info(simple_searches_fetched_result):
    """Test that the number of decisions in the list matches the actualSize in info."""
    assert (
        len(simple_searches_fetched_result.decisions)
        == simple_searches_fetched_result.info.actualSize
    )


def test_search_response_matches_expected(
    simple_searches_fetched_result, simple_searches_expected_response
):
    """Test that the fetched response matches the expected response."""
    assert (
        simple_searches_fetched_result.info.total
        == simple_searches_expected_response["info"]["total"]
    )
    # assert (
    #     simple_searches_fetched_result.info.query
    #     == simple_searches_expected_response["info"]["query"]
    # )
    assert len(simple_searches_fetched_result.decisions) == len(
        simple_searches_expected_response["decisions"]
    )
