import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback

#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
langchain.verbose = False

class Chatbot:

    def __init__(self, model_name, temperature, vectors):
        self.model_name = model_name
        self.temperature = temperature
        self.vectors = vectors

    qa_template = """
    You help users with job search using their resume. Please use this resume and context to 
    answer the question at the end. Additionally, please provide information on relevant job 
    opportunities based on the user's resume. Instead of providing lengthy explanations, 
    try to summarize or paraphrase. Break down long messages and prioritize important 
    information. If you don't know the answer, simply state that you don't know. 
    When responding, please provide as much detail as possible. Along with your answer, 
    display relevant job details that match the user's resume.

    Context:
    {context}
    ==========
    Question:
    {question}
    ==========
    """


    QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

    def conversational_chat(self, query):
        """
        Start a conversational chat with a model via Langchain
        """
        llm = ChatOpenAI(model_name=self.model_name, temperature=self.temperature)

        retriever = self.vectors.as_retriever()

        chain = ConversationalRetrievalChain.from_llm(llm=llm,
            retriever=retriever, verbose=True, return_source_documents=True, combine_docs_chain_kwargs={'prompt': self.QA_PROMPT})

        chain_input = {"question": query, "chat_history": st.session_state["history"]}
        result = chain(chain_input)

        st.session_state["history"].append((query, result["answer"]))
        return result["answer"]