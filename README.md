## Claim Processing Pipeline

This project demonstrates a multi-agent document processing pipeline for insurance claims using FastAPI and LangGraph.

### Flow
1. PDF is split into pages
2. A segregator agent classifies each page into document types
3. Only relevant pages are routed to:
   - ID Agent
   - Discharge Summary Agent
   - Itemized Bill Agent
4. An aggregator merges all extracted outputs into a final JSON response

### LLM
Ollama is used for local, cost-free inference.  
The architecture is model-agnostic and can be switched to any hosted LLM.

### Run
```bash
uvicorn main:app --reload
