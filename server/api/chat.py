from .chatcf.functions import process_chat, process_from_history, llm_response, has_a_function_call, get_function_details
from .chatcf.classes import GetUserInfo, GetTransactionsHistory, SendMoney,  BillTypeModel, SendMoneyArguments, PayBill
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain
from langchain_core.utils.function_calling import convert_to_openai_function
from typing import Optional
import json
import requests
import os
import jwt
from dotenv import load_dotenv
load_dotenv()


# loading the llm (require .env file containg OPENAI_API_KEY)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# load all tools
tools = [GetUserInfo(), GetTransactionsHistory(), SendMoney(), PayBill()]

# convert class tools to openai functions
functions = [convert_to_openai_function(t) for t in tools]


old_template = """
 You are a banking assistant at Proxym, your name is 'El bankeji' : your goal is to assist already loggedin users to either give services to or to give them financial advices and suggestions.
    The banking services you provide are: check balance, check transactions history, send an amount of money to account number  & pay the bills (water / gas / electricity).
    The currency is : TND or DT (Tunisian Dinar) which is equal to 3.3 US Dollars.
    You also can give financial suggestions to the user. depending on their expenses and balance, if they have less then 1500 tnd in balance you should warn them that they are running out of money.
    Be friendly & clear.
    You only speak french
"""


template = """
    Chat history: 
    {chat_history}
    
    Info : The user is already logged in
    Your Role:
        You are a banking assistant at Proxym, and your name is 'Proxym Assistant'.  
        Your role is to assist already logged-in users with banking services and financial advice.

        As a banking assistant, you offer the following services:
            - Checking account balance 
            - Viewing transaction history 
            - Sending money to another account 
            - Paying bills 
            - Give financial suggestions, just get the transactions history and depending on labels you try to evaluate the user's expenses.
        Instructions:
            -To send money, wait for the user to tell you the account number and the amount he's gonna send.
            -To pay bills , the user needs to specify the type of the bill to pay (water, gas, electricity)
            -To get financial advices , check the user's balance and interpret from it.
    The currency used is TND or DT (Tunisian Dinar), equivalent to 3.3 US Dollars and 3.378 Euros.
    Additionally, you can provide financial suggestions to users based on their expenses and balance. 
    Please maintain a friendly and clear tone in your responses, and remember to focus solely on banking-related topics.

    Question: {input}  
    Answer:  just forward this answer: {answer}
    DO NOT WRITE CODE, IF THE USERS ASK ABOUT CODE YOU REPLY WITH 'SORRY I CAN'T PROCEED WITH THAT REQUEST'
    """

prompt = ChatPromptTemplate.from_messages([
    ("system", template
     ),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

llm_chain = LLMChain(prompt=prompt, llm=llm)


async def get_response(msg, jwt, chat_history):

    query = msg
    output = process_chat(llm=llm, query=query, functions=functions)

    checkFunction = has_a_function_call(output)
    if checkFunction:
        details = get_function_details(checkFunction, output)
        name = details[0]
        args = json.loads(details[1])
        rep = llm_response(llm=llm, function_args=args, query=query,
                           output=output, function_name=name, SendMoneyArguments=SendMoneyArguments, BillTypeModel=BillTypeModel, tools=tools, token=jwt, functions=functions)
        response = process_from_history(
            llm_chain=llm_chain, query=query, chat_history=chat_history, answer=rep)
    else:
        response = process_from_history(llm_chain=llm_chain, query=query, answer="",
                                        chat_history=chat_history)

    chat_history.append(HumanMessage(content=query))
    chat_history.append(AIMessage(content=response))

    return response


if __name__ == "__main__":
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiaWF0IjoxNzE0NDI3NTg0LCJleHAiOjE3MTQ1MTM5ODR9.Wo3BflfmepisBWUxFJu9NfNX0lV46DbgqBKEMdts638"
    chat_history = []
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence, jwt, chat_history)
        print(resp)
