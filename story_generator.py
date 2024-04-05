# story_generator.py
import os
import openai
from openai import AsyncOpenAI
from getpass import getpass

#openai.api_key = getpass("Please provide your OpenAI Key: ")
#os.environ["OPENAI_API_KEY"] = openai.api_key
#client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


async def generate_story_from_info(client, user_info, information):
    #generates a story from the user_input dictionary:
    
    
    formatted_info = ", ".join([f"{key}: {value}" for key, value in user_info.items()])
    
    response = await client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please create a story for 7-10 year-old children that incorporates the following knowledge: {information} into the following story plan: {formatted_info}. Ignore the keys pdf and email. Please avoid fancy words and try to make the narrative interesting for your audience specifically. Assume your audience can understand all languages used in the story. Don't forget to add a title at the beginning of the story. Let's start writing the story..."},
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

async def generate_summary_from_story(client, story):
    #generates a story from the user_input dictionary:
    
    
    response = await client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the following story in one sentence: " + story},
        ],
        temperature=1.1,
        max_tokens=500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    
    # The response includes several pieces; the 'choices' list contains the generated texts
    summary = response.choices[0].message.content
    
    return summary

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
            {"role": "user", "content": f"{conversation_history}. - Summarize the main characteristics of the intended story as discussed in the previous conversation. Your output must be a json that incorporates the following as keys: plot, characters_description, characters_physical_appearance, setting, educational_topic, search_topic, language, pdf, email, special_observations. The search_topic can be seen as the essence of educational_topic, exactly what the search assistant will search to bring specialized information to the writer who will write the story. Examples of search_topic: influence of the Norman conquest on the English language, quantum mechanics, origin of vulcanos, invention of agriculture, prime numbers, history of first Portuguese settlements in Northeastern Brazil, etc etc. The search_topic should have only one entry. Pay special attention to the plot and make sure to include requests made by the user or your own observations in the key special_observations"},
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