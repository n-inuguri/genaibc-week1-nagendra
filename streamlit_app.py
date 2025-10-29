"""
Streamlit Frontend for Groq LLM Application
"""
import streamlit as st
from main import LLMApp

# page configuration
st.set_page_config(
    page_title="Simple LLM Chat Application",
    page_icon="🤖",
    layout="centered"
)

# initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "llm_app" not in st.session_state:
    st.session_state.llm_app = None

# Title and description
st.title("Chat with Quippy 🎭")
st.markdown("Hey there! I'm Quippy, your witty digital sidekick powered by AI! 🎪 I'm here to make our chat both fun AND helpful. Whether you need a hand with complex problems or just want to learn something new, I'll keep it entertaining! To get started, just pop your Groq / OpenAI API key in the sidebar and let the fun begin! 🎯")

# Implement sidebar for configuration
# Persist API keys in session state so switching providers doesn't lose entered keys
if "groq_api_key" not in st.session_state:
    st.session_state.groq_api_key = LLMApp().groq_api_key
if "openai_api_key" not in st.session_state:
    try:
        st.session_state.openai_api_key = LLMApp().openai_api_key
    except:
        st.session_state.openai_api_key = None

with st.sidebar:
    st.header("Configuration")

    # Provider selection (show this first so API key input can adapt)
    st.subheader("Model Selection")
    provider = st.selectbox(
        "AI Provider",
        ["Groq", "OpenAI"],
        help="Select the AI provider"
    )

    # Single API key input that adapts to the selected provider. Values are stored
    # per-provider in session_state so switching back and forth keeps the keys.
    if provider == "Groq":
        groq_input_key = "groq_api_key_input"
        # show input with the previously stored value
        st.text_input("API Key (Groq)", type="password", value=st.session_state.get("groq_api_key", ""), key=groq_input_key, help="Enter your Groq API key")
        # copy the transient input value into the canonical session var
        st.session_state.groq_api_key = st.session_state.get(groq_input_key, st.session_state.get("groq_api_key"))

        model = st.selectbox(
            "Model",
            [
                "llama-3.1-8b-instant",
                "llama-3.3-70b-versatile",
                "openai/gpt-oss-120b",
            ],
            help="Select the Groq model to use"
        )
    else:
        openai_input_key = "openai_api_key_input"
        st.text_input("API Key (OpenAI)", type="password", value=st.session_state.get("openai_api_key", ""), key=openai_input_key, help="Enter your OpenAI API key")
        st.session_state.openai_api_key = st.session_state.get(openai_input_key, st.session_state.get("openai_api_key"))

        model = st.selectbox(
            "Model",
            [
                "gpt-5",
                "gpt-5-mini",
                "gpt-5-nano",
            ],
            help="Select the OpenAI model to use"
        )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.5,
        step=0.1,
        help="Select a value to control response randomness. Higher values make output more random."
    )

    max_tokens = st.slider(
        "Max Tokens",
        min_value=256,
        max_value=2048,
        value=1024,
        step=256,
        help="Set the response length"
    )

    system_prompt = st.text_area(
        "Custom System Prompt (Optional)",
        placeholder="Leave empty to let Quippy be their fun, witty self...",
        help="Want to give Quippy a different personality? Type it here!"
    )

    # Clear chat button
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.llm_app:
            st.session_state.llm_app.clear_history()
        st.rerun()

# expose canonical API key values from session_state into local vars
groq_api_key = st.session_state.get("groq_api_key")
openai_api_key = st.session_state.get("openai_api_key")

if st.session_state.llm_app is None:
    try:
        st.session_state.llm_app = LLMApp(
            groq_api_key=groq_api_key,
            openai_api_key=openai_api_key,
            model=model
        )
    except Exception as e:
        st.error(f"Error initializing LLM App: {str(e)}")
        st.session_state.llm_app = None

# display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    if provider == "Groq" and not groq_api_key:
        st.warning("Please enter your Groq API key in the sidebar")
    elif provider == "OpenAI" and not openai_api_key:
        st.warning("Please enter your OpenAI API key in the sidebar")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        # get Quippy's response
        with st.chat_message("assistant", avatar="🎭"):
            with st.spinner("Quippy is cooking up something clever..."):
                try:
                    # Ensure LLM app is properly initialized (create if missing)
                    if st.session_state.llm_app is None:
                        st.session_state.llm_app = LLMApp(
                            groq_api_key=groq_api_key,
                            openai_api_key=openai_api_key,
                            model=model
                        )

                    # Sync any updated API keys or model selection from session_state
                    # into the existing LLMApp instance so lazy initialization uses
                    # the latest values entered in the UI.
                    st.session_state.llm_app.groq_api_key = groq_api_key
                    st.session_state.llm_app.openai_api_key = openai_api_key
                    if st.session_state.llm_app.model != model:
                        st.session_state.llm_app.model = model
                        # clear existing clients so they will be recreated with new keys
                        st.session_state.llm_app.groq_client = None
                        st.session_state.llm_app.openai_client = None

                    response = st.session_state.llm_app.chat(
                        user_message=prompt,
                        system_prompt=system_prompt if system_prompt else None,
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")