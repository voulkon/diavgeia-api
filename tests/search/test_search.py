import pytest
from diavgeia_api.models.search import SearchResponse, SearchInfo
from diavgeia_api.models.decisions import Decision
import datetime
from pytest_lazy_fixtures import lf as lazy_fixture


@pytest.mark.parametrize(
    "fetched_result",
    [
        lazy_fixture("simple_searches_fetched_result"),
        lazy_fixture("complex_searches_fetched_result"),
    ],
)
def test_search_response_structure(fetched_result):
    """Test that the search response has the expected structure."""
    assert isinstance(fetched_result, SearchResponse)
    assert hasattr(fetched_result, "decisions")
    assert hasattr(fetched_result, "info")
    assert isinstance(fetched_result.decisions, list)
    assert isinstance(fetched_result.info, SearchInfo)


@pytest.mark.parametrize(
    "fetched_result",
    [
        lazy_fixture("simple_searches_fetched_result"),
        lazy_fixture("complex_searches_fetched_result"),
    ],
)
def test_search_info_fields(fetched_result):
    """Test that the search info has the expected fields."""
    info = fetched_result.info
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


@pytest.mark.parametrize(
    "fetched_result",
    [
        lazy_fixture("simple_searches_fetched_result"),
        lazy_fixture("complex_searches_fetched_result"),
    ],
)
def test_decisions_list_content(fetched_result):
    """Test that the decisions list contains actual Decision objects."""
    decisions = fetched_result.decisions
    assert len(decisions) > 0
    for decision in decisions:
        assert isinstance(decision, Decision)
        assert hasattr(decision, "ada")
        assert hasattr(decision, "subject")
        assert hasattr(decision, "issueDate")
        assert isinstance(decision.ada, str)
        assert isinstance(decision.subject, str)
        assert isinstance(decision.issueDate, datetime.datetime)


@pytest.mark.parametrize(
    "fetched_result",
    [
        lazy_fixture("simple_searches_fetched_result"),
        lazy_fixture("complex_searches_fetched_result"),
    ],
)
def test_decisions_count_matches_info(fetched_result):
    """Test that the number of decisions in the list matches the actualSize in info."""
    assert len(fetched_result.decisions) == fetched_result.info.actualSize


@pytest.mark.parametrize(
    "fetched_result,expected_response",
    [
        (
            lazy_fixture("simple_searches_fetched_result"),
            lazy_fixture("simple_searches_expected_response"),
        ),
        (
            lazy_fixture("complex_searches_fetched_result"),
            lazy_fixture("complex_searches_expected_response"),
        ),
    ],
)
def test_search_response_matches_expected(fetched_result, expected_response):
    """Test that the fetched response matches the expected response."""
    assert fetched_result.info.total == expected_response["info"]["total"]

    assert len(fetched_result.decisions) == len(expected_response["decisions"])


# def test_edge_case(edge_case_that_breaks_my_model):
#     ...
#     ...
#     ...
