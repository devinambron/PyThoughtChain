import os
from app.config import CONFIG
from app.utils import (
    stream_format, process_buffer, format_bold_text, get_user_feedback,
    calculate_confidence_score, generate_mind_map, BOLD, RED, GREEN, CYAN, YELLOW, RESET
)
from app.services.openai_service import call_openai, prepare_messages, determine_task_type_and_criteria
from app.prompts import get_task_type_prompt, get_thought_process_prompt, get_final_answer_prompt

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

            # Determine task type and evaluation criteria
            task_type, evaluation_criteria = determine_task_type_and_criteria(user_message)
            print(f"\n{BOLD}{YELLOW}=== Task Type ==={RESET}")
            print(f"{BOLD}{CYAN}{task_type}{RESET}")
            print(f"\n{BOLD}{YELLOW}=== Evaluation Criteria ==={RESET}")
            print(f"{BOLD}{CYAN}{', '.join(evaluation_criteria)}{RESET}")

            thought_process = ""
            iteration = 1
            max_iterations = CONFIG['max_iterations']
            iterations_before_feedback = CONFIG['iterations_before_feedback']

            while iteration <= max_iterations:
                # Prepare the system prompt and messages
                system_prompt = get_thought_process_prompt(iteration=iteration, task_type=task_type)
                messages = prepare_messages(chat_history, user_message, system_prompt, thought_process)
                
                if os.environ.get('VERBOSE_LOGGING') == '1':
                    print(f"Prepared messages: {messages}")
                
                # Call OpenAI and stream the response
                response = call_openai(messages)
                
                if isinstance(response, dict) and 'error' in response:
                    print(f"{BOLD}{RED}Error: {response['error']}{RESET}")
                    break

                new_thoughts = ""
                print(f"\n{BOLD}{YELLOW}=== Thought Process (Iteration {iteration}) ==={RESET}", end="", flush=True)
                print(f"")
                for formatted_content in stream_format(response, process_buffer):
                    print(formatted_content, end="", flush=True)
                    new_thoughts += formatted_content
                print()

                # Calculate and display the confidence score
                confidence_score = calculate_confidence_score(new_thoughts)
                print(f"\n{BOLD}{YELLOW}=== Confidence Score ==={RESET}")
                print(f"{BOLD}{CYAN}{confidence_score:.2f}{RESET}")

                # Generate and display the mind map
                mind_map = generate_mind_map(new_thoughts)
                print(f"\n{BOLD}{YELLOW}=== Mind Map ==={RESET}\n{BOLD}{CYAN}{mind_map}{RESET}")

                thought_process += f"\n\nIteration {iteration}:\n{new_thoughts}"

                # Check if confidence score exceeds threshold
                if confidence_score > CONFIG['confidence_threshold']:
                    break

                # User feedback mechanism
                if iterations_before_feedback <= 0:
                    print(f"{BOLD}{RED}Error: iterations_before_feedback must be a positive integer.{RESET}")
                    return

                if iteration > 0 and iteration % iterations_before_feedback == 0:
                    user_feedback = get_user_feedback()
                    if user_feedback == 'finalize':
                        break
                    elif user_feedback:
                        user_message += f"\n\nUser feedback: {user_feedback}"

                iteration += 1

            # Final answer generation and streaming response
            final_system_prompt = get_final_answer_prompt(thought_process, evaluation_criteria)
            final_response = call_openai(prepare_messages(chat_history, user_message, final_system_prompt), stream=True)
            
            if isinstance(final_response, dict) and 'error' in final_response:
                print(f"{BOLD}{RED}Error: {final_response['error']}{RESET}")
                continue

            final_answer = ""
            print(f"\n{BOLD}{YELLOW}=== Final Answer ==={RESET}", end="", flush=True)
            buffer = ""
            for chunk in final_response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    buffer += content
                    formatted_content, remaining_buffer = process_buffer(buffer)
                    if formatted_content:
                        print(formatted_content, end="", flush=True)
                        final_answer += formatted_content
                    buffer = remaining_buffer
            
            if buffer:
                formatted_content = format_bold_text(buffer)
                print(formatted_content, end="", flush=True)
                final_answer += formatted_content
            print()  # New line after streaming is complete

            # Update chat history
            chat_history.append({'sender': 'user', 'text': user_message})
            chat_history.append({'sender': 'assistant', 'text': final_answer})
    
    except KeyboardInterrupt:
        print(f"\n{BOLD}{RED}Chat interrupted. Exiting gracefully...{RESET}")
        return
    except ConnectionError as e:
        print(f"{BOLD}{RED}Failed to connect to a resource: {str(e)}{RESET}")
    except TimeoutError as e:
        print(f"{BOLD}{RED}Timeout occurred: {str(e)}{RESET}")
    except Exception as e:
        print(f"{BOLD}{RED}An unexpected error occurred: {str(e)}{RESET}")

    finally:
        # Clean up any resources or finalize your chat logic here...
        pass