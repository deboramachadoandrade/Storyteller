# You can find this code for Chainlit python streaming here (https://docs.chainlit.io/concepts/streaming/python)

# OpenAI Chat completion

import os
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools
from story_generator import generate_story_from_info, generate_user_info_json, check_for_email
from dotenv import load_dotenv




load_dotenv()

# ChatOpenAI Templates
system_template = """You are a helpful children's book writer assistant. 
"""

user_template = """You are a helpful children's book writer assistant. You will help producing short stories for children, like children's books narratives. 
The user might be an educator or a parent. 
Whoever the user might be, the final product, which is a short story, is always focused on children aged 5-8 years old. 

In order to write the story, you will first have a conversation with the user to understand what they are interested in writing. 
If requested to generate a story that should have an educational topic embedded in the background, you should request references in the form of pdf documents or links. 
You will proactively ask questions, in a conversational fashion. 
You will only ask one question at a time. Your follow-up questions will depend on the user feedback. 
In the first part of your task, your aim is to end up with a clear idea of the following:

1) Main message the story should convey
2) All main characters, their personalities, their physical appearance (if applicable), their personal story (if applicable)
3) Where and when the story happens
4) Why this story is interesting. What can you do to make it even more interesting.
6) How can you choose and ending that is either clever or witty or educative or funny.

When and only when you gather all the information you need, (unless the user lets you know that they are leaving certain aspects of the story up to you), 
ask the user the following question exactly: 

"Can you please provide a link to a pdf file that provides the educational content to be added to the story?"

After you get a response, ask the following question exactly:

"Can you please provide your email address?"

After the user enters their email address, comes the second part of your task, which is very important: write a comprehensive summary of all the information you gathered from the user (except for their email address and link to pdf). 
{input}. 
"""


@cl.on_chat_start  # marks a function that will be executed at the start of a user session

async def start_chat():
    settings = {
        "model": "gpt-4",
        "temperature": 1.0,
        "max_tokens": 1500,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }

    cl.user_session.set("settings", settings)
    cl.user_session.set("conversation_history", [])  # Initialize empty conversation history

@cl.on_message
async def main(message: cl.Message):
    settings = cl.user_session.get("settings")
    conversation_history = cl.user_session.get("conversation_history")

    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Append the new user message to the conversation history
    conversation_history.append({"role": "user", "content": message.content})

    # Constructing a dynamic prompt using the conversation history
    dynamic_messages = []
    for msg in conversation_history:
        if msg["role"] == "system":
            dynamic_messages.append(PromptMessage(role="system", template=system_template, formatted=system_template))
        else:
            dynamic_messages.append(PromptMessage(role="user", template=user_template, formatted=user_template.format(input=msg["content"])))

    dynamic_prompt = Prompt(
        provider=ChatOpenAI.id,
        messages=dynamic_messages,
        inputs={"input": message.content},
        settings=settings,
    )

    #print("Sending to OpenAI:", [m.to_openai() for m in dynamic_prompt.messages])

    msg = cl.Message(content="")

    #final_prompt = "\n".join([m.formatted for m in dynamic_messages])
    #print("Final prompt being sent to GPT-4:", final_prompt)

    # Call OpenAI with the dynamic prompt
    async for stream_resp in await client.chat.completions.create(
        messages=[m.to_openai() for m in dynamic_prompt.messages], stream=True, **settings
    ):
        token = stream_resp.choices[0].delta.content
        if not token:
            token = ""
        await msg.stream_token(token)

    # Update the prompt object with the completion and add it to the conversation history
    dynamic_prompt.completion = msg.content
    conversation_history.append({"role": "system", "content": msg.content})
    
    # Save the updated conversation history back to the session
    cl.user_session.set("conversation_history", conversation_history)

    msg.prompt = dynamic_prompt

    print(conversation_history)

    # Send and close the message stream
    await msg.send()


#async def main(message: cl.Message):
#    settings = cl.user_session.get("settings")

#    client = AsyncOpenAI(
#    api_key=os.environ.get("OPENAI_API_KEY"),
#)

#    print(message.content)

#    prompt = Prompt(
#        provider=ChatOpenAI.id,
#        messages=[
#            PromptMessage(
#                role="system",
#                template=system_template,
#                formatted=system_template,
#            ),
#            PromptMessage(
#                role="user",
#                template=user_template,
#                formatted=user_template.format(input=message.content),
#            ),
#        ],
#        inputs={"input": message.content},
#        settings=settings,
#    )

#    print([m.to_openai() for m in prompt.messages])

#    msg = cl.Message(content="")

    # Call OpenAI
#    async for stream_resp in await client.chat.completions.create(
#        messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
#    ):
#        token = stream_resp.choices[0].delta.content
 #       if not token:
 #           token = ""
 #       await msg.stream_token(token)

    # Update the prompt object with the completion
 #   prompt.completion = msg.content
 #   msg.prompt = prompt

    # Send and close the message stream
 #   await msg.send()
