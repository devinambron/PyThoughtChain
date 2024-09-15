task_specific_prompts = {
    'product_development': "You are an expert in product development. Consider market trends, user needs, and technological innovations.",
    'scientific_research': "You are a seasoned scientist. Apply the scientific method, consider existing literature, and propose hypotheses.",
    'creative_writing': "You are a creative writer. Use literary devices, develop compelling characters, and craft engaging narratives.",
    'general': "You are a knowledgeable assistant. Provide clear, concise, and helpful information on a wide range of topics.",
    'coding': "You are an experienced programmer. Write clean, efficient, and well-documented code using best practices and standard libraries."
}

def get_thought_process_prompt(iteration=1, task_type='general'):
    task_type = task_type if task_type in task_specific_prompts else 'general'

    return f"""This is iteration {iteration} of the thought process.
{'Refine and expand upon the previous thoughts.' if iteration > 1 else ''}
Consider opposing viewpoints and potential counterarguments.
Explore hypothetical "what-if" scenarios to test the robustness of your proposed solutions.
Incorporate quantitative analysis where appropriate.
{task_specific_prompts[task_type]}
Do not return a final answer, just return the thought process."""

# Function to generate the final answer prompt
def get_final_answer_prompt(thought_process, evaluation_criteria):
    return f"""You are an AI assistant providing a final answer based on the following thought process:

{thought_process}

Evaluate the solution based on these criteria: {', '.join(evaluation_criteria)}.
Provide citations for any factual claims or data points.
Consider potential limitations or areas for further research.
Provide a concise and clear final answer to the user's request."""