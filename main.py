import random
import time
import tkinter as tk
from tkinter import ttk, messagebox
import turtle

APP_TITLE = "Treasure Quiz — Login + Game"
QUESTION_TIME = 10  # seconds per question
PASS_MARK = 0.6     # 60% and above triggers turtle celebration

QUESTIONS = [
    {"category": "Math", "question": "Simplify: (2 + 4)", "options": ["6", "5x + 7", "6x + 4", "3x + 12"], "answer": "6"},
    {"category": "Science", "question": "Which particle has a negative charge?", "options": ["Proton", "Electron", "Neutron", "Alpha particle"], "answer": "Electron"},
    {"category": "Geo", "question": "Which country has the city of Lagos?", "options": ["Kenya", "Ghana", "Nigeria", "South Africa"], "answer": "Nigeria"},
    {"category": "Tech", "question": "Binary number 1010 equals what in decimal?", "options": ["9", "10", "11", "12"], "answer": "10"},
    {"category": "English", "question": "Pick the correctly punctuated sentence.", "options": ["Its a great day, isnt it?", "It's a great day, isn't it?", "Its a great day; isnt it?", "It's a great day; isnt it?"], "answer": "It's a great day, isn't it?"},
]

class TreasureQuizApp(tk.Tk):
    def __init__(self, questions):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("860x560")
        self.configure(bg="#120f24")
        self.resizable(False, False)

        self.questions = questions[:]
        random.shuffle(self.questions)
        self.total = len(self.questions)

        self.username = ""
        self.age = ""
        self.index = 0
        self.score = 0
        self.correct_count = 0
        self.start_time = 0
        self.remaining = QUESTION_TIME
        self.timer_job = None
        self.responses = []

        # show login first
        self.show_login()

    # ---------------- Login Screen ----------------
    def show_login(self):
        self.login_frame = tk.Frame(self, bg="#14182f")
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Welcome to Teen Quiz!", fg="white", bg="#14182f", font=("Segoe UI", 22, "bold")).pack(pady=30)

        tk.Label(self.login_frame, text="Enter your name:", fg="white", bg="#14182f").pack(pady=5)
        self.entry_name = tk.Entry(self.login_frame, font=("Arial", 14))
        self.entry_name.pack(pady=5)

        tk.Label(self.login_frame, text="Enter your age:", fg="white", bg="#14182f").pack(pady=5)
        self.entry_age = tk.Entry(self.login_frame, font=("Arial", 14))
        self.entry_age.pack(pady=5)

        tk.Button(self.login_frame, text="Start Quiz", command=self.start_quiz, font=("Arial", 14)).pack(pady=20)

    def start_quiz(self):
        name = self.entry_name.get().strip()
        age = self.entry_age.get().strip()

        if not name or not age:
            messagebox.showwarning("Missing Info", "Please enter both name and age!")
            return

        self.username = name
        self.age = age
        self.login_frame.destroy()
        self.start_time = time.time()
        self.build_quiz_ui()
        self.load_question()

    # ---------------- Quiz UI ----------------
    def build_quiz_ui(self):
        top = tk.Frame(self, bg="#0f1224")
        top.pack(fill="x", padx=16, pady=(16, 0))

        self.progress = ttk.Progressbar(top, mode="determinate", maximum=self.total)
        self.progress.pack(fill="x", side="left", expand=True)

        self.timer_lbl = tk.Label(top, text="⏱ 20s", fg="#e0e6ff", bg="#0f1224", font=("Segoe UI", 12, "bold"))
        self.timer_lbl.pack(side="left", padx=16)

        self.user_lbl = tk.Label(top, text=f"Player: {self.username}", fg="#e0e6ff", bg="#0f1224", font=("Segoe UI", 12))
        self.user_lbl.pack(side="left", padx=10)

        self.score_lbl = tk.Label(top, text="Score: 0", fg="#e0e6ff", bg="#0f1224", font=("Segoe UI", 12, "bold"))
        self.score_lbl.pack(side="right")

        # Card
        self.card = tk.Frame(self, bg="#14182f")
        self.card.pack(padx=16, pady=16, fill="both", expand=True)

        self.category_lbl = tk.Label(self.card, text="", fg="#ff9f9f", bg="#2f1414", font=("Segoe UI", 11, "bold"))
        self.category_lbl.pack(anchor="w", padx=20, pady=(18, 0))

        self.question_lbl = tk.Label(self.card, text="", wraplength=780, justify="left", fg="#f4f6ff", bg="#14182f", font=("Segoe UI", 20, "bold"))
        self.question_lbl.pack(anchor="w", padx=20, pady=(6, 16))

        self.var_choice = tk.StringVar(value="")
        self.option_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.card, text="", variable=self.var_choice, value=f"opt{i}", command=self.enable_next)
            rb.pack(anchor="w", padx=32, pady=6)
            self.option_buttons.append(rb)

        self.help_lbl = tk.Label(self.card, text="", fg="#c9d1ff", bg="#14182f", font=("Segoe UI", 11))
        self.help_lbl.pack(anchor="w", padx=20, pady=(2, 8))

        self.next_btn = ttk.Button(self.card, text="Next ▶", command=self.next_question, state="disabled")
        self.next_btn.pack(pady=10, anchor="e", padx=20)

    # ---------------- Quiz Logic ----------------
    def enable_next(self):
        self.next_btn.configure(state="normal")

    def load_question(self):
        if self.index >= self.total:
            self.show_results()
            return

        q = self.questions[self.index]
        self.remaining = QUESTION_TIME
        self.update_timer_label()
        if self.timer_job:
            self.after_cancel(self.timer_job)
        self.timer_job = self.after(1000, self.tick)

        self.category_lbl.config(text=f"Category: {q['category']}")
        self.question_lbl.config(text=f"Q{self.index+1}. {q['question']}")

        options = q['options'][:]
        random.shuffle(options)
        for rb, opt in zip(self.option_buttons, options):
            rb.config(text=opt, value=opt, state="normal")
        self.var_choice.set("")
        self.help_lbl.config(text="")
        self.next_btn.config(state="disabled")
        self.progress['value'] = self.index

    def tick(self):
        self.remaining -= 1
        self.update_timer_label()
        if self.remaining <= 0:
            self.record(False, self.var_choice.get() or "(no answer)", self.questions[self.index]['answer'])
            self.advance()
        else:
            self.timer_job = self.after(1000, self.tick)

    def update_timer_label(self):
        self.timer_lbl.config(text=f"⏱ {self.remaining}s")

    def next_question(self):
        chosen = self.var_choice.get()
        if not chosen:
            messagebox.showinfo("Choose one", "Please select an answer.")
            return

        correct = self.questions[self.index]['answer']
        self.record(chosen == correct, chosen, correct)
        self.advance()

    def record(self, is_correct, chosen, correct):
        self.responses.append((is_correct, chosen, correct))
        if is_correct:
            self.correct_count += 1
            self.score += 10
        self.score_lbl.config(text=f"Score: {self.score}")

    def advance(self):
        if self.timer_job:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.index += 1
        self.load_question()

    def show_results(self):
        for w in self.card.winfo_children():
            w.destroy()

        total_time = int(time.time() - self.start_time)
        accuracy = (self.correct_count / self.total) if self.total else 0.0

        tk.Label(self.card, text=f"Results for {self.username} (Age {self.age})", fg="#f4f6ff", bg="#14182f", font=("Segoe UI", 20, "bold")).pack(pady=20)
        tk.Label(self.card, text=f"Score: {self.score}\\nCorrect: {self.correct_count}/{self.total} (Accuracy: {accuracy*100:.0f}%)\\nTime: {total_time}s", fg="white", bg="#14182f", font=("Segoe UI", 14)).pack(pady=10)

        if accuracy >= PASS_MARK:
            tk.Button(self.card, text="Celebrate 🎆", command=self.celebrate).pack(pady=10)

    def celebrate(self):
        self.destroy()
        fireworks_show()

# ---------------- Turtle Fireworks ----------------
def fireworks_show():
    scr = turtle.Screen()
    scr.title("🎆 Congrats! 🎆")
    scr.bgcolor("black")
    t = turtle.Turtle(visible=False)
    t.speed(0)
    scr.tracer(False)

    colors = ["red","orange","yellow","green","cyan","blue","magenta","white"]

    def burst(x,y,r=100,spokes=24):
        t.penup()
        t.goto(x,y)
        t.pendown()
        col = random.choice(colors)
        t.pencolor(col)
        for i in range(spokes):
            t.penup()
            t.goto(x,y)
            t.setheading(i*(360/spokes))
            t.pendown()
            t.forward(r)
        t.penup()
        t.goto(x,y-10)
        t.pendown()
        t.circle(10)

    for _ in range(8):
        burst(random.randint(-200,200), random.randint(-100,200))
        scr.update()

    t.penup()
    t.goto(0,-220)
    t.color("white")
    t.write("Well done! Click screen to close", align="center", font=("Segoe UI",14,"bold"))
    scr.update()
    scr.exitonclick()

if __name__ == "__main__":
    app = TreasureQuizApp(QUESTIONS)
    app.mainloop()
