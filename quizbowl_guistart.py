import tkinter as tk
from tkinter import messagebox

# Constants
ADMIN_PASSWORD = "admin123"  # You can change this

# Root window setup
root = tk.Tk()
root.title("Quiz Bowl")
root.geometry("400x300")

# Title label
title_label = tk.Label(root, text="Welcome to Quiz Bowl!", font=("Arial", 18))
title_label.pack(pady=20)

# --- Admin Login Flow ---
def show_admin_login():
    def validate_password():
        entered = password_entry.get()
        if entered == ADMIN_PASSWORD:
            messagebox.showinfo("Access Granted", "Welcome, Admin!")
            root.destroy()
            # TODO: Open admin interface here
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x150")

    tk.Label(login_window, text="Enter Admin Password:").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=validate_password).pack(pady=10)

# --- Quiz Taker Flow ---
def launch_quiz_taker():
    messagebox.showinfo("Quiz Taker", "Launching quiz interface...")
    root.destroy()
    # TODO: Open quiz interface here

# Buttons
admin_button = tk.Button(root, text="Administrator", command=show_admin_login, width=20)
admin_button.pack(pady=10)

quiz_button = tk.Button(root, text="Take a Quiz", command=launch_quiz_taker, width=20)
quiz_button.pack(pady=10)

# Run app
root.mainloop()
