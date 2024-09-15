import os
import openai
from dotenv import load_dotenv
from app.utils import BOLD, RED, YELLOW, RESET

load_dotenv()

if os.environ.get('VERBOSE_LOGGING') == '1':
    print(f"OPENAI_BASE_URL: {os.getenv('OPENAI_BASE_URL')}")
    print(f"OPENAI_API_KEY: {'*' * len(os.getenv('OPENAI_API_KEY', ''))}")
    print(f"OPENAI_MODEL: {os.getenv('OPENAI_MODEL')}")

if not os.getenv("OPENAI_API_KEY"):
    print(f"{BOLD}{RED}Error: OPENAI_API_KEY is not set. Please run the setup script again.{RESET}")
    exit(1)

client = openai.OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.getenv("OPENAI_API_KEY")
)

if not os.getenv("OPENAI_MODEL") and os.environ.get('VERBOSE_LOGGING') == '1':
    print(f"{BOLD}{YELLOW}Warning: OPENAI_MODEL is not set. Using default model.{RESET}")

def call_openai(messages, stream=False):
    try:
        if os.environ.get('VERBOSE_LOGGING') == '1':
            print(f"Calling OpenAI with model: {os.getenv('OPENAI_MODEL', 'YOUR_MODEL_HERE')}")
            print(f"Messages: {messages}")
        completion = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "YOUR_MODEL_HERE"),
            messages=messages,
            temperature=0.7,
            stream=stream
        )
        if stream:
            return completion
        else:
            return completion.choices[0].message.content
    except openai.APIError as e:
        print(f"{BOLD}{RED}OpenAI API Error: {str(e)}{RESET}")
        return {'error': str(e)}
    except Exception as e:
        print(f"{BOLD}{RED}Unexpected error in call_openai: {str(e)}{RESET}")
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

def determine_task_type_and_criteria(user_message):
    user_message = user_message.lower()
    
    product_keywords = ['product', 'business', 'market', 'customer', 'innovation']
    scientific_keywords = ['research', 'experiment', 'hypothesis', 'data', 'analysis']
    creative_keywords = ['story', 'character', 'plot', 'writing', 'narrative']
    
    product_count = sum(user_message.count(keyword) for keyword in product_keywords)
    scientific_count = sum(user_message.count(keyword) for keyword in scientific_keywords)
    creative_count = sum(user_message.count(keyword) for keyword in creative_keywords)
    
    if product_count > scientific_count and product_count > creative_count:
        task_type = 'product_development'
        criteria = ['market viability', 'innovation', 'user needs', 'feasibility']
    elif scientific_count > product_count and scientific_count > creative_count:
        task_type = 'scientific_research'
        criteria = ['methodology', 'data analysis', 'hypothesis testing', 'literature review']
    elif creative_count > product_count and creative_count > scientific_count:
        task_type = 'creative_writing'
        criteria = ['character development', 'plot coherence', 'narrative style', 'originality']
    else:
        task_type = 'general'
        criteria = ['clarity', 'relevance', 'accuracy', 'completeness']
    
    return task_type, criteria