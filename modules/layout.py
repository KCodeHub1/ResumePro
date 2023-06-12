import streamlit as st

class Layout:

    def show_header(self, types_files):
        """
        Displays the header of the app
        """
        st.markdown(
            """
            <style>
            .header-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: lightgray;
                background-repeat: no-repeat;
                padding: 20px;
                margin-bottom: 20px;
            }
            .gen-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                background-repeat: no-repeat;
                padding: 20px;
                margin-bottom: 20px;
            }
            .header {
                text-align: center;
                font-family: 'Arial', sans-serif;
                color: #007bff;
                margin-bottom: 20px;
            }
            .sub-header {
                text-align: center;
                font-family: 'Arial', sans-serif;
                color: #4c1685;
                margin-bottom: 20px;
            }
            .headline {
                text-align: center;
                color: #007bff;
                font-size: 48px;
                line-height: 1.0834933333;
                font-weight: 600;
                letter-spacing: -0.003em;
                font-family: SF Pro Display,SF Pro Icons,Helvetica Neue,Helvetica,Arial,sans-serif;
            }
            .subhead {
                text-align: center;
                font-size: 16px;
                line-height: 1.1904761905;
                font-weight: 600;
                letter-spacing: .011em;
                font-family: SF Pro Display,SF Pro Icons,Helvetica Neue,Helvetica,Arial,sans-serif;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    
        st.markdown(
            """
            <div class="gen-container">
                <h1 class="headline">ResumePro</h1>
                <h3 class="subhead">Get Resume Insights and Latest Jobs To Apply</h3>     
            </div>
            """,
            unsafe_allow_html=True,
        )


    def show_api_key_missing(self):
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div class="header-container">
                <div style='text-align: center;'>
                    <h4 class="subhead">How to use ResumePro?</h3>
                    <h3 class="subhead">Step 1: Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a> to start chatting</h4>
                    <h3 class="subhead">Step 2: Upload a resume in PDF format to continue</h3>
                </div>
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
                width: 100%;
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
                help="Enter your query here",
                height=150
            )
            submit_button = st.form_submit_button(label="Send")

            is_ready = submit_button and user_input
        return is_ready, user_input