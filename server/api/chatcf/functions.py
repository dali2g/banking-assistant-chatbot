import jwt
from langchain.schema import HumanMessage, AIMessage, ChatMessage
from langchain.chains import create_tagging_chain, create_tagging_chain_pydantic


def extract_id_from_jwt(token):
    try:
        # Decode the JWT token without verifying the signature
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        # Extract the 'id' field from the decoded token
        user_id = decoded_token.get('id')
        return user_id
    except jwt.ExpiredSignatureError:
        return {"err": "Token has expired."}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token."}


def has_a_function_call(msg):
    function = msg.additional_kwargs.get("function_call")
    if function:
        return 1
    return 0


def get_function_details(checkFunction, msg):
    if checkFunction:
        function_name = msg.additional_kwargs["function_call"]["name"]
        function_args = msg.additional_kwargs["function_call"]["arguments"]

        return (function_name, function_args)
    else:
        return None


# process which function to run
def run_api_functions(llm, query, function_args, tools, token, SendMoneyArguments, BillTypeModel, function_name):
    toolRes = None

    match function_name:
        case "GetUserInfo":
            toolRes = tools[0]._run(jwt=token, query=function_args)
        case "GetTransactionsHistory":
            toolRes = tools[1]._run(jwt=token, query=function_args)
        case "SendMoney":

            chain = create_tagging_chain_pydantic(SendMoneyArguments, llm)
            # solution 3al 7it
            try:
                parse = chain.invoke(query)

                accountNumber = parse.get("text").accountNumber

                amount = parse.get("text").amount

                toolRes = tools[2]._run(
                    jwt=token, receiver_id=accountNumber, amount=amount)

            except:
                toolRes = {
                    'error': 'Did not specify the account number or amount'}

        case "PayBill":
            chain = create_tagging_chain_pydantic(BillTypeModel, llm)
            try:
                parse = chain.invoke(query)

                print(parse)
                billType = parse.get("text").type
                print(billType)
                toolRes = tools[3]._run(jwt=token, bill_type=billType)
            except:
                toolRes = {
                    'error': "did not specify the bill type"
                }
        case _:
            toolRes = {'msg': 'no function was selected'}
    print("\nrun_api_fucntion: \n", toolRes, "\n=====\n")
    return toolRes


def process_chat(llm, query, functions):
    response = llm.invoke(

        # the llm automatically chooses the correct function for the query
        # determines which function to execute
        [HumanMessage(content=query)], functions=functions)

    return response


def llm_response(llm, function_args,  query, output, tools, token, SendMoneyArguments, BillTypeModel, function_name, functions):
    # Second response: make api response human readable
    second_response = llm.invoke(
        [
            HumanMessage(content=query),
            AIMessage(content=str(output.additional_kwargs)),
            ChatMessage(
                role="function",
                additional_kwargs={
                    "name": output.additional_kwargs["function_call"]["name"]
                },
                content=f"{run_api_functions(llm=llm, function_args=function_args, query=query, tools=tools,
                                             token=token, SendMoneyArguments=SendMoneyArguments, BillTypeModel=BillTypeModel, function_name=function_name)}"
            ),
        ],
        functions=functions,
    )
    return second_response.content


def process_from_history(llm_chain, query, chat_history, answer):
    response = llm_chain.invoke({
        "chat_history": chat_history,
        "input": query,
        "answer": answer,
    })
    print("\nprocess_from_history: ================== history===========================\n",
          chat_history, "\n llm_response: ", answer, "\n === user request", query, "\n=================================\n")
    return response["text"]
