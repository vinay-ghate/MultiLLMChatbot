# [Multi-LLM Chatbot](http://mymultillmchatbot.streamlit.app/)

This project is a Streamlit-based web application that allows users to interact with multiple Large Language Models (LLMs) from different providers in a single interface.

## File Structure

```
MultiLLMChatbot/
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── README.md
├── uv.lock
├── .git/
└── .venv/
```

## How to Use

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/MultiLLMChatbot.git
    cd MultiLLMChatbot
    ```

2.  **Install dependencies:**
    This project uses `uv` for package management.
    ```bash
    uv pip install -r requirements.txt
    ```
    *(Note: You may need to generate a `requirements.txt` file from `pyproject.toml` if one is not already present.)*

3.  **Run the Streamlit application:**
    ```bash
    streamlit run main.py
    ```

4.  **Configure the application:**
    *   Open the application in your web browser.
    *   Select an AI provider from the sidebar (Google Gemini, OpenAI, Groq, Anthropic, Cohere).
    *   Enter your API key for the selected provider.
    *   Click "Set API Key".

5.  **Start chatting:**
    Once the API key is set, you can start a conversation with the selected LLM.


