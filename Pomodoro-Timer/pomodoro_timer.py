import tkinter as tk
import time
import threading

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro-Timer 🎯")

        self.cycles = tk.IntVar(value=4)
        self.work_time = tk.IntVar(value=25)
        self.short_break = tk.IntVar(value=5)
        self.long_break = tk.IntVar(value=15)


        self.current_cycle = 0
        self.running = False
        self.seconds_remaining = 0
        self.thread = None


        self.create_interface()

    def create_interface(self):

        tk.Label(self.root, text="Cycles:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.cycles, width=5).grid(row=0, column=1)


        tk.Label(self.root, text="Work (min):").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.work_time, width=5).grid(row=1, column=1)


        tk.Label(self.root, text="Short Break (min):").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.short_break, width=5).grid(row=2, column=1)


        tk.Label(self.root, text="Long Break (min):").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(self.root, textvariable=self.long_break, width=5).grid(row=3, column=1)


        self.label_timer = tk.Label(self.root, text="00:00", font=("Arial", 30))
        self.label_timer.grid(row=0, column=2, rowspan=2, padx=20, pady=10)

        self.label_status = tk.Label(self.root, text="Ready!", font=("Arial", 14))
        self.label_status.grid(row=2, column=2, rowspan=2, padx=20)


        tk.Button(self.root, text="▶️ Start", command=self.start).grid(row=4, column=0, pady=10)

        tk.Button(self.root, text="⏸️ Pause", command=self.pause).grid(row=4, column=1, pady=10)

        tk.Button(self.root, text="🔄 Reset", command=self.reset).grid(row=4, column=2, pady=10)

    def start(self):
        if not self.running:
            self.running = True
            self.current_cycle = 0
            self.new_cycle()


    def pause(self):
        self.running = False
        self.label_status.config(text="⏸️ Paused")


    def reset(self):
        self.running = False
        self.current_cycle = 0
        self.seconds_remaining = 0
        self.label_timer.config(text="00:00")
        self.label_status.config(text="🔄 Reset")


    def new_cycle(self):
        if self.current_cycle < self.cycles.get():
            self.current_cycle += 1
            self.label_status.config(
                text=f"Cycle {self.current_cycle} of {self.cycles.get()}"
            )
            self.start_timer(self.work_time.get() * 60, is_break=False)
        else:
            self.label_status.config(text="🎉 All cycles done! Long break ☕")
            self.start_timer(self.long_break.get() * 60, is_break=True)


    def start_timer(self, seconds, is_break):
        self.seconds_remaining = seconds
        self.thread = threading.Thread(target=self.countdown, args=(is_break,))
        self.thread.start()


    def countdown(self, is_break):
        while self.seconds_remaining > 0 and self.running:
            mins, secs = divmod(self.seconds_remaining, 60)
            self.label_timer.config(text=f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            self.seconds_remaining -= 1

        if self.running:

            if is_break:
                self.label_status.config(text="✅ Long break finished")
            else:
                if self.current_cycle < self.cycles.get():
                    self.label_status.config(text="☕ Short break")
                    self.start_timer(self.short_break.get() * 60, is_break=True)
                else:
                    self.label_status.config(text="🎯 Pomodoro Finished!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
