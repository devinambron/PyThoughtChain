# PyThoughtChain

PyThoughtChain is a Python-based chat application that utilizes the OpenAI API to provide a conversational interface with advanced chain of thought capabilities.

![Sample](https://github.com/devinambron/PyThoughtChain/blob/main/assets/example.png)

## Features

- Determines the appropriate task type (product development, scientific research, creative writing, coding, or general) based on the user's input.
- Generates a detailed thought process using a structured approach tailored to the task type.
- Provides a confidence score for the generated thought process.
- Displays a mind map visualization of the thought process.
- Allows users to provide feedback and refine the thought process iteratively.
- Generates a final answer based on the accumulated thought process and evaluation criteria.
- Supports streaming responses for real-time interaction.

## Task Types and Thought Processes

PyThoughtChain supports the following task types, each with a specialized thought process:

1. Product Development
2. Scientific Research
3. Creative Writing
4. Coding
5. General Problem Solving

Each task type follows a structured approach to ensure a logical flow of thoughts and comprehensive analysis.

## Confidence Scoring

The application calculates a confidence score for each thought iteration based on:

- Presence of confidence and uncertainty keywords
- Iteration progress
- Self-evaluation score

This score helps determine when to stop the iteration process and proceed to the final answer.

## Mind Map Generation

PyThoughtChain generates a simple text-based mind map of the thought process, providing a visual representation of the ideas and their relationships.

## User Interaction

Users can provide feedback after each thought iteration, allowing for refinement of the process. They can also choose to finalize the answer at any point.

## Use Cases

- Product development: Brainstorm and evaluate ideas for new products or features.
- Scientific research: Propose hypotheses, design experiments, and analyze research findings.
- Creative writing: Develop characters, craft narratives, and apply literary devices.
- Coding: Solve programming problems with a structured approach.
- General knowledge: Explore a wide range of topics with a logical problem-solving approach.


## Installation

1. Clone the repository:
   ```
   git clone https://github.com/devinambron/PyThoughtChain.git
   ```
2. Change to the project directory:
   ```
   cd PyThoughtChain
   ```
3. Run the setup script:
   ```
   python setup.py
   ```
4. Run the application:
   ```
   python -m app.main
   ```

## Usage


1. Run the application:
   ```
   python -m app.main
   ```
2. Follow the on-screen instructions to interact with the chat application.

**Note:** This application has been tested with the LM Studio on an M1 Pro Max processor using the latest Llama3.1-8B model. Caution is advised when using any APIs with non-locally hosted models due to the potential for high token counts, which may result in unexpected behavior or costs. Use this application at your own risk if you are not using a local language model.

## Contributing

If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the original repository.

## License

This project is licensed under the [MIT License](LICENSE).

**Attribution:** This project was originally based on [ReflectionAnyLLM](https://github.com/antibitcoin/ReflectionAnyLLM), which was developed in PHP.
