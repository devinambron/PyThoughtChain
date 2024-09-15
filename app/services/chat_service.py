from app.utils import format_bold_text, get_user_feedback, calculate_confidence_score, generate_mind_map, BOLD, RED, GREEN, CYAN, YELLOW, RESET
from app.services.openai_service import call_openai, prepare_messages, determine_task_type_and_criteria
from app.prompts import get_thought_process_prompt, get_final_answer_prompt

def chat():
    chat_history = []
    
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
                system_prompt = get_thought_process_prompt(iteration, task_type)
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

            final_system_prompt = get_final_answer_prompt(thought_process, evaluation_criteria)
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