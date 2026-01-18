import tkinter as tk

def add_task():
    task = entry.get()
    if task != "":
        # Add the task to the bottom of the list
        listbox.insert(tk.END, task)
        entry.delete(0, tk.END)

def delete_task():
    # Get the index of the selected item and remove it
    try:
        selected_index = listbox.curselection()[0]
        listbox.delete(selected_index)
    except:
        pass # Do nothing if nothing is selected

def complete_task():
    try:
        index = listbox.curselection()[0]
        current_text = listbox.get(index)
        
        # Check if it's already completed
        if " (DONE)" not in current_text:
            # Change text to show it is finished (like a strike-through)
            new_text = "✓ " + current_text + " (DONE)"
            listbox.delete(index)
            listbox.insert(index, new_text)
            
            # Change the color to gray to show it's completed
            listbox.itemconfig(index, fg="gray")
    except:
        pass

# 1. Create the Main Window
root = tk.Tk()
root.title("My Easy To-Do")
root.geometry("300x400")

# 2. Add an Entry box (where you type)
entry = tk.Entry(root, font=("Arial", 12))
entry.pack(pady=10)

# 3. Add the "Add" Button
add_button = tk.Button(root, text="Add Task", command=add_task, bg="teal", fg="white")
add_button.pack(pady=5)

# 4. Add the Listbox (the white box that shows tasks)
listbox = tk.Listbox(root, font=("Arial", 12), width=25, height=10)
listbox.pack(pady=10)

# 5. Add "Complete" and "Delete" Buttons
complete_button = tk.Button(root, text="Complete Task", command=complete_task, bg="blue", fg="white")
complete_button.pack(side="left", padx=20, pady=10)

delete_button = tk.Button(root, text="Delete", command=delete_task, bg="red", fg="white")
delete_button.pack(side="right", padx=20, pady=10)

root.mainloop()