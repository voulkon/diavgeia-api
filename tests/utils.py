import json
from pathlib import Path


def load_json_fixture(base_dir: Path, filename: str):
    return json.loads((base_dir / "fixtures" / filename).read_text("utf‑8"))


def assert_deep_equal(actual, expected, path=""):
    """
    Recursively compare actual (possibly Pydantic) values with expected dict/list values
    Only compares fields that exist in the expected structure
    """
    if isinstance(expected, dict):
        # For dictionaries, check that all expected keys exist in actual
        if hasattr(actual, "model_dump"):
            # Convert Pydantic model to dict
            actual_dict = actual.model_dump()
        elif isinstance(actual, dict):
            actual_dict = actual
        else:
            assert False, f"{path}: Expected dict but got {type(actual)}"

        for key, exp_value in expected.items():
            assert key in actual_dict, f"{path}.{key}: Missing in actual"
            assert_deep_equal(actual_dict[key], exp_value, f"{path}.{key}")

    elif isinstance(expected, list):
        # For lists, check each item
        assert isinstance(actual, list), f"{path}: Expected list but got {type(actual)}"
        assert len(actual) >= len(
            expected
        ), f"{path}: List too short ({len(actual)} < {len(expected)})"

        for i, exp_item in enumerate(expected):
            assert_deep_equal(actual[i], exp_item, f"{path}[{i}]")

    else:
        # For simple values, direct comparison
        assert (
            actual == expected
        ), f"""{path}: Values don't match
            Actual: {actual}
            Expected: {expected}
            """
