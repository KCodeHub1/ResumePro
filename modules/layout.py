import streamlit as st

class Layout:

    def show_header(self, types_files):
        """
        Displays the header of the app
        """
        st.markdown(
            """
            <style>
            .header {
                text-align: center;
                font-family: 'Arial', sans-serif;
                color: #007bff;
                margin-bottom: 20px;
            }
            .sub-header {
                text-align: center;
                font-family: 'Arial', sans-serif;
                color: #495057;
                margin-bottom: 20px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
        st.markdown(
            """
            <h1 class="header">ResumePro</h1>
            <h3 class="sub-header">Get Resume Insights and Latest Jobs To Apply</h3>
            <h3 class="sub-header">Please upload a resume in PDF format to continue</h3>
            """,
            unsafe_allow_html=True,
        )


    def show_api_key_missing(self):
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div style='text-align: center;'>
                <h4>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a> to start chatting</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def prompt_form(self):
        """
        Displays the prompt form
        """
        st.markdown(
            """
            <style>
            .stTextInput input {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 12px;
                color: #495057;
                border: none;
                box-shadow: none;
            }
            .stTextInput input:focus {
                background-color: #e9ecef;
            }
            .stButton button {
                background-color: #007bff;
                color: #fff;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            .stButton button:hover {
                background-color: #0056b3;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                key="input",
                help="Enter your query here"
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input
        return is_ready, user_input


    