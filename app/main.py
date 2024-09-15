import os
from dotenv import load_dotenv
from app.services.chat_service import chat
from app.utils import BOLD, GREEN, RESET
import argparse

load_dotenv()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the chat application')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    os.environ['VERBOSE_LOGGING'] = '1' if args.verbose else '0'

    if args.verbose:
        print(f"{BOLD}{GREEN}Verbose logging enabled{RESET}")

    chat()