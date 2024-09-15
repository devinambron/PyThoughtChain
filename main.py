import json
import re
import random
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RESET = '\033[0m'

def format_bold_text(text):
    return re.sub(r'\*\*(.*?)\*\*', f'{BOLD}\\1{RESET}', text)

def call_openai(messages, stream=False):
    try:
        completion = client.chat.completions.create(
            model="YOUR_MODEL_HERE",
            messages=messages,
            temperature=0.7,
            stream=stream
        )
        if stream:
            return completion
        else:
            return completion.choices[0].message.content
    except Exception as e:
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

def get_user_feedback():
    while True:
        feedback = input(f"{BOLD}{CYAN}Your feedback (or press Enter to continue, type 'finalize' to get the final answer): {RESET}").strip()
        if feedback.lower() in ['', 'continue', 'next']:
            return None
        elif feedback.lower() in ['stop', 'exit', 'finalize']:
            return 'finalize'
        else:
            return feedback

def calculate_confidence_score(thought_process):
    confidence_keywords = ['certain', 'confident', 'sure', 'likely', 'probable']
    uncertainty_keywords = ['uncertain', 'unsure', 'maybe', 'perhaps', 'possible']

    confidence_score = sum(thought_process.lower().count(word) for word in confidence_keywords)
    uncertainty_score = sum(thought_process.lower().count(word) for word in uncertainty_keywords)

    total_score = confidence_score - uncertainty_score
    normalized_score = (total_score + 5) / 10
    return max(0, min(1, normalized_score))

def generate_mind_map(thought_process):
    lines = thought_process.split('\n')
    mind_map = []
    current_level = 0
    for line in lines:
        if line.strip():
            depth = len(line) - len(line.lstrip())
            node = line.strip()
            if depth == 0:
                current_level = 0
                mind_map.append(f"{'  ' * current_level}• {node}")
            else:
                current_level = depth // 2
                mind_map.append(f"{'  ' * current_level}└─ {node}")
    
    return "\n".join(mind_map)

def determine_task_type_and_criteria(user_message):
    system_prompt = """Analyze the user's request and determine:
1. The most appropriate task type (product_development, scientific_research, or creative_writing)
2. Relevant evaluation criteria (comma-separated list)

Respond in the format:
Task Type: [determined task type]
Evaluation Criteria: [criterion1, criterion2, ...]"""

    response = call_openai(prepare_messages([], user_message, system_prompt))

    if isinstance(response, dict) and 'error' in response:
        return 'general', ['relevance', 'clarity', 'feasibility']

    task_type = 'general'
    evaluation_criteria = ['relevance', 'clarity', 'feasibility']

    for line in response.split('\n'):
        if line.startswith('Task Type:'):
            task_type = line.split(':')[1].strip().lower()
        elif line.startswith('Evaluation Criteria:'):
            evaluation_criteria = [criterion.strip() for criterion in line.split(':')[1].split(',')]

    return task_type, evaluation_criteria

    return "\n".join(mind_map)
def chat():
    chat_history = []
    task_specific_prompts = {
        'product_development': "You are an expert in product development. Consider market trends, user needs, and technological innovations.",
        'scientific_research': "You are a seasoned scientist. Apply the scientific method, consider existing literature, and propose hypotheses.",
        'creative_writing': "You are a creative writer. Use literary devices, develop compelling characters, and craft engaging narratives.",
        'general': "You are a knowledgeable assistant. Provide clear, concise, and helpful information on a wide range of topics."
    }
    
    print(f"{BOLD}{GREEN}Welcome to PyThoughtChain.{RESET}")
    print(f"Type your messages below. Type 'exit' to quit the application.")
    print(f"You can provide feedback after each thought iteration, press Enter to continue, or type 'finalize' to get the final answer.\n")

    try:
        while True:
            user_message = input(f"{BOLD}{CYAN}You: {RESET}").strip()
            
            if user_message.lower() == 'exit':
                print(f"{BOLD}{GREEN}Exiting chat...{RESET}")
                break

            if not user_message:
                print(f"{BOLD}{RED}Error: Empty message.{RESET}")
                continue

            task_type, evaluation_criteria = determine_task_type_and_criteria(user_message)
            print(f"{BOLD}{YELLOW}Determined Task Type: {RESET}{task_type}")
            print(f"{BOLD}{YELLOW}Evaluation Criteria: {RESET}{', '.join(evaluation_criteria)}")

            thought_process = ""
            iteration = 1
            max_iterations = 5

            while iteration <= max_iterations:
                system_prompt = f"""Help solve the user's request by generating a detailed step-by-step plan.
Please ensure that your thought process is clear and detailed.
This is iteration {iteration} of the thought process.
{'Refine and expand upon the previous thoughts.' if iteration > 1 else ''}
Consider opposing viewpoints and potential counterarguments.
Explore hypothetical "what-if" scenarios to test the robustness of your proposed solutions.
Incorporate quantitative analysis where appropriate.
{task_specific_prompts.get(task_type, '')}
Do not return a final answer, just return the thought process."""

                response = call_openai(prepare_messages(chat_history, user_message, system_prompt, thought_process))
                
                if isinstance(response, dict) and 'error' in response:
                    print(f"{BOLD}{RED}Error: {response['error']}{RESET}")
                    break

                new_thoughts = response
                formatted_new_thoughts = format_bold_text(new_thoughts)
                print(f"{BOLD}{YELLOW}Thought Process (Iteration {iteration}): {RESET}{formatted_new_thoughts}")

                confidence_score = calculate_confidence_score(new_thoughts)
                print(f"{BOLD}{YELLOW}Confidence Score: {RESET}{confidence_score:.2f}")

                mind_map = generate_mind_map(new_thoughts)
                print(f"{BOLD}{YELLOW}Mind Map:{RESET}\n{mind_map}")

                thought_process += f"\n\nIteration {iteration}:\n{new_thoughts}"

                user_feedback = get_user_feedback()
                if user_feedback == 'finalize':
                    break
                elif user_feedback:
                    user_message += f"\n\nUser feedback: {user_feedback}"

                iteration += 1
                if confidence_score > 0.8:
                    break

            final_system_prompt = f"""You are an AI assistant providing a final answer based on the following thought process:

{thought_process}

Evaluate the solution based on these criteria: {', '.join(evaluation_criteria)}
Provide citations for any factual claims or data points.
Consider potential limitations or areas for further research.
Provide a concise and clear final answer to the user's request."""

            final_response = call_openai(prepare_messages(chat_history, user_message, final_system_prompt))
            
            if isinstance(final_response, dict) and 'error' in final_response:
                print(f"{BOLD}{RED}Error: {final_response['error']}{RESET}")
                continue

            final_answer = final_response
            formatted_final_answer = format_bold_text(final_answer)
            print(f"{BOLD}{YELLOW}Final Answer: {RESET}{formatted_final_answer}")

            chat_history.append({'sender': 'user', 'text': user_message})
            chat_history.append({'sender': 'assistant', 'text': final_answer})
    
    except KeyboardInterrupt:
        print(f"\n{BOLD}{RED}Chat interrupted. Exiting gracefully...{RESET}")

if __name__ == '__main__':
    chat()