from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bentoml
import jwt
from bentoml.exceptions import BentoMLException
from http import HTTPStatus
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
        raise BentoMLException("Token expired", error_code=HTTPStatus.UNAUTHORIZED) from exc
    except jwt.InvalidTokenError as exc:
        raise BentoMLException("Invalid token", error_code=HTTPStatus.UNAUTHORIZED) from exc


@bentoml.service(name="admission_prediction_service")
class AdmissionPredictionService:
    @bentoml.api(input_spec=LoginRequest)
    def login(self, username: str, password: str) -> TokenResponse:
        if username != "admin" or password != "admin123":
            raise BentoMLException("Invalid credentials", error_code=HTTPStatus.UNAUTHORIZED)
        token = create_access_token({"sub": username})
        return TokenResponse(access_token=token)

    @bentoml.api(input_spec=PredictRequest)
    def predict(
        self,
        gre_score: float,
        toefl_score: float,
        university_rating: float,
        sop: float,
        lor: float,
        cgpa: float,
        research: float,
        ctx: bentoml.Context,
    ) -> PredictResponse:
        authorization = ctx.request.headers.get("authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise BentoMLException("Missing token", error_code=HTTPStatus.UNAUTHORIZED)
        token = authorization.removeprefix("Bearer ").strip()
        verify_token(token)

        features = [[gre_score, toefl_score, university_rating, sop, lor, cgpa, research]]
        prediction = float(model.predict(features)[0])
        return PredictResponse(chance_of_admit=prediction)


svc = AdmissionPredictionService