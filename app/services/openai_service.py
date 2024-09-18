import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Verbose logging for environment variables
if os.environ.get('VERBOSE_LOGGING') == '1':
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"OPENAI_API_KEY: {'*' * len(os.getenv('OPENAI_API_KEY', ''))}")
    print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

# Check if API key is missing
if not os.getenv("OPENAI_API_KEY"):
    # Import formatting only when needed to avoid circular imports
    from app.utils import BOLD, RED, RESET
    print(f"{BOLD}{RED}Error: OPENAI_API_KEY is not set. Please run the setup script again.{RESET}")
    exit(1)

# Initialize OpenAI client
client = openai.OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

# Warn if model is not set
if not os.getenv("OPENAI_MODEL") and os.environ.get('VERBOSE_LOGGING') == '1':
    from app.utils import BOLD, YELLOW, RESET
    print(f"{BOLD}{YELLOW}Warning: OPENAI_MODEL is not set. Using default model.{RESET}")

def call_openai(messages, stream=True):
    """
    Calls the OpenAI API with provided messages and handles potential errors.
    """
    try:
        if os.environ.get('VERBOSE_LOGGING') == '1':
            print(f"Calling OpenAI with model: {os.getenv('OPENAI_MODEL', 'YOUR_MODEL_HERE')}")
            print(f"Messages: {messages}")
        
        # API call to OpenAI
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "YOUR_MODEL_HERE"),
            messages=messages,
            temperature=0.2,
            stream=stream
        )
        return completion
    except openai.APIError as e:
        # Import formatting when an error occurs to avoid circular import at the top level
        from app.utils import BOLD, RED, RESET
        print(f"{BOLD}{RED}OpenAI API Error: {str(e)}{RESET}")
        return {'error': str(e)}
    except Exception as e:
        from app.utils import BOLD, RED, RESET
        print(f"{BOLD}{RED}Unexpected error in call_openai: {str(e)}{RESET}")
        return {'error': str(e)}

def prepare_messages(chat_history, user_message, system_prompt, thought_process=None):
    """
    Prepares the message payload for OpenAI API by organizing chat history and appending the latest user input.
    """
    messages = []
    history_limit = 10
    recent_history = chat_history[-history_limit:]

    for entry in recent_history:
        if entry['sender'] == 'user':
            messages.append({'role': 'user', 'content': entry['text']})
        elif entry['sender'] == 'assistant':
            messages.append({'role': 'assistant', 'content': entry['text']})

    if thought_process:
        system_prompt += f"\n\nPrevious thought process:\n{thought_process}"

    messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': user_message})

    return messages

def determine_task_type_and_criteria(user_message):
    """
    Determines the task type based on the user's input and provides criteria to evaluate the task.
    """
    user_message = user_message.lower()
    
    task_keywords = {
        'product_development': ['product', 'business', 'market', 'customer', 'innovation'],
        'scientific_research': ['research', 'experiment', 'hypothesis', 'data', 'analysis'],
        'creative_writing': ['story', 'character', 'plot', 'writing', 'narrative'],
        'coding': ['code', 'programming', 'function', 'algorithm', 'debug']
    }
    
    counts = {task: sum(user_message.count(keyword) for keyword in keywords)
              for task, keywords in task_keywords.items()}
    
    task_type = max(counts, key=counts.get) if any(counts.values()) else 'general'
    
    criteria = {
        'product_development': ['market viability', 'innovation', 'user needs', 'feasibility'],
        'scientific_research': ['methodology', 'data analysis', 'hypothesis testing', 'literature review'],
        'creative_writing': ['character development', 'plot coherence', 'narrative style', 'originality'],
        'coding': ['functionality', 'efficiency', 'readability', 'best practices'],
        'general': ['clarity', 'relevance', 'accuracy', 'completeness']
    }
    
    return task_type, criteria[task_type]