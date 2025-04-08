import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import random

CATEGORIES = ["marketing", "appdev", "analyticalthinking", "database", "stats"]

def launch_quiz():
    window = tk.Tk()
    window.title("Select Quiz Category")
    window.geometry("400x200")

    tk.Label(window, text="Choose a Quiz Category:", font=("Arial", 14)).pack(pady=20)

    selected_category = tk.StringVar()
    dropdown = ttk.Combobox(window, textvariable=selected_category, values=CATEGORIES, state='readonly')
    dropdown.pack(pady=10)

    def start_quiz():
        category = selected_category.get()
        if not category:
            messagebox.showwarning("Hold up", "Please select a category!")
            return
        window.destroy()
        load_questions(category)

    tk.Button(window, text="Start Quiz", command=start_quiz).pack(pady=10)
    window.mainloop()


def load_questions(category):
    try:
        conn = sqlite3.connect("quiz_bowl.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {category}_questions")
        data = cursor.fetchall()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load questions:\n{e}")
        return

    if len(data) < 1:
        messagebox.showinfo("No Questions", "No questions found for this category.")
        return

    random.shuffle(data)
    quiz_session(data[:10])  # Use only first 10 questions


def quiz_session(questions):
    score = [0]
    index = [0]

    quiz_window = tk.Tk()
    quiz_window.title("Quiz In Progress")
    quiz_window.geometry("600x400")

    counter_label = tk.Label(quiz_window, text="", font=("Arial", 10))
    counter_label.pack()

    question_label = tk.Label(quiz_window, text="", wraplength=500, font=("Arial", 12))
    question_label.pack(pady=10)

    feedback_label = tk.Label(quiz_window, text="", font=("Arial", 12))
    feedback_label.pack()

    selected_answer = tk.StringVar()
    radio_buttons = []
    for val in ["A", "B", "C", "D"]:
        rb = tk.Radiobutton(quiz_window, text="", variable=selected_answer, value=val, font=("Arial", 10))
        rb.pack(anchor='w')
        radio_buttons.append(rb)

    def display_question():
        if index[0] < len(questions):
            q = questions[index[0]]
            selected_answer.set("")
            counter_label.config(text=f"Question {index[0] + 1} of {len(questions)}")
            question_label.config(text=f"{q[0]}")
            radio_buttons[0].config(text=f"A. {q[1]}")
            radio_buttons[1].config(text=f"B. {q[2]}")
            radio_buttons[2].config(text=f"C. {q[3]}")
            radio_buttons[3].config(text=f"D. {q[4]}")
            feedback_label.config(text="")
        else:
            quiz_window.destroy()
            show_score(score[0], len(questions))

    def submit_answer():
        if not selected_answer.get():
            messagebox.showwarning("No Answer", "Please select an answer.")
            return

        correct = questions[index[0]][5]
        if selected_answer.get() == correct:
            score[0] += 1
            feedback_label.config(text="✅ Correct!", fg="green")
        else:
            feedback_label.config(text=f"❌ Incorrect. Correct answer: {correct}", fg="red")

        quiz_window.after(1500, next_question)

    def next_question():
        index[0] += 1
        display_question()

    tk.Button(quiz_window, text="Submit Answer", command=submit_answer).pack(pady=20)

    display_question()
    quiz_window.mainloop()


def show_score(score, total):
    final_window = tk.Tk()
    final_window.title("Quiz Complete")
    final_window.geometry("300x150")

    tk.Label(final_window, text=f"You scored {score} out of {total}!", font=("Arial", 16)).pack(pady=30)
    tk.Button(final_window, text="Close", command=final_window.destroy).pack()
