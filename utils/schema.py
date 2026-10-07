import json
from pathlib import Path

from jsonschema import validate

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def assert_schema(payload, schema_name: str):
    schema = json.loads((SCHEMA_DIR / f"{schema_name}.json").read_text())
    validate(instance=payload, schema=schema)
