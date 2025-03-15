import os

# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  # Or set directly


def generate_gherkin_with_langchain(user_input):
    """Generates Gherkin feature file steps using LangChain and OpenAI."""

    # llm = OpenAI(temperature=0)  # Lower temperature for more deterministic output
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="""
        Given the user input: "{user_input}", generate Gherkin feature file steps for stock analysis.

        The steps should always start with:
        "Given stocks from index nifty50"

        There can be multiple "When" steps of the form "let <id> = <operator> in <number> samples of <interval> <ohlc> <indicator> <window>"
        the allowed options are 
        <id>: any word, 
        <operator>: latest, oldest, minimum, maximum, average, rate, change, defualt is latest
        <number>: positive integer defualt 1, 
        <interval>: day, minute5, minute30, hour, default is minute5
        <ohlc>: open, high, low, close default is close
        <indicator>: ma, ema, atr, rsi, vwap, rvol defualt is ema
        <window>: positive integer default 10

           
        The "Then" and "*" steps should list tickers, respectively.

        Examples:
        User input: "rate of ema 10 > 0"
        Gherkin:
        Given stocks from index nifty50
        When let ema10Change = rate in 20 samples of minute5 close ema 10
        Then list bull = tickers with ema10Change > 0
        * list bear = tickers with ema10Change < 0

        User input: "sma 20 less than zero"
        Gherkin:
        Given stocks from index nifty50
        When let sma20Change = rate in 20 samples of minute5 close sma 20
        Then list bear = tickers with sma20Change < 0
        * list bull = tickers with sma20Change > 0

        User input: "{user_input}"
        Gherkin:
        """,
    )

    # chain = LLMChain(llm=llm, prompt=prompt_template)
    chain = prompt_template | llm | StrOutputParser()
    gherkin = chain.invoke(user_input)
    return gherkin.strip()


# Example usage
user_input1 = (
    "20 sample rate of ema 10 > 0," "20 sample rate vwap10 > 0",
    "latest close > 2 sample oldest day ema 10",
)
# user_input2 = "ema 20 < 0"
# user_input3 = "sma 20 greater than 0"
# user_input4 = "find stocks where 10 period sma is increasing"
# user_input5 = "stocks with ema 55 less than 0"
# user_input6 = "show me when sma 100 is positive"

print(f"User Input: {user_input1}\n{generate_gherkin_with_langchain(user_input1)}")
# print(f"\nUser Input: {user_input2}\n{generate_gherkin_with_langchain(user_input2)}")
# print(f"\nUser Input: {user_input3}\n{generate_gherkin_with_langchain(user_input3)}")
# print(f"\nUser Input: {user_input4}\n{generate_gherkin_with_langchain(user_input4)}")
# print(f"\nUser Input: {user_input5}\n{generate_gherkin_with_langchain(user_input5)}")
# print(f"\nUser Input: {user_input6}\n{generate_gherkin_with_langchain(user_input6)}")

gherkin = (
    "Given stocks from index nifty50\n"
    "When let ema10Change = rate in 20 samples of minute5 close ema 10\n"
    "* let vwap10Change = rate in 20 samples of minute5 close vwap 10\n"
    "* let vwapMax = maximum in 10 samples of minute5 close vwap 10\n"
    "* let vwapMin = minimum in 10 samples of minute5 close vwap 10\n"
    "* let emaMax = maximum in 10 samples of minute5 close ema 10\n"
    "* let emaMin = minimum in 10 samples of minute5 close ema 10\n"
    "* let ema10Day = oldest in 2 samples of day close ema 10\n"
    "* let close = latest in 1 samples of minute5 close\n"
    "* let dayClose = oldest in 2 samples of day close\n"
    "Then list bulls = tickers with ema10Change > 0 and vwap10Change > 0 and close > ema10Day * 0.99 and close < ema10Day * 1.01\n"
    "* list bears = tickers with ema10Change < 0 and vwap10Change < 0 and close > ema10Day * 0.99 and close < ema10Day * 1.01\n"
    "* list vwapMovers = tickers with ((ema10Change < 0 and vwap10Change < 0) or (ema10Change > 0 and vwap10Change > 0)) and abs(dayClose - close) / dayClose > 0.01\n* list movers = tickers with abs(dayClose - close) / dayClose > 0.01\n",
)
