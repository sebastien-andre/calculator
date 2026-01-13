# Calculator

A multi-interface calculator application supporting natural math expression evaluation with a CLI, REST API, and GUI.

## Usage

### CLI
```bash
python -m calc.cli.main
```
Start the CLI to interactively evaluate math expressions.

### API Server
```bash
python -m calc.api.main
```
Runs on `http://localhost:5000` with endpoints for programmatic expression evaluation.

### GUI
```bash
python -m calc.gui.main
```
Launch the graphical interface for desktop calculator functionality.

### Tests
```bash
PYTHONPATH=. pytest -v
```
Run all tests with verbose output. Use `PYTHONPATH=. pytest tests/core/` to run specific test suites.

## Features

- **Expression Evaluation**: Evaluate mathematical expressions with proper operator precedence and parentheses support
- **Command Line Interface**: Interactive CLI for quick calculations
- **REST API**: Programmatic access to evaluation, history, and state management
- **Graphical Interface**: Desktop GUI application for user-friendly interaction

## API Endpoints

- `POST /evaluate` - Evaluate a math expression
- `GET /history` - Get last 10 evaluations
- `POST /clear` - Clear evaluation history
- `POST /reset` - Reset calculator state
