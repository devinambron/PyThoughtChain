import os
from dotenv import load_dotenv, set_key

def setup():
    print("Welcome to the PyThoughtChain setup!")

    load_dotenv()
    api_key = input("Enter your OpenAI API key: ")
    base_url = input("Enter the base URL for the OpenAI API (default: http://localhost:1234/v1): ") or "http://localhost:1234/v1"

    set_key(".env", "OPENAI_API_KEY", api_key)
    set_key(".env", "OPENAI_BASE_URL", base_url)

    print("Setup complete. You can now run the PyThoughtChain application.")

if __name__ == "__main__":
    setup()