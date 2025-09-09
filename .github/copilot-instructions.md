# Copilot Instructions for DevDevBot

This guide helps AI coding agents work productively in the DevDevBot codebase. It summarizes architecture, workflows, and project-specific conventions.

## Architecture Overview
- **Main Components:**
  - `main.py`: Entry for DevDevBot code assistant. Handles CLI, user prompts, Gemini API, and function call routing.
  - `functions/`: Modular helpers for file operations, Python execution, caching, and utilities. Each file is a single-responsibility helper.
  - `call_function.py`: Maps Gemini function calls to helpers, normalizes arguments, and handles errors.
  - `prompts.py`: System prompt and rules for Gemini agent behavior.
  - `config.py`: Centralized configuration (paths, model, log file, etc.).
  - `conversation.log`: Logs assistant responses and actions.
  - `calculator/`: Standalone calculator app with its own entry (`main.py`), logic (`pkg/calculator.py`), rendering (`pkg/render.py`), and tests.

## Data Flow & Service Boundaries
- User input flows through `main.py` → Gemini API → function calls → `call_function.py` → helpers in `functions/`.
- Calculator app is independent; uses its own CLI and logic.
- All file operations, Python execution, and caching are handled via helpers in `functions/`.

## Developer Workflows
- **Run DevDevBot assistant:**
  ```bash
  python main.py "your prompt here"
  ```
- **Run calculator:**
  ```bash
  cd calculator
  python main.py "3 + 5"
  ```
- **Run tests:**
  - For helpers: `python tests.py`
  - For calculator: `cd calculator && python tests.py`
- **Add new helper:**
  - Create a new file in `functions/`.
  - Map it in `call_function.py`.
  - Add tests in `tests.py`.

## Project-Specific Patterns & Conventions
- **Helpers:** Each helper in `functions/` should be single-responsibility and stateless.
- **Function Mapping:** All Gemini function calls are routed via `call_function.py`.
- **Logging:** All assistant actions are logged in `conversation.log`.
- **Configuration:** Use `config.py` for all constants and paths.
- **Calculator:** Uses infix expression parsing and pretty output via `render.py`.

## Integration Points
- **Gemini API:** Used for code assistance and function call generation.
- **CLI:** Both DevDevBot and calculator are CLI-driven.
- **No external build system:** All scripts are run directly with Python.

## Key Files & Directories
- `main.py`, `call_function.py`, `functions/`, `config.py`, `prompts.py`, `conversation.log`, `calculator/`

---

**Review and update this file as the codebase evolves.**
