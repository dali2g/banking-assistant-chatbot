from .models import UserInfo
from .chatcf.functions import extract_id_from_jwt
import requests
from langchain_core.pydantic_v1 import BaseModel, Field
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
load_dotenv()

BANKING_API_URL = os.getenv("BANKING_API_URL")



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




class Provider():
    @abstractmethod
    def providerName():
        pass

    @abstractmethod
    def getUserInfo():
        pass
    @abstractmethod
    def getTransctionHistory():
        pass
    @abstractmethod
    def sendMoney():
        pass
    @abstractmethod
    def payBill():
        pass


class MockProvider(Provider):
    def providerName():
        return "MOCK"

    def getUserInfo(jwt: str):
        print("start user info")
        print("jwt:", jwt)
        userId = extract_id_from_jwt(jwt)
        print("userId: ", userId)
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
        print("user data: ", user_data)
        # Merge the dictionaries
        merged_data = {**user_data, **account_data, **balance_data}

        print("merged data :", merged_data)
        return merged_data
    
    def getTransctionHistory(jwt: str):
        bills_url = f"{BANKING_API_URL}/transfer/transferhistory"
        transfers_url = f"{BANKING_API_URL}/bill/billhistory"

        headers = set_headers(jwt)

        bills_history = requests.get(bills_url, headers=headers)
        transfers_history = requests.get(transfers_url, headers=headers)

        bills_data = bills_history.json()
        transfers_data = transfers_history.json()

        merged_data = bills_data + transfers_data
        return merged_data
    


    def sendMoney(jwt: str, amount: float , receiver_id: int):
        url = f"{BANKING_API_URL}/transfer/transfer"
        headers = set_headers(jwt)

        data = send_money_to_json(amount, receiver_id)
        response = requests.post(url, headers=headers, json=data)
        print(response.status_code)
        return response.json()
    
    def payBill(jwt: str, bill_type : str):
        url = f"{BANKING_API_URL}/bill/pay"
        headers = set_headers(jwt)

        data = bill_type_to_json(bill_type)

        response = requests.post(url, headers=headers, json=data)
        return response.json()

class BankeriseProvider(Provider):
    def providerName():
        return "BANKERISE"


class ProviderHolder():
    activeProvider = None

    def getProvider():
        if (ProviderHolder.activeProvider is None):
            providerName = os.getenv('PROVIDER')
            for provider in Provider.__subclasses__():
                if (provider.providerName() == providerName):
                    ProviderHolder.activeProvider = provider
                    return provider
        return ProviderHolder.activeProvider


print("response: ", ProviderHolder.getProvider().providerName())
print("response: ", ProviderHolder.getProvider().providerName())
