import os

from application.use_cases.find_ownership import (
    find_shares_entities_own_of_focus_company,
    find_shares_focus_company_owns_of_entities,
    get_focus_company_id_and_name,
)
from config.config import Constants
from infrastructure.repositories.json_repository import OwnershipRepository
from presentation.cli.utils.print import print_results


def run_cli():
    json_files = [
        os.path.join(Constants.DATA_DIRECTORY.value, filename)
        for filename in sorted(os.listdir(Constants.DATA_DIRECTORY.value))
        if filename.endswith(".json")
    ]

    for index, filepath in enumerate(json_files):
        print(f"Processing {filepath}...")

        ownership_repository = OwnershipRepository()
        owners_of_company, companies_company_owns = (
            ownership_repository.get_ownership_structure(filepath)
        )

        focus_company_id, focus_company_name = get_focus_company_id_and_name(
            owners_of_company, companies_company_owns
        )
        print(f"Focus company found: {focus_company_name} (ID: {focus_company_id})")
        print()

        # Find shares each entity owns of focus company
        print(f"Ownership of {focus_company_name} by other entities:")
        shares_entities_own_of_focus_company = (
            find_shares_entities_own_of_focus_company(
                focus_company_id, focus_company_name, owners_of_company
            )
        )
        print_results(shares_entities_own_of_focus_company)

        print()

        # Find shares focus company owns of each entity
        print(f"Ownership of other entities by {focus_company_name}:")
        shares_focus_company_owns_of_entities = (
            find_shares_focus_company_owns_of_entities(
                focus_company_id, focus_company_name, companies_company_owns
            )
        )
        print_results(shares_focus_company_owns_of_entities)

        if index != len(json_files) - 1:
            print()
            print()
