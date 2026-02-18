from typing import TypedDict, Dict, List, Any

class GraphState(TypedDict):
    claim_id: str
    pages: List[Dict[str, Any]]
    routed_pages: Dict[str, List[Dict[str, Any]]]

    id_data: Dict[str, Any]
    discharge_data: Dict[str, Any]
    bill_data: Dict[str, Any]

    final_output: Dict[str, Any]
