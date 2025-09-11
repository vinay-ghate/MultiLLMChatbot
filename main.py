import streamlit as st
import os

# Import provider-specific libraries
import google.generativeai as genai
from openai import OpenAI
from groq import Groq
from anthropic import Anthropic
from cohere import Client as CohereClient

# --- Page Configuration ---
st.set_page_config(
    page_title="Multi-Provider Chatbot 🤖",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Multi-Provider Chatbot 🤖")
st.caption("Select a provider, enter your API key, and start chatting.")

# --- Provider Selection and API Key Input in Sidebar ---
with st.sidebar:
    st.header("Configuration")
    
    # List of available providers
    # You can easily add more here
    providers = {
        "Google Gemini": "gemini",
        "OpenAI": "openai",
        "Groq": "groq",
        "Anthropic (Claude)": "anthropic",
        "Cohere": "cohere"
    }
    
    selected_provider_name = st.selectbox("Choose an AI Provider:", list(providers.keys()))
    selected_provider = providers[selected_provider_name]

    api_key = st.text_input(f"Enter your {selected_provider_name} API Key", type="password")

    if st.button("Set API Key"):
        if not api_key:
            st.error("API key is required.")
        else:
            # Clear previous session state if provider changes
            if "provider" in st.session_state and st.session_state.provider != selected_provider:
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                    
            st.session_state.api_key = api_key
            st.session_state.provider = selected_provider
            st.success(f"{selected_provider_name} API key set successfully!")
            st.rerun() # Rerun to update the main page state

# --- Chat Logic ---

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get the model's response
def get_model_response(client, provider, messages):
    try:
        if provider == "gemini":
            # Gemini requires a specific format
            model = client.GenerativeModel('gemini-2.0-flash-lite')
            response = model.generate_content(messages[-1]['parts'])
            return response.text
        elif provider in ["openai", "groq"]:
            # OpenAI and Groq use a similar message format
            chat_completion = client.chat.completions.create(
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                model="openai/gpt-oss-20b" if provider == "openai" else "llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        elif provider == "anthropic":
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620", # Or other Claude models
                max_tokens=1024,
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            return response.content[0].text
        elif provider == "cohere":
            # Cohere has a different message format
            chat_history = [{"role": "USER" if msg["role"] == "user" else "CHATBOT", "message": msg["content"]} for msg in st.session_state.messages[:-1]]
            prompt = st.session_state.messages[-1]["content"]
            response = client.chat(message=prompt, chat_history=chat_history,model="command-a-03-2025")
            return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Check if API key and provider are set
if "api_key" in st.session_state and "provider" in st.session_state:
    # --- Initialize the correct client based on provider ---
    try:
        if st.session_state.provider == "gemini":
            genai.configure(api_key=st.session_state.api_key)
            client = genai
        elif st.session_state.provider == "openai":
            client = OpenAI(api_key=st.session_state.api_key)
        elif st.session_state.provider == "groq":
            client = Groq(api_key=st.session_state.api_key)
        elif st.session_state.provider == "anthropic":
            client = Anthropic(api_key=st.session_state.api_key)
        elif st.session_state.provider == "cohere":
            client = CohereClient(api_key=st.session_state.api_key)

        # --- Display chat messages ---
        for message in st.session_state.messages:
            role = message.get("role")
            content = ""
            if st.session_state.provider == "gemini" and role == "user":
                 content = message["parts"][0]
            elif role in ["user", "assistant"]:
                 content = message["content"]
            
            if content:
                with st.chat_message(role):
                    st.markdown(content)
        
        # --- Chat input field ---
        if prompt := st.chat_input("What would you like to ask?"):
            # Prepare message based on provider
            user_message = {}
            if st.session_state.provider == "gemini":
                user_message = {"role": "user", "parts": [prompt]}
            else:
                user_message = {"role": "user", "content": prompt}
                
            st.session_state.messages.append(user_message)
            
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_model_response(client, st.session_state.provider, st.session_state.messages)
                    st.markdown(response)
            
            # Add assistant response to history
            assistant_message = {}
            if st.session_state.provider == "gemini":
                 # Gemini doesn't use role for history from the model side in this simple setup
                 # We are managing history on our own.
                 # Let's keep a consistent format internally.
                 st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                assistant_message = {"role": "assistant", "content": response}
                st.session_state.messages.append(assistant_message)


    except Exception as e:
        st.error(f"Failed to initialize the client. Please check your API key. Error: {e}")
else:
    st.info("Please configure your API key in the sidebar to start chatting.")