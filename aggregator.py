def aggregate(state):
    """
    Aggregator ONLY merges outputs.
    No business logic here.
    """

    state["final_output"] = {
        "claim_id": state["claim_id"],
        "identity": state.get("id_data", {}),
        "discharge_summary": state.get("discharge_data", {}),
        "billing": state.get("bill_data", {})
    }

    return state
