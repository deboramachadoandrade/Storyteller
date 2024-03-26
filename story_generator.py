# story_generator.py
import os
import openai
from openai import AsyncOpenAI
from getpass import getpass

#openai.api_key = getpass("Please provide your OpenAI Key: ")
#os.environ["OPENAI_API_KEY"] = openai.api_key
#client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def generate_story_from_info(client, user_info_json):
    #generates a story from the user_input json:
    
    # Convert user_info_json from string to dictionary
    import json
    user_info = json.loads(user_info_json)
    
    formatted_info = ", ".join([f"{key}: {value}" for key, value in user_info.items()])
    
    response = await client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please create a story based on the following information: {formatted_info}. Ignore the keys pdf, email and physical_appearance. Your audience comprises 7-10 year-old children, so please avoid fancy words and try to make the story interesting for your audience specifically. Your audience can understand all languages used in the story already, no need to translate any word. Let's start writing the story..."},
        ],
        temperature=1.1,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    #print(response.choices[0].message.content)

    
    # The response includes several pieces; the 'choices' list contains the generated texts
    story = response.choices[0].message.content
    
    return story

# Example usage



user_info1 = {
"plot": "The story revolves around a day in the life of Rebecca, a 7-year-old girl who becomes interested in the concept of Retrieval Augmented-Generation (RAG) after hearing her mom talk about it. She discusses it with her dad, who doesn't know much about it, and later asks her teacher about it. After learning about it, she explains it to her younger twin sisters, Cecilia and Antonia.",
"characters": {
    "Rebecca": "A cheeky, smiley 7-year-old girl with long flat brown hair. She likes to wear dresses combined with colourful leggings.",
    "Dad": "A 38-year-old red-haired German who enjoys teaching Rebecca new things.",
    "Mom": "A 39-year-old brunette Brazilian who works with AI.",
    "Cecilia and Antonia": "Adorable and sweet blond toddlers who are very curious.",
    "Teacher": "Details about the teacher's personality and teaching style are left to the writer's imagination."
},
"setting": "The story is set in London, where Rebecca lives. The conversations between the characters happen in different languages: Rebecca speaks German with her dad, Brazilian Portuguese with her mom, and English with her teacher.",
"educational_topic": "The story aims to explain the concept of Retrieval Augmented-Generation (RAG), a form of information retrieval system that leverages AI, in a way that is understandable to children.",
"language": "The story is primarily in English, but incorporates German and Brazilian Portuguese in the dialogues between Rebecca and her parents.",
"special_observations": "The story does not aim to convey a specific message, but rather to depict a day in Rebecca's life and her curiosity about RAG. The concept of RAG is explained as part of the story, not as a lesson."
}
#story = generate_story_from_info(user_info1)

#print(story)




async def generate_user_info_json(client, conversation_history):
# transforms the raw conversation history into a summary json
    
    response = await client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{conversation_history}. - Summarize the main characteristics of the intended story as discussed in the previous conversation. Your output must be a json that incorporates the following as keys: plot, characters_description, characters_physical_appearance, setting, educational_topic, language, pdf, email, special_observations"},
        ],
        temperature=0.1,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

   
    user_info_json = response.choices[0].message.content

    return user_info_json





def check_for_email(message):
    import re

    # Define email pattern in order to trigger story generation at the end of the chat:
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    if re.search(email_pattern, message):
        return True
    else:
        return False