from langchain.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import json
import requests
from .functions import extract_id_from_jwt
from typing import Optional
from typing import Dict, Any
from pydantic import ValidationError
from ..constants import BANKING_API_URL


class SendMoneyArguments(BaseModel):
    accountNumber: int = Field(
        ...,
        description="This is the receiver id who's gonna receive the money.",
    )
    amount: float = Field(
        ...,
        description="This is the amount of money to send to a user.",
    )


class BillTypeModel(BaseModel):
    type: str = Field(..., description="This is the type of the bill to pay for. get only the name (gas/electricity/water)")


def send_money_to_json(amount: float, receiver_id: int) -> dict:
    return {"amount": amount, "receiverAccountId": receiver_id}


def bill_type_to_json(bill_type: str) -> dict:
    return {"type": bill_type}


# Function to generate headers
def set_headers(jwt: str) -> dict:
    return {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json"
    }


# get the user's info (balnace , id , name , email ) still returns pw (from backend)
class GetUserInfo(BaseTool):
    name = "GetUserInfo"
    description = "Tool to get the user's id, username/name, email & current balance/amount of money in his account(JWT)"

    def _run(self, jwt: str, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:

        userId = extract_id_from_jwt(jwt)

        balance_url = f"{BANKING_API_URL}/balance"
        user_url = f"{BANKING_API_URL}/users/{userId}"
        accountDetails_url = f"{BANKING_API_URL}/accounts"

        headers = set_headers(jwt)

        balance_info = requests.get(balance_url, headers=headers)
        user_info = requests.get(user_url, headers=headers)
        account_info = requests.get(accountDetails_url, headers=headers)

        # extract json data from all responses
        balance_data = balance_info.json()
        user_data = user_info.json()
        account_data = account_info.json()

        # Merge the dictionaries
        merged_data = {**user_data, **account_data, **balance_data}

        return merged_data

    async def _arun(
        self,  run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:

        raise NotImplementedError("tool does not support async")


# get the user's transaction history
class GetTransactionsHistory(BaseTool):
    name = "GetTransactionsHistory"
    description = "Tool to get the user's transaction history (transfers & bill payments) (JWT)"

    def _run(self,  jwt: str, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        bills_url = f"{BANKING_API_URL}/transfer/transferhistory"
        transfers_url = f"{BANKING_API_URL}/bill/billhistory"

        headers = set_headers(jwt)

        bills_history = requests.get(bills_url, headers=headers)
        transfers_history = requests.get(transfers_url, headers=headers)

        bills_data = bills_history.json()
        transfers_data = transfers_history.json()

        merged_data = bills_data + transfers_data
        return merged_data

    async def _arun(
        self,  run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:

        raise NotImplementedError("tool does not support async")


# send an amount of money to another user (id)
# this class requires the SendMoneyArguments to get the parsed query
class SendMoney(BaseTool):
    name = "SendMoney"
    description = "Tool to send an amount of money to another user via his account id (JWT)"

    def _run(
        self,  jwt: str, amount: float, receiver_id: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Synchronous method to send money."""
        url = f"{BANKING_API_URL}/transfer/transfer"
        headers = set_headers(jwt)

        data = send_money_to_json(amount, receiver_id)
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        return response.json()

    async def _arun(
        self,  run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:

        raise NotImplementedError("tool does not support async")


# pay a constant bill specified in the backend(100$)
class PayBill(BaseTool):
    name = "PayBill"
    description = "Tool to pay a bill type (gas , electricity , water)"

    def _run(
        self, jwt: str, bill_type: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Synchronous method to send money."""
        url = f"{BANKING_API_URL}/bill/pay"
        headers = set_headers(jwt)

        data = bill_type_to_json(bill_type)

        response = requests.post(url, headers=headers, json=data)
        return response.json()

    async def _arun(
        self,  run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:

        raise NotImplementedError("tool does not support async")
