import httpx
from config import settings

async def invoke_ai_service(filename: str, content: bytes, content_type: str) -> dict:
    url = f"{settings.AI_SERVICE_URL}/predict"
    async with httpx.AsyncClient(timeout=30.0) as client:
        files = {"file": (filename, content, content_type)}
        response = await client.post(url, files=files)
        response.raise_for_status()
        return response.json()
