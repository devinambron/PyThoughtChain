task_specific_prompts = {
    'product_development': "You are an expert in product development. Consider market trends, user needs, and technological innovations.",
    'scientific_research': "You are a seasoned scientist. Apply the scientific method, consider existing literature, and propose hypotheses.",
    'creative_writing': "You are a creative writer. Use literary devices, develop compelling characters, and craft engaging narratives.",
    'general': "You are a knowledgeable assistant. Provide clear, concise, and helpful information on a wide range of topics."
}

def get_thought_process_prompt(iteration, task_type, previous_thoughts=None):
    prompt = f"""Help solve the user's request by generating a detailed step-by-step plan.
Please ensure that your thought process is clear and detailed.
This is iteration {iteration} of the thought process.
{'Refine and expand upon the previous thoughts.' if iteration > 1 else ''}
Consider opposing viewpoints and potential counterarguments.
Explore hypothetical "what-if" scenarios to test the robustness of your proposed solutions.
Incorporate quantitative analysis where appropriate.
{task_specific_prompts.get(task_type, '')}
Do not return a final answer, just return the thought process."""
    return prompt

def get_final_answer_prompt(thought_process, evaluation_criteria):
    return f"""You are an AI assistant providing a final answer based on the following thought process:

{thought_process}

Evaluate the solution based on these criteria: {', '.join(evaluation_criteria)}
Provide citations for any factual claims or data points.
Consider potential limitations or areas for further research.
Provide a concise and clear final answer to the user's request."""