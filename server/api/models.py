from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    email: str
    password: str


class UserInfo(BaseModel):
    name: str
    balance: float
    accountNumber: str
