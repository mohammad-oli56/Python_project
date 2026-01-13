import tkinter as tk
from tkinter import ttk, messagebox
import re

# ---------------- Database ----------------
contacts_list = []

# ---------------- Functions ----------------
def refresh_contacts(filtered_list=None):
    """Show contacts (either all or search results)"""
    for widget in list_frame.winfo_children():
        widget.destroy()

    display_list = filtered_list if filtered_list is not None else contacts_list

    if not display_list:
        ttk.Label(list_frame, text="No contacts found.", font=("Arial", 10, "italic"), background="white").pack(pady=20)
        return

    for i, contact in enumerate(display_list):
        # Find actual index in original list for deletion
        actual_idx = contacts_list.index(contact)
        
        row = ttk.Frame(list_frame, style="Card.TFrame")
        row.pack(fill="x", pady=5, padx=10)

        # Info Section
        info_frame = ttk.Frame(row, style="Card.TFrame")
        info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        ttk.Label(info_frame, text=contact['name'], font=("Arial", 14, "bold"), background="white").pack(anchor="w")
        ttk.Label(info_frame, text=contact['phone'], font=("Arial", 10), foreground="#555", background="white").pack(anchor="w")
        ttk.Label(info_frame, text=contact['email'], font=("Arial", 9), foreground="#777", background="white").pack(anchor="w")

        # Action Section (Delete Button)
        btn_del = tk.Button(row, text="✕", bg="#ff7675", fg="white", font=("Arial", 12, "bold"),
                           relief="flat", command=lambda idx=actual_idx: delete_contact(idx))
        btn_del.pack(side="right", fill="y")

def save_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()

    if len(name) < 3:
        messagebox.showerror("Error", "Name is too short")
        return
    if not re.match(r"\d{11}$", phone):
        messagebox.showerror("Error", "Phone must be 11 digits")
        return
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "Invalid Email")
        return

    contacts_list.append({"name": name, "phone": phone, "email": email})
    
    # Clear fields
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    
    refresh_contacts()

def search_contact(event=None):
    query = search_entry.get().strip().lower()
    results = [c for c in contacts_list if query in c["name"].lower() or query in c["phone"]]
    refresh_contacts(results)

def delete_contact(index):
    if messagebox.askyesno("Delete", "Delete this contact?"):
        contacts_list.pop(index)
        refresh_contacts()

# ---------------- UI Setup ----------------
root = tk.Tk()
root.title("Phone Book")
# Mobile Portrait Dimensions
root.geometry("400x700")
root.configure(bg="#f0f2f5")

# Styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Card.TFrame", background="white", relief="flat")
style.configure("Header.TLabel", background="#2d3436", foreground="white", font=("Arial", 16, "bold"))

# --- Sticky Header ---
header = tk.Frame(root, bg="#2d3436", height=60)
header.pack(fill="x")
tk.Label(header, text="My Contacts", bg="#2d3436", fg="white", font=("Arial", 18, "bold")).pack(pady=15)

# --- Add Contact Form (Collapsible/Scrollable Area) ---
form_container = ttk.Frame(root)
form_container.pack(fill="x", padx=15, pady=10)

# Input Helper Function for Mobile Look
def create_input(parent, label_text):
    tk.Label(parent, text=label_text, font=("Arial", 9, "bold"), fg="#636e72").pack(anchor="w", pady=(5,0))
    entry = tk.Entry(parent, font=("Arial", 12), bd=0, highlightthickness=1, highlightbackground="#dfe6e9")
    entry.pack(fill="x", ipady=8)
    return entry

name_entry = create_input(form_container, "FULL NAME")
phone_entry = create_input(form_container, "PHONE NUMBER")
email_entry = create_input(form_container, "EMAIL ADDRESS")

btn_save = tk.Button(form_container, text="ADD CONTACT", bg="#0984e3", fg="white", 
                     font=("Arial", 10, "bold"), relief="flat", command=save_contact, pady=10)
btn_save.pack(fill="x", pady=15)

# --- Search Bar ---
search_frame = tk.Frame(root, bg="#dfe6e9", padx=15, pady=10)
search_frame.pack(fill="x")
search_entry = tk.Entry(search_frame, font=("Arial", 11), bd=0, highlightthickness=0)
search_entry.pack(fill="x", ipady=8)
search_entry.insert(0, "Search contacts...")
search_entry.bind("<KeyRelease>", search_contact)
search_entry.bind("<FocusIn>", lambda e: search_entry.delete(0, tk.END) if search_entry.get() == "Search contacts..." else None)

# --- Scrollable Contact List ---
list_canvas = tk.Canvas(root, bg="#f0f2f5", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=list_canvas.yview)
list_frame = ttk.Frame(list_canvas)

list_frame.bind("<Configure>", lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all")))
list_canvas.create_window((0, 0), window=list_frame, anchor="nw", width=380) # Fixed width for scroll
list_canvas.configure(yscrollcommand=scrollbar.set)

list_canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

refresh_contacts()
root.mainloop()