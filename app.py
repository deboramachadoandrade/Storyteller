# Final project: Nólë 
#by Débora Machado Andrade

#Nólë means "knowledge" in Quenya, a fictional Elvish language created by J.R.R.Tolkien 

#In the following notebook we'll build RAG and agentic pipelines that will allow us to interactively 
#retrieve information from our knowledge sources, as well as construct the building blocks of a narrative 
#story-telling book for children, where the chosen knowledge will be embedded. 

import os
import openai
from openai import AsyncOpenAI  # importing openai for API usage
import chainlit as cl  # importing chainlit for our app
#from chainlit.prompt import Prompt, PromptMessage  # importing prompt tools
from chainlit.prompt import Prompt, PromptMessage 
from chainlit.playground.providers import ChatOpenAI  # importing ChatOpenAI tools



from getpass import getpass

openai.api_key = getpass("Please provide your OpenAI Key: ")
os.environ["OPENAI_API_KEY"] = openai.api_key



#Loading data
from langchain_community.document_loaders import PyMuPDFLoader

loader = PyMuPDFLoader(
    "data/Tratado_Descritivo_Brasil_1587.pdf",
)

documents = loader.load()

#Splitting data
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap = 100
)

documents = text_splitter.split_documents(documents)

#Loading OpenAI embeddings model:
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

#Creating a FAISS VectorStore:
from langchain_community.vectorstores import FAISS

vector_store = FAISS.from_documents(documents, embeddings)

#Creating a retriever:
retriever = vector_store.as_retriever()

#Creating a prompt template:
from langchain.prompts import ChatPromptTemplate

template = """Answer the question based only on the following context. If you cannot answer the question with the context, please respond with 'I don't know':

Context:
{context}

Question:
{question}
"""

prompt = ChatPromptTemplate.from_template(template)

#Creating a RAG chain:
from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

primary_qa_llm = ChatOpenAI(model_name="gpt-4", temperature=0)

retrieval_augmented_qa_chain = (
    # INVOKE CHAIN WITH: {"question" : "<<SOME USER QUESTION>>"}
    # "question" : populated by getting the value of the "question" key
    # "context"  : populated by getting the value of the "question" key and chaining it into the base_retriever
    {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
    # "context"  : is assigned to a RunnablePassthrough object (will not be called or considered in the next step)
    #              by getting the value of the "context" key from the previous step
    | RunnablePassthrough.assign(context=itemgetter("context"))
    # "response" : the "context" and "question" values are used to format our prompt object and then piped
    #              into the LLM and stored in a key called "response"
    # "context"  : populated by getting the value of the "context" key from the previous step
    | {"response": prompt | primary_qa_llm, "context": itemgetter("context")}
)

#We will be using the advanced Multiquery retriever provided by Langchain:
from langchain.retrievers import MultiQueryRetriever
advanced_retriever = MultiQueryRetriever.from_llm(retriever=retriever, llm=primary_qa_llm)

#We create a chain to stuff our documents into our prompt:
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub

retrieval_qa_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
document_chain = create_stuff_documents_chain(primary_qa_llm, retrieval_qa_prompt)

#Create the new retrieval chain with advanced retriever:
from langchain.chains import create_retrieval_chain
retrieval_chain = create_retrieval_chain(advanced_retriever, document_chain)

#And we create our chatbot functions:
user_template = """{input}
Think through your response step by step.
"""
@cl.on_chat_start  # marks a function that will be executed at the start of a user session
async def start_chat():
    settings = {
        "model": "gpt-3.5-turbo",
        #"model": "gpt-4",
        "temperature": 1.0,
        "max_tokens": 500,
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
        #provider=ChatOpenAI.id,
        provider="ChatOpenAI",
        messages=[
            PromptMessage(
                role="system",
                template=template,
                formatted=template,
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
    #async for stream_resp in await client.chat.completions.create(
    #    messages=[m.to_openai() for m in prompt.messages], stream=True, **settings
    #):
        
    #    token = stream_resp.choices[0].delta.content
    #    if not token:
    #        token = ""
    #    await msg.stream_token(token)

    # Update the prompt object with the completion
    result = retrieval_chain.invoke({"input":message.content})
    msg.content = result["answer"]
    #print(temp)
    #prompt.completion = msg.content
    #prompt.completion = temp
    #msg.content = temp
    

    #prompt.completion = completion
    msg.prompt = prompt

    # Send and close the message stream
    await msg.send()
    
     

