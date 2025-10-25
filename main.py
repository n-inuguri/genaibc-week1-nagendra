"""
Enhanced LLM Application supporting both Groq and OpenAI APIs
"""
from groq import Groq
from openai import OpenAI
from appconfig import env_config

class LLMApp:
    # Define available models by provider
    GROQ_MODELS = [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile",
        "openai/gpt-oss-120b"
    ]
    
    OPENAI_MODELS = [
        "gpt-5",
        "gpt-5-mini",
        "gpt-5-nano"
    ]

    def __init__(self, groq_api_key=None, openai_api_key=None, model="llama-3.3-70b-versatile", chatbot_name="Quippy"):
        """
        Initialize the LLM application
        
        Args:
            groq_api_key: Groq API key (if None, reads from GROQ_API_KEY env var)
            openai_api_key: OpenAI API key (if None, reads from OPENAI_API_KEY env var)
            model: Model to use for completions
            chatbot_name: Name of the chatbot (default: Quippy)
        """
        
        self.chatbot_name = chatbot_name
        self.default_system_prompt = f"""You are {chatbot_name}, a witty and clever AI assistant.
You have a playful personality and love adding a dash of humor to your conversations! 🎭
While you keep things fun, you're also incredibly knowledgeable and great at explaining complex topics with clever analogies.
You occasionally throw in relevant puns or wordplay (but never force them), and you're not afraid to be a bit silly!
When you're not sure about something, you admit it with a humorous twist.
Remember: you're here to make learning and problem-solving fun while still being helpful and accurate."""
        
        # Initialize API keys
        self.groq_api_key = groq_api_key or env_config.groq_api_key
        self.openai_api_key = openai_api_key or env_config.openai_api_key
        
        # Initialize clients as needed
        self.groq_client = None
        self.openai_client = None
        self.model = model
        self.conversation_history = []
        
        # Initialize the appropriate client based on the model
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate client based on the selected model"""
        if self.model in self.GROQ_MODELS:
            if not self.groq_api_key:
                raise ValueError("Groq API key must be provided or set in `GROQ_API_KEY` environment variable")
            self.groq_client = Groq(api_key=self.groq_api_key)
        
        elif self.model in self.OPENAI_MODELS:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key must be provided or set in `OPENAI_API_KEY` environment variable")
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        
        else:
            raise ValueError(f"Unsupported model: {self.model}")

    def _get_active_client(self):
        """Get the appropriate client for the current model"""
        if self.model in self.GROQ_MODELS:
            return self.groq_client
        elif self.model in self.OPENAI_MODELS:
            return self.openai_client
        else:
            raise ValueError(f"No client available for model: {self.model}")

    def chat(self, user_message, system_prompt=None, temperature=0.5, max_tokens=1024):
        """
        Send a message and get a response
        
        Args:
            user_message: The user's message
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            The assistant's response text
        """
        messages = []

        # Add system prompt (use default if none provided)
        messages.append(
            {
                "role": "system",
                "content": system_prompt if system_prompt else self.default_system_prompt
            }
        )

        # Add conversation history
        if self.conversation_history:
            messages.extend(self.conversation_history)
        
        # Add current user's message
        messages.append(
            {
                "role": "user",
                "content": f"{user_message}"
            }
        )

        # Get the appropriate client
        client = self._get_active_client()

        # Prepare parameters based on provider
        if self.model in self.GROQ_MODELS:
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        else:  # OpenAI models
            params = {
                "model": self.model,
                "messages": messages,
                "max_completion_tokens": max_tokens  # OpenAI uses different parameter name
                # Note: GPT-5 models don't support custom temperature values
            }

        # Make LLM call
        response = client.chat.completions.create(**params)

        # Extract response text
        assistant_message = response.choices[0].message.content
        
        # Update conversation history with both user message and assistant response
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": assistant_message})

        return assistant_message
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
    
    def get_history(self):
        """Get the current conversation history"""
        return self.conversation_history

if __name__=="__main__":

    # Initialize the app
    app = LLMApp()

    # while True:
    message = input(f"What do you want to ask: ")
    response = app.chat(message)
    print(f"\nAssistant Response: {response}\n")

