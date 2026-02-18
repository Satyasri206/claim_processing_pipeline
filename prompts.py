SEGREGATOR_PROMPT = """
You are given a single page from an insurance claim document.

Classify it into ONE of the following types:
- claim_forms
- cheque_or_bank_details
- identity_document
- itemized_bill
- discharge_summary
- prescription
- investigation_report
- cash_receipt
- other

Return only the document type.
"""

ID_AGENT_PROMPT = """
You are an information extraction system.

From the following document text, extract patient identity details.

Rules:
- Carefully search for insurance-related identifiers.
- A policy number may appear as:
  "Policy Number", "Policy No", "Insurance ID", "Member ID", "Health ID", or similar.
- If a policy number is present anywhere in the text, extract it exactly.
- Do NOT guess values.
- Return valid JSON only. No explanation text.

JSON schema:
{
  "patient_name": string | null,
  "dob": string | null,
  "id_number": string | null,
  "policy_number": string | null
}

"""

DISCHARGE_PROMPT = """
Extract discharge summary information.
Return JSON with keys:
diagnosis, admission_date, discharge_date, doctor_name
"""

BILL_PROMPT = """
Extract itemized billing details.
Return JSON with keys:
items (list of {name, cost}), total_amount
"""
