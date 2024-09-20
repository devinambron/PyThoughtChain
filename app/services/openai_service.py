import os
import openai
from app.utils import BOLD, RED, RESET, YELLOW

# Check for required environment variables
required_env_vars = ['OPENAI_API_KEY', 'OPENAI_BASE_URL', 'OPENAI_MODEL', 'LLM_SERVICE']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    print(f"{BOLD}{RED}Error: The following environment variables are missing: {', '.join(missing_vars)}{RESET}")
    print("Please update your .env file and run the application again.")
    exit(1)

if os.environ.get('VERBOSE_LOGGING') == '1':
    print(f"LLM_SERVICE: {os.getenv('LLM_SERVICE')}")
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

llm_service = os.getenv("LLM_SERVICE", "openai").lower()
openai_base_url = os.getenv("OPENAI_BASE_URL")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client based on the service
if llm_service == "ollama":
    # Ensure the base URL ends with '/v1/'
    if not openai_base_url.endswith('/v1/'):
        openai_base_url = openai_base_url.rstrip('/') + '/v1/'

    openai.api_base = openai_base_url
    openai.api_key = "ollama"  # Required but not used by Ollama
elif llm_service == "lmstudio":
    # Adjust based on LM Studio's API requirements
    openai.api_base = openai_base_url
    openai.api_key = "lmstudio"  # Required but not used by LM Studio
else:  # Default to OpenAI
    openai.api_key = openai_api_key
    # openai.api_base defaults to OpenAI's API

if not os.getenv("OPENAI_MODEL") and os.environ.get('VERBOSE_LOGGING') == '1':
    print(f"{BOLD}{YELLOW}Warning: OPENAI_MODEL is not set. Using default model.{RESET}")

def call_openai(messages, stream=True):
    try:
        if os.environ.get('VERBOSE_LOGGING') == '1':
            print(f"Calling {llm_service.upper()} API at URL: {openai_base_url}")
            print(f"Using model: {os.getenv('OPENAI_MODEL', 'DEFAULT_MODEL')}")
            print(f"Messages: {messages}")

        payload = {
            "model": os.getenv("OPENAI_MODEL", "DEFAULT_MODEL"),
            "messages": messages,
            "temperature": 0.2,
            "stream": stream
        }

        response = openai.ChatCompletion.create(**payload)

        if stream:
            # Handle streaming responses
            for chunk in response:
                if 'choices' in chunk and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if 'content' in delta:
                        print(delta.content, end="", flush=True)
            print()  # For newline after streaming
            return {'status': 'streaming completed'}
        else:
            return response
    except Exception as e:
        print(f"{BOLD}{RED}API Error: {str(e)}{RESET}")
        return {'error': str(e)}

def prepare_messages(chat_history, user_message, system_prompt, thought_process=None):
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

# Export functions
__all__ = ['call_openai', 'prepare_messages']

def determine_task_type_and_criteria(user_message):
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