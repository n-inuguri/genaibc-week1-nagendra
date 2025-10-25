# Quippy - Multi-Model Chat Assistant

Meet Quippy, a versatile and witty chat assistant that combines the power of multiple Language Model providers (Groq and OpenAI) in an engaging Streamlit interface. This application demonstrates LLM integration with a personality-driven approach to AI interaction.

What makes Quippy special:
* 🎭 **Personality-Driven:** More than just a Q&A bot - Quippy brings charm and wit to every conversation
* 🔄 **Multi-Provider Support:** Switch between Groq's open-source models and OpenAI's GPT-5 series
* 🎯 **Adaptive Behavior:** Parameter handling for different models while maintaining consistent personality
* 🎪 **User-Friendly Interface:** Clean, intuitive Streamlit frontend with model switching and configuration

## 1\. Overview

This application showcases LLM integration with a focus on user experience and adaptability. At its core, it features:

* A unified chat interface powered by multiple AI providers (Groq and OpenAI)
* A character-driven interaction model through Quippy's distinct personality
* Smart handling of model-specific parameters and requirements
* Web interface (for user interaction) using streamlit

The application demonstrates how to create engaging AI assistants by combining technical capabilities with personality-driven design.

## 2\. Features

  * **Multi-Provider Integration:** 
    * Groq API for access to open-source LLMs
    * OpenAI API for GPT-5 model series
    * Provider switching based on model selection
  
  * **Chatbot Personality - Meet Quippy!**
    * Witty and clever AI assistant with a unique personality
    * Built-in default system prompt for consistent character
    * Fun, engaging interactions while maintaining helpfulness
  
  * **Extended Model Selection:**
    * Groq Models:
      * Llama 3.1 8B (Instant)
      * Llama 3.3 70B (Versatile)
      * OpenAI OSS 20B
    * OpenAI Models:
      * GPT-5
      * GPT-5-mini
      * GPT-5-nano
  
  * **Enhanced Configuration:**
    * Dual API key support (Groq and OpenAI)
    * Adjustable temperature for response randomness (Note: Temparature parameter is not considered for GPT 5 models)
    * Customizable maximum token length
    * Optional system prompt override
    * Chat history management with clear function

## 3\. Tools & Frameworks Used

  * **Python:** The primary programming language.
  * **API Integrations:**
    * **Groq API:** For accessing open-source LLMs
    * **OpenAI API:** For GPT-5 series models
  * **Streamlit:** For building the interactive web frontend.
  * **`python-dotenv`:** For loading environment variables (API keys).
  * **`uv`** For virtual environment and dependency management.

## 4\. Setup and Installation

### 4.1. Prerequisites

  * Python 3.13.9 
  * A Groq API key (sign up at `https://console.groq.com/` to get one).
  * An Open AI API Key

### 4.2. Clone the Repository

``` bash
git clone https://github.com/n-inuguri/genaibc-week1-nagendra.git

```

### 4.3. Virtual Environment Setup

#### Using `uv` (Recommended)

1.  **Create a virtual environment:**
    
    ``` bash
    uv venv .venv
    
    ```

2.  **Activate the virtual environment:**
    
      * **On macOS/Linux:**
        
        ``` bash
        source .venv/bin/activate
        
        ```
    
      * **On Windows (PowerShell):**
        
        ``` bash
        .venv\Scripts\Activate.ps1
        
        ```
    
      * **On Windows (Command Prompt):**
        
        ``` bash
        .venv\Scripts\activate.bat
        
        ```

3.  **Install dependencies:**
    
    ``` bash
    uv pip install -r requirements.txt
    
    ```

### 4.4. API Key Configuration

1.  **Create a `.env` file** in the root directory of your project.

2.  **Add your API keys** to the `.env` file:
    
    ```
    GROQ_API_KEY="your_groq_api_key_here"
    OPENAI_API_KEY="your_openai_api_key_here"
    ```

    Note: You can use either or both APIs. The application will adapt based on your model selection.

## 5\. Usage

### 5.1. Running the Main LLM App in Command Line (for testing)

To test the core LLM functionality without the Streamlit frontend:

``` bash
uv run main.py

```

The application will prompt you to enter questions in the console.

### 5.2. Running the Streamlit Web Application

To launch the interactive web interface:

``` bash
streamlit run streamlit_app.py
```

This will open the application in your web browser. You can then:

  * **Configure API Access:**
    * Enter your Groq API Key (for Groq models)
    * Enter your OpenAI API Key (for GPT-5 models)
    * Keys can also be set in `.env`
  
  * **Choose Your Model:**
    * Select AI Provider (Groq or OpenAI)
    * Pick a specific model from the provider's offerings
  
  * **Customize Behavior:**
    * Adjust Temperature for response variability (Note: GPT-5 models use fixed temperature)
    * Set Max Tokens for response length
    * Override Quippy's default personality with custom system prompts
  
  * **Chat Interface:**
    * Interact with Quippy through the chat input
    * View conversation history with clear formatting
    * Reset the chat with "Clear Chat History" button

## 6\. Project Structure

``` 
.
├── .env                  # Environment variables (e.g., GROQ_API_KEY)
├── main.py               # Core LLM application logic
├── app_config.py         # Configuration for environment variables
├── requirements.txt      # Python dependencies
└── streamlit_app.py      # Streamlit web application

```
