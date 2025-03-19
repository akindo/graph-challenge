def print_results(ownerships: list[tuple[str, float, float]]):
    """Prints the results of the ownership analysis."""

    def format_share(share):
        return f"{int(share * 100)}" if (share * 100) % 1 == 0 else f"{share * 100:.1f}"

    for node_name, share_lower, share_upper in ownerships:
        share_average = (share_lower + share_upper) / 2

        print(
            f"* {node_name}: {format_share(share_lower)}%, {format_share(share_average)}%, {format_share(share_upper)}%"
        )
