import httpx
import pytest

from llm_runtime_gateway.main import app


@pytest.mark.asyncio
async def test_healthz_returns_service_status() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "llm-runtime-gateway",
    }
