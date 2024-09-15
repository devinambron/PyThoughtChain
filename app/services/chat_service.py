# app/services/chat_service.py

import threading
from PySide6.QtCore import QObject, Signal

# Import necessary functions and configurations
from app.config import CONFIG, save_config
from app.utils import (
    stream_format, process_buffer, format_bold_text, get_user_feedback,
    calculate_confidence_score, generate_mind_map, BOLD, RED, GREEN, CYAN, YELLOW, RESET
)
from app.services.openai_service import call_openai, prepare_messages, determine_task_type_and_criteria
from app.prompts import get_thought_process_prompt, get_final_answer_prompt

class ChatService(QObject):
    # Define signals
    assistant_message = Signal(str)
    error_message = Signal(str)

    def __init__(self):
        super().__init__()
        self.chat_history = []

    def process_user_message(self, user_message):
        # Start a new thread to handle the message
        thread = threading.Thread(target=self._handle_message, args=(user_message,))
        thread.start()

    def _handle_message(self, user_message):
        try:
            if user_message.lower() == 'exit':
                self.assistant_message.emit('<div style="color: #00FF00;">Exiting chat...</div>')
                return

            # Determine task type and evaluation criteria
            task_type, evaluation_criteria = determine_task_type_and_criteria(user_message)
            self.assistant_message.emit(f'<div style="color: #FFFF00;">Task Type: {task_type}</div>')
            self.assistant_message.emit(f'<div style="color: #00FFFF;">Evaluation Criteria: {", ".join(evaluation_criteria)}</div>')

            thought_process = ""
            iteration = 1
            max_iterations = CONFIG.get('max_iterations', 5)  # Default to 5 if not set

            while iteration <= max_iterations:
                system_prompt = get_thought_process_prompt(iteration=iteration, task_type=task_type)
                messages = prepare_messages(self.chat_history, user_message, system_prompt, thought_process)
                
                response = call_openai(messages)
                
                if isinstance(response, dict) and 'error' in response:
                    self.error_message.emit(f'<div style="color: #FF0000;">Error: {response["error"]}</div>')
                    break

                new_thoughts = ""
                self.assistant_message.emit(f'<div style="color: #FFFF00;">Thought Process (Iteration {iteration})</div>')
                for formatted_content in stream_format(response, process_buffer):
                    self.assistant_message.emit(f'<div style="color: #FFFFFF;">{formatted_content}</div>')
                    new_thoughts += formatted_content

                thought_process += f"\n\nIteration {iteration}:\n{new_thoughts}"

                confidence_score = calculate_confidence_score(new_thoughts)
                if confidence_score > CONFIG.get('confidence_threshold', 0.8):  # Default threshold
                    break

                iteration += 1

            final_system_prompt = get_final_answer_prompt(thought_process, evaluation_criteria)
            final_response = call_openai(prepare_messages(self.chat_history, user_message, final_system_prompt), stream=True)
            
            if isinstance(final_response, dict) and 'error' in final_response:
                self.error_message.emit(f'<div style="color: #FF0000;">Error: {final_response["error"]}</div>')
                return

            self.assistant_message.emit('<div style="color: #FFFF00;">Final Answer</div>')
            final_answer = ""
            for chunk in final_response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    self.assistant_message.emit(f'<span>{content}</span>')
                    final_answer += content

            self.chat_history.append({'sender': 'user', 'text': user_message})
            self.chat_history.append({'sender': 'assistant', 'text': final_answer})

        except Exception as e:
            self.error_message.emit(f'<div style="color: #FF0000;">An unexpected error occurred: {str(e)}</div>')