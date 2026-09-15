# FastAPI Backend — Phase 4
#
# Will expose a single POST /chat endpoint that calls into agent/graph.py
# and returns a grounded, cited answer.
#
# Not yet implemented. Depends on the LangGraph agent (Phase 3) being ready.

from fastapi import FastAPI

app = FastAPI(title="Shruti API")


@app.get("/health")
def health():
    return {"status": "ok"}
