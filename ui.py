import sys
import os
import time
import threading
from tkinter import *
from database import initial_text
from choose_text import ChooseText

PINK = "#F56D91"
PURPLE = "#8D8DAA"
WHITE = "#F7F5F2"
GREY = "#DFDFDE"
BLUE = "#6F9EAF"
FONT_NAME = "Arial"
font = (FONT_NAME, 20, "normal")


def restart_test():
    python = sys.executable
    os.execl(python, python, *sys.argv)


class TypeSpeedInterface:
    def __init__(self, text_chosen: ChooseText):

        # Imports
        self.text_to_type = text_chosen.text

        # Variables
        self.users_typing = False
        self.timer = 0
        self.count_mistakes = 0

        # Create window
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.config(padx=100, pady=50, background=GREY)
        self.window.geometry("1250x970")

        # Labels
        self.initial_label = Label(font=(FONT_NAME, 26, "normal"), bg=GREY, fg=PINK, text="Test Your Typing Speed!")
        self.cpm_label = Label(font=(FONT_NAME, 16, "normal"), bg=GREY, fg="black", text="chars/min")
        self.wpm_label = Label(font=(FONT_NAME, 16, "normal"), bg=GREY, fg="black", text="words/min")
        self.accuracy_label = Label(font=(FONT_NAME, 16, "normal"), bg=GREY, fg="black", text="accuracy")

        # Canvas for Instructions
        self.canvas_instruction = Canvas(width=1000, height=250, background=WHITE)
        self.text_instruction = self.canvas_instruction.create_text(500, 125, text=initial_text, width=978,
                                                                    font=font, fill=PURPLE)

        # Canvas for the Text
        self.canvas_text = Canvas(width=1000, height=250, background=WHITE)
        self.text = self.canvas_text.create_text(500, 125, text=self.text_to_type, width=978,
                                                 font=(FONT_NAME, 20, "italic"), fill=PURPLE)
        self.text_to_write = self.canvas_text.itemcget(self.text, 'text')

        # Canvas for the speed and accuracy
        self.canvas_cpm = Canvas(width=100, height=100, background=WHITE)
        self.text_cpm = self.canvas_cpm.create_text(50, 50, text=self.timer, width=90,
                                                    font=font, fill=BLUE)
        self.canvas_wpm = Canvas(width=100, height=100, background=WHITE)
        self.text_wpm = self.canvas_wpm.create_text(50, 50, text=self.timer, width=90,
                                                    font=font, fill=BLUE)
        self.canvas_accuracy = Canvas(width=100, height=100, background=WHITE)
        self.text_accuracy = self.canvas_accuracy.create_text(50, 50, text=self.count_mistakes, width=90,
                                                              font=font, fill=BLUE)

        # Buttons
        self.start_button = Button(self.window, text="Start the Test", relief="groove", font=font, bg=PINK,
                                   fg=WHITE, command=self.start_test)
        self.restart_button = Button(self.window, text="Restart the Test", relief="groove", font=font, bg=PINK,
                                     fg=WHITE, command=restart_test)

        # Inputs
        self.text_input = Text(self.window, height=8, width=67, font=font, wrap=WORD)

        self.start()
        self.window.mainloop()

    def start(self):
        # Show the initial page of the program
        self.initial_label.grid(column=0, row=1, columnspan=3, pady=50, padx=20)
        self.canvas_instruction.grid(column=0, row=2, columnspan=3, pady=50, padx=20)
        self.start_button.grid(column=1, row=3, padx=20, pady=50)

        # Make the widgets centered
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(4, weight=1)

    def start_test(self):
        # Forget grid
        self.canvas_instruction.grid_forget()
        self.start_button.grid_forget()
        self.initial_label.grid_forget()

        # Undo the weights to make the widgets centered in the first window
        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(4, weight=0)

        # Show necessary widgets
        self.canvas_text.grid(column=0, row=0, columnspan=3, pady=20, padx=20)

        self.text_input.grid(column=0, columnspan=3, row=1, pady=20, padx=20)
        self.text_input.focus()
        self.text_input.bind("<KeyRelease>", self.key_pressed)

        self.canvas_cpm.grid(column=0, row=2, pady=(20, 5), padx=20)
        self.canvas_wpm.grid(column=1, row=2, pady=(20, 5), padx=20)
        self.canvas_accuracy.grid(column=2, row=2, pady=(20, 5), padx=20)

        self.cpm_label.grid(column=0, row=3, padx=20, pady=(0, 20))
        self.wpm_label.grid(column=1, row=3, padx=20, pady=(0, 20))
        self.accuracy_label.grid(column=2, row=3, padx=20, pady=(0, 20))

        self.restart_button.grid(column=0, row=4, columnspan=3, padx=20, pady=20)

    def key_pressed(self, event):
        if not self.users_typing:
            # keycode is a number that represents a key in the keyboard (i.e. 9 = left TAB)
            if not event.keycode in [16, 17, 18, 9]:
                self.users_typing = True
                # Create threads and use it to run the app faster
                thread = threading.Thread(target=self.timer_thread)
                thread.start()

        # Check if users input == text chosen to change the color
        if not self.text_to_write.startswith(self.text_input.get("1.0", "end-1c")):
            self.text_input.config(fg=PINK)
            self.count_mistakes += 1
        else:
            self.text_input.config(fg="black")

        # Check if user wrote the entire text to change the color and stop the clock
        if self.text_input.get("1.0", "end-1c").rstrip() == self.text_to_write.rstrip():
            self.users_typing = False
            self.text_input.config(fg=BLUE)

    def timer_thread(self):
        # Start the clock when user starts typing
        while self.users_typing:
            time.sleep(0.1)
            self.timer += 0.1
            # Get the character per seconds
            cpm = len(self.text_input.get("1.0", "end-1c")) * 60 / self.timer

            # Get the word per minute
            wpm = len(self.text_input.get("1.0", "end-1c").split(" ")) * 60 / self.timer

            # Accuracy
            accuracy = len(self.text_input.get("1.0", "end-1c")) - self.count_mistakes
            accuracy_percent = accuracy * 100 / len(self.text_input.get("1.0", "end-1c"))

            # Update Canvas
            self.canvas_cpm.itemconfig(self.text_cpm, text=f"{cpm:.0f}")
            self.canvas_wpm.itemconfig(self.text_wpm, text=f"{wpm:.0f}")
            self.canvas_accuracy.itemconfig(self.text_accuracy, text=f"{accuracy_percent:.0f}%")







