from pydantic import BaseModel
from typing import Optional
from fastapi import FastAPI, HTTPException, Header, Response, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
import jwt
from constants import BANKING_API_URL
import asyncio

from chat import get_response
app = FastAPI()

# Allow requests from http://localhost:3000
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/login")
async def login(login_request: LoginRequest, response: Response):
    email = login_request.email
    password = login_request.password

    # banking server login url
    url = f"{BANKING_API_URL}/auth/login"

    try:
        async with httpx.AsyncClient() as client:
            response_from_bank = await client.post(url, json={"email": email, "password": password})

            if (response_from_bank.status_code == 200):

                response = response_from_bank.json()
                return response
            else:
                response.status_code = 400
                response = response_from_bank.json()
                return response
    except httpx.HTTPStatusError as e:

        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@app.post("/generate")
async def generate(request: Request, response: Response, authorization: str = Header(None)):

    try:
        # check body presence
        if not request:
            raise HTTPException(
                status_code=401, detail="User input missing")

        # check token presence
        if not authorization:
            raise HTTPException(
                status_code=401, detail="Authorization header missing")

        # split authorization header and get token
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=401, detail="Invalid authorization header format")

        # get token
        token = parts[1]
        print("Headers token from client: ", token)
        # get query from body
        body = await request.json()

        query = body.get("message")
        print("Body message from client: ", query)
        res = await get_response(query, token)
        print("Bot response: ", res)
        response = JSONResponse(content={"message": res})
        return response

    except HTTPException as e:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
