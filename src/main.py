import os
from enum import Enum

from graph import (
    find_shares_entities_own_of_focus_company,
    find_shares_focus_company_owns_of_entities,
)
from ownership import (
    get_focus_company_id_and_name,
    get_ownership_structure_from_file,
)


# Using enum to get immutable constants
class Constants(Enum):
    DATA_DIRECTORY = "data"


def _print_results(ownerships: list[tuple[str, float, float]]):
    """Prints the results of the ownership analysis."""

    def format_share(share):
        return f"{int(share * 100)}" if (share * 100) % 1 == 0 else f"{share * 100:.1f}"

    for node_name, share_lower, share_upper in ownerships:
        share_average = (share_lower + share_upper) / 2

        print(
            f"* {node_name}: {format_share(share_lower)}%, {format_share(share_average)}%, {format_share(share_upper)}%"
        )


json_files = [
    os.path.join(Constants.DATA_DIRECTORY.value, filename)
    for filename in sorted(os.listdir(Constants.DATA_DIRECTORY.value))
    if filename.endswith(".json")
]

for index, filepath in enumerate(json_files):
    print(f"Processing {filepath}...")
    owners_of_company, companies_company_owns = get_ownership_structure_from_file(
        filepath
    )

    focus_company_id, focus_company_name = get_focus_company_id_and_name(
        owners_of_company, companies_company_owns
    )
    print(f"Focus company found: {focus_company_name} (ID: {focus_company_id})")
    print()

    # Find shares each entity owns of focus company
    print(f"Ownership of {focus_company_name} by other entities:")
    shares_entities_own_of_focus_company = find_shares_entities_own_of_focus_company(
        focus_company_id, focus_company_name, owners_of_company
    )
    _print_results(shares_entities_own_of_focus_company)

    print()

    # Find shares focus company owns of each entity
    print(f"Ownership of other entities by {focus_company_name}:")
    shares_focus_company_owns_of_entities = find_shares_focus_company_owns_of_entities(
        focus_company_id, focus_company_name, companies_company_owns
    )
    _print_results(shares_focus_company_owns_of_entities)

    if index != len(json_files) - 1:
        print()
        print()
