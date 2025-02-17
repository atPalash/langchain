from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()


@tool
def multiply(x: float, y: float) -> float:
    """Muliply two numbers

    Args:
        x (float): first
        y (float): second

    Returns:
        float: multiplication result
    """
    return x * y


def main():
    print("hello")
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "you are assistant"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    )

    tools = [TavilySearchResults(), multiply]
    llm = ChatOpenAI(model="gpt-4-turbo")
    agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    res = agent_executor.invoke(
        {
            "input": "What is the weather of helsinki and kolkata, then multiply the temperature"
        }
    )
    print(res)


if __name__ == "__main__":
    main()
