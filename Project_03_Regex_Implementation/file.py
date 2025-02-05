import re
from collections import Counter
from tkinter import Tk, Toplevel, Text, Scrollbar, Label, Button, RIGHT, Y, END
from tkinter import messagebox


def file_processing(input_path, output_path):
    try:
        # 1. Reading the input file
        with open(input_path, 'r') as file:
            lines = file.readlines()

        # 2. Count the number of unique words and frequency of each
        words = []
        for line in lines:
            words.extend(re.findall(r'\b\w+\b', line.lower()))

        word_count = Counter(words)
        unique_word_count = len(word_count)

        # 3. Count the number of new lines
        num_new_lines = len(lines)

        # 4. Transforming first and last letters to uppercase
        transformed_lines = []
        for line in lines:
            transformed_line = re.sub(
                r'(?<=^)([a-zA-Z])|([a-zA-Z])(?=$)',
                lambda m: m.group(0).upper(),
                line.strip()
            )
            transformed_lines.append(transformed_line)

        with open(output_path, 'w') as output_file:
            output_file.write('\n'.join(transformed_lines))

        # A Pop-Up window to show results.
        root = Tk()
        root.withdraw()  

        results_window = Toplevel(root)
        results_window.title("Output Window")
        results_window.geometry("600x400")

        # Adding labels for results.
        Label(results_window, text="File Processing Results", font=("Arial", 16, "bold")).pack(pady=10)

        results_text = Text(results_window, wrap="word", font=("Arial", 12), bg="white", padx=10, pady=10)
        scrollbar = Scrollbar(results_window, command=results_text.yview)
        results_text.config(yscrollcommand=scrollbar.set)
        results_text.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        results_text.insert(END, "• Number of unique words: " + str(unique_word_count) + "\n")
        results_text.insert(END, "• Unique words and their frequencies:\n")
        for word, freq in word_count.items():
            results_text.insert(END, f"    - {word}: {freq}\n")
        results_text.insert(END, "\n• Number of new lines: " + str(num_new_lines) + "\n")
        results_text.insert(END, f"\n• Transformed lines saved to: {output_path}\n")
        
        results_text.config(state="disabled")  

        # Adding an Exit button.
        Button(
            results_window,
            text="Exit",
            command=results_window.destroy,
            font=("Arial", 12),
            bg="yellow"
        ).pack(pady=10)

        root.mainloop()

    except FileNotFoundError:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", f"File {input_path} not found.")
    except Exception as e:
        root = Tk()
        root.withdraw()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


input_file = "input.txt"  ### Our input file (I have chosen a song as input)
output_file = "output.txt" 

# Calling the function
file_processing(input_file, output_file)
