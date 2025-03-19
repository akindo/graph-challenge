from collections import defaultdict
from typing import Dict, List

from domain.models.ownership import Ownership


def get_entities_focus_company_owns(
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


def get_owners_of_focus_company(
    ownership_structure: List[Ownership],
) -> Dict[int, List[tuple]]:
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


def get_total_shares_owned_for_each_entity(
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
            get_total_shares_owned_for_each_entity(
                neighbour_id,
                neighbour_name,
                new_share_lower,
                new_share_upper,
                visited,
                graph,
            )
        )

    return results
