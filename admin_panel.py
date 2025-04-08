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
    manage_window = tk.Toplevel(parent_window)
    manage_window.title("Manage Questions")
    manage_window.geometry("600x400")

    tk.Label(manage_window, text="Select Category:").pack()
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(manage_window, textvariable=category_var, values=CATEGORIES, state='readonly')
    category_dropdown.pack(pady=5)

    # Listbox to display questions
    question_listbox = tk.Listbox(manage_window, width=80)
    question_listbox.pack(pady=10)

    def load_questions():
        question_listbox.delete(0, tk.END)
        category = category_var.get()
        if not category:
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT id, question FROM {category}_questions")
            questions = cursor.fetchall()
            conn.close()

            for q in questions:
                display = f"{q[0]}: {q[1][:80]}..."  # Show ID and first part of question
                question_listbox.insert(tk.END, display)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load questions:\n{e}")

    def delete_selected_question():
        selected = question_listbox.curselection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a question to delete.")
            return

        question_text = question_listbox.get(selected[0])
        question_id = question_text.split(":")[0]
        category = category_var.get()

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
        if not confirm:
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {category}_questions WHERE id = ?", (question_id,))
            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", "Question deleted successfully.")
            load_questions()

        except Exception as e:
            messagebox.showerror("Error", f"Could not delete question:\n{e}")

    # Load and delete buttons
    tk.Button(manage_window, text="Load Questions", command=load_questions).pack(pady=5)
    tk.Button(manage_window, text="Delete Selected Question", command=delete_selected_question).pack(pady=5)

    tk.Button(manage_window, text="Edit Selected Question", command=lambda: edit_selected_question(category_var.get(), question_listbox)).pack(pady=5)

def edit_selected_question(category, listbox):
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No selection", "Please select a question to edit.")
        return

    item = listbox.get(selected[0])
    question_id = item.split(":")[0]

    try:
        conn = sqlite3.connect("quiz_bowl.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM {category}_questions WHERE id = ?", (question_id,))
        data = cursor.fetchone()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load question:\n{e}")
        return

    # Open edit window
    edit_win = tk.Toplevel()
    edit_win.title("Edit Question")
    edit_win.geometry("500x550")

    tk.Label(edit_win, text="Edit Question:").pack()
    question_entry = tk.Text(edit_win, height=4, width=50)
    question_entry.insert("1.0", data[0])
    question_entry.pack()

    labels = ["A", "B", "C", "D"]
    options_entries = []

    for i in range(4):
        tk.Label(edit_win, text=f"Option {labels[i]}:").pack()
        entry = tk.Entry(edit_win, width=50)
        entry.insert(0, data[i+1])
        entry.pack()
        options_entries.append(entry)

    tk.Label(edit_win, text="Correct Answer (A/B/C/D):").pack()
    correct_var = tk.StringVar()
    correct_dropdown = ttk.Combobox(edit_win, textvariable=correct_var, values=["A", "B", "C", "D"], state='readonly')
    correct_dropdown.set(data[5])
    correct_dropdown.pack(pady=10)

    def save_changes():
        new_question = question_entry.get("1.0", tk.END).strip()
        new_options = [e.get().strip() for e in options_entries]
        new_correct = correct_var.get()

        if not all([new_question] + new_options + [new_correct]):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        try:
            conn = sqlite3.connect("quiz_bowl.db")
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {category}_questions
                SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_answer = ?
                WHERE id = ?
            """, (new_question, *new_options, new_correct, question_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Question updated successfully.")
            edit_win.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update question:\n{e}")

    tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=20)

