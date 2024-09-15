import openai

client = openai.OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

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