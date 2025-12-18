from langchain_openai import ChatOpenAI
import os

llm_url="http://10.186.172.59:1234/v1"
llm=ChatOpenAI(
    base_url=llm_url,
    model="google/gemma-3-4b",
    api_key="dummy-key"
)

user_input=input("YOU:")

result=llm.stream(user_input)
for chunk in result:
    print(chunk.content,end="")