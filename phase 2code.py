import tkinter as tk
from tkinter import ttk, messagebox

# =====================================================
# PHASE 2 - RECRUITMENT & HR ANALYTICS
# =====================================================

candidates = [
    ["1", "Rahul Sharma", "Python Developer", "B.Tech", "2 Years", "Shortlisted"],
    ["2", "Priya Patil", "HR Executive", "MBA", "1 Year", "Interview"],
    ["3", "Amit Verma", "Data Analyst", "B.Tech", "3 Years", "Selected"],
    ["4", "Sneha Joshi", "Web Developer", "BCA", "2 Years", "Applied"],
    ["5", "Rohan Gupta", "Software Engineer", "B.Tech", "3 Years", "Selected"]
]

interviews = [
    ["Rahul Sharma", "Python Developer", "25 Sep 2026", "10:00 AM", "Online"],
    ["Priya Patil", "HR Executive", "26 Sep 2026", "12:00 PM", "Offline"]
]

employees = [
    ["Amit Verma", "Data Analyst", "01 Sep 2026", "Analytics"],
    ["Rohan Gupta", "Software Engineer", "05 Sep 2026", "IT"]
]


# =====================================================
# COLORS
# =====================================================

BG = "#F1F5F9"
WHITE = "#FFFFFF"
DARK = "#0F1E4A"
BLUE = "#2563EB"
BLUE_LIGHT = "#EFF6FF"
GREEN = "#16A34A"
ORANGE = "#F59E0B"
RED = "#DC2626"
PURPLE = "#7C3AED"
GRAY = "#64748B"
TEXT = "#0F172A"


# =====================================================
# WINDOW
# =====================================================

root = tk.Tk()
root.title("Recruitment & HR Analytics - Phase 2")
root.geometry("1200x700")
root.configure(bg=BG)


# =====================================================
# HEADER
# =====================================================

header = tk.Frame(root, bg=WHITE, height=75)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="RECRUITMENT & HR ANALYTICS",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 21, "bold")
).pack(side="left", padx=30, pady=20)

tk.Label(
    header,
    text="PHASE 2",
    bg=BLUE_LIGHT,
    fg=BLUE,
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8
).pack(side="right", padx=30)


# =====================================================
# SIDEBAR
# =====================================================

sidebar = tk.Frame(root, bg=DARK, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="HR PORTAL",
    bg=DARK,
    fg=WHITE,
    font=("Segoe UI", 19, "bold")
).pack(pady=(30, 5))

tk.Label(
    sidebar,
    text="Recruitment Management",
    bg=DARK,
    fg="#93C5FD",
    font=("Segoe UI", 9)
).pack(pady=(0, 25))


# =====================================================
# MAIN AREA
# =====================================================

main = tk.Frame(root, bg=BG)
main.pack(side="left", fill="both", expand=True)


# =====================================================
# TITLE
# =====================================================

title_frame = tk.Frame(main, bg=BG)
title_frame.pack(fill="x", padx=25, pady=20)

page_title = tk.Label(
    title_frame,
    text="HR Dashboard",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 22, "bold")
)
page_title.pack(side="left")


# =====================================================
# DASHBOARD CARDS
# =====================================================

card_frame = tk.Frame(main, bg=BG)
card_frame.pack(fill="x", padx=25)


def card(title, value, color):

    frame = tk.Frame(
        card_frame,
        bg=WHITE,
        height=105,
        highlightbackground="#E2E8F0",
        highlightthickness=1
    )

    frame.pack(
        side="left",
        expand=True,
        fill="both",
        padx=6
    )

    tk.Label(
        frame,
        text=title,
        bg=WHITE,
        fg=GRAY,
        font=("Segoe UI", 9, "bold")
    ).pack(pady=(18, 3))

    label = tk.Label(
        frame,
        text=value,
        bg=WHITE,
        fg=color,
        font=("Segoe UI", 25, "bold")
    )

    label.pack()

    return label


total_card = card(
    "TOTAL CANDIDATES",
    len(candidates),
    BLUE
)

interview_card = card(
    "INTERVIEWS",
    len(interviews),
    ORANGE
)

employee_card = card(
    "EMPLOYEES",
    len(employees),
    GREEN
)

selected = sum(
    1 for c in candidates
    if c[5] == "Selected"
)

selected_card = card(
    "SELECTED",
    selected,
    PURPLE
)


# =====================================================
# TABLE
# =====================================================

table_box = tk.Frame(
    main,
    bg=WHITE,
    highlightbackground="#E2E8F0",
    highlightthickness=1
)

table_box.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=20
)

table_title = tk.Label(
    table_box,
    text="Candidate Applications",
    bg=WHITE,
    fg=TEXT,
    font=("Segoe UI", 14, "bold")
)

table_title.pack(
    anchor="w",
    padx=20,
    pady=15
)

tree = ttk.Treeview(
    table_box,
    show="headings"
)

tree.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20)
)


# =====================================================
# TREEVIEW STYLE
# =====================================================

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=WHITE,
    foreground=TEXT,
    rowheight=36,
    font=("Segoe UI", 10)
)

style.configure(
    "Treeview.Heading",
    background="#E8EEF7",
    foreground=TEXT,
    font=("Segoe UI", 10, "bold")
)


# =====================================================
# CLEAR TABLE
# =====================================================

def clear_table():

    for item in tree.get_children():
        tree.delete(item)


# =====================================================
# CANDIDATES
# =====================================================

def show_candidates():

    page_title.config(text="Candidates")
    table_title.config(text="Candidate Applications")

    clear_table()

    columns = (
        "ID",
        "Candidate",
        "Job Position",
        "Education",
        "Experience",
        "Status"
    )

    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)

    for candidate in candidates:

        tree.insert(
            "",
            "end",
            values=candidate
        )


# =====================================================
# ADD CANDIDATE
# =====================================================

def add_candidate():

    win = tk.Toplevel(root)
    win.title("Add Candidate")
    win.geometry("430x500")
    win.configure(bg=WHITE)
    win.resizable(False, False)

    tk.Label(
        win,
        text="ADD NEW CANDIDATE",
        bg=WHITE,
        fg=TEXT,
        font=("Segoe UI", 18, "bold")
    ).pack(pady=20)

    fields = [
        "Candidate Name",
        "Job Position",
        "Education",
        "Experience"
    ]

    entries = []

    for field in fields:

        tk.Label(
            win,
            text=field,
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=40)

        entry = tk.Entry(
            win,
            font=("Segoe UI", 10),
            width=35
        )

        entry.pack(
            padx=40,
            pady=7,
            ipady=6
        )

        entries.append(entry)

    def save():

        name = entries[0].get()
        job = entries[1].get()
        education = entries[2].get()
        experience = entries[3].get()

        if name == "" or job == "":
            messagebox.showwarning(
                "Warning",
                "Enter candidate name and job position."
            )
            return

        new_id = str(len(candidates) + 1)

        candidates.append([
            new_id,
            name,
            job,
            education,
            experience,
            "Applied"
        ])

        total_card.config(text=len(candidates))

        show_candidates()

        messagebox.showinfo(
            "Success",
            "Candidate added successfully!"
        )

        win.destroy()

    tk.Button(
        win,
        text="SAVE CANDIDATE",
        command=save,
        bg=BLUE,
        fg=WHITE,
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        padx=20,
        pady=10
    ).pack(pady=20)


# =====================================================
# INTERVIEWS
# =====================================================

def show_interviews():

    page_title.config(text="Interview Schedule")
    table_title.config(text="Scheduled Interviews")

    clear_table()

    columns = (
        "Candidate",
        "Job Position",
        "Date",
        "Time",
        "Mode"
    )

    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=180)

    for interview in interviews:

        tree.insert(
            "",
            "end",
            values=interview
        )


# =====================================================
# EMPLOYEES
# =====================================================

def show_employees():

    page_title.config(text="Employees")
    table_title.config(text="Employee Records")

    clear_table()

    columns = (
        "Employee Name",
        "Position",
        "Joining Date",
        "Department"
    )

    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=200)

    for employee in employees:

        tree.insert(
            "",
            "end",
            values=employee
        )


# =====================================================
# ANALYTICS
# =====================================================

def show_analytics():

    page_title.config(text="HR Analytics")
    table_title.config(text="Recruitment Analytics")

    clear_table()

    total = len(candidates)

    applied = sum(
        1 for c in candidates
        if c[5] == "Applied"
    )

    shortlisted = sum(
        1 for c in candidates
        if c[5] == "Shortlisted"
    )

    interview = sum(
        1 for c in candidates
        if c[5] == "Interview"
    )

    selected = sum(
        1 for c in candidates
        if c[5] == "Selected"
    )

    rejected = sum(
        1 for c in candidates
        if c[5] == "Rejected"
    )

    rate = 0

    if total > 0:
        rate = (selected / total) * 100

    columns = (
        "HR Metric",
        "Result"
    )

    tree["columns"] = columns

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=300)

    data = [
        ["Total Candidates", total],
        ["Applications Received", total],
        ["Applied", applied],
        ["Shortlisted", shortlisted],
        ["Interviews", len(interviews)],
        ["Interview Stage", interview],
        ["Selected", selected],
        ["Rejected", rejected],
        ["Employees Hired", len(employees)],
        ["Selection Rate", f"{rate:.2f}%"]
    ]

    for row in data:
        tree.insert(
            "",
            "end",
            values=row
        )


# =====================================================
# NAVIGATION BUTTON
# =====================================================

def nav_button(text, command):

    button = tk.Button(
        sidebar,
        text=text,
        command=command,
        bg=DARK,
        fg="#CBD5E1",
        activebackground="#2444A8",
        activeforeground=WHITE,
        font=("Segoe UI", 10, "bold"),
        anchor="w",
        relief="flat",
        padx=25,
        pady=13,
        cursor="hand2"
    )

    button.pack(
        fill="x",
        padx=10,
        pady=3
    )


# =====================================================
# SIDEBAR MENU
# =====================================================

nav_button(
    "  Dashboard",
    show_candidates
)

nav_button(
    "  Candidates",
    show_candidates
)

nav_button(
    "  + Add Candidate",
    add_candidate
)

nav_button(
    "  Interview Schedule",
    show_interviews
)

nav_button(
    "  Employees",
    show_employees
)

nav_button(
    "  HR Analytics",
    show_analytics
)


# =====================================================
# EXIT
# =====================================================

tk.Button(
    sidebar,
    text="  Exit Portal",
    command=root.destroy,
    bg="#991B1B",
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    font=("Segoe UI", 10, "bold"),
    relief="flat",
    anchor="w",
    padx=25,
    pady=12
).pack(
    side="bottom",
    fill="x",
    padx=15,
    pady=20
)


# =====================================================
# START
# =====================================================

show_candidates()

root.mainloop()