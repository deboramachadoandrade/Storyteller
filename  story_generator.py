# story_generator.py

import os
import openai
from openai import OpenAI
from getpass import getpass

openai.api_key = getpass("Please provide your OpenAI Key: ")
os.environ["OPENAI_API_KEY"] = openai.api_key

client = OpenAI() 

def generate_story_from_info(user_info):
    # Construct a prompt from the gathered information
    
    prompt = f"Now, based on the collected information: {user_info}. Let's start writing the story..."

    response = client.chat.completions.create( 
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Please create a story based on the following information: {user_info}. Let's start writing the story..."},
        ]
        prompt=prompt,
        temperature=1.0,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    print(response.choices[0].message['content'])

    
    # The response includes several pieces; the 'choices' list contains the generated texts
    story = response.choices[0].message['content']
    return story

# Example usage

user_info = {
    "summary": "Rebecca hears her mom, an AI engineer, discussing Retrieval Augmented-Generation, which sparks her interest. She attempts to understand it through conversations with her dad and teacher before explaining it to her sisters. Finally, she goes to her mom to confirm her understanding.",
    "characters": "The characters are Rebecca, a 7 year old cheeky girl with long flat brown her who likes to wear colourful clothes. Rebecca's dad, a 38 year-old German man with light brown hair and a red trimmed beard. Rebecca's mom is a 39 year-old Brazilian brunete lady. Rebecca's twin sisters, Antonia and Cecilia, are 2-year old identical twins. They are blond, very sweet, and they usually wear striped dungarees.",
    "setting": "The story happens in present day, primarily at Rebecca's home and her school in London.",
    "educational_topic": "It brings out the concept of information retrieval, which is commonplace in today's world (e.g., Google), as well as aritificial intelligence.",
    "language": "The narrator will use English to tell the story, but if there are conversations between Rebecca and her mom, they should happen in Brazilian Portuguese. Rebecca and her dad speak German to each other. Rebecca speaks English at school. She speaks Brazilian Portuguese or German to the twins."
    # Add other relevant info here
}

# Assuming you format `user_info` into a string or another structure suitable for your prompt
formatted_info = ", ".join([f"{key}: {value}" for key, value in user_info.items()])
story = generate_story_from_info(formatted_info)

print(story)