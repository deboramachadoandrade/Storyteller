# story_generator.py

import os
import openai
from openai import OpenAI
from getpass import getpass

openai.api_key = getpass("Please provide your OpenAI Key: ")
os.environ["OPENAI_API_KEY"] = openai.api_key

client = OpenAI() 

def generate_story_from_info(user_info):
    #generate a story from the user_input json:

    formatted_info = ", ".join([f"{key}: {value}" for key, value in user_info.items()])

    response = client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please create a story based on the following information: {formatted_info}. Your audience comprises 7-10 year-old children, so please avoid fancy words and try to make the story interesting for your audience specifically. Your audience can understand all languages used in the story already, no need to translate any word. Let's start writing the story..."},
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

user_info = {
    "summary": "Rebecca hears her mom, an AI engineer, discussing Retrieval Augmented-Generation, which sparks her interest. She attempts to understand it through conversations with her dad and teacher before explaining it to her sisters. Finally, she goes to her mom to confirm her understanding.",
    "characters": "The characters are Rebecca, a 7 year old cheeky girl. Rebecca's dad, a 38 year-old German man. Rebecca's mom is a 39 year-old Brazilian lady. Rebecca's twin sisters, Antonia and Cecilia, are 2-year old identical twins. They are very sweet.",
    "setting": "The story happens in present day, primarily at Rebecca's home and her school in London.",
    "educational_topic": "It brings out the concept of information retrieval, which is commonplace in today's world (e.g., Google), as well as aritificial intelligence.",
    "language": "The narrator will use English to tell the story, but if there are conversations between Rebecca and her mom, they should happen in Brazilian Portuguese. Rebecca and her dad speak German to each other. Rebecca speaks English at school. She speaks Brazilian Portuguese or German to the twins."
    # Add other relevant info here
}


story = generate_story_from_info(user_info)

print(story)




def generate_user_info_json(conversation_history):
# transforms the raw conversation history into a summary json
    
    response = client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{conversation_history}. - Summarize the main characteristics of the intended story as discussed in the previous conversation. Your output must be a json that incorporates the following as keys: plot, characters, setting, educational_topic, language, special_observations"},
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