from collections import defaultdict
from typing import Dict, List

from ownership import Ownership


def _build_adjacency_list(
    ownership_structure: List[Ownership],
) -> Dict[int, List[tuple]]:
    """Builds an adjacency list where each source points to its target nodes."""

    adjacency_list = defaultdict(list)

    for ownership in ownership_structure:
        adjacency_list[ownership.source].append(
            (
                ownership.target,
                ownership.target_name,
                ownership.share_lower,
                ownership.share_upper,
            )
        )

    return dict(adjacency_list)


def _build_reverse_list(ownership_structure: List[Ownership]) -> Dict[int, List[tuple]]:
    """Builds a reverse adjacency list where each target points to its source nodes."""

    reverse_list = defaultdict(list)

    for ownership in ownership_structure:
        reverse_list[ownership.target].append(
            (
                ownership.source,
                ownership.source_name,
                ownership.share_lower,
                ownership.share_upper,
            )
        )

    return dict(reverse_list)


def _get_total_shares_owned_for_each_entity(
    node_id: int,
    node_name: str,
    share_lower: float,
    share_upper: float,
    visited: set,
    graph: Dict[int, List[int]],
) -> List[tuple[str, float, float]]:
    """Finds total shares owned by entities/focus company using the depth first search algorithm."""

    # Leaf node found, stopping traversal.
    if node_id not in graph:
        return [(node_name, share_lower, share_upper)]

    if node_id in visited:  # Detect and prevent cycles
        return []
    visited.add(node_id)

    results: List[tuple[str, float, float]] = []

    for (
        neighbour_id,
        neighbour_name,
        neighbour_share_lower,
        neighbour_share_upper,
    ) in graph[node_id]:
        new_share_lower = share_lower * neighbour_share_lower
        new_share_upper = share_upper * neighbour_share_upper

        results.extend(
            _get_total_shares_owned_for_each_entity(
                neighbour_id,
                neighbour_name,
                new_share_lower,
                new_share_upper,
                visited,
                graph,
            )
        )

    return results


def find_shares_entities_own_of_focus_company(
    start_node_id: int, start_company_name: str, owners_of_company: List[Ownership]
) -> List[tuple[str, float, float]]:
    """Traverses outward from a given node and only return shares entities own of focus company."""

    reverse_list = _build_reverse_list(owners_of_company)

    # Return empty dict if no entities own the focus company
    if not reverse_list.get(start_node_id, []):
        return {}

    return _get_total_shares_owned_for_each_entity(
        start_node_id, start_company_name, 1, 1, set(), reverse_list
    )


def find_shares_focus_company_owns_of_entities(
    start_node_id: int, start_company_name: str, companies_company_owns: List[Ownership]
) -> List[tuple[str, float, float]]:
    """Traverses infward from focus company and return shares it owns of entities."""

    adjacency_list = _build_adjacency_list(companies_company_owns)

    # Return empty dict if focus company owns no entities
    if not adjacency_list.get(start_node_id, []):
        return {}

    return _get_total_shares_owned_for_each_entity(
        start_node_id, start_company_name, 1, 1, set(), adjacency_list
    )
