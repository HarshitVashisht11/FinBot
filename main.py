import json
from difflib import get_close_matches as gcm
import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY = os.getenv("API_KEY")

def cryptoprice(symbol: str,api_Key: str) -> float:
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey={api_Key}"
    response = requests.get(url)
    data = response.json()
    if "Realtime Currency Exchange Rate" in data:
        price = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
        return float(price)
    else:
        return None
    
def stockprice(symbol: str, api_key: str):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if "Global Quote" in data:
        quote_data = data["Global Quote"]
        if "05. price" in quote_data:
            return quote_data["05. price"]
    return None

def load(file_path: str):
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def match(user_question: str, questions: list[str]):
    matches: list = gcm(user_question, questions, n=1, cutoff=0.4)
    return matches[0] if matches else None


def getans(question: str, knowledge_base: dict):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None


def add(*nums):
    return sum(nums)


def sub(*nums):
    result = nums[0]
    for num in nums[1:]:
        result -= num
    return result


def multiply(*nums):
    result = 1
    for num in nums:
        result *= num
    return result


def div(num1, num2):
    if num2 != 0:
        return num1 / num2
    else:
        return "Error: Cannot divide by zero"


def sipcalc(p, ir, time):
    amount = p * ((1 + ir) ** (time * 12) - 1) / ir
    return amount


def emicalc(p, ir, time):
    emi = p * ir * (1 + ir) ** (time * 12) / ((1 + ir) ** (time * 12) - 1)
    return emi






def bot():
    data: dict = load('Data.json')

    introduction = "Bot: How can I help you today? If you want to use the calculator, type 'calc'. " \
                   "To get the latest stock price, type 'stock'. To get the latest cryptocurrency price, type 'crypto'."
    print(introduction)


    is_calc_mode = False 

    while True:
        userinp: str = input("You: ")

        if userinp.lower() == 'calc':
            print("Bot: Calculator mode activated. Enter numbers and operation.")
            print("I only have these calculator till now ")
            print("Type a for add")
            print("Type s for subtract")
            print("Type m for multiply")
            print("Type d for divide")
            print("Type sip for Sip Calculator")
            print("Type emi for Emi Calculator")
            print("Type tm to calculte Time for becoming Millionare :)")
            calct: str = input("You: ")
            
            if calct.lower() in ['a', 's', 'm', 'd', 'sip', 'emi', 'tm']:
                operation = calct.lower()

                if operation == 'a':
                    numbers = input("Bot: Enter numbers separated by spaces: ").split()
                    numbers = [float(num) for num in numbers]
                    result = add(*numbers)
                    print(f"Bot: The sum is {result}")
                elif operation == 's':
                    numbers = input("Bot: Enter numbers separated by spaces: ").split()
                    numbers = [float(num) for num in numbers]
                    result = sub(*numbers)
                    print(f"Bot: The difference is {result}")

                elif operation == 'm':
                    numbers = input("Bot: Enter numbers separated by spaces: ").split()
                    numbers = [float(num) for num in numbers]
                    result = multiply(*numbers)
                    print(f"Bot: The product is {result}")

                elif operation == 'd':
                    numbers = input("Bot: Enter numbers separated by spaces: ").split()
                    numbers = [float(num) for num in numbers]
                    result = div(*numbers)
                    print(f"Bot: The quotient is {result}")

                elif operation == 'sip':
                    p = float(input("Bot: Enter the principal amount: "))
                    ir = float(input("Bot: Enter the monthly interest rate: "))
                    t = float(input("Bot: Enter the time (in years): "))
                    amount = sipcalc(p, ir, t)
                    print(f"Bot: The SIP amount is {amount}")

                elif operation == 'emi':
                    p = float(input("Bot: Enter the principal amount: "))
                    ir = float(input("Bot: Enter the monthly interest rate: "))
                    t = float(input("Bot: Enter the time (in years): "))
                    emi = emicalc(p, ir, t)
                    print(f"Bot: The EMI amount is {emi}")

                print("Bot: Do you want to continue using the calculator? Type 'calc' to continue or 'chat' to switch to chat mode.")

        elif userinp.lower() == 'stock':
            print("Bot: Enter the Name of Stock in Capital")
            ss = input("You: ")
            sp = stockprice(ss, API_KEY)
            if sp:
                print(f"Bot: The latest stock price of {ss} is {sp}")
            else:
                print(f"Bot: Sorry, could not retrieve the stock price for {ss}")
            print("Bot: Do you want to find other stock price ? Type 'stock' to continue or 'chat' to switch to chat mode.")
            
        elif userinp.lower() == 'crypto':
            cs = input("You: ")
            cp = cryptoprice(cs, API_KEY)
            if cp:
                print(f"Bot: The latest price of {cs} is {cp}")
            else:
                print(f"Bot: Sorry,could not retrive the stock price for{cs}")
            print("Bot: Do you want to find other Crypto price ? Type 'crypto' to continue or 'chat' to switch to chat mode.")
        elif userinp.lower() == 'chat':
            is_calc_mode = False
            print("Bot: Chat mode activated. You can continue chatting.")

        elif userinp.lower() == 'quit':
            break

        else:
            bmatch: str | None = match(userinp, [q["question"] for q in data["questions"]])

            if bmatch:
                answer: str = getans(bmatch, data)
                print(f"Bot: {answer}")
                print("If my answer is wrong type 'n'")
                feedback: str = input("You: ")
                if feedback.lower() == 'n':
                    print("Bot: What is the correct answer?")
                    correctans: str = input("You: ")
                    if bmatch:
                        for q in data["questions"]:
                            if q["question"] == bmatch:
                                q["answer"] = correctans
                                break
                    else:
                        data["questions"].append({"question": userinp, "answer": correctans})
                    save('Data.json', data)
                    print("Bot: Thank you for the feedback! I've updated my knowledge.")
                else:
                    print("Bot: Next question.")

            else:
                print("Bot: I don't know the answer. Can you teach me?")
                newans: str = input("You: ")

                if newans.lower() != 'skip':
                    data["questions"].append({"question": userinp, "answer": newans})
                else:
                    data["questions"].append({"question": userinp, "answer": newans})
                    save('Data.json', data)
                    print("Bot: Thank you! I've learned something new.")

if __name__ == "__main__":
    bot()
