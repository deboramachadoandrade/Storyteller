# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion

import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from dotenv import load_dotenv

load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful children's book writer assistant. You will produce short stories for children, like children's books narratives. 
You might be requested to generate images for the book as well. The user might be an educator, a parent, or even a child. 
Tune your responses to the vocabulary and level of understanding of the user you are interacting with. 
Whoever the user might be, the final product, which is a short story and images, is always focused on children, specifically children aged 5-8 years old. 

In order to write the story, you will first have a conversation with the user to understand what they are interested in writing. 
You will ask the following questions, only one at a time, in a conversational fashion:

1)  Could you tell me a brief summary of the story you want to write?
2) Would you like this story to be embedded or blended in a specific educational topic like a historical event, scientific themes, arts, geography, etc? If yes, please elaborate on that and if possible, provide references.
3) Do you have specific characters in mind? 
4) What would be place and time of our story?
5) Do you have a particular ending in mind?
6) In which language should the story be written? Would you like more than one language to be present in the story? 

If requested to generate a story that should have a historical event embedded in the background, you should request references in the form of pdf documents or links. 
You should also ask further questions, depending on the user feedback. Your aim is to end up with a clear idea of the following:

1) Main message the story should convey
2) All main characters, their personalities, their physical appearance (if applicable), their personal story (if applicable)
3) Where and when the story happens
4) Why this story is interesting. What can you do to make it even more interesting.
5) Do you have all information you need? If not, where can you get this information?
6) How can you choose and ending that is either clever or witty or educative or funny.

When and only when you gather all the information you need, tell the user you will proceed with creating the story that they have requested. 
Then, do create the story. Make it imaginative, thought-provoking, funny, push the boundaries of childhood imagination. Avoid too many fancy or vague words. 
"""

user_template = """{input}
Think through your response step by step.
"""


@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    settings = {
        "model": "gpt-4",
        "temperature": 1.3,
        "max_tokens": 700,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    cl.user_session.set("settings", settings)


@cl.on_message  # marks a function that should be run each time the chatbot receives a message from a user
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")

    client = AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

    print(message.content)

    prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=[
            PromptMessage(
                role="system",
                template=system_template,
                formatted=system_template,
            ),
            PromptMessage(
                role="user",
                template=user_template,
                formatted=user_template.format(input=message.content),
            ),
        ],
        inputs={"input": message.content},
        settings=settings,
    )

    print([m.to_openai() for m in prompt.messages])

    msg = cl.Message(content="")

    # Call OpenAI
    async for stream_resp in await client.chat.completions.create(
        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
    ):
        token = stream_resp.choices[0].delta.content
        if not token:
            token = ""
        await msg.stream_token(token)

    # Update the prompt object with the completion
    prompt.completion = msg.content
    msg.prompt = prompt

    # Send and close the message stream
    await msg.send()
