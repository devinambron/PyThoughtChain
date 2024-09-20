task_specific_prompts = {
    'product_development': """
    You are an expert in product development. To ensure a clear, methodical thought process, follow these steps:
    1. Identify the core problem or need based on current market trends and user pain points.
    2. Explore and evaluate technological innovations that can address these needs.
    3. Develop potential solutions or products.
    4. Compare and contrast solutions by evaluating cost, feasibility, and potential market reception.
    5. Propose a final solution based on your analysis.
    """,
    'scientific_research': """
    You are a seasoned scientist. To conduct a thorough thought process, use this structure:
    1. Clearly define the research question or hypothesis.
    2. Review and summarize existing literature to frame your hypothesis.
    3. Outline a detailed methodology, explaining the rationale behind each step.
    4. Consider potential variables, controls, and limitations.
    5. Predict potential outcomes and suggest next steps in research.
    """,
    'creative_writing': """
    You are a creative writer. Use the following structure to guide your process:
    1. Define the core theme or emotion you want to explore.
    2. Introduce and develop the main character(s) with motivations, conflicts, and backstory.
    3. Outline the story arc, including the climax and resolution.
    4. Use literary devices (such as metaphor, symbolism, or foreshadowing) to enhance the narrative.
    5. Conclude by suggesting how the story reflects on or challenges the initial theme.
    """,
    'general': """
    You are a knowledgeable assistant. To solve general problems or answer questions, follow these steps:
    1. Clarify the user's request and break it down into smaller parts if necessary.
    2. Present any background information or context that might be relevant.
    3. Explore multiple potential solutions or viewpoints.
    4. Weigh the pros and cons of each solution.
    5. Propose a final recommendation based on the analysis.
    """,
    'coding': """
    You are an experienced programmer. To solve programming problems, follow this thought process:
    1. Clarify the coding task and identify the requirements.
    2. Break down the task into smaller, manageable parts.
    3. Write the code for each part while explaining the reasoning for your approach.
    4. Ensure the code follows best practices and is optimized for readability and efficiency.
    5. Test the solution, considering edge cases, and propose improvements if necessary.
    """
}

def get_task_type_prompt(user_message):
    return f"""Analyze the following user message and determine the most appropriate task type from the list below:
    - product_development
    - scientific_research
    - creative_writing
    - coding
    - general

User message: "{user_message}"

Respond with only the task type, in lowercase, without any additional text or explanation."""

def get_thought_process_prompt(iteration=1, task_type='general'):
    task_type = task_type if task_type in task_specific_prompts else 'general'

    return f"""This is iteration {iteration} of the thought process.
{'Refine and expand upon the previous thoughts.' if iteration > 1 else ''}
You will follow the structured process laid out below to ensure a logical flow:
{task_specific_prompts[task_type]}
Explore hypothetical "what-if" scenarios and potential counterarguments.
Incorporate quantitative analysis where appropriate.
Do not return a final answer, just return the step-by-step thought process."""

def get_final_answer_prompt(thought_process, evaluation_criteria):
    return f"""You are an AI assistant providing a final answer based on the following thought process:

{thought_process}

Evaluate the solution based on these criteria: {', '.join(evaluation_criteria)}.
Provide citations for any factual claims or data points.
Consider potential limitations or areas for further research.
Provide a concise and clear final answer to the user's request."""

evaluation_prompt = """
Evaluate the following thought process on a scale from 0 to 1, where 0 is completely flawed and 1 is perfect:

{thought_process}

Consider the following criteria:
1. Logical coherence
2. Depth of analysis
3. Consideration of alternative viewpoints
4. Use of relevant information
5. Clarity of expression

Provide a single float value between 0 and 1 as the score, without any additional explanation.
"""

def get_problem_solving_framework_prompt(user_message):
    return f"""Analyze the following user message and determine the most appropriate problem-solving framework to use:
User message: "{user_message}"
Consider frameworks such as:
1. Scientific method
2. Design thinking
3. SWOT analysis
4. Root cause analysis
5. Six Sigma DMAIC
6. Agile methodology
7. Critical thinking framework
8. Systems thinking
9. Decision matrix
10. Cost-benefit analysis
Respond with only the name of the most suitable framework, without any additional text or explanation."""

def get_framework_steps(framework):
    steps = {
        "Scientific method": [
            "Define the question",
            "Gather information and resources",
            "Form hypothesis",
            "Perform experiment and collect data",
            "Analyze data",
            "Interpret results and draw conclusions",
            "Publish results"
        ],
        "Design thinking": [
            "Empathize",
            "Define",
            "Ideate",
            "Prototype",
            "Test"
        ],
        "SWOT analysis": [
            "Identify Strengths",
            "Identify Weaknesses",
            "Identify Opportunities",
            "Identify Threats",
            "Analyze SWOT matrix",
            "Develop strategies"
        ],
        "Root cause analysis": [
            "Define the problem",
            "Collect data",
            "Identify possible causal factors",
            "Identify root cause(s)",
            "Recommend and implement solutions",
            "Verify solution effectiveness"
        ],
        "Six Sigma DMAIC": [
            "Define",
            "Measure",
            "Analyze",
            "Improve",
            "Control"
        ],
        "Agile methodology": [
            "Plan",
            "Design",
            "Develop",
            "Test",
            "Deploy",
            "Review",
            "Launch"
        ],
        "Critical thinking framework": [
            "Identify the problem",
            "Gather information",
            "Analyze and evaluate",
            "Identify assumptions",
            "Consider alternatives",
            "Develop conclusions",
            "Reflect on the process"
        ],
        "Systems thinking": [
            "Identify the system",
            "Understand interconnections",
            "Identify leverage points",
            "Develop intervention strategies",
            "Anticipate consequences",
            "Implement and monitor"
        ],
        "Decision matrix": [
            "Identify decision criteria",
            "Weight the criteria",
            "Identify alternatives",
            "Score alternatives",
            "Calculate weighted scores",
            "Select best alternative"
        ],
        "Cost-benefit analysis": [
            "Identify costs and benefits",
            "Monetize all factors",
            "Calculate net present value",
            "Perform sensitivity analysis",
            "Make recommendation"
        ]
    }
    return steps.get(framework, ["Identify the problem", "Analyze", "Propose solutions", "Implement"])

def get_thought_process_prompt(iteration, framework, thought_process):
    steps = get_framework_steps(framework)
    steps_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))
    
    base_prompt = f"""You are using the {framework} framework to solve the given problem. This is iteration {iteration} of the thought process.

Follow these steps:
{steps_str}

Previous thought process:
{thought_process}

Continue the problem-solving process, focusing on the next logical step within the {framework} framework. Be persistent and creative in your approach while adhering to the framework's methodology. If you encounter a dead end, clearly state "DEAD END:" and explain why, then suggest a new approach within the same framework.

If you believe you've found a solution, clearly state "SOLUTION FOUND:" followed by a brief explanation.

Provide your next thoughts and reasoning, explicitly mentioning which step of the {framework} you are currently on:"""
    
    return base_prompt