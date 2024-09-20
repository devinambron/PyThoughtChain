import os
from app.services.openai_service import call_openai, prepare_messages
from app.prompts import get_problem_solving_framework_prompt, get_thought_process_prompt
from app.utils import stream_format, process_buffer, BOLD, GREEN, CYAN, RED, YELLOW, RESET

def chat():
    chat_history = []
    
    if os.environ.get('VERBOSE_LOGGING') == '1':
        openai_base_url = os.getenv('OPENAI_BASE_URL', 'Default URL not set')
        print(f"{BOLD}{YELLOW}Verbose: OpenAI Base URL: {openai_base_url}{RESET}")

    print(f"{BOLD}{GREEN}Welcome to PyThoughtChain.{RESET}")
    print(f"Type your messages below. Type 'exit' to quit the application.")

    try:
        while True:
            user_message = input(f"{BOLD}{CYAN}You: {RESET}").strip()
            
            if user_message.lower() == 'exit':
                print(f"{BOLD}{GREEN}Exiting chat...{RESET}")
                break

            if not user_message:
                print(f"{BOLD}{RED}Error: Empty message.{RESET}")
                continue

            # Determine problem-solving framework
            framework_prompt = get_problem_solving_framework_prompt(user_message)
            framework_messages = prepare_messages(chat_history, user_message, framework_prompt)
            framework_response = call_openai(framework_messages, stream=False)
            
            if isinstance(framework_response, dict) and 'error' in framework_response:
                print(f"{BOLD}{RED}Error: {framework_response['error']}{RESET}")
                continue

            framework = framework_response.choices[0].message.content.strip()
            print(f"\n{BOLD}{YELLOW}=== Problem-Solving Framework ==={RESET}")
            print(f"{BOLD}{CYAN}{framework}{RESET}")

            thought_process = ""
            iteration = 1
            max_iterations = 20  # Increased for persistence
            
            while iteration <= max_iterations:
                # Prepare the system prompt and messages
                system_prompt = get_thought_process_prompt(iteration=iteration, framework=framework, thought_process=thought_process)
                messages = prepare_messages(chat_history, user_message, system_prompt)
                
                # Call OpenAI and stream the response
                response = call_openai(messages)
                
                if isinstance(response, dict) and 'error' in response:
                    print(f"{BOLD}{RED}Error: {response['error']}{RESET}")
                    break

                new_thoughts = ""
                print(f"\n{BOLD}{YELLOW}=== Thought Process (Iteration {iteration}) ==={RESET}")
                for formatted_content in stream_format(response, process_buffer):
                    print(formatted_content, end="", flush=True)
                    new_thoughts += formatted_content
                print()

                thought_process += f"\n\nIteration {iteration}:\n{new_thoughts}"

                # Check for solution or dead end
                if "SOLUTION FOUND:" in new_thoughts:
                    break
                elif "DEAD END:" in new_thoughts:
                    print(f"\n{BOLD}{YELLOW}Encountered a dead end. Generating new approach...{RESET}")
                    continue

                iteration += 1

            # Final answer generation
            final_prompt = f"Based on the following thought process, provide a concise final answer:\n\n{thought_process}"
            final_messages = prepare_messages(chat_history, user_message, final_prompt)
            final_response = call_openai(final_messages, stream=True)
            
            if isinstance(final_response, dict) and 'error' in final_response:
                print(f"{BOLD}{RED}Error: {final_response['error']}{RESET}")
                continue

            print(f"\n{BOLD}{YELLOW}=== Final Answer ==={RESET}")
            for formatted_content in stream_format(final_response, process_buffer):
                print(formatted_content, end="", flush=True)
            print()

            # Update chat history
            chat_history.append({'sender': 'user', 'text': user_message})
            chat_history.append({'sender': 'assistant', 'text': thought_process})

    except KeyboardInterrupt:
        print(f"\n{BOLD}{RED}Chat interrupted. Exiting gracefully...{RESET}")
    except Exception as e:
        print(f"{BOLD}{RED}An unexpected error occurred: {str(e)}{RESET}")

    finally:
        # Clean up any resources or finalize your chat logic here...
        pass