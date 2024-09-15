# PyThoughtChain

PyThoughtChain is a Python-based chat application that utilizes the OpenAI API to provide a conversational interface with advanced chain of thought capabilities. This project is a fork of the [ReflectionAnyLLM](https://github.com/antibitcoin/ReflectionAnyLLM) project, which was originally developed in PHP.

## Features

- Determines the appropriate task type (product development, scientific research, or creative writing) and evaluation criteria based on the user's input.
- Generates a detailed thought process, including consideration of opposing viewpoints and potential counterarguments.
- Provides a confidence score for the generated thought process.
- Displays a mind map visualization of the thought process.
- Allows users to provide feedback and refine the thought process iteratively.
- Generates a final answer based on the accumulated thought process and evaluation criteria.

## Use Cases

- Product development: Brainstorm and evaluate ideas for new products or features, considering market trends, user needs, and technological innovations.
- Scientific research: Propose hypotheses, design experiments, and analyze research findings using the scientific method.
- Creative writing: Develop compelling characters, craft engaging narratives, and apply literary devices to your writing projects.
- General knowledge: Explore a wide range of topics and receive clear, concise, and helpful information from the AI assistant.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/devinambron/PyThoughtChain.git
   ```
2. Change to the project directory:
   ```
   cd PyThoughtChain
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Open the `main.py` file and update the `OpenAI` configuration with your own API key and base URL.

   ```python
   client = OpenAI(base_url="http://localhost:1234/v1", api_key="your-api-key")
   ```

2. Run the application:
   ```
   python main.py
   ```
3. Follow the on-screen instructions to interact with the chat application.

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