from fastapi import HTTPException, Header, Request, Response
from fastapi.responses import JSONResponse
from fastapi import APIRouter
import httpx
from .constants import BANKING_API_URL
from .chat import get_response
from .models import LoginRequest
from .chatcf.functions import extract_id_from_jwt
from pymongo import MongoClient
import jwt
router = APIRouter()


@router.post("/login")
async def login(login_request: LoginRequest, response: Response):
    email = login_request.email
    password = login_request.password

    # banking server login url
    url = f"{BANKING_API_URL}/auth/login"

    try:
        async with httpx.AsyncClient() as client:
            response_from_bank = await client.post(url, json={"email": email, "password": password})

            if response_from_bank.status_code == 200:
                response = response_from_bank.json()
                return response
            else:
                response.status_code = 400
                return response_from_bank.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

chat_history = []

# Connect to MongoDB
# Change URL as per your MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["bankingChat"]
collection = db["chats"]


@router.post("/generate")
async def generate(request: Request, response: Response, authorization: str = Header(None)):

    try:
        # check body presence
        if not request:
            raise HTTPException(status_code=401, detail="User input missing")

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
        try:
            res = await get_response(query, token, chat_history)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while generating response: {e}")

        print("Bot response: ", res)
        # Store chat history in MongoDB

        user_id = extract_id_from_jwt(token)
        print(user_id)
        chat_entry = {"userId": user_id,
                      "userMessage": query, "assistantMessage": res}
        collection.insert_one(chat_entry)

        response = JSONResponse(content={"message": res})
        return response

    except HTTPException as e:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def fetch_chat_by_user(token):

    try:
        user_id = extract_id_from_jwt(token)
    except:
        return None

    # Fetch chat documents for the specified user ID
    user_chat = collection.find({"userId": user_id})
    return list(user_chat)


@router.get("/history")
async def history(response: Response, authorization: str = Header(None)):
    try:
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
        userChat = fetch_chat_by_user(token)
        for item in userChat:
            item['_id'] = str(item['_id'])

        return JSONResponse(content=userChat)

    except HTTPException as e:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
