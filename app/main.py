import os
import sys
from dotenv import load_dotenv
from app.services.chat_service import chat
from app.utils import BOLD, GREEN, RED, RESET
import argparse
from app.config import CONFIG, save_config

def main():
    try:
        load_dotenv()

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
        required_env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL']
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_vars:
            print(f"{BOLD}{RED}Error: The following environment variables are missing: {', '.join(missing_vars)}{RESET}")
            print("Please run the setup script again.")
            return

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
    main()