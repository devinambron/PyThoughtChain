import os
import subprocess
from dotenv import load_dotenv, set_key
from app.config import DEFAULT_CONFIG, save_config
from app.utils import BOLD, CYAN, RESET

def setup():
    print(f"{BOLD}{CYAN}Welcome to the PyThoughtChain setup!{RESET}")

    # Load environment variables from .env file
    load_dotenv()

    # Prompt the user for OpenAI API key and base URL
    api_key = input("Enter your OpenAI API key: ")
    base_url = input("Enter the base URL for the OpenAI API (default: http://localhost:1234/v1): ") or "http://localhost:1234/v1"

    # Present available model options to the user
    model_options = ["gpt-3.5-turbo", "gpt-4", "YOUR_CUSTOM_MODEL_NAME"]
    print(f"{BOLD}{CYAN}Available models:{RESET}")
    for i, model in enumerate(model_options):
        print(f"{i+1}. {model}")

    # Allow the user to select a model
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

    # Save API key, base URL, and selected model in the .env file
    set_key(".env", "OPENAI_API_KEY", api_key)
    set_key(".env", "OPENAI_BASE_URL", base_url)
    set_key(".env", "OPENAI_MODEL", selected_model)

    # Prompt for configuration options and update DEFAULT_CONFIG
    print(f"{BOLD}{CYAN}Configuration options:{RESET}")
    config = DEFAULT_CONFIG.copy()

    config['iterations_before_feedback'] = int(input(f"Enter the number of iterations before asking for feedback (default: {DEFAULT_CONFIG['iterations_before_feedback']}): ") or DEFAULT_CONFIG['iterations_before_feedback'])
    config['max_iterations'] = int(input(f"Enter the maximum number of iterations (default: {DEFAULT_CONFIG['max_iterations']}): ") or DEFAULT_CONFIG['max_iterations'])
    config['confidence_threshold'] = float(input(f"Enter the confidence threshold to stop iterations (0-1, default: {DEFAULT_CONFIG['confidence_threshold']}): ") or DEFAULT_CONFIG['confidence_threshold'])

    # Save updated configuration
    save_config(config)

    # Install dependencies from requirements.txt
    print("Implementing the installation instructions...")
    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

    print(f"{BOLD}{CYAN}Setup complete. You can now run the PyThoughtChain application with 'python -m app.main'.{RESET}")

if __name__ == "__main__":
    setup()