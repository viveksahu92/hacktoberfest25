import tkinter as tk
import random
import time

class ReactionTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaction Time Test")
        self.root.geometry("1600x900")

        self.state = "waiting"
        self.start_time = 0

        self.label = tk.Label(root, text="Press Space to start\nPress Esc to quit", font=("Helvetica", 16))
        self.label.pack(expand = True)

        self.root.bind("<space>", self.space_pressed)
        self.root.bind("<Escape>", lambda e: self.root.quit())

        self.root.configure(bg = "red")

    def space_pressed(self, event):
        if self.state == "waiting":
            self.state = "ready"
            self.label.config(text = "Wait for green.")
            self.root.configure(bg = "red")

            delay = random.randint(1000, 5000)
            self.root.after(delay, self.turn_green)

        elif self.state == "ready":
            self.state = "waiting"
            self.label.config(text = "Too early.\nPress Space to try again.\nPress Esc to quit.")
            self.root.configure(bg = "red")

        elif self.state == "green":
            reaction_time = time.time() - self.start_time
            self.state = "clicked"
            self.label.config(text = f"Reaction Time: {reaction_time:.3f} seconds\nPress Space to play again.\nPress Esc to quit.")
            self.root.configure(bg = "blue")

        elif self.state == "clicked":
            self.state = "waiting"
            self.label.config(text = "Press Space to start.")
            self.root.configure(bg = "red")

    def turn_green(self):
        if self.state == "ready":
            self.state = "green"
            self.start_time = time.time()
            self.label.config(text = "Press Space now.")
            self.root.configure(bg = "green")

root = tk.Tk()
app = ReactionTimeApp(root)
root.mainloop()