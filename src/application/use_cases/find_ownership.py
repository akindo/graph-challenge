from typing import List

from application.use_cases.process_graph import (
    get_entities_focus_company_owns,
    get_owners_of_focus_company,
    get_total_shares_owned_for_each_entity,
)
from domain.models.ownership import Ownership


def get_focus_company_id_and_name(
    owners_of_company: list[Ownership], companies_company_owns: list[Ownership]
) -> tuple[int, str]:
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


def find_shares_entities_own_of_focus_company(
    focus_company_id: int, focus_company_name: str, owners_of_company: List[Ownership]
) -> List[tuple[str, float, float]]:
    """Traverses outward from a given node and only return shares entities own of focus company."""

    owners_of_focus_company = get_owners_of_focus_company(owners_of_company)

    # Return empty dict if no entities own the focus company
    if not owners_of_focus_company.get(focus_company_id, []):
        return {}

    return get_total_shares_owned_for_each_entity(
        focus_company_id, focus_company_name, 1, 1, set(), owners_of_focus_company
    )


def find_shares_focus_company_owns_of_entities(
    focus_company_id: int,
    focus_company_name: str,
    companies_company_owns: List[Ownership],
) -> List[tuple[str, float, float]]:
    """Traverses infward from focus company and return shares it owns of entities."""

    entities_focus_company_owns = get_entities_focus_company_owns(
        companies_company_owns
    )

    # Return empty dict if focus company owns no entities
    if not entities_focus_company_owns.get(focus_company_id, []):
        return {}

    return get_total_shares_owned_for_each_entity(
        focus_company_id, focus_company_name, 1, 1, set(), entities_focus_company_owns
    )
