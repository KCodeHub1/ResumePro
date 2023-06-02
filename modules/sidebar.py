import streamlit as st

class Sidebar:
    MODEL_OPTIONS = ["gpt-3.5-turbo"]
    TEMPERATURE_DEFAULT_VALUE = 0.9

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    @staticmethod
    def about():
        about = st.sidebar.expander("About")
        sections = [
            "#### Resume Pro Chatbot is an AI-powered assistant designed to help users with resume-related insights and job search.📄",
            "#### It leverages advanced language models to provide users with natural language interactions and support throughout the resume and job search process.",
        ]
        for section in sections:
            about.write(section)
            
    def show_info(self):
            self.reset_chat_button()
            st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)