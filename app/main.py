import os
import sys
from dotenv import load_dotenv
from app.services.chat_service import ChatService
from app.utils import BOLD, GREEN, RED, RESET
import argparse
from app.config import CONFIG, save_config
from app.gui import run_gui

print("Environment variables after loading .env file:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

def check_required_env_vars():
    """
    Check if the required environment variables are set.
    Return a list of missing environment variables if any.
    """
    required_env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    return missing_vars

def main():
    try:
        # Load environment variables from the .env file
        print("Loading environment variables from .env file...")
        load_dotenv()

        # Check if the required environment variables are set
        missing_vars = check_required_env_vars()
        if missing_vars:
            print(f"{BOLD}{RED}Error: The following environment variables are missing: {', '.join(missing_vars)}{RESET}")
            print("Please run the setup script again.")
            return

        # Print the values of the environment variables
        print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
        print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
        print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

        # Set up argument parser
        parser = argparse.ArgumentParser(description='Run the chat application')
        parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
        parser.add_argument('-i', '--iterations', type=int, help='Set the number of iterations before feedback')
        parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
        args = parser.parse_args()

        # Enable verbose logging if specified
        if args.verbose:
            os.environ['VERBOSE_LOGGING'] = '1'

        # Update iterations in config if specified
        if args.iterations is not None:
            CONFIG['iterations_before_feedback'] = args.iterations
            save_config(CONFIG)
            print(f"{BOLD}{GREEN}Updated iterations before feedback to {args.iterations}{RESET}")

        # Determine mode of running the app (CLI or GUI)
        if args.cli:
            chat_service = ChatService()
            chat_service.process_user_message("hello")
        else:
            run_gui()

    except Exception as e:
        print(f"{BOLD}{RED}An error occurred while starting the application:{RESET}")
        print(f"{str(e)}")
        print("\nPlease check your configuration and try again.")
        if args.verbose:
            import traceback
            print("\nDetailed error information:")
            traceback.print_exc()

if __name__ == '__main__':
    main()