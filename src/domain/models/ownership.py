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


def convert_share(share_str: str) -> tuple[int, int]:
    """Extracts numerical values from a share string and returns a tuple of lower and upper share)."""

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
