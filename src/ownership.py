import json
import re
from dataclasses import dataclass
from typing import List


# Could consider using ordinary class, as dataclass has overhead due to automatic __init__() generation
@dataclass(frozen=True)
class Ownership:
    id: str
    source: int
    source_name: str
    source_depth: int
    target: int
    target_name: str
    target_depth: int
    share_lower: float
    share_upper: float
    active: bool


def _convert_share(share_str: str) -> tuple[int, int]:
    """Extracts numerical values from a share string and returns a tuple (lower, upper)."""

    numbers = list(map(int, re.findall(r"\d+", share_str)))

    if ">" in share_str:  # Handle cases like ">10%"
        return (numbers[0] / 100, None)
    elif "<" in share_str:  # Handle cases like "<5%"
        return (0, numbers[0] / 100)
    elif len(numbers) == 1:  # Handle cases like "10%"
        return (numbers[0] / 100, numbers[0] / 100)
    elif len(numbers) == 2:  # Handle cases like "5-10%"
        return (numbers[0] / 100, numbers[1] / 100)

    return None  # If the format is unrecognized


def _convert_to_ownership_objects(data: List[dict]) -> List[Ownership]:
    """Converts list of dictionaries to list of Ownership dataclass instances."""

    ownership_list = []

    for item in data:
        share_lower, share_upper = _convert_share(item["share"])

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


def _read_file(filepath: str) -> List[dict]:
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


def get_ownership_structure_from_file(filepath: str):
    """Reads JSON file, convert it to Ownership objects, and return the list."""

    ownership_file_data = _read_file(filepath)
    ownership_objects = _convert_to_ownership_objects(ownership_file_data)

    owners_of_company = [item for item in ownership_objects if item.source_depth > 0]
    companies_company_owns = [
        item for item in ownership_objects if item.source_depth <= 0
    ]

    return (owners_of_company, companies_company_owns)


def get_focus_company_id_and_name(
    owners_of_company: list[Ownership], companies_company_owns: list[Ownership]
):
    """Gets ID and name of the focus company."""

    focus_company_id, focus_company_name = next(
        (
            (entry.target, entry.target_name)
            if entry.target_depth == 0
            else (entry.source, entry.source_name)
            for entry in owners_of_company + companies_company_owns
            if entry.target_depth == 0 or entry.source_depth == 0
        ),
        None,
    )

    return focus_company_id, focus_company_name
