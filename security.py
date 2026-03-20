import os

from fastapi import Header, HTTPException, status


API_KEY_HEADER_NAME = "X-API-Key"
DEFAULT_API_KEY = "change-me-in-env"


def get_api_key_value() -> str:
    return os.getenv("API_KEY", DEFAULT_API_KEY)


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    expected_key = get_api_key_value()

    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing {API_KEY_HEADER_NAME} header",
        )

    if x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return x_api_key