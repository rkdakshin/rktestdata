from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import MaxMessageTermination
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

async def main():
    model_client = OpenAIChatCompletionClient(model='gpt-4',api_key=api_key)
    #story_agent = AssistantAgent(name = "my_assistant", model_client=model_client, description="A friendly assistant that tells story about a cat and a dog.", system_message="You are a story teller that tells story about a cat and a dog.")
    
    add_1_agent_first = AssistantAgent(name = "add_1_agent_first", model_client=model_client, description="Add one to the number.", system_message="Add 1 to the number. First number is 0. Give result as output")

    add_1_agent_second = AssistantAgent(name = "add_1_agent_second", model_client=model_client, description="Add one to the number.", system_message="Add 1 to the number. Give result as output")

    add_1_agent_third = AssistantAgent(name = "add_1_agent_third", model_client=model_client, description="Add one to the number.", system_message="Add 1 to the number. Give result as output")
    
    termination = MaxMessageTermination(5)

    team = RoundRobinGroupChat(
        [add_1_agent_first, add_1_agent_second, add_1_agent_third],
       # max_turns=3
       termination_condition=termination
    )
    
    #await Console(team.run_stream(task="First number is 0"))
    #await team.reset()
    await Console(team.run_stream())
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