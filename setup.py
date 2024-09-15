import os
import subprocess
from app.utils import BOLD, CYAN, RESET
from dotenv import load_dotenv, set_key

def setup():
    print(f"{BOLD}{CYAN}Welcome to the PyThoughtChain setup!{RESET}")

    load_dotenv()

    api_key = input("Enter your OpenAI API key: ")
    base_url = input("Enter the base URL for the OpenAI API (default: http://localhost:1234/v1): ") or "http://localhost:1234/v1"

    model_options = ["gpt-3.5-turbo", "gpt-4", "YOUR_CUSTOM_MODEL_NAME"]
    print(f"{BOLD}{CYAN}Available models:{RESET}")
    for i, model in enumerate(model_options):
        print(f"{i+1}. {model}")

    while True:
        try:
            model_choice = int(input(f"{BOLD}{CYAN}Enter the number of the model you want to use: {RESET}"))
            if 1 <= model_choice <= len(model_options):
                selected_model = model_options[model_choice - 1]
                break
            else:
                print(f"{BOLD}{CYAN}Please enter a valid model number.{RESET}")
        except ValueError:
            print(f"{BOLD}{CYAN}Please enter a valid model number.{RESET}")

    set_key(".env", "OPENAI_API_KEY", api_key)
    set_key(".env", "OPENAI_BASE_URL", base_url)
    set_key(".env", "OPENAI_MODEL", selected_model)

    print("Implementing the installation instructions...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

    print(f"{BOLD}{CYAN}Setup complete. You can now run the PyThoughtChain application with 'python -m app.main'.{RESET}")

if __name__ == "__main__":
    setup()