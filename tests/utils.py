import json
from pathlib import Path


def load_json_fixture(base_dir: Path, filename: str):
    return json.loads((base_dir / "fixtures" / filename).read_text("utf‑8"))
