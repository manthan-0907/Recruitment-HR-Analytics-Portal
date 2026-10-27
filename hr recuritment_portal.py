import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json, os, csv
from datetime import datetime
 
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hr_data.json")
 
# ---------------- COLORS & FONTS ----------------
BG, WHITE, DARK = "#F1F5F9", "#FFFFFF", "#0F1E4A"
BLUE, BLUE_LIGHT, GREEN = "#2563EB", "#EFF6FF", "#16A34A"
ORANGE, RED, PURPLE = "#F59E0B", "#DC2626", "#7C3AED"
GRAY, TEXT, BORDER, NAV_ACTIVE = "#64748B", "#0F172A", "#E2E8F0", "#294497"
FONT = "Segoe UI"
 
STATUSES = ["Applied", "Shortlisted", "Interview", "Selected", "Hired", "Rejected"]
STATUS_COLOR = {"Applied": GRAY, "Shortlisted": BLUE, "Interview": ORANGE,
                "Selected": PURPLE, "Hired": GREEN, "Rejected": RED}
 
DEFAULT_DATA = {
    "candidates": [
        {"id": 1, "name": "Rahul Sharma", "job": "Python Developer", "edu": "B.Tech", "exp": "2 Years", "status": "Shortlisted"},
        {"id": 2, "name": "Priya Patil", "job": "HR Executive", "edu": "MBA", "exp": "1 Year", "status": "Interview"},
        {"id": 3, "name": "Amit Verma", "job": "Data Analyst", "edu": "B.Tech", "exp": "3 Years", "status": "Hired"},
        {"id": 4, "name": "Sneha Joshi", "job": "Web Developer", "edu": "BCA", "exp": "2 Years", "status": "Applied"},
        {"id": 5, "name": "Rohan Gupta", "job": "Software Engineer", "edu": "B.Tech", "exp": "3 Years", "status": "Hired"},
    ],
    "interviews": [
        {"name": "Rahul Sharma", "job": "Python Developer", "date": "25 Sep 2026", "time": "10:00 AM", "mode": "Online"},
        {"name": "Priya Patil", "job": "HR Executive", "date": "26 Sep 2026", "time": "12:00 PM", "mode": "Offline"},
    ],
    "employees": [
        {"name": "Amit Verma", "job": "Data Analyst", "joined": "01 Sep 2026", "dept": "Analytics"},
        {"name": "Rohan Gupta", "job": "Software Engineer", "joined": "05 Sep 2026", "dept": "IT"},
    ],
}
 
 
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return json.loads(json.dumps(DEFAULT_DATA))
 
 
def guess_dept(job):
    j = job.lower()
    if "analyst" in j or "data" in j:
        return "Analytics"
    if "hr" in j:
        return "HR"
    if any(k in j for k in ("developer", "engineer", "python", "web", "software")):
        return "IT"
    return "General"
 
 
def parse_date(s):
    try:
        return datetime.strptime(s, "%d %b %Y")
    except Exception:
        return datetime.max
 
 
class HRApp:
    def __init__(self, root):
        self.root = root
        self.db = load_data()
        root.title("Recruitment & HR Analytics - Phase 3 (Final)")
        root.geometry("1280x760")
        root.minsize(1100, 650)
        root.configure(bg=BG)
        self.setup_style()
        self.build_header()
        self.build_sidebar()
        self.build_pages()
        self.build_footer()
        self.show_page("Dashboard")
        self.tick()
 
    # ---------------- infrastructure ----------------
    def setup_style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background=WHITE, fieldbackground=WHITE, foreground=TEXT,
                    rowheight=36, font=(FONT, 10), borderwidth=0)
        s.configure("Treeview.Heading", background="#E8EEF7", foreground=TEXT,
                    font=(FONT, 10, "bold"), relief="flat", padding=6)
        s.map("Treeview", background=[("selected", BLUE_LIGHT)], foreground=[("selected", BLUE)])
 
    def save(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.db, f, indent=2)
        except Exception as e:
            messagebox.showerror("Save Error", str(e))
 
    def toast(self, msg, color=GREEN):
        self.status.config(text="  " + msg, fg=color)
        self.root.after(3500, lambda: self.status.config(text="  Ready", fg=GRAY))
 
    def tick(self):
        self.clock.config(text=datetime.now().strftime("%a, %d %b %Y  |  %I:%M:%S %p"))
        self.root.after(1000, self.tick)
 
    # ---------------- layout ----------------
    def build_header(self):
        h = tk.Frame(self.root, bg=WHITE, height=75, highlightbackground=BORDER, highlightthickness=1)
        h.pack(fill="x")
        h.pack_propagate(False)
        tk.Label(h, text="RECRUITMENT & HR ANALYTICS", bg=WHITE, fg=TEXT,
                 font=(FONT, 21, "bold")).pack(side="left", padx=30)
        tk.Label(h, text="PHASE 3 - FINAL", bg=BLUE_LIGHT, fg=BLUE, font=(FONT, 10, "bold"),
                 padx=15, pady=8).pack(side="right", padx=30)
        self.clock = tk.Label(h, bg=WHITE, fg=GRAY, font=(FONT, 10))
        self.clock.pack(side="right", padx=10)
 
    def build_footer(self):
        self.status = tk.Label(self.root, text="  Ready", bg=WHITE, fg=GRAY, anchor="w",
                               font=(FONT, 9), pady=5, highlightbackground=BORDER, highlightthickness=1)
        self.status.pack(side="bottom", fill="x")
 
    def build_sidebar(self):
        sb = tk.Frame(self.root, bg=DARK, width=230)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)
        tk.Label(sb, text="HR PORTAL", bg=DARK, fg=WHITE, font=(FONT, 19, "bold")).pack(pady=(30, 3))
        tk.Label(sb, text="Recruitment Management", bg=DARK, fg="#93C5FD",
                 font=(FONT, 9)).pack(pady=(0, 25))
        self.nav = {}
        for name, icon in [("Dashboard", "\u25A3"), ("Candidates", "\u263A"),
                           ("Interviews", "\u29D7"), ("Employees", "\u2692"), ("Analytics", "\u2593")]:
            b = tk.Button(sb, text=f"  {icon}   {name}", bg=DARK, fg="#CBD5E1", anchor="w",
                          activebackground=NAV_ACTIVE, activeforeground=WHITE, relief="flat",
                          font=(FONT, 10, "bold"), padx=22, pady=13, cursor="hand2", bd=0,
                          command=lambda n=name: self.show_page(n))
            b.pack(fill="x", padx=10, pady=3)
            b.bind("<Enter>", lambda e, b=b: b["bg"] == DARK and b.config(bg="#1B2F6B"))
            b.bind("<Leave>", lambda e, b=b: b["bg"] == "#1B2F6B" and b.config(bg=DARK))
            self.nav[name] = b
        tk.Button(sb, text="  \u2715   Exit Portal", command=self.root.destroy, bg="#991B1B", fg=WHITE,
                  activebackground=RED, activeforeground=WHITE, font=(FONT, 10, "bold"), relief="flat",
                  anchor="w", padx=22, pady=12, cursor="hand2").pack(side="bottom", fill="x", padx=15, pady=20)
 
    def build_pages(self):
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self.title = tk.Label(self.main, bg=BG, fg=TEXT, font=(FONT, 22, "bold"))
        self.title.pack(anchor="w", padx=25, pady=(18, 8))
        self.pages = {}
        for name in ("Dashboard", "Candidates", "Interviews", "Employees", "Analytics"):
            self.pages[name] = tk.Frame(self.main, bg=BG)
        self.build_dashboard()
        self.build_candidates()
        self.build_interviews()
        self.build_employees()
        self.build_analytics()
 
    def show_page(self, name):
        for n, p in self.pages.items():
            p.pack_forget()
            self.nav[n].config(bg=DARK, fg="#CBD5E1")
        self.pages[name].pack(fill="both", expand=True, padx=25, pady=(0, 15))
        self.nav[name].config(bg=NAV_ACTIVE, fg=WHITE)
        self.title.config(text=name if name != "Dashboard" else "HR Dashboard")
        self.current = name
        self.refresh_all()
 
    # ---------------- reusable widgets ----------------
    def make_card(self, parent, title, color):
        f = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        f.pack(side="left", expand=True, fill="both", padx=6)
        tk.Frame(f, bg=color, height=4).pack(fill="x")
        tk.Label(f, text=title, bg=WHITE, fg=GRAY, font=(FONT, 9, "bold")).pack(pady=(14, 2))
        lbl = tk.Label(f, text="0", bg=WHITE, fg=color, font=(FONT, 25, "bold"))
        lbl.pack(pady=(0, 12))
        return lbl
 
    def make_box(self, parent, title):
        box = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        tk.Label(box, text=title, bg=WHITE, fg=TEXT, font=(FONT, 13, "bold")).pack(anchor="w", padx=18, pady=(14, 6))
        return box
 
    def make_tree(self, parent, cols, widths):
        wrap = tk.Frame(parent, bg=WHITE)
        wrap.pack(fill="both", expand=True, padx=18, pady=(0, 16))
        tree = ttk.Treeview(wrap, columns=cols, show="headings", selectmode="browse")
        sc = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sc.set)
        for c, w in zip(cols, widths):
            tree.heading(c, text=c)
            tree.column(c, width=w, anchor="w")
        tree.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")
        for st, col in STATUS_COLOR.items():
            tree.tag_configure(st, foreground=col)
        return tree
 
    def btn(self, parent, text, color, cmd):
        b = tk.Button(parent, text=text, command=cmd, bg=color, fg=WHITE, activebackground=color,
                      activeforeground=WHITE, font=(FONT, 9, "bold"), relief="flat", padx=14, pady=7,
                      cursor="hand2", bd=0)
        b.pack(side="left", padx=4)
        return b
 
    def draw_bars(self, canvas, items):
        """items: list of (label, value, color)"""
        canvas.delete("all")
        w = max(canvas.winfo_width(), 300)
        top = max([v for _, v, _ in items] + [1])
        y = 14
        for label, val, col in items:
            canvas.create_text(8, y + 14, text=label, anchor="w", font=(FONT, 10), fill=TEXT)
            x0, maxw = 130, w - 130 - 60
            canvas.create_rectangle(x0, y + 4, x0 + maxw, y + 24, fill="#EEF2F7", outline="")
            canvas.create_rectangle(x0, y + 4, x0 + max(maxw * val / top, 2 if val else 0), y + 24,
                                    fill=col, outline="")
            canvas.create_text(x0 + maxw + 10, y + 14, text=str(val), anchor="w",
                               font=(FONT, 10, "bold"), fill=col)
            y += 38
 
    def form(self, title, fields, on_save, initial=None):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.configure(bg=WHITE)
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()
        tk.Label(win, text=title.upper(), bg=WHITE, fg=TEXT, font=(FONT, 16, "bold")).pack(pady=18, padx=40)
        widgets = {}
        for label, kind, opts in fields:
            tk.Label(win, text=label, bg=WHITE, fg=TEXT, font=(FONT, 10, "bold")).pack(anchor="w", padx=40)
            if kind == "combo":
                w = ttk.Combobox(win, values=opts, state="readonly", width=33, font=(FONT, 10))
                w.set((initial or {}).get(label, opts[0]))
            else:
                w = tk.Entry(win, font=(FONT, 10), width=35, relief="solid", bd=1)
                w.insert(0, (initial or {}).get(label, ""))
            w.pack(padx=40, pady=(2, 8), ipady=4)
            widgets[label] = w
 
        def submit():
            vals = {k: w.get().strip() for k, w in widgets.items()}
            if on_save(vals) is not False:
                win.destroy()
 
        tk.Button(win, text="SAVE", command=submit, bg=BLUE, fg=WHITE, font=(FONT, 10, "bold"),
                  relief="flat", padx=30, pady=9, cursor="hand2").pack(pady=18)
        win.bind("<Return>", lambda e: submit())
 
    def selected_candidate(self):
        sel = self.c_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select a candidate first.")
            return None
        return next(c for c in self.db["candidates"] if str(c["id"]) == sel[0])
 
    # ---------------- DASHBOARD ----------------
    def build_dashboard(self):
        p = self.pages["Dashboard"]
        row = tk.Frame(p, bg=BG)
        row.pack(fill="x")
        self.d_total = self.make_card(row, "TOTAL CANDIDATES", BLUE)
        self.d_int = self.make_card(row, "INTERVIEWS", ORANGE)
        self.d_emp = self.make_card(row, "EMPLOYEES", GREEN)
        self.d_sel = self.make_card(row, "SELECTED / HIRED", PURPLE)
        bottom = tk.Frame(p, bg=BG)
        bottom.pack(fill="both", expand=True, pady=(15, 0))
        left = self.make_box(bottom, "Hiring Pipeline")
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.d_canvas = tk.Canvas(left, bg=WHITE, highlightthickness=0)
        self.d_canvas.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        self.d_canvas.bind("<Configure>", lambda e: self.refresh_dashboard())
        right = self.make_box(bottom, "Upcoming Interviews")
        right.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.d_tree = self.make_tree(right, ("Candidate", "Date", "Time"), (150, 110, 90))
 
    def refresh_dashboard(self):
        c = self.db["candidates"]
        self.d_total.config(text=len(c))
        self.d_int.config(text=len(self.db["interviews"]))
        self.d_emp.config(text=len(self.db["employees"]))
        self.d_sel.config(text=sum(1 for x in c if x["status"] in ("Selected", "Hired")))
        self.draw_bars(self.d_canvas, [(s, sum(1 for x in c if x["status"] == s), STATUS_COLOR[s]) for s in STATUSES])
        self.d_tree.delete(*self.d_tree.get_children())
        for i in sorted(self.db["interviews"], key=lambda i: parse_date(i["date"]))[:8]:
            self.d_tree.insert("", "end", values=(i["name"], i["date"], i["time"]))
 
    # ---------------- CANDIDATES ----------------
    def build_candidates(self):
        p = self.pages["Candidates"]
        bar = tk.Frame(p, bg=BG)
        bar.pack(fill="x", pady=(0, 10))
        tk.Label(bar, text="Search:", bg=BG, fg=GRAY, font=(FONT, 10)).pack(side="left", padx=(0, 5))
        self.search = tk.StringVar()
        self.search.trace_add("write", lambda *a: self.refresh_candidates())
        tk.Entry(bar, textvariable=self.search, font=(FONT, 10), width=22, relief="solid", bd=1).pack(side="left", ipady=4)
        self.filter = ttk.Combobox(bar, values=["All"] + STATUSES, state="readonly", width=12)
        self.filter.set("All")
        self.filter.pack(side="left", padx=8)
        self.filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_candidates())
        for t, col, cmd in [("+ Add", BLUE, self.add_candidate), ("Update Status", PURPLE, self.update_status),
                            ("Schedule", ORANGE, self.schedule_selected), ("Hire", GREEN, self.hire_selected),
                            ("Delete", RED, self.delete_candidate), ("Export CSV", GRAY, self.export_csv)]:
            self.btn(bar, t, col, cmd)
        box = self.make_box(p, "Candidate Applications")
        box.pack(fill="both", expand=True)
        self.c_tree = self.make_tree(box, ("ID", "Candidate", "Job Position", "Education", "Experience", "Status"),
                                     (50, 190, 190, 120, 120, 120))
        self.c_tree.bind("<Double-1>", lambda e: self.edit_candidate())
 
    def refresh_candidates(self):
        q, f = self.search.get().lower(), self.filter.get()
        self.c_tree.delete(*self.c_tree.get_children())
        for c in self.db["candidates"]:
            if f != "All" and c["status"] != f:
                continue
            if q and q not in (c["name"] + c["job"] + c["edu"]).lower():
                continue
            self.c_tree.insert("", "end", iid=str(c["id"]), tags=(c["status"],),
                               values=(c["id"], c["name"], c["job"], c["edu"], c["exp"], c["status"]))
 
    def candidate_fields(self):
        return [("Candidate Name", "entry", None), ("Job Position", "entry", None),
                ("Education", "entry", None), ("Experience", "entry", None)]
 
    def add_candidate(self):
        def save(v):
            if not v["Candidate Name"] or not v["Job Position"]:
                messagebox.showwarning("Warning", "Enter candidate name and job position.")
                return False
            nid = max([c["id"] for c in self.db["candidates"]] + [0]) + 1
            self.db["candidates"].append({"id": nid, "name": v["Candidate Name"], "job": v["Job Position"],
                                          "edu": v["Education"], "exp": v["Experience"], "status": "Applied"})
            self.save(); self.refresh_all(); self.toast("Candidate added successfully")
        self.form("Add Candidate", self.candidate_fields(), save)
 
    def edit_candidate(self):
        c = self.selected_candidate()
        if not c:
            return
        def save(v):
            if not v["Candidate Name"] or not v["Job Position"]:
                messagebox.showwarning("Warning", "Name and job position are required.")
                return False
            c.update(name=v["Candidate Name"], job=v["Job Position"], edu=v["Education"], exp=v["Experience"])
            self.save(); self.refresh_all(); self.toast("Candidate updated")
        self.form("Edit Candidate", self.candidate_fields(), save,
                  {"Candidate Name": c["name"], "Job Position": c["job"], "Education": c["edu"], "Experience": c["exp"]})
 
    def update_status(self):
        c = self.selected_candidate()
        if not c:
            return
        def save(v):
            if v["Status"] == "Hired":
                messagebox.showinfo("Use Hire", "Use the Hire button to hire a candidate.")
                return False
            c["status"] = v["Status"]
            self.save(); self.refresh_all(); self.toast(f"{c['name']} -> {v['Status']}")
        self.form("Update Status", [("Status", "combo", [s for s in STATUSES if s != "Hired"])], save,
                  {"Status": c["status"] if c["status"] != "Hired" else "Selected"})
 
    def schedule_selected(self):
        c = self.selected_candidate()
        if c:
            self.schedule_dialog(c)
 
    def schedule_dialog(self, c):
        def save(v):
            if parse_date(v["Date (DD Mon YYYY)"]) == datetime.max:
                messagebox.showwarning("Date", "Use date format like 25 Sep 2026.")
                return False
            if not v["Time"]:
                messagebox.showwarning("Time", "Enter interview time.")
                return False
            self.db["interviews"].append({"name": c["name"], "job": c["job"], "date": v["Date (DD Mon YYYY)"],
                                          "time": v["Time"], "mode": v["Mode"]})
            if c["status"] in ("Applied", "Shortlisted"):
                c["status"] = "Interview"
            self.save(); self.refresh_all(); self.toast(f"Interview scheduled for {c['name']}")
        self.form(f"Schedule: {c['name']}", [("Date (DD Mon YYYY)", "entry", None), ("Time", "entry", None),
                                              ("Mode", "combo", ["Online", "Offline"])], save,
                  {"Date (DD Mon YYYY)": datetime.now().strftime("%d %b %Y"), "Time": "10:00 AM"})
 
    def hire_selected(self):
        c = self.selected_candidate()
        if not c:
            return
        if c["status"] != "Selected":
            messagebox.showinfo("Hire", "Only candidates with status 'Selected' can be hired.\nUse Update Status first.")
            return
        self.db["employees"].append({"name": c["name"], "job": c["job"],
                                     "joined": datetime.now().strftime("%d %b %Y"), "dept": guess_dept(c["job"])})
        c["status"] = "Hired"
        self.save(); self.refresh_all(); self.toast(f"{c['name']} hired successfully")
 
    def delete_candidate(self):
        c = self.selected_candidate()
        if c and messagebox.askyesno("Delete", f"Delete candidate {c['name']}?"):
            self.db["candidates"].remove(c)
            self.save(); self.refresh_all(); self.toast("Candidate deleted", RED)
 
    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")],
                                            initialfile="candidates.csv")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ID", "Candidate", "Job Position", "Education", "Experience", "Status"])
            for c in self.db["candidates"]:
                w.writerow([c["id"], c["name"], c["job"], c["edu"], c["exp"], c["status"]])
        self.toast("Exported to CSV")
 
    # ---------------- INTERVIEWS ----------------
    def build_interviews(self):
        p = self.pages["Interviews"]
        bar = tk.Frame(p, bg=BG)
        bar.pack(fill="x", pady=(0, 10))
        self.btn(bar, "+ Schedule Interview", ORANGE, self.new_interview)
        self.btn(bar, "Delete", RED, self.delete_interview)
        box = self.make_box(p, "Scheduled Interviews")
        box.pack(fill="both", expand=True)
        self.i_tree = self.make_tree(box, ("Candidate", "Job Position", "Date", "Time", "Mode"),
                                     (200, 200, 140, 120, 120))
 
    def refresh_interviews(self):
        self.i_tree.delete(*self.i_tree.get_children())
        for n, i in enumerate(sorted(self.db["interviews"], key=lambda i: parse_date(i["date"]))):
            self.i_tree.insert("", "end", iid=str(n), values=(i["name"], i["job"], i["date"], i["time"], i["mode"]))
 
    def new_interview(self):
        names = [c["name"] for c in self.db["candidates"] if c["status"] != "Rejected"]
        if not names:
            messagebox.showinfo("Interviews", "No candidates available.")
            return
        def pick(v):
            c = next(x for x in self.db["candidates"] if x["name"] == v["Candidate"])
            self.root.after(100, lambda: self.schedule_dialog(c))
        self.form("Choose Candidate", [("Candidate", "combo", names)], pick)
 
    def delete_interview(self):
        sel = self.i_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Please select an interview first.")
            return
        vals = self.i_tree.item(sel[0])["values"]
        for i in self.db["interviews"]:
            if [i["name"], i["job"], i["date"], i["time"], i["mode"]] == [str(v) for v in vals]:
                self.db["interviews"].remove(i)
                break
        self.save(); self.refresh_all(); self.toast("Interview removed", RED)
 
    # ---------------- EMPLOYEES ----------------
    def build_employees(self):
        p = self.pages["Employees"]
        bar = tk.Frame(p, bg=BG)
        bar.pack(fill="x", pady=(0, 10))
        self.btn(bar, "Remove Employee", RED, self.remove_employee)
        box = self.make_box(p, "Employee Records")
        box.pack(fill="both", expand=True)
        self.e_tree = self.make_tree(box, ("Employee Name", "Position", "Joining Date", "Department"),
                                     (220, 220, 160, 160))
 
    def refresh_employees(self):
        self.e_tree.delete(*self.e_tree.get_children())
        for n, e in enumerate(self.db["employees"]):
            self.e_tree.insert("", "end", iid=str(n), values=(e["name"], e["job"], e["joined"], e["dept"]))
 
    def remove_employee(self):
        sel = self.e_tree.selection()
        if sel and messagebox.askyesno("Remove", "Remove this employee record?"):
            self.db["employees"].pop(int(sel[0]))
            self.save(); self.refresh_all(); self.toast("Employee removed", RED)
        elif not sel:
            messagebox.showinfo("Select", "Please select an employee first.")
 
    # ---------------- ANALYTICS ----------------
    def build_analytics(self):
        p = self.pages["Analytics"]
        row = tk.Frame(p, bg=BG)
        row.pack(fill="x")
        self.a_rate = self.make_card(row, "SELECTION RATE", PURPLE)
        self.a_hire = self.make_card(row, "HIRE RATE", GREEN)
        self.a_rej = self.make_card(row, "REJECTION RATE", RED)
        self.a_open = self.make_card(row, "IN PIPELINE", BLUE)
        bottom = tk.Frame(p, bg=BG)
        bottom.pack(fill="both", expand=True, pady=(15, 0))
        l = self.make_box(bottom, "Candidates by Status")
        l.pack(side="left", fill="both", expand=True, padx=(0, 8))
        self.a_c1 = tk.Canvas(l, bg=WHITE, highlightthickness=0)
        self.a_c1.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        r = self.make_box(bottom, "Employees by Department")
        r.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.a_c2 = tk.Canvas(r, bg=WHITE, highlightthickness=0)
        self.a_c2.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        self.a_c1.bind("<Configure>", lambda e: self.refresh_analytics())
        self.a_c2.bind("<Configure>", lambda e: self.refresh_analytics())
 
    def refresh_analytics(self):
        c = self.db["candidates"]
        total = len(c) or 1
        n = lambda *s: sum(1 for x in c if x["status"] in s)
        self.a_rate.config(text=f"{n('Selected', 'Hired') / total * 100:.1f}%")
        self.a_hire.config(text=f"{n('Hired') / total * 100:.1f}%")
        self.a_rej.config(text=f"{n('Rejected') / total * 100:.1f}%")
        self.a_open.config(text=n("Applied", "Shortlisted", "Interview"))
        self.draw_bars(self.a_c1, [(s, n(s), STATUS_COLOR[s]) for s in STATUSES])
        depts = {}
        for e in self.db["employees"]:
            depts[e["dept"]] = depts.get(e["dept"], 0) + 1
        cols = [BLUE, GREEN, ORANGE, PURPLE, RED, GRAY]
        self.draw_bars(self.a_c2, [(d, v, cols[i % 6]) for i, (d, v) in enumerate(sorted(depts.items()))])
 
    # ---------------- refresh ----------------
    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_candidates()
        self.refresh_interviews()
        self.refresh_employees()
        self.refresh_analytics()
 
 
if __name__ == "__main__":
    root = tk.Tk()
    HRApp(root)
    root.mainloop()