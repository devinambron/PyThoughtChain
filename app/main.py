import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from app.services.chat_service import chat
from app.utils import BOLD, GREEN, RED, RESET, YELLOW
import argparse
from app.config import CONFIG, save_config

def main():
    try:
        # Get the absolute path to the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct the path to the .env file
        dotenv_path = os.path.join(project_root, '.env')
        
        # Load environment variables from .env file
        load_dotenv(dotenv_path)

        # Print environment variables after loading
        print(f"{BOLD}{YELLOW}Environment variables after loading:{RESET}")
        print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
        print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
        print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")
        print(f"LLM_SERVICE: {os.getenv('LLM_SERVICE', 'openai')}")
        print(f"Debug: LLM_SERVICE = {os.getenv('LLM_SERVICE')}")

        parser = argparse.ArgumentParser(description='Run the chat application')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
        parser.add_argument('-i', '--iterations', type=int, help='Set the number of iterations before feedback')
        args = parser.parse_args()

        if args.verbose:
            os.environ['VERBOSE_LOGGING'] = '1'

        if args.iterations is not None:
            CONFIG['iterations_before_feedback'] = args.iterations
            save_config(CONFIG)
            print(f"{BOLD}{GREEN}Updated iterations before feedback to {args.iterations}{RESET}")

        # Check for required environment variables
        required_env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL', 'LLM_SERVICE']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            print(f"{BOLD}{RED}Error: The following environment variables are missing: {', '.join(missing_vars)}{RESET}")
            print("Please update your .env file and run the application again.")
            return

        # Print verbose information if enabled
        if args.verbose:
            print(f"{BOLD}{YELLOW}Verbose: LLM Service: {os.environ.get('LLM_SERVICE')}{RESET}")
            print(f"{BOLD}{YELLOW}Verbose: OpenAI Base URL: {os.environ.get('OPENAI_BASE_URL')}{RESET}")
            print(f"{BOLD}{YELLOW}Verbose: OpenAI Model: {os.environ.get('OPENAI_MODEL')}{RESET}")

        chat()
    except Exception as e:
        print(f"{BOLD}{RED}An error occurred while starting the application:{RESET}")
        print(f"{str(e)}")
        print("\nPlease check your configuration and try again.")
        if args.verbose:
            import traceback
            print("\nDetailed error information:")
            traceback.print_exc()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the chat application')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('-i', '--iterations', type=int, help='Set the number of iterations before feedback')
    args = parser.parse_args()
    main()

    if args.iterations is not None:
        CONFIG['iterations_before_feedback'] = args.iterations
        save_config(CONFIG)
        print(f"{BOLD}{GREEN}Updated iterations before feedback to {args.iterations}{RESET}")
