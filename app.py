import os
from dotenv import load_dotenv
import ollama
import mesop as me
import mesop.labs as mel
from groq import Groq, GroqError

# Load environment variables
load_dotenv()

# Fetch environment variables
GROQ_API_KEY = os.getenv('GROQ_CLOUD_API_KEY')
OLLAMA_URL = os.getenv('OLLAMA_URL')

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

@me.page(
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
    path="/",
    title="KariosChat",
)
def page():
    mel.chat(transform, title="KarioChat", bot_user="KariosBot")

def transform(input: str, history: list[mel.ChatMessage]):
    messages = [{"role": "user", "content": message.content} for message in history]
    messages.append({"role": "user", "content": input})

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    try:
        response = groq_client.chat.completions.create(
            messages=messages,
            model="llama3:latest",  # Ensure this matches the model name in Groq
            stream=True
        )

        for chunk in response:
            content = chunk.get('message', {}).get('content', '')
            if content:
                yield content

    except GroqError as e:
        yield f"Error with Groq: {e}"

if __name__ == "__main__":
    me.run()
































# import ollama
# import mesop as me
# import mesop.labs as mel
# import logging

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# @me.page(
#     security_policy=me.SecurityPolicy(
#         allowed_iframe_parents=["https://google.github.io"]
#     ),
#     path="/",
#     title="Mesop Demo Chat",
# )
# def page():
#     mel.chat(transform, title="KariosChat", bot_user="Karios Bot")

# def transform(input: str, history: list[mel.ChatMessage]):
#     messages = [{"role": "user", "content": message.content} for message in history]
#     messages.append({"role": "user", "content": input})
    
#     # Use Ollama to process the messages
#     response = ollama.chat(model='llama3', messages=messages, stream=True)
    
#     for chunk in response:
#         content = chunk.get('message', {}).get('content', '')
#         if content:
#             yield content

# if __name__ == "__main__":
#     me.run()

