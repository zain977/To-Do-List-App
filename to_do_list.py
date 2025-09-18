import customtkinter as ctk
from tkinter import messagebox
import json
import os

# ================= Settings ================= #
ctk.set_appearance_mode("dark")   # dark / light
ctk.set_default_color_theme("blue")  # blue / green / dark-blue

# ================= App Class ================= #
class ToDoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List App")
        self.geometry("600x500")
        self.resizable(False, False)

        # Tasks list
        self.tasks = []

        # Load previous tasks
        self.load_tasks()

        # Title
        self.title_label = ctk.CTkLabel(self, text="✅ To-Do List", font=("Arial", 28, "bold"))
        self.title_label.pack(pady=20)

        # Input frame
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10)

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter a new task...",
                                       width=350, height=40, font=("Arial", 16))
        self.task_entry.grid(row=0, column=0, padx=10)

        self.add_button = ctk.CTkButton(self.input_frame, text="Add Task", width=100,
                                        command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10)

        # Tasks listbox
        self.task_listbox = ctk.CTkTextbox(self, width=500, height=250, font=("Arial", 14))
        self.task_listbox.pack(pady=20)

        # Buttons frame
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)

        self.done_button = ctk.CTkButton(self.btn_frame, text="✔ Mark as Done",
                                         command=self.mark_done)
        self.done_button.grid(row=0, column=0, padx=10)

        self.delete_button = ctk.CTkButton(self.btn_frame, text="🗑 Delete Task",
                                           fg_color="red", hover_color="#b30000",
                                           command=self.delete_task)
        self.delete_button.grid(row=0, column=1, padx=10)

        # Show saved tasks
        self.show_tasks()

    # ================= Functions ================= #
    def add_task(self):
        task = self.task_entry.get().strip()
        if task != "":
            self.tasks.append({"task": task, "done": False})
            self.task_entry.delete(0, "end")
            self.show_tasks()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please enter a task!")

    def show_tasks(self):
        self.task_listbox.delete("1.0", "end")
        for i, task in enumerate(self.tasks, start=1):
            if task["done"]:
                self.task_listbox.insert("end", f"{i}. {task['task']} ✅\n")
            else:
                self.task_listbox.insert("end", f"{i}. {task['task']}\n")

    def mark_done(self):
        try:
            index = int(self.task_entry.get()) - 1
            if 0 <= index < len(self.tasks):
                self.tasks[index]["done"] = True
                self.task_entry.delete(0, "end")
                self.show_tasks()
                self.save_tasks()
            else:
                messagebox.showerror("Error", "Invalid task number!")
        except ValueError:
            messagebox.showerror("Error", "Enter task number to mark as done.")

    def delete_task(self):
        try:
            index = int(self.task_entry.get()) - 1
            if 0 <= index < len(self.tasks):
                del self.tasks[index]
                self.task_entry.delete(0, "end")
                self.show_tasks()
                self.save_tasks()
            else:
                messagebox.showerror("Error", "Invalid task number!")
        except ValueError:
            messagebox.showerror("Error", "Enter task number to delete.")

    def save_tasks(self):
        with open("tasks.json", "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as f:
                self.tasks = json.load(f)

# ================= Run App ================= #
if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()