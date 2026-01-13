import tkinter as tk
from tkinter import font
import threading
import requests
import json
from calc.api.main import create_app


class CalculatorGUI:
    # MacBook calculator style GUI

    def __init__(self, root):
        # Initialize GUI
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.configure(bg="#333333")
        self.root.resizable(False, False)
        
        self.api_url = "http://localhost:5001"
        self.expression = ""
        self.just_evaluated = False  # Track if we just got a result
        
        self.setup_ui()
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Return>", lambda e: self.on_button_click("="))
        self.root.bind("<KP_Enter>", lambda e: self.on_button_click("="))

    def setup_ui(self):
        # Create display and buttons
        self.create_display()
        self.create_buttons()

    def create_display(self):
        # Display for expression and result
        display_frame = tk.Frame(self.root, bg="#333333")
        display_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=False)
        
        self.display = tk.Label(
            display_frame,
            text="0",
            font=("Helvetica", 48, "bold"),
            bg="#333333",
            fg="white",
            anchor="e",
            justify="right"
        )
        self.display.pack(fill=tk.BOTH, expand=True)

    def create_buttons(self):
        # Button layout (MacBook style)
        button_frame = tk.Frame(self.root, bg="#333333")
        button_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        buttons = [
            ["C", "±", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["0", ".", "="],
            ["H"],  # History button
        ]
        
        for row in buttons:
            row_frame = tk.Frame(button_frame, bg="#333333")
            row_frame.pack(fill=tk.BOTH, expand=True, pady=5)
            
            for btn_text in row:
                self.create_button(row_frame, btn_text)

    def create_button(self, parent, text):
        # Create individual button
        if text == "H":
            # History button spans full width
            btn = tk.Button(
                parent,
                text="History",
                font=("Helvetica", 18, "bold"),
                bg="white",
                fg="black",
                command=lambda: self.on_button_click(text),
                activebackground="#e0e0e0",
                bd=0,
                highlightthickness=0
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2)
        elif text == "0":
            # Zero button spans 2 columns
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 24, "bold"),
                bg="white",
                fg="black",
                command=lambda: self.on_button_click(text),
                activebackground="#e0e0e0",
                bd=0,
                highlightthickness=0
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=2, padx=2)
        elif text in ["C", "±", "%"]:
            # Function buttons (white)
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 24, "bold"),
                bg="white",
                fg="black",
                command=lambda: self.on_button_click(text),
                activebackground="#e0e0e0",
                bd=0,
                highlightthickness=0
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2)
        elif text in ["÷", "×", "−", "+", "="]:
            # Operator buttons (white)
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 24, "bold"),
                bg="white",
                fg="black",
                command=lambda: self.on_button_click(text),
                activebackground="#e0e0e0",
                bd=0,
                highlightthickness=0
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2)
        else:
            # Number buttons (white)
            btn = tk.Button(
                parent,
                text=text,
                font=("Helvetica", 24, "bold"),
                bg="white",
                fg="black",
                command=lambda: self.on_button_click(text),
                activebackground="#8b8b89",
                bd=0,
                highlightthickness=0
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=1, padx=2)

    def on_button_click(self, char):
        # Handle button clicks
        if char == "C":
            self.expression = ""
            self.just_evaluated = False
            self.update_display("0")
        elif char == "H":
            self.show_history()
        elif char == "=":
            self.evaluate()
        elif char == "±":
            if self.expression and self.expression != "0":
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
            self.update_display(self.expression or "0")
            self.just_evaluated = False
        elif char == "÷":
            self.append_operator("/")
        elif char == "×":
            self.append_operator("*")
        elif char == "−":
            self.append_operator("-")
        elif char == "+":
            self.append_operator("+")
        elif char == ".":
            if "." not in self.expression.split()[-1] if self.expression else True:
                self.expression += "."
            self.update_display(self.expression or "0")
            self.just_evaluated = False
        else:
            # Number button
            # If we just evaluated, start fresh with this number
            if self.just_evaluated:
                self.expression = char
                self.just_evaluated = False
            else:
                if self.expression == "0":
                    self.expression = char
                else:
                    self.expression += char
            self.update_display(self.expression)

    def on_key_press(self, event):
        # Handle keyboard input
        char = event.char
        
        if char in "0123456789":
            self.on_button_click(char)
        elif char == ".":
            self.on_button_click(".")
        elif char == "+":
            self.on_button_click("+")
        elif char == "-":
            self.on_button_click("−")
        elif char == "*":
            self.on_button_click("×")
        elif char == "/":
            self.on_button_click("÷")
        elif event.keysym == "Return" or event.keysym == "KP_Enter":  # enter key
            self.on_button_click("=")
        elif char == "=":  # equals sign
            self.on_button_click("=")
        elif char.lower() == "c":  # clear
            self.on_button_click("C")
        elif event.keysym == "BackSpace":
            # Delete last character
            self.expression = self.expression[:-1]
            self.update_display(self.expression or "0")
            self.just_evaluated = False

    def append_operator(self, op):
        # Append operator to expression
        if self.expression and not self.expression.endswith((" ", "+", "-", "*", "/")):
            self.expression += " " + op + " "
            self.update_display(self.expression)
        self.just_evaluated = False

    def evaluate(self):
        # Evaluate the expression via API
        if not self.expression:
            return
        
        try:
            response = requests.post(
                f"{self.api_url}/evaluate",
                json={"expression": self.expression},
                timeout=5
            )
            data = response.json()
            
            if data.get("status") == "success":
                result = data.get("result")
                self.expression = result
                self.update_display(result)
                self.just_evaluated = True
            else:
                self.update_display("Error")
                self.expression = ""
                self.just_evaluated = False
        except requests.exceptions.RequestException as e:
            self.update_display("API Error")
            self.expression = ""
            self.just_evaluated = False

    def show_history(self):
        # Show history in a popup window
        try:
            response = requests.get(f"{self.api_url}/history", timeout=5)
            data = response.json()
            history = data.get("history", [])
            
            # Create popup window
            history_window = tk.Toplevel(self.root)
            history_window.title("History")
            history_window.geometry("400x400")
            history_window.configure(bg="#333333")
            
            # Title label
            title_label = tk.Label(
                history_window,
                text="Last 10 Calculations",
                font=("Helvetica", 16, "bold"),
                bg="#333333",
                fg="white",
                pady=10
            )
            title_label.pack()
            
            # History list
            if not history:
                no_history_label = tk.Label(
                    history_window,
                    text="No history available",
                    font=("Helvetica", 14),
                    bg="#333333",
                    fg="white"
                )
                no_history_label.pack(pady=20)
            else:
                # Create scrollable frame
                canvas = tk.Canvas(history_window, bg="#333333", highlightthickness=0)
                scrollbar = tk.Scrollbar(history_window, orient="vertical", command=canvas.yview)
                scrollable_frame = tk.Frame(canvas, bg="#333333")
                
                scrollable_frame.bind(
                    "<Configure>",
                    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                )
                
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                
                # Add history items
                for i, entry in enumerate(history, 1):
                    expr = entry.get("expression", "")
                    result = entry.get("result", "")
                    
                    entry_frame = tk.Frame(scrollable_frame, bg="#333333")
                    entry_frame.pack(fill=tk.X, padx=20, pady=5)
                    
                    history_label = tk.Label(
                        entry_frame,
                        text=f"{i}. {expr} = {result}",
                        font=("Helvetica", 12),
                        bg="#333333",
                        fg="white",
                        anchor="w"
                    )
                    history_label.pack(fill=tk.X)
                
                canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
        except requests.exceptions.RequestException as e:
            # Show error in main display briefly
            self.update_display("History Error")

    def update_display(self, text):
        # Update display label
        self.display.config(text=text)


def start_api_server():
    # Start Flask API in background thread
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=5001, use_reloader=False)


def main():
    # Start API server in background thread
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    
    # Start GUI
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
