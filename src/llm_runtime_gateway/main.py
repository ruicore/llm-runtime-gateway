from typing import Final

from fastapi import FastAPI

SERVICE_NAME: Final = "llm-runtime-gateway"

app = FastAPI(
    title="LLM Runtime Gateway",
    summary="Production-style LLM runtime gateway for reliable AI applications.",
    version="0.1.0",
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok", "service": SERVICE_NAME}
