import pytest


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


@pytest.mark.skipif(
    "not config.getoption('--live')",
    reason="Run with --live to hit the real API",
)
@pytest.mark.integration
def test_get_details_of_type(
    details_of_a_type_result,
    details_of_a_type,
    type_to_target,
    general_label_of_type_details_to_look_for,
):
    main_label = details_of_a_type_result.label

    assert (
        main_label == general_label_of_type_details_to_look_for
    ), f"""
        Main label is not as expected. 
        Actual: {main_label}
        Expected: {general_label_of_type_details_to_look_for}
        """

    main_types_uid = details_of_a_type_result.uid
    assert (
        main_types_uid == type_to_target
    ), f"""
        Main types uid is not as expected. 
        Actual: {main_types_uid}
        Expected: {type_to_target}
        """
    if type_to_target == "Β.6":
        # Find a field in the fixture that has type: null
        null_type_fields = [
            field
            for field in details_of_a_type["extraFields"]
            if field.get("type") is None
        ]

        # Ensure at least one field with null type exists in the fixture
        assert (
            null_type_fields
        ), "Test fixture for B.6 should have at least one field with type: null"

        # Check if the model correctly handles the null type
        for null_field in null_type_fields:
            uid = null_field["uid"]
            # Find the corresponding field in the result
            result_field = next(
                (
                    field
                    for field in details_of_a_type_result.extraFields
                    if field.uid == uid
                ),
                None,
            )

            assert result_field is not None, f"Field with uid {uid} not found in result"
            assert (
                result_field.type is None
            ), f"Field {uid} should have type=None, but got {result_field.type}"
