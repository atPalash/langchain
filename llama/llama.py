from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage


llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    # other params...
)
messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Hindi. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)
