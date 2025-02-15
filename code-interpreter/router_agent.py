from typing import Any
from dotenv import load_dotenv
from langchain import hub
from langchain.tools import Tool
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
    instructions = "You are an agent to generate random number from 1 to 100"
    base_prompt = hub.pull("langchain-ai/react-agent-template")
    prompt = base_prompt.partial(instructions=instructions)

    tools = [PythonREPLTool()]
    agent = create_react_agent(
        prompt=prompt, llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), tools=tools
    )
    python_agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    pandas_agent_executor = create_pandas_dataframe_agent(
        llm,
        pandas.read_csv("ABB.csv"),
        agent_type="openai-tools",
        verbose=True,
        allow_dangerous_code=True,
    )

    def python_agent_executor_wrapper(original_prompt: str) -> dict[str, Any]:
        return python_agent_executor.invoke({"input": original_prompt})

    tools = [
        Tool(
            name="Python Agent",
            func=python_agent_executor_wrapper,
            description="used when transform from natural language to python code",
        ),
        Tool(
            name="Pandas Agent",
            func=pandas_agent_executor.invoke,
            description="used when analysis to pandas df is needed",
        ),
    ]

    prompt = base_prompt.partial(instructions="")
    grand_agent = create_react_agent(
        prompt=prompt, llm=ChatOpenAI(temperature=0, model="gpt-4-turbo"), tools=tools
    )
    grand_agent_executor = AgentExecutor(agent=grand_agent, tools=tools, verbose=True)

    print(grand_agent_executor.invoke(input={"input": "Find a random number"}))


if __name__ == "__main__":
    main()
