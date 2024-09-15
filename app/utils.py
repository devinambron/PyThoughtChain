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

def calculate_confidence_score(thought_process):
    confidence_keywords = ['certain', 'confident', 'sure', 'likely', 'probable', 'definitely', 'undoubtedly']
    uncertainty_keywords = ['uncertain', 'unsure', 'maybe', 'perhaps', 'possible', 'might', 'could']

    confidence_score = sum(thought_process.lower().count(word) for word in confidence_keywords)
    uncertainty_score = sum(thought_process.lower().count(word) for word in uncertainty_keywords)

    total_words = len(thought_process.split())
    if total_words == 0:
        return 0

    confidence_ratio = (confidence_score - uncertainty_score) / total_words
    normalized_score = (confidence_ratio + 0.1) / 0.2
    return max(0, min(1, normalized_score))

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