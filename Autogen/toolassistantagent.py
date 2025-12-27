from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def get_weather(city:str) -> str:
    return f"weather in {city} is sunny with a high of 25degree celcius"

async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-4',api_key=api_key)
    assistant = AssistantAgent(name = "my_assistant", model_client=model_client, description="A friendly assistant to get weather details.", system_message="You are a weather assistant , use the get_weather tool to find weather in a city.", tools=[get_weather])
    text_message = TextMessage(content="what is the weather in Chennai",source="User")
    result = await assistant.run(task=text_message)
    print(result.messages[-1].content)

asyncio.run(main())