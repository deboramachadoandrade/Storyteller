

async def process_text_for_image_prompts(client, text):
    #Splits the text into paragraphs and rewrites each for image prompt generation.
    import openai
    import asyncio

    # Split the text by two newline characters to separate paragraphs
    paragraphs = text.split('\n\n')
    
    # Initialize a list to store rewritten paragraphs
    rewritten_paragraphs = []
    
    # Rewrite each paragraph
    for paragraph in paragraphs:
        paragraph = paragraph.strip()  # Clean up whitespace
        if paragraph:  # Ensure paragraph is not empty
            try:
                response = await client.chat.completions.create( 
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"Describe one character featured in the paragraph below. Your description should consist of only one sentence and focus on one character performing one action, and not on abstract ideas. Example of a concrete scene description : Arabella, a beautiful brunette dressing a colourful dress, buys oranges in the market on a beutiful sunny day. If there is not enough information to describe a character in their setting, feel free to be creative.\n\n{paragraph}"},
                    ],
                    temperature=0.7,
                    max_tokens=150,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                )
                
                rewritten_paragraph = response.choices[0].message.content
                #rewritten_paragraph = rewritten_paragraph.text.strip()
                rewritten_paragraphs.append(rewritten_paragraph)
                 
            except Exception as e:
                print(f"An error occurred while processing paragraph: {e}")
                # Optionally, append the original paragraph or a placeholder
                rewritten_paragraphs.append(paragraph)
    
    return rewritten_paragraphs

#async def main():
#    original_text = """Once upon a time there lived a family by the name of Hoskin. They were nobles of a lower rank, settled in a picturesque corner of medieval England, peacefully spending their days in modest grandeur. The intellectual patriarch, James, a short but handsome brunet ruled with a loving hand; Catherine, his beautiful wife, embodied the graceful spirit of art. Their children, Mary, an impulsive red-haired maiden, Ann, a friendly, short, blond who loves art, and the youngest, William - a brunet like his father who was outgoing, inquisitive and clever as a fox. 

#Their peaceful kingdom shifted under their feet when the tides of time ushered in an era that would change everything - the Norman conquest of 1066. The new rulers, the Normans, arrived with their strong traditions and strange language. They sprinkled the plain language of England with the pepper of French vocabulary - words like "jury" and "squire", filling the air with an unfamiliar melody as the new rulers tried to integrate themselves with the locals."""

    rewritten_paragraphs = await process_text_for_image_prompts(client, original_text)
    for paragraph in rewritten_paragraphs:
        print(paragraph)
        print("------")

# Run the main async function
#if __name__ == "__main__":
#    asyncio.run(main())