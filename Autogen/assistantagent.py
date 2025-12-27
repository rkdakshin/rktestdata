from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-4',api_key=api_key)
    assistant = AssistantAgent(name = "my_assistant", model_client=model_client, description="A friendly assistant that tells joke.", system_message="You are a helpful assistant that tells jokes.")
    result = await assistant.run(task="Tell me a joke..")
    print(result.messages[-1].content)

asyncio.run(main())