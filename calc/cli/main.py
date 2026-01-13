from calc.core.session import CalculatorSession
from calc.core.errors import CalcError


class CommandLoop:

    def __init__(self):
        self.session = CalculatorSession()
        self.running = True

    def run(self):
        print("Calculator CLI - Type 'help' for commands, 'quit' to exit")
        
        while self.running:
            try:
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                
                self.handle_command(user_input)
            except KeyboardInterrupt:
                print("\nInterrupted")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")

    def handle_command(self, user_input):
        # route user input to appropriate funciton
        if user_input.lower() == "quit":
            self.running = False
            print("Goodbye")
        elif user_input.lower() == "help":
            self.show_help()
        elif user_input.lower() == "history":
            self.show_history()
        elif user_input.lower() == "clear":
            self.session.clear_history()
            print("History cleared")
        elif user_input.lower() == "reset":
            self.session.reset()
            print("Calculator reset")
        else:
            # try to evaluate as expression
            self.evaluate_expression(user_input)

    def evaluate_expression(self, expr):
        # evaluate and display result
        try:
            result = self.session.evaluate(expr)
            print(f"= {result}")
        except CalcError as e:
            print(f"Error: {e}")

    def show_history(self):
        # display last 10 evaluations
        history = self.session.get_history()
        if not history:
            print("No history")
            return
        
        print("History:")
        for i, entry in enumerate(history, 1):
            print(f"  {i}. {entry['expression']} = {entry['result']}")

    def show_help(self):
        print("""
Commands:
  <expression>  - Evaluate math expression (e.g., 2 + 3 * 4)
  history       - Show last 10 evaluations
  clear         - Clear history
  reset         - Reset calculator state
  help          - Show this message
  quit          - Exit calculator
        """)


def main():
    # entry point
    loop = CommandLoop()
    loop.run()


if __name__ == "__main__":
    main()
