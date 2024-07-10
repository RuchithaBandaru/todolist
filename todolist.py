import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# Set up the database
conn = sqlite3.connect('todo_list.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    priority INTEGER NOT NULL,
    due_date TEXT NOT NULL,
    is_complete INTEGER NOT NULL
)
''')
conn.commit()

# Function to add a task
def add_task():
    description = entry_description.get()
    priority = entry_priority.get()
    due_date = entry_due_date.get()
    if description and priority.isdigit() and due_date:
        cursor.execute('''
            INSERT INTO tasks (description, priority, due_date, is_complete)
            VALUES (?, ?, ?, 0)
        ''', (description, int(priority), due_date))
        conn.commit()
        entry_description.delete(0, tk.END)
        entry_priority.delete(0, tk.END)
        entry_due_date.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showerror("Error", "Please enter valid data.")

# Function to delete a task
def delete_task():
    selected_task = tree.selection()
    if selected_task:
        task_id = tree.item(selected_task)['values'][0]
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        load_tasks()
    else:
        messagebox.showerror("Error", "Please select a task to delete.")

# Function to update a task
def update_task():
    selected_task = tree.selection()
    if selected_task:
        task_id = tree.item(selected_task)['values'][0]
        description = entry_description.get()
        priority = entry_priority.get()
        due_date = entry_due_date.get()
        if description and priority.isdigit() and due_date:
            cursor.execute('''
                UPDATE tasks
                SET description = ?, priority = ?, due_date = ?
                WHERE id = ?
            ''', (description, int(priority), due_date, task_id))
            conn.commit()
            load_tasks()
        else:
            messagebox.showerror("Error", "Please enter valid data.")
    else:
        messagebox.showerror("Error", "Please select a task to update.")

# Function to mark a task as complete
def complete_task():
    selected_task = tree.selection()
    if selected_task:
        task_id = tree.item(selected_task)['values'][0]
        cursor.execute('UPDATE tasks SET is_complete = 1 WHERE id = ?', (task_id,))
        conn.commit()
        load_tasks()
    else:
        messagebox.showerror("Error", "Please select a task to mark as complete.")

# Function to load tasks into the treeview
def load_tasks():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('SELECT * FROM tasks')
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

# Function to filter tasks
def filter_tasks():
    filter_priority = entry_filter_priority.get()
    filter_date = entry_filter_date.get()
    query = 'SELECT * FROM tasks WHERE 1=1'
    params = []
    if filter_priority.isdigit():
        query += ' AND priority = ?'
        params.append(int(filter_priority))
    if filter_date:
        query += ' AND due_date = ?'
        params.append(filter_date)
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute(query, params)
    for row in cursor.fetchall():
        tree.insert('', tk.END, values=row)

# Create the main window
root = tk.Tk()
root.title("To-Do List")

# Create the entry fields and labels
tk.Label(root, text="Description:").grid(row=0, column=0, padx=10, pady=5)
entry_description = tk.Entry(root, width=20)
entry_description.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Priority:").grid(row=1, column=0, padx=10, pady=5)
entry_priority = tk.Entry(root, width=20)
entry_priority.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
entry_due_date = tk.Entry(root, width=20)
entry_due_date.grid(row=2, column=1, padx=10, pady=5)

# Create the buttons
tk.Button(root, text="Add Task", command=add_task).grid(row=3, column=0, padx=10, pady=5)
tk.Button(root, text="Delete Task", command=delete_task).grid(row=3, column=1, padx=10, pady=5)
tk.Button(root, text="Update Task", command=update_task).grid(row=3, column=2, padx=10, pady=5)
tk.Button(root, text="Mark as Complete", command=complete_task).grid(row=3, column=3, padx=10, pady=5)

# Create the treeview for displaying tasks
columns = ('id', 'description', 'priority', 'due_date', 'is_complete')
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading('id', text='ID')
tree.heading('description', text='Description')
tree.heading('priority', text='Priority')
tree.heading('due_date', text='Due Date')
tree.heading('is_complete', text='Complete')
tree.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

# Create the filter fields and button
tk.Label(root, text="Filter by Priority:").grid(row=5, column=0, padx=10, pady=5)
entry_filter_priority = tk.Entry(root, width=20)
entry_filter_priority.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Filter by Due Date:").grid(row=5, column=2, padx=10, pady=5)
entry_filter_date = tk.Entry(root, width=20)
entry_filter_date.grid(row=5, column=3, padx=10, pady=5)

tk.Button(root, text="Filter Tasks", command=filter_tasks).grid(row=6, column=1, columnspan=2, padx=10, pady=5)

# Load the tasks initially
load_tasks()

# Run the application
root.mainloop()