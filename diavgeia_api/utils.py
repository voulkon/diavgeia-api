import json
from pathlib import Path


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
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"Data has been written to {file_path}")
