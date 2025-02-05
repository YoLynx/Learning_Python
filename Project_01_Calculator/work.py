import tkinter as tk
import operations  # Import the custom library

def button_click(value):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current + str(value))

def clear_entry():
    entry.delete(0, tk.END)

def backspace():
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(tk.END, current[:-1])

def evaluate():
    try:
        expression = entry.get().replace('^', '**')  # Replace ^ with ** for exponentiation
        result = eval_expression(expression)
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")

def eval_expression(expression):
    try:
        if 'log' in expression:
            x = float(expression.split('log(')[1][:-1])        
            if x <= 0:
                return "Error! Logarithm of non-positive value."    # Error handling for negative values in log.
            return operations.logarithm(x)

        elif 'sin' in expression:
            x = float(expression.split('sin(')[1][:-1])
            return operations.sine(x)

        elif 'cos' in expression:
            x = float(expression.split('cos(')[1][:-1])
            return operations.cosine(x)

        elif 'tan' in expression:
            x = float(expression.split('tan(')[1][:-1])
            result = operations.tangent(x)
            if result == "Error! Tangent undefined.":          # Error handling for tan. eg- tan(90).
                return result   
            return result

        elif '√' in expression:
            x = float(expression.split('√(')[1][:-1])
            if x < 0:
                return "Error! Square root of negative number."    # negative values in root.
            return operations.square_root(x)

        elif '1/' in expression:
            x = float(expression.split('1/')[1])
            if x == 0:
                return "Error! Division by zero."                # Division by zero.
            return operations.reciprocal(x)

        elif '%' in expression:
            x, y = map(float, expression.split('%'))
            if y == 0:
                return "Error! Modulus by zero."
            return operations.modulus(x, y)

        else:
            if '/0' in expression:
                return "Error! Division by zero."
            return eval(expression)

    except Exception as e:
        return f"Error: {str(e)}"


# Initialize the main window
root = tk.Tk()
root.title("Advanced Calculator")
root.geometry("400x650")
root.config(bg="#2e2e2e")

# Entry widget
entry = tk.Entry(root, width=20, font=('Arial', 20), justify=tk.RIGHT, bd=10, bg="#dcdcdc", fg="#333333")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=20)

# Basic buttons
buttons = [
    ('7', '#4da8da'), ('8', '#4da8da'), ('9', '#4da8da'), ('/', '#1976d2'),
    ('4', '#4da8da'), ('5', '#4da8da'), ('6', '#4da8da'), ('*', '#1976d2'),
    ('1', '#4da8da'), ('2', '#4da8da'), ('3', '#4da8da'), ('-', '#1976d2'),
    ('0', '#4da8da'), ('.', '#4da8da'), ('=', '#1976d2'), ('+', '#1976d2')
]

function_buttons = {
    'log': (lambda: button_click('log('), '#b39ddb'), 'sin': (lambda: button_click('sin('), '#b39ddb'),
    'cos': (lambda: button_click('cos('), '#b39ddb'), 'tan': (lambda: button_click('tan('), '#b39ddb'),
    '√': (lambda: button_click('√('), '#b39ddb'), '1/x': (lambda: button_click('1/'), '#b39ddb'),
    '%': (lambda: button_click('%'), '#b39ddb'), '^': (lambda: button_click('^'), '#b39ddb')
}

# Create basic operation buttons
row_val, col_val = 1, 0
for text, color in buttons:
    tk.Button(
        root, text=text, padx=20, pady=20, font=('Arial', 16),
        command=lambda b=text: button_click(b) if b != '=' else evaluate(),
        bg=color, fg="#ffffff"
    ).grid(row=row_val, column=col_val, sticky="nsew")
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Create function buttons
for text, (command, color) in function_buttons.items():
    tk.Button(
        root, text=text, padx=20, pady=20, font=('Arial', 16),
        command=command, bg=color, fg="#333333" if color == "#b39ddb" else "#ffffff"
    ).grid(row=row_val, column=col_val, sticky="nsew")
    col_val += 1
    if col_val > 3:
        col_val = 0
        row_val += 1

# Add Clear, Backspace, and Bracket buttons in the bottom-most row
row_val += 1
tk.Button(
    root, text='(', padx=20, pady=20, font=('Arial', 16),
    command=lambda: button_click('('), bg="#66bb6a", fg="#ffffff"
).grid(row=row_val, column=0, sticky="nsew")

tk.Button(
    root, text=')', padx=20, pady=20, font=('Arial', 16),
    command=lambda: button_click(')'), bg="#66bb6a", fg="#ffffff"
).grid(row=row_val, column=3, sticky="nsew")

tk.Button(
    root, text='C', padx=40, pady=20, font=('Arial', 16),
    command=clear_entry, bg="#f44336", fg="#ffffff"
).grid(row=row_val, column=1, sticky="nsew")

tk.Button(
    root, text='⌫', padx=40, pady=20, font=('Arial', 16),
    command=backspace, bg="#f44336", fg="#ffffff"
).grid(row=row_val, column=2, sticky="nsew")

# Adjust grid weights for responsiveness
for i in range(1, 8):  # Adjusted for additional rows
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

root.mainloop()

