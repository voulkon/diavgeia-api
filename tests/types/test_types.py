import pytest
from tests.utils import assert_deep_equal


@pytest.mark.integration
@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
def test_get_all_types(all_types_expected_result):
    label_to_look_for = "ΠΡΑΞΕΙΣ ΟΙΚΟΝΟΜΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ"
    label_exists_in_response = any(
        label_to_look_for.lower() in decision_type.label.lower()
        for decision_type in all_types_expected_result.decisionTypes
    )
    assert (
        label_exists_in_response
    ), f"Label '{label_to_look_for}' not found in response."


# @pytest.mark.skipif(
#     "not config.getoption('--live')",
#     reason="Run with --live to hit the real API",
# )
# @pytest.mark.integration
def test_get_details_of_type(
    details_of_a_type_result, details_of_a_type, type_to_target
):
    label_to_look_for = "ΠΡΑΞΕΙΣ ΧΩΡΟΤΑΞΙΚΟΥ - ΠΟΛΕΟΔΟΜΙΚΟΥ ΠΕΡΙΕΧΟΜΕΝΟΥ"
    main_label = details_of_a_type_result.label

    assert (
        main_label == label_to_look_for
    ), f"""
        Main label is not as expected. 
        Actual: {main_label}
        Expected: {label_to_look_for}
        """

    main_types_uid = details_of_a_type_result.uid
    assert (
        main_types_uid == type_to_target
    ), f"""
        Main types uid is not as expected. 
        Actual: {main_types_uid}
        Expected: {type_to_target}
        """

    # TODO: Make this work
    # for key, value in details_of_a_type.items():
    #     assert hasattr(details_of_a_type_result, key), f"Missing attribute: {key}"
    #     actual_value = getattr(details_of_a_type_result, key)
    #     assert_deep_equal(actual_value, value, key)

    # Check if the details_of_a_type dictionary is the same as details_of_a_type_result
    # for key, value in details_of_a_type.items():
    #     assert hasattr(
    #         details_of_a_type_result, key
    #     ), f"Missing attribute: {key} in response"
    #     assert (
    #         getattr(details_of_a_type_result, key) == value
    #     ), f"""
    #         Attribute {key} value does not match.
    #         Actual: {getattr(details_of_a_type_result, key)}
    #         Expected: {value}
    #         """
