# Here we take care of searching the research topics to be included in our story



async def RAG_search(pdf, search_topic):

    import httpx
    import requests

    # URL of the PDF file
    pdf_url = pdf

    async with httpx.AsyncClient() as client:
        # Send a GET request to the URL
        response = await client.get(pdf)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            with open('knowledge_file.pdf', 'wb') as file:
                file.write(response.content)
            print("PDF downloaded and saved successfully.")
        else:
            print("Failed to retrieve the PDF. Status code:", response.status_code)
            return "Failed to retrieve PDF."

    # Send a GET request to the URL
    #response = requests.get(pdf_url)

    # Check if the request was successful (status code 200)
    #if response.status_code == 200:
        # Open a binary file in write mode, write the content, and save it
    #    with open('knowledge_file.pdf', 'wb') as file:
    #        file.write(response.content)
    #    print("PDF downloaded and saved successfully.")
    #else:
    #    print("Failed to retrieve the PDF. Status code:", response.status_code)
        #Loading data
 
 
    from langchain_community.document_loaders import PyMuPDFLoader

    loader = PyMuPDFLoader(
        "knowledge_file.pdf",
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

    primary_qa_llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

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


    information = retrieval_chain.invoke({"input": "Explain " + search_topic + " in detail."})
    
    print(information["answer"]) 
    return information["answer"]
    