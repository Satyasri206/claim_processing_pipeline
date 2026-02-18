import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form
from graph import build_graph
from pdf_utils import load_pdf_pages

app = FastAPI()
graph = build_graph()


@app.post("/api/process")
async def process_claim(
    claim_id: str = Form(...),
    file: UploadFile = File(...)
):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    pages = load_pdf_pages(tmp_path)
    os.unlink(tmp_path)

    initial_state = {
        "claim_id": claim_id,
        "pages": pages,
        "routed_pages": {},
        "id_data": {},
        "discharge_data": {},
        "bill_data": {},
        "final_output": {}
    }

    result = graph.invoke(initial_state)
    return result["final_output"]
