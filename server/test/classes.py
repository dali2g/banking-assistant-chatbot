from langchain.tools import BaseTool
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import json
import requests
from functions import extract_id_from_jwt
from typing import Optional
from typing import Dict, Any
from pydantic import ValidationError
from constants import BANKING_API_URL


class SendMoneyArguments(BaseModel):
    accountNumber: int = Field(
        ...,
        description="This is the receiver id who's gonna receive the money.",
    )
    amount: float = Field(
        ...,
        description="This is the amount of money to send to a user.",
    )
# https://github.com/langchain-ai/langchain/issues/13662

    # @root_validator
    # def validate_inputs(cls, values: Dict[int, Any]) -> Dict:
    #     accountNumber = values.get("accountNumber")
    #     amount = values.get("amount")
    #     print(amount, "======", accountNumber)
    #     # Add your validation logic here
    #     if not isinstance(accountNumber, int) or not isinstance(amount, float):
    #         err = {'error': 'Did not specify the account number or amount'}
    #         return err
    #     return values


# get the user's info (balnace , id , name , email ) still returns pw (from backend)
class GetUserInfo(BaseTool):
    name = "GetUserInfo"
    description = "Tool to get the user's id, username/name, email & current balance/amount of money in his account(JWT)"

    def _run(self, jwt: str, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:

        userId = extract_id_from_jwt(jwt)

        balance_url = f"{BANKING_API_URL}/balance"
        user_url = f"{BANKING_API_URL}/users/{userId}"
        accountDetails_url = f"{BANKING_API_URL}/accounts"

        headers = {"Authorization": f"Bearer {jwt}",
                   "Content-Type": "application/json"}

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
        self, amount: float, receiver_id: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:
        """Asynchronous method to send money."""

        raise NotImplementedError("tool does not support async")


# get the user's transaction history
class GetTransactionsHistory(BaseTool):
    name = "GetTransactionsHistory"
    description = "Tool to get the user's transaction history (JWT)"

    def _run(self,  jwt: str, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> dict:
        url = f"{BANKING_API_URL}/transactions/history"

        headers = {"Authorization": f"Bearer {jwt}",
                   "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)

        return response.json()

    async def _arun(
        self, amount: float, receiver_id: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:
        """Asynchronous method to send money."""

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
        url = f"{BANKING_API_URL}/transactions/send"
        headers = {"Authorization": f"Bearer {jwt}",
                   "Content-Type": "application/json"}
        data = {"amount": amount, "accountNumber": receiver_id}
        response = requests.post(url, headers=headers, json=data)

        return response.json()

    async def _arun(
        self, amount: float, receiver_id: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:
        """Asynchronous method to send money."""

        raise NotImplementedError("tool does not support async")


# pay a constant bill specified in the backend(100$)
class PayBill(BaseTool):
    name = "PayBill"
    description = "Tool to pay the constant bill 100"

    def _run(
        self, jwt: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> dict:
        """Synchronous method to send money."""
        url = f"{BANKING_API_URL}/transactions/pay"
        headers = {"Authorization": f"Bearer {jwt}",
                   "Content-Type": "application/json"}

        response = requests.post(url, headers=headers)
        return response.json()

    async def _arun(
        self, amount: float, receiver_id: int, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> dict:
        """Asynchronous method to send money."""

        raise NotImplementedError("tool does not support async")
