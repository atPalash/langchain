from dotenv import load_dotenv
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_experimental.agents import (
    create_csv_agent,
    create_pandas_dataframe_agent,
)
import pandas

load_dotenv()


def main():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_pandas_dataframe_agent(
        llm,
        pandas.read_csv("ABB.csv"),
        agent_type="openai-tools",
        verbose=True,
        allow_dangerous_code=True,
    )
    agent_executor.invoke(
        input={"input": "calculate ema10 and ema20 and print when ema10=ema20"}
    )


if __name__ == "__main__":
    main()
