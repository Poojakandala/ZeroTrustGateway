from fastapi import FastAPI, Header, HTTPException
from jose import jwt
from auth import verify_api_key, verify_jwt
from behavior import analyze_behavior
from context import analyze_context
from risk_engine import calculate_risk
from decision import make_decision
from logger import log_event

app = FastAPI(title="AI Driven Zero Trust Gateway")

# 🔹 Add this here 👇
SECRET_KEY = "fintech-secret"
ALGORITHM = "HS256"

@app.get("/generate-token")
def generate_token(user_id: str = "user1"):
    token = jwt.encode(
        {
            "sub": user_id,
            "api_key": "fintech123"
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"token": token}


# 🔹 Your existing transaction API
@app.post("/transaction")
def process_transaction(
    api_key: str = Header(...),
    token: str = Header(...),
    user_id: str = "user1",
    location: str = "India",
    amount: float = 1000,
    payload_size: int = 200
):

    verify_api_key(api_key)
    identity_risk = verify_jwt(token, api_key)

    behavior_score = analyze_behavior(amount, payload_size)
    context_score = analyze_context(location, payload_size)

    risk_score = calculate_risk(identity_risk, behavior_score, context_score)
    decision = make_decision(risk_score)

    log_event(user_id, risk_score, decision)

    return {
        "user": user_id,
        "risk_score": risk_score,
        "decision": decision
    }