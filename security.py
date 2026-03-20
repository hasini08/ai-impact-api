from fastapi import Header, HTTPException, status

API_KEY_HEADER_NAME = "X-API-Key"
EXPECTED_API_KEY = "super-secret-coursework-key"


def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Missing {API_KEY_HEADER_NAME} header",
        )

    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return x_api_key