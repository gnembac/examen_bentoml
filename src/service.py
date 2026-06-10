from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bentoml
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel, Field

MODEL_REF = "admission_lr:latest"
JWT_SECRET = "change-me-in-production"
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

model = bentoml.sklearn.load_model(MODEL_REF)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PredictRequest(BaseModel):
    gre_score: float = Field(..., alias="GRE Score")
    toefl_score: float = Field(..., alias="TOEFL Score")
    university_rating: float = Field(..., alias="University Rating")
    sop: float = Field(..., alias="SOP")
    lor: float = Field(..., alias="LOR")
    cgpa: float = Field(..., alias="CGPA")
    research: float = Field(..., alias="Research")


class PredictResponse(BaseModel):
    chance_of_admit: float


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc


@bentoml.service(name="admission_prediction_service")
class AdmissionPredictionService:
    @bentoml.api
    def login(self, body: LoginRequest) -> TokenResponse:
        if body.username != "admin" or body.password != "admin123":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = create_access_token({"sub": body.username})
        return TokenResponse(access_token=token)

    @bentoml.api
    def predict(self, body: PredictRequest, authorization: str | None = None) -> PredictResponse:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
        token = authorization.removeprefix("Bearer ").strip()
        verify_token(token)

        features = [[
            body.gre_score,
            body.toefl_score,
            body.university_rating,
            body.sop,
            body.lor,
            body.cgpa,
            body.research,
        ]]
        prediction = float(model.predict(features)[0])
        return PredictResponse(chance_of_admit=prediction)


svc = AdmissionPredictionService()