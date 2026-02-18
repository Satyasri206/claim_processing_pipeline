import json
import re
from typing import Dict, Any, List

from llm import get_llm
from prompts import (
    SEGREGATOR_PROMPT,
    ID_AGENT_PROMPT,
    DISCHARGE_PROMPT,
    BILL_PROMPT,
)

llm = get_llm()


def safe_json_load(text: str) -> Dict[str, Any]:
    """
    Safely extract JSON from LLM output.
    Handles fenced blocks and raw JSON.
    """
    if not text:
        return {}

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{[\s\S]*?\}", text)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            return {}

    return {}


# ---------------- SEGREGATOR ----------------
def segregator_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Running Segregator Agent")

    routed_pages: Dict[str, List[Dict]] = {}

    for page in state.get("pages", []):
        text = page.get("text", "")

        try:
            doc_type = llm.invoke(
                SEGREGATOR_PROMPT + "\n\n" + text
            ).strip().lower()
        except Exception:
            doc_type = "unknown"

        routed_pages.setdefault(doc_type, []).append(page)

    print("Segregator output keys:", routed_pages.keys())

    return {
        "routed_pages": routed_pages
    }


# ---------------- ID AGENT ----------------
def id_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Running ID Agent")

    pages = state.get("routed_pages", {}).get("identity_document", [])
    print("ID pages count:", len(pages))

    if not pages:
        return {"id_data": {}}

    combined_text = "\n".join(p["text"] for p in pages)

    response = llm.invoke(ID_AGENT_PROMPT + "\n\n" + combined_text)
    print("ID RAW OUTPUT:", response)

    return {
        "id_data": safe_json_load(response)
    }


# ---------------- DISCHARGE ----------------
def discharge_summary_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Running Discharge Summary Agent")

    pages = state.get("routed_pages", {}).get("discharge_summary", [])
    print("Discharge pages count:", len(pages))

    if not pages:
        return {"discharge_data": {}}

    combined_text = "\n".join(p["text"] for p in pages)

    response = llm.invoke(DISCHARGE_PROMPT + "\n\n" + combined_text)
    print("DISCHARGE RAW OUTPUT:", response)

    return {
        "discharge_data": safe_json_load(response)
    }


# ---------------- ITEMIZED BILL ----------------
def itemized_bill_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    print("Running Itemized Bill Agent")

    pages = state.get("routed_pages", {}).get("itemized_bill", [])
    print("Bill pages count:", len(pages))

    if not pages:
        return {"bill_data": {}}

    combined_text = "\n".join(p["text"] for p in pages)

    response = llm.invoke(BILL_PROMPT + "\n\n" + combined_text)
    print("BILL RAW OUTPUT:", response)

    # Extract all JSON blocks from LLM output
    json_blocks = re.findall(r"\{[\s\S]*?\}", response)

    all_items = []
    total_amount = 0.0

    for block in json_blocks:
        data = safe_json_load(block)

        for item in data.get("items", []):
            try:
                cost = float(item.get("cost", 0))
            except Exception:
                cost = 0.0

            all_items.append(item)
            total_amount += cost

    return {
        "bill_data": {
            "items": all_items,
            "total_amount": round(total_amount, 2)
        }
    }
