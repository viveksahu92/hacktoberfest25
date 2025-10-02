import tkinter as tk
from tkinter import messagebox

WORK_BG = "#e74c3c"    # Pomodoro Red
BREAK_BG = "#2ecc71"   # Green for breaks
IDLE_BG = "#f1c40f"    # Yellow for idle/reset

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("340x230")
        self.root.configure(bg=IDLE_BG)

        self.working = False
        self.cycle = 1

        self.label = tk.Label(
            root, text="Pomodoro Timer",
            font=("Arial", 20, "bold"), bg=IDLE_BG, fg="#2d3436"
        )
        self.label.pack(pady=(16, 8))

        self.time_var = tk.StringVar(value="25:00")
        self.timer_label = tk.Label(
            root, textvariable=self.time_var,
            font=("Arial", 44, "bold"), bg=IDLE_BG, fg="#2d3436"
        )
        self.timer_label.pack(pady=5)

        self.start_button = tk.Button(
            root, text="Start Pomodoro", font=("Arial", 12, "bold"),
            command=self.start_pomodoro, bg="#e17055", fg="white", activebackground="#d35400"
        )
        self.start_button.pack(pady=(12, 3), ipadx=6, ipady=2)

        self.reset_button = tk.Button(
            root, text="Reset", font=("Arial", 12),
            command=self.reset_timer, bg="#636e72", fg="white", activebackground="#b2bec3"
        )
        self.reset_button.pack(pady=(2, 10), ipadx=6, ipady=2)

        self.state = "work"  # can be "work" or "break"
        self.remaining = 25 * 60

    def set_bg(self, color):
        self.root.configure(bg=color)
        self.label.configure(bg=color)
        self.timer_label.configure(bg=color)

    def start_pomodoro(self):
        if not self.working:
            self.working = True
            self.state = "work"
            self.remaining = 25 * 60
            self.set_bg(WORK_BG)
            self.update_timer()
            self.countdown()

    def countdown(self):
        if self.working and self.remaining > 0:
            mins, secs = divmod(self.remaining, 60)
            self.time_var.set(f"{mins:02d}:{secs:02d}")
            self.remaining -= 1
            self.root.after(1000, self.countdown)
        elif self.working:
            self.timer_done()

    def timer_done(self):
        if self.state == "work":
            messagebox.showinfo("Pomodoro Timer", "Work session finished! Time for a break.")
            self.state = "break"
            self.set_bg(BREAK_BG)
            self.remaining = 5 * 60
            self.update_timer()
            self.countdown()
        else:
            messagebox.showinfo("Pomodoro Timer", "Break finished! Back to work.")
            self.working = False
            self.cycle += 1
            self.set_bg(IDLE_BG)
            self.time_var.set("25:00")

    def reset_timer(self):
        self.working = False
        self.state = "work"
        self.remaining = 25 * 60
        self.time_var.set("25:00")
        self.set_bg(IDLE_BG)

    def update_timer(self):
        mins, secs = divmod(self.remaining, 60)
        self.time_var.set(f"{mins:02d}:{secs:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    PomodoroTimer(root)
    root.mainloop()