---
title: Nole
emoji: 📊
colorFrom: pink
colorTo: red
sdk: docker
pinned: false
license: openrail
---
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


# Nólë Storyteller 
**by Débora Andrade, 28.03.2024**

Welcome to Nólë Storyteller, I hope you have fun building great stories!

Nólë is a tool that leverages GPT-4, Dall-e-3, LangChain and Chainlit to allow you to build on-demand educational stories for children in any language. 

# Requirements 

The first thing to do in order to run this code is **pip install -r requirements.txt**

Once requirements are installed, you will need to create an .env file containing your OpenAI API key: (OPENAI_API_KEY=sk-###)

Then, run the app in Chainlit and off you go create your first story: **chainlit run app.py -w**

Just a friendly heads up, if you run the code as it is, each short story accompanied by images will cost you roughly just below $2 in API calls to OpenAI. This cost can be greatly reduced especially by producing less images. The current implementation generates one image per paragraph + title, and that usually amounts to 12 images. 

# How to interact with the chatbot

The chatbot will ask you which story you would like to build today. You are expected to discuss your ideas regarding a theme for your book, an overall narrative, characters and their characteristics, the educational topic you would like to be featured as a backdrop, etc. If you have concrete ideas, please be as specific as you can. You don't need to have all these details clear in your mind, it is perfectly fine to delegate several aspects of the narrative to the tool itself. If you think you said all you wanted for the story and the chatbot keeps asking for more details, simply say that you will leave all other details up to its creativity. 

In the current implementation, you will be expected to provide a link to a pdf containing in-depth knowledge about the educational topic you would like to cover. Sending this link can either come from your initiative or it will be prompted by the tool in due time during the conversation. 

When the storyteller assistant decides that they have all relevant information, you will be asked to provide your email address. This was constructed this way so that the final package containing the story and images can be sent later on to the user by email. 

# Package output

Once you enter an email address, the workflows of information retrieval, story and image generation will be triggered (this will take roughly 2 min to be completed). Expect the story to be created as a docx file and saved in your local directory, as well as the images to be saved there as png files. Image files are named according to the time they were created, and they will be created in order of appearance in the story, each image corresponding to title and each subsequent paragraph.

# About the images
The default style of images is currently "van Gogh - like". I thought images rendered like this were fun but certainly taste is a personal thing. Dall-e-3 naturally doesn't have pre-defined image styles, it is up to the user to define it. In image_module2.py, please find the part related to style within the prompt, and change according to your preference. I do not recommend changing the settings to have Dall-e-2 as image generator. Although cheaper, it is not worth it, unless you are interested in abstract images.

# Languages
You are completely free to choose your language of preference for the story, and it is also possible to have the story written in more than one language. Just specify all these details when you chat with the tool. Likewise, the pdf whose link you refer to in the chat doesn't have to be in English. It will work just as well in all broadly spoken languages. It is also possible, for example, to write a story in English and provide the document reference in another language. This is spcially useful when the topic of interest is related to the history of non English-speaking countries, where most of the specialized material was written in the local language.

# Have fun! :)
