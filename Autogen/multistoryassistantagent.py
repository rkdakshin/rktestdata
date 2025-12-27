from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-4',api_key=api_key)
    #story_agent = AssistantAgent(name = "my_assistant", model_client=model_client, description="A friendly assistant that tells story about a cat and a dog.", system_message="You are a story teller that tells story about a cat and a dog.")
    
    situation_agent = AssistantAgent(name = "situation_writer", model_client=model_client, description="A friendly assistant that is situation writer.", system_message="You create engaging situation for stories, focus on situation.")

    character_agent = AssistantAgent(name = "character_writer", model_client=model_client, description="A friendly assistant that is charater writer.", system_message="You are a charater writer , create interesting charater for the story.")

    ending_agent = AssistantAgent(name = "ending_writer", model_client=model_client, description="A friendly assistant that is ending writer.", system_message="You are a engaging ending writer, conclude the story with a twist")
    
    team = RoundRobinGroupChat(
        [situation_agent, character_agent, ending_agent],
        max_turns=3
    )
    
    await Console(team.run_stream(task="Write a story about a cat and dog"))
    #await team.reset() to rest the stateful details while each turns
    #async for message in team.run_stream(task="Write a story about a cat and dog"):
    #    if isinstance(message, TaskResult):
     #       print(message.stop_reason)
     #   else:
     #       print( message)


    #    print(message.content)
    #task = TextMessage(role="user", content="Tell a Story about a cat and a dog",source="User")
    #result = await team.run(task=task)
    #print(result.messages[-1].content)

asyncio.run(main())