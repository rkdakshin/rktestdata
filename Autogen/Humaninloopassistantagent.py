from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def user_input(prompt: str) -> str:
    text = input(prompt)
    if text.lower() in ["exit", "quit"]:
        raise KeyboardInterrupt
    return text

async def main():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=api_key
    )

    add_1_agent_first = AssistantAgent(
        name="add_1_agent_first",
        model_client=model_client,
        system_message="Add 1 to the number. First number is 0. Give result as output."
    )

    add_1_agent_second = AssistantAgent(
        name="add_1_agent_second",
        model_client=model_client,
        system_message="Add 1 to the output. Give result as output."
    )

    add_1_agent_third = AssistantAgent(
        name="add_1_agent_third",
        model_client=model_client,
        system_message="Add 1 to the output. Give result as output."
    )

    # 👤 Human-in-the-loop agent
    user_proxy_agent = UserProxyAgent(
        name="user",
        description="Human user providing input",
        input_func=user_input
    )

    team = RoundRobinGroupChat(
        participants=[
            user_proxy_agent,
            add_1_agent_first,
            add_1_agent_second,
            add_1_agent_third
        ],
        max_turns=10
    )

    await Console(team.run_stream())
 

asyncio.run(main())
