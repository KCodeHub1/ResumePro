import os
import pandas as pd
import streamlit as st
import requests
import json
import pdfplumber
from modules.chatbot import Chatbot
from modules.embedder import Embedder
import openai
from PyPDF2 import PdfReader
import tempfile
import pycountry
import re

class Utilities:
   
    @staticmethod
    def load_api_key():
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
        #you can define your API key in .env directly
        if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
            user_api_key = os.environ["OPENAI_API_KEY"]
            st.sidebar.success("API key loaded from .env", icon="🚀")
        else:
            if st.session_state.api_key is not None:
                user_api_key = st.session_state.api_key
                st.sidebar.success("API key loaded from previous input", icon="🚀")
            else:
                user_api_key = st.sidebar.text_input(
                    label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
                )
                if user_api_key:
                    st.session_state.api_key = user_api_key

        return user_api_key

    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["pdf"]
        """
        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
            
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)

            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
        else:
            st.session_state["reset_chat"] = True

        return uploaded_file

    @staticmethod
    def setup_chatbot(uploaded_file, model, temperature,apiKey):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()
        openai.api_key = apiKey
        uploaded_file.seek(0)
        file1 = uploaded_file.read()
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as tmp_file1:
            tmp_file1.write(file1)
            tmp_file_path1 = tmp_file1.name

        reader = PdfReader(tmp_file_path1)
        #jdataformat = {"applicant_name":"","applicant_email":"","applicant_phone":"","applicant_city":"","applicant_state":"","applicant_country":"","academicCredentials":[{"degree":"","major":"","university":"","college_location":"","year":""}],"projects":[{"name":"","languages":"","database":"","softwarePackages":""}],"Skills":{"languages":"","database":"","softwares":"","Technologies":""},"personalInformation":{"fatherName":"","motherName":"","dateOfBirth":"","gender":"","languagesKnown":"","maritalStatus":"","nationality":""}}
        jdataformat2 = {"JobTitle": "StringValue","CountryCode" :  "StringValue"}
        raw_text = ''
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                raw_text += text

        #question = json.dumps(raw_text) + 'analyse the above information and return countrycode and job_title of the user' 
        #question = 'extract relevant in the following json format and analyse and return just the json, do not use return any info that is not part of json structure provided' + json.dumps(jdataformat) + 'for below content' + json.dumps(raw_text)
        question = 'extract job_title and country of the user only for below data' + json.dumps(raw_text)       
        max_prompt_length = 2000
        prompt = question[:max_prompt_length]
        response_text = ""
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        response_text += response.choices[0].text

        job_title_match = re.search(r"Job Title: (.+)", response_text)
        if job_title_match:
            job_title = job_title_match.group(1)
        else:
            job_title = ""  # Handle case when job title is not found

        # Extract country
        country_match = re.search(r"Country: (.+)", response_text)
        if country_match:
            country = country_match.group(1)
        else:
            country = ""  # Handle case when country is not found
        res = pycountry.countries.get(name=country)
        if res is not None:
            country_code = res.alpha_2
        else:
            country_code = 'IN'
        # get jobs data
        API_URL = "https://jobsapi-wp.firebrickgroup.com/JavaStaggingApi/?keyword="+job_title+"&zipcode=&city_job=&state_job=&radius=75&start=0&offset=100&domain=&ipaddress=139.99.148.8&country="+country_code+"&exportPartner=JobRapido_AU_Dir&isCountryMismatch=False&skipMinCpcRule=False&similar_job=true"
        jobs_list = []
        response = requests.get(API_URL)
        if response.status_code == 200:
            jobs_list.append(response.json().get('jobs',[]))

        top_10_jobs = jobs_list[0][:10]  # Retrieve only the top 10 jobs

        jobsListJSON = json.dumps(top_10_jobs)

        with st.spinner("Processing..."):
            uploaded_file.seek(0)
            file = uploaded_file.read()
            # Get the document embeddings for the uploaded file
            vector1= embeds.getDocEmbeds(file, uploaded_file.name, jobsListJSON)
            vector2 = embeds.getJsonEmbeds(jobsListJSON)

            # Create a Chatbot instance with the specified model and temperature and vectors
            chatbot = Chatbot(model, temperature, vectors=vector1)

        st.session_state["ready"] = True

        return chatbot


    