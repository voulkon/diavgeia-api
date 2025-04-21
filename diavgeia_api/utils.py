import json
from pathlib import Path
from datetime import datetime


def custom_serializer(obj):
    """Custom serializer for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 string
    raise TypeError(f"Type {type(obj)} not serializable")


def write_to_json(data, file_path):
    """
    Writes the given data to a JSON file at the specified file path.

    Args:
    - data: The data to be written (can be a dictionary or list).
    - file_path: The file path where the JSON data will be written.
    """
    # Convert the file path to a Path object
    path = Path(file_path)

    # Create the directory if it doesn't exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # Open the file and write the data as JSON
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(
            data, json_file, ensure_ascii=False, indent=4, default=custom_serializer
        )

    print(f"Data has been written to {file_path}")
