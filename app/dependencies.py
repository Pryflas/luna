from fastapi import Header, HTTPException
from .config import settings


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Неверный API ключ")
    return x_api_key
