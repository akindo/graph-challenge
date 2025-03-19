import json
from typing import List

from domain.models.ownership import Ownership, convert_share


def read_file(filepath: str) -> List[dict]:
    """Reads JSON file at given filepath and return contents."""

    print(f"Loading {filepath}...")

    try:
        with open(filepath, "r") as file:
            content = file.read().strip()
            if not content:
                raise ValueError(f"File {filepath} is empty.")
            return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"File {filepath} contains invalid JSON. Error: {e}")


def convert_to_ownership_objects(data: List[dict]) -> List[Ownership]:
    """Converts list of dictionaries to list of Ownership dataclass instances."""

    ownership_list = []

    for item in data:
        share_lower, share_upper = convert_share(item["share"])

        ownership_list.append(
            Ownership(
                id=item["id"],
                source=item["source"],
                source_name=item["source_name"],
                source_depth=item["source_depth"],
                target=item["target"],
                target_name=item["target_name"],
                target_depth=item["target_depth"],
                share_lower=share_lower,
                share_upper=share_upper,
                active=item["active"],
            )
        )

    return ownership_list
