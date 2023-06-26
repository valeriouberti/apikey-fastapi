from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery

api_keys = [
    "my_api_key"
]

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def get_api_key(
        api_key_header: str = Security(api_key_header),
) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


app = FastAPI()


@app.get("/public")
def public():
    """A public endpoint that does not require any authentication."""
    return "Public Endpoint"


@app.get("/protected")
def private(api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
