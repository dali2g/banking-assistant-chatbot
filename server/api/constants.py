from abc import ABC, abstractmethod
import os
from dotenv import load_dotenv
from .models import UserInfo
from .chatcf.functions import extract_id_from_jwt
import requests
# Load the .env file
load_dotenv()

BANKING_API_URL = "http://localhost:5000/api"


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
