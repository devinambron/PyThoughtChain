from app.services.openai_service import call_openai as send_request
from app.config import CONFIG
from app.prompts import evaluation_prompt
import re

BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RESET = '\033[0m'

def format_bold_text(text):
    state = {'bold': False}
    formatted_text = ""

    def toggle_bold():
        state['bold'] = not state['bold']
        return BOLD if state['bold'] else RESET

    i = 0
    while i < len(text):
        if text[i:i+2] == '**':
            formatted_text += toggle_bold()
            i += 2
        else:
            formatted_text += text[i]
            i += 1
    
    if state['bold']:  # Ensure we close any open bold tags
        formatted_text += RESET
    
    return formatted_text

def get_user_feedback():
    while True:
        feedback = input(f"{BOLD}{CYAN}Your feedback (or press Enter to continue, type 'finalize' to get the final answer): {RESET}").strip()
        if feedback.lower() in ['', 'continue', 'next']:
            return None
        elif feedback.lower() in ['stop', 'exit', 'finalize']:
            return 'finalize'
        else:
            return feedback

def calculate_confidence_score(thought_process, iteration, max_iterations, correct_answers, total_answers, self_evaluation_score):
    confidence_keywords = ['certain', 'confident', 'sure', 'likely', 'probable', 'definitely', 'undoubtedly']
    uncertainty_keywords = ['uncertain', 'unsure', 'maybe', 'perhaps', 'possible', 'might', 'could']

    # Count confidence and uncertainty keyword occurrences
    confidence_score = sum(thought_process.lower().count(word) for word in confidence_keywords)
    uncertainty_score = sum(thought_process.lower().count(word) for word in uncertainty_keywords)

    # Total words in thought process (avoid division by zero)
    total_words = len(thought_process.split())
    if total_words == 0:
        return 0

    # Calculate confidence ratio
    confidence_ratio = (confidence_score - uncertainty_score) / total_words
    base_confidence = max(0, min(1, (confidence_ratio + 0.1) / 0.2))  # Ensuring it's between 0 and 1

    # Introduce a scaling factor for iteration progress
    iteration_factor = 1 - (iteration / max_iterations)

    # Safeguard for zero total answers
    if total_answers > 0:
        initial_confidence = base_confidence * (1 + iteration_factor) * (correct_answers / total_answers)
    else:
        initial_confidence = base_confidence * (1 + iteration_factor)

    # Adjust confidence based on self-evaluation score (Ensure it is non-zero)
    adjusted_confidence = initial_confidence * (self_evaluation_score if self_evaluation_score > 0 else 1)

    return max(0, min(1, adjusted_confidence))

def self_evaluate(thought_process):
    """
    Evaluates the thought process by sending it to an LLM API and getting a score between 0 and 1.
    
    :param thought_process: A string or list representing the thought process to be evaluated.
    :return: A score between 0 and 1, indicating the quality of the thought process.
    """
    
    # Construct the evaluation prompt
    prompt = evaluation_prompt.format(thought_process=thought_process)

    # Send the request to OpenAI or other LLM via the existing API call infrastructure
    response = send_request(prompt)  # Assuming send_request handles API call, response parsing, and errors

    # Ensure valid response format
    if 'score' in response:
        try:
            evaluation_score = float(response['score'])
        except ValueError:
            evaluation_score = 0.0  # Fallback if score is not a valid float

        # Compare the score with the confidence threshold and adjust
        if evaluation_score < CONFIG['confidence_threshold']:
            evaluation_score *= 0.9  # Penalize low confidence score
        return max(0, min(1, evaluation_score))  # Keep it between 0 and 1
    
    # If no score is returned, return a default low score
    return 0.0

def process_buffer(buffer):
    formatted_content = ""
    while '**' in buffer:
        parts = buffer.split('**', 2)
        if len(parts) >= 2:
            formatted_content += format_bold_text(parts[0] + '**' + parts[1] + '**')
            buffer = ''.join(parts[2:])
        else:
            break
    return formatted_content, buffer

def stream_format(response, process_func):
    buffer = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            buffer += content
            formatted_content, remaining_buffer = process_func(buffer)
            if formatted_content:
                yield formatted_content
            buffer = remaining_buffer
    
    if buffer:
        yield format_bold_text(buffer)

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