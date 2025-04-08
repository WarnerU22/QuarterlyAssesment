import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

CATEGORIES = ["marketing", "appdev", "analyticalthinking", "database", "stats"]

def open_admin_panel():
    panel = tk.Tk()
    panel.title("Admin Panel")
    panel.geometry("400x300")

    tk.Label(panel, text="Admin Panel", font=("Arial", 16)).pack(pady=20)

    # Add Question
    tk.Button(panel, text="Add Question", command=lambda: open_add_question(panel), width=25).pack(pady=10)

    # View/Edit/Delete
    tk.Button(panel, text="View/Edit/Delete Questions", command=lambda: open_manage_questions(panel), width=25).pack(pady=10)

    # Exit Button
    tk.Button(panel, text="Exit", command=panel.destroy, width=25).pack(pady=10)


def open_add_question(parent_window):
    add_window = tk.Toplevel(parent_window)
    add_window.title("Add New Question")
    add_window.geometry("500x500")

    tk.Label(add_window, text="Select Category:").pack()
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(add_window, textvariable=category_var, values=CATEGORIES, state='readonly')
    category_dropdown.pack(pady=5)

    tk.Label(add_window, text="Question Text:").pack()
    question_entry = tk.Text(add_window, height=4, width=50)
    question_entry.pack(pady=5)

    tk.Label(add_window, text="Option A:").pack()
    option_a = tk.Entry(add_window, width=50)
    option_a.pack()

    tk.Label(add_window, text="Option B:").pack()
    option_b = tk.Entry(add_window, width=50)
    option_b.pack()

    tk.Label(add_window, text="Option C:").pack()
    option_c = tk.Entry(add_window, width=50)
    option_c.pack()

    tk.Label(add_window, text="Option D:").pack()
    option_d = tk.Entry(add_window, width=50)
    option_d.pack()

    tk.Label(add_window, text="Correct Answer (A/B/C/D):").pack()
    correct_answer_var = tk.StringVar()
    correct_answer_dropdown = ttk.Combobox(add_window, textvariable=correct_answer_var, values=["A", "B", "C", "D"], state='readonly')
    correct_answer_dropdown.pack(pady=5)

    def submit_question():
        category = category_var.get()
        question = question_entry.get("1.0", tk.END).strip()
        a = option_a.get().strip()
        b = option_b.get().strip()
        c = option_c.get().strip()
        d = option_d.get().strip()
        answer = correct_answer_var.get().strip()

        if not all([category, question, a, b, c, d, answer]):
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {category}_questions 
                (question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (question, a, b, c, d, answer))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Question added successfully!")
            add_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Could not insert question:\n{e}")

    tk.Button(add_window, text="Submit Question", command=submit_question).pack(pady=20)


def open_manage_questions(parent_window):
    messagebox.showinfo("Coming Soon", "Edit/Delete question screen is under construction.")

