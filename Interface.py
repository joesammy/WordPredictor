import tkinter as tk

class SuggestionApp:
    def __init__(self, suggestor):
        print("Opening window...")
        self.root = tk.Tk()
        self.root.title("Word Suggestions")
        self.root.geometry("800x100")

        self.suggestor = suggestor

        self.entry_text = tk.StringVar()
        self.entry = tk.Entry(self.root, width=100, textvariable=self.entry_text, font=("Arial", 14))

        self.entry.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        # Create suggestion buttons
        self.buttons = []
        for i in range(3):
            btn = tk.Button(button_frame, text=f"Suggestion_{i+1}", bg="light blue", font=("Arial", 14), width=25, height=15, command=lambda i=i: self.use_suggestion(i))
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons.append(btn)

        self.on_text_change()
        self.entry_text.trace('w', self.on_text_change)

        self.root.mainloop()

    def on_text_change(self, *args):
        current_text = self.entry_text.get().split(" ")
        
        
        # Add <s> at start if not already there
        if not current_text[0] == "<s>":
            current_text.insert(0, "<s>")

        # Handle the previous and current words
        if len(current_text) > 1:
            prevWord = current_text[-2]
            currWord = current_text[-1]
            
            # Clean up previous word - remove punctuation if present
            if len(prevWord) > 0 and prevWord[-1] in ".!?":
                prevWord = "<s>"

        else:
            prevWord = "<s>"
            currWord = ""

        self.suggestions = self.suggestor.nextWord(prevWord, currWord)

        for button, suggestion in zip(self.buttons, self.suggestions):
            if (suggestion == ""):
                button.config(state = tk.DISABLED)
            else:
                button.config(state = tk.NORMAL)
            button.config(text=suggestion)

        self.entry.xview_moveto(1)

        print(f"nText array: {current_text}")
        print(f"Previous Word: {prevWord}, Current word: {currWord}")
        print(f"Suggestions: {self.suggestions}\n\n")


    def use_suggestion(self, button_index):       
        suggestion = self.buttons[button_index]['text']
        
        # Get current text and split into words
        current_text = self.entry_text.get().split(" ")

        # if button.cget("text") == "":
        # # Disable the button if the text is empty
        #     button.config(state=tk.DISABLED)
        
        # Replace or add the suggestion
        if current_text and current_text[-1] == "":
            print("empty word")
            current_text.append(suggestion)
        elif current_text:
            current_text[-1] = suggestion
        else:
            current_text = [suggestion]  # Start new text

        previous_text = self.entry_text.get()
        self.entry_text.set(previous_text[:previous_text.rfind(' ')+1] + current_text[-1] + " ")
        self.entry.icursor(tk.END)
        self.entry.xview_moveto(1)
