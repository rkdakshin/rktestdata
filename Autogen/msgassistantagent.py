from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
#from autogen_core import Image as AGimage

#from PIL import Image
#from io import BytesIO
import requests

from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model_client = OpenAIChatCompletionClient(model='gpt-4o',api_key=api_key)
assistant = AssistantAgent(name = "my_assistant", model_client=model_client, description="A friendly assistant to image details.", system_message="You are a helpful assistant ,analyse the image and answer the question.")


async def multi_model_task():
   # response = requests.get("https://picsum.photos/id/237/200/300")
   # image = Image.open(BytesIO(response.content))
   # ag_image = AGimage (image)

    message = TextMessage(
        source="user",
        content="""
Describe this image:

![image](https://picsum.photos/id/237/200/300)
"""
    )

    result = await assistant.run(task=message)
    print(result.messages[-1].content)

asyncio.run(multi_model_task())