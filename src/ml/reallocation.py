def reallocate_budget(current_split: dict, change: str):
    """
    Reallocates budget based on user change
    """

    updated_split = current_split.copy()

    # Normalize first (safety)
    total = sum(updated_split.values())
    updated_split = {k: v / total for k, v in updated_split.items()}

    # Example: user adds music importance
    if "music" in change.lower():
        increase = 0.05  # increase 5%

        if "music" in updated_split:
            updated_split["music"] += increase

        # reduce others proportionally
        reduction_keys = [k for k in updated_split if k != "music"]

        total_reduction = sum(updated_split[k] for k in reduction_keys)

        for k in reduction_keys:
            proportion = updated_split[k] / total_reduction
            updated_split[k] -= proportion * increase

    # Final normalization
    total = sum(updated_split.values())
    updated_split = {k: v / total for k, v in updated_split.items()}

    return updated_split