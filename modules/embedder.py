import os
import pickle
import tempfile
import uuid
import streamlit as st
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

class Embedder:

    def __init__(self):
        self.PATH = "embeddings"
        self.createEmbeddingsDir()

    def createEmbeddingsDir(self):
        """
        Creates a directory to store the embeddings vectors
        """
        if not os.path.exists(self.PATH):
            os.mkdir(self.PATH)

    def createDocVectors(self, file, original_filename, json_data):
        """
        Stores document embeddings using Langchain and FAISS
        """
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file:
            tmp_file.write(file)
            tmp_file_path = tmp_file.name

        # Read PDF file and extract text
        reader = PdfReader(tmp_file_path)
        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text
        
        # We need to split the text that we read into smaller chunks so that during information retrieval we don't hit the token size limits. 
        text_splitter = CharacterTextSplitter(        
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        data1 = text_splitter.split_text(raw_text)
        data2 = text_splitter.split_text(json_data)

        documents = []
        documents.extend(data1)
        documents.extend(data2)

        # Download embeddings from OpenAI
        embeddings = OpenAIEmbeddings()

        vectors = FAISS.from_texts(documents, embeddings)
        os.remove(tmp_file_path)

        # Generate a GUID for the filename
        filename = str(uuid.uuid4())
        
        # Save the vectors to a pickle file
        with open(f"{self.PATH}/{original_filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)
        
        return vectors

    def createDocVectorsFromJSON(self, json_data):
        """
        Stores document embeddings using Langchain and FAISS
        """

        # We need to split the text that we read into smaller chunks so that during information retrieval we don't hit the token size limits. 
        text_splitter = CharacterTextSplitter(        
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        data = text_splitter.split_text(json_data)

        # Download embeddings from OpenAI
        embeddings = OpenAIEmbeddings()

        vectors = FAISS.from_texts(data, embeddings)
        
        # Generate a GUID for the filename
        filename = str(uuid.uuid4())
        # Save the vectors to a pickle file

        with open(f"{self.PATH}/{filename}.pkl", "wb") as f:
            pickle.dump(vectors, f)

        return filename


    def getDocEmbeds(self, file, original_filename, json_data):
        """
        Retrieves document embeddings
        """
        vectors = self.createDocVectors(file, original_filename, json_data)       
        return vectors
    
    def getJsonEmbeds(self, jsondata):
        """
        Retrieves document embeddings
        """
        filename = self.createDocVectorsFromJSON(jsondata)   
        # Load the vectors from the pickle file
        with open(f"{self.PATH}/{filename}.pkl", "rb") as f:
            vectors = pickle.load(f)

        return vectors