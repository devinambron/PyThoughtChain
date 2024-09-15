import re

BOLD = '\033[1m'
RED = '\033[31m'
GREEN = '\033[32m'
CYAN = '\033[36m'
YELLOW = '\033[33m'
RESET = '\033[0m'

def format_bold_text(text):
    formatted_text = ""
    bold_start = -1
    i = 0
    while i < len(text):
        if text[i:i+2] == '**':
            if bold_start == -1:
                formatted_text += BOLD
                bold_start = i
            else:
                formatted_text += RESET
                bold_start = -1
            i += 2
        else:
            formatted_text += text[i]
            i += 1
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