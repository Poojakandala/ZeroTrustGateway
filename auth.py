from jose import jwt, JWTError
from fastapi import HTTPException

SECRET_KEY = "fintech-secret"
ALGORITHM = "HS256"

def verify_jwt(token: str, api_key: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("api_key") != api_key:
            raise HTTPException(status_code=401, detail="API Key mismatch")

        # If valid identity → low risk
        return 1   # identity risk low

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")
def verify_api_key(api_key: str):
    if api_key != "fintech123":
        raise HTTPException(status_code=401, detail="Invalid API Key")