

async def download_image(session, url, filename):
    from PIL import Image
    from io import BytesIO
    async with session.get(url) as response:
        if response.status == 200:
            content = await response.read()
            image = Image.open(BytesIO(content))
            image.save(filename)
            print(f"{filename} was saved")
        else:
            print(f"Failed to download image from {url}. Status: {response.status}")


async def generate_image(client, paragraph, characters_appearance, summary):
    #generates an image given a prompt and a client

    import asyncio
    from io import BytesIO
    import openai
    from datetime import datetime
    import base64
    from PIL import Image
    from aiohttp import ClientSession
    from openai import AsyncOpenAI 

    client = AsyncOpenAI()  # Async client for OpenAI

    prompt = ("Subject: " + paragraph + ". Description of characters: (you should only look up characters cited in Subject): " 
              + str(characters_appearance) 
              + ". If it is not clear which characters are being referred to in the Subject, put the Subject in the context of the whole story to figure that out. The story is the following: " 
              + summary + " Style: Picasso -like. The images should not contain any letters or numbers.")

    image_params = {
        "model": "dall-e-3",
        "n": 1,
        "size": "1024x1024",
        "prompt": prompt,
        "user": "Deb",
        "response_format": "b64_json"
    }

    try:
        images_response = await client.images.generate(**image_params)
        images_dt = datetime.utcfromtimestamp(images_response.created)
        img_filename = images_dt.strftime('DALLE-%Y%m%d_%H%M%S')

        image_data_list = [image.model_dump()["b64_json"] for image in images_response.data]

        async with ClientSession() as session:
            tasks = []
            for i, data in enumerate(image_data_list):
                filename = f"{img_filename}_{i}.png"
                if data:  # Assuming `data` is base64 encoded image data
                    Image.open(BytesIO(base64.b64decode(data))).save(filename)
                    print(f"{filename} was saved")
                else:
                    # Assuming URL fallback which is not in the original code but added for completeness
                    url = images_response.data[i].url
                    tasks.append(download_image(session, url, filename))
                    image = download_image(session, url, filename)
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return filename

# Run the async main
#if __name__ == "__main__":
#    asyncio.run(main_async())

