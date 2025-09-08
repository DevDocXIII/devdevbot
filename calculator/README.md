
# DevDevBot

DevDevBot is a code assistant and calculator project powered by Gemini AI. It provides a command-line interface for code assistance and a calculator app, with modular helpers for file operations and Python execution.

## Project Structure

```
devdevbot/
│
├── main.py                # Entry point for DevDevBot (code assistant)
├── config.py              # Configuration constants
├── prompts.py             # System prompt for Gemini
├── call_function.py       # Maps function calls to helpers
├── tests.py               # Test cases for helpers
├── conversation.log       # Log file for assistant responses
│
├── functions/             # Modular helper functions
│   ├── cache.py
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python.py
│   ├── write_file_content.py
│   ├── utils.py
│
└── calculator/            # Calculator app
		├── main.py            # Entry point for calculator
		├── tests.py           # Calculator tests
		├── pkg/
		│   ├── calculator.py  # Calculator logic
		│   ├── render.py      # Renders results in a box
		└── src/, lorem.txt, README.md, etc.
```

## Main Program Flow

### DevDevBot (main.py)

1. **Startup**: Loads API key, configuration, and initializes Gemini client.
2. **User Input**: Accepts a prompt from the command line.
3. **Main Loop**: 
		- Sends prompt to Gemini.
		- Receives response, which may include function calls (list files, read files, run Python, write files).
		- Executes requested functions via helpers in `functions/`.
		- Logs assistant responses.
		- Continues for up to `MAX_ITERATIONS` or until completion.

### Calculator App (calculator/main.py)

1. **Startup**: Instantiates `Calculator` and parses command-line arguments.
2. **Expression Evaluation**: 
		- Evaluates infix math expressions (e.g., `"3 + 5"`).
		- Uses `Calculator` class for parsing and computation.
		- Renders result using `render.py` (pretty box output).

## Key Modules

- **functions/**: Each file provides a helper for a specific operation (listing files, reading content, running Python, writing files, caching, argument normalization).
- **call_function.py**: Maps Gemini function calls to helpers, filters arguments, and handles errors.
- **prompts.py**: Defines the system prompt and rules for Gemini's behavior.
- **config.py**: Centralizes configuration (working directory, model, log path, etc.).

## How to Contribute

- **Add new helpers** in `functions/` for new operations.
- **Update `call_function.py`** to map new functions and schemas.
- **Document new features** in this README and in code comments.
- **Run tests** in `tests.py` and `calculator/tests.py` to validate changes.
- **Keep code modular** and follow the flow described above.

## Getting Started

- Run the assistant:
	```bash
	python main.py "your prompt here"
	```
- Run the calculator:
	```bash
	cd calculator
	python main.py "3 + 5"
	```

---


