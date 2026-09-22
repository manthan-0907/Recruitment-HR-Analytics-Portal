import tkinter as tk
from tkinter import ttk, messagebox

candidates = [
    ["1", "Rahul Sharma", "Python Developer", "B.Tech", "2 Years", "Shortlisted"],
    ["2", "Priya Patil", "HR Executive", "MBA", "1 Year", "Interview"],
    ["3", "Amit Verma", "Data Analyst", "B.Tech", "3 Years", "Selected"]
]

status = ["Applied", "Shortlisted", "Interview", "Selected", "Rejected"]

root = tk.Tk()
root.title("HR Recruitment Portal")
root.geometry("900x550")
root.configure(bg="#F1F5F9")

tk.Label(root, text="Recruitment & HR Portal",
         font=("Arial", 22, "bold"),
         bg="#0F1E4A", fg="white",
         pady=15).pack(fill="x")

frame = tk.Frame(root, bg="#F1F5F9")
frame.pack(pady=20)

# Entries
tk.Label(frame, text="Name", bg="#F1F5F9").grid(row=0, column=0)
name = tk.Entry(frame)
name.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Job", bg="#F1F5F9").grid(row=0, column=2)
job = tk.Entry(frame)
job.grid(row=0, column=3, padx=5)

tk.Label(frame, text="Education", bg="#F1F5F9").grid(row=1, column=0)
edu = ttk.Combobox(frame, values=["B.Tech", "MBA", "BCA", "MCA"])
edu.grid(row=1, column=1, padx=5)
edu.set("B.Tech")

tk.Label(frame, text="Experience", bg="#F1F5F9").grid(row=1, column=2)
exp = ttk.Combobox(frame, values=["Fresher", "1 Year", "2 Years", "3 Years"])
exp.grid(row=1, column=3, padx=5)
exp.set("Fresher")

# Table
columns = ("ID", "Name", "Job", "Education", "Experience", "Status")
table = ttk.Treeview(root, columns=columns, show="headings")

for c in columns:
    table.heading(c, text=c)
    table.column(c, width=130)

table.pack(fill="both", expand=True, padx=20, pady=10)


def refresh():
    table.delete(*table.get_children())
    for c in candidates:
        table.insert("", "end", values=c)


def add_candidate():
    if not name.get() or not job.get():
        messagebox.showwarning("Warning", "Enter Name and Job")
        return

    new_id = str(len(candidates) + 1)

    candidates.append([
        new_id,
        name.get(),
        job.get(),
        edu.get(),
        exp.get(),
        "Applied"
    ])

    name.delete(0, "end")
    job.delete(0, "end")
    refresh()


def delete_candidate():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a candidate")
        return

    item = table.item(selected[0])
    candidate_id = item["values"][0]

    for c in candidates:
        if c[0] == candidate_id:
            candidates.remove(c)
            break

    refresh()


def update_status():
    selected = table.selection()

    if not selected:
        messagebox.showwarning("Warning", "Select a candidate")
        return

    item = table.item(selected[0])
    candidate_id = item["values"][0]

    win = tk.Toplevel(root)
    win.title("Update Status")
    win.geometry("300x180")

    tk.Label(win, text="Select Status").pack(pady=10)

    box = ttk.Combobox(win, values=status, state="readonly")
    box.pack()
    box.set("Applied")

    def save():
        for c in candidates:
            if c[0] == candidate_id:
                c[5] = box.get()

        refresh()
        win.destroy()

    tk.Button(win, text="Save", command=save,
              bg="#2563EB", fg="white").pack(pady=20)


tk.Button(frame, text="Add Candidate",
          command=add_candidate,
          bg="#2563EB", fg="white").grid(row=2, column=0, pady=15)

tk.Button(frame, text="Update Status",
          command=update_status,
          bg="#F59E0B", fg="white").grid(row=2, column=1)

tk.Button(frame, text="Delete",
          command=delete_candidate,
          bg="#DC2626", fg="white").grid(row=2, column=2)

refresh()
root.mainloop()