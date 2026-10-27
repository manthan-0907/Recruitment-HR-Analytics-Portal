"use strict";

const STORAGE_KEY = "recruitment-hr-analytics-portal-v1";
const STATUSES = ["Applied", "Shortlisted", "Interview", "Selected", "Hired", "Rejected"];
const STATUS_COLORS = {
  Applied: "#64748b",
  Shortlisted: "#2563eb",
  Interview: "#d97706",
  Selected: "#7c3aed",
  Hired: "#16a34a",
  Rejected: "#dc2626",
};
const DEFAULT_DATA = {
  candidates: [
    { id: 1, name: "Rahul Sharma", job: "Python Developer", edu: "B.Tech", exp: "2 Years", status: "Shortlisted" },
    { id: 2, name: "Priya Patil", job: "HR Executive", edu: "MBA", exp: "1 Year", status: "Interview" },
    { id: 3, name: "Amit Verma", job: "Data Analyst", edu: "B.Tech", exp: "3 Years", status: "Hired" },
    { id: 4, name: "Sneha Joshi", job: "Web Developer", edu: "BCA", exp: "2 Years", status: "Applied" },
    { id: 5, name: "Rohan Gupta", job: "Software Engineer", edu: "B.Tech", exp: "3 Years", status: "Hired" },
  ],
  interviews: [
    { id: 1, name: "Rahul Sharma", job: "Python Developer", date: "2026-09-25", time: "10:00 AM", mode: "Online" },
    { id: 2, name: "Priya Patil", job: "HR Executive", date: "2026-09-26", time: "12:00 PM", mode: "Offline" },
  ],
  employees: [
    { id: 1, name: "Amit Verma", job: "Data Analyst", joined: "2026-09-01", dept: "Analytics" },
    { id: 2, name: "Rohan Gupta", job: "Software Engineer", joined: "2026-09-05", dept: "IT" },
  ],
};

const pageContent = document.querySelector("#page-content");
const pageTitle = document.querySelector("#page-title");
const notice = document.querySelector("#notice");
const dialog = document.querySelector("#form-dialog");
const form = document.querySelector("#data-form");
const dialogFields = document.querySelector("#dialog-fields");
let currentPage = "Dashboard";
let selectedCandidateId = null;
let selectedInterviewId = null;
let selectedEmployeeId = null;
let toastTimer;
let storageNotice = "";

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function normalizeState(value) {
  if (!value || !Array.isArray(value.candidates) || !Array.isArray(value.interviews) || !Array.isArray(value.employees)) {
    throw new Error("Saved portal data has an invalid format.");
  }
  value.candidates = value.candidates.map((candidate, index) => ({
    ...candidate,
    id: Number(candidate.id) || index + 1,
  }));
  value.interviews = value.interviews.map((interview, index) => ({
    ...interview,
    id: Number(interview.id) || index + 1,
    date: toISODate(interview.date),
  }));
  value.employees = value.employees.map((employee, index) => ({
    ...employee,
    id: Number(employee.id) || index + 1,
    joined: toISODate(employee.joined),
  }));
  return value;
}

function toISODate(value) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(value || "")) return value;
  const parsed = new Date(value || "");
  if (Number.isNaN(parsed.getTime())) return "";
  const day = String(parsed.getDate()).padStart(2, "0");
  const month = String(parsed.getMonth() + 1).padStart(2, "0");
  return `${parsed.getFullYear()}-${month}-${day}`;
}

let db;
try {
  const saved = localStorage.getItem(STORAGE_KEY);
  db = normalizeState(saved ? JSON.parse(saved) : clone(DEFAULT_DATA));
  if (!saved) localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
} catch (error) {
  db = clone(DEFAULT_DATA);
  storageNotice = `Saved data could not be loaded: ${error.message} Your existing browser data was not changed; edits may not persist.`;
}

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[char]);
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(db));
    return true;
  } catch (error) {
    showToast(`Could not save changes in this browser: ${error.message}`, true);
    return false;
  }
}

function showToast(message, isError = false) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.add("visible");
  window.clearTimeout(toastTimer);
  toastTimer = window.setTimeout(() => toast.classList.remove("visible"), 3200);
}

function dateLabel(iso) {
  if (!iso) return "—";
  const date = new Date(`${iso}T12:00:00`);
  return Number.isNaN(date.getTime())
    ? "—"
    : new Intl.DateTimeFormat("en-GB", { day: "2-digit", month: "short", year: "numeric" }).format(date);
}

function nextId(items) {
  return Math.max(0, ...items.map((item) => Number(item.id) || 0)) + 1;
}

function guessDepartment(job) {
  const title = job.toLowerCase();
  if (title.includes("analyst") || title.includes("data")) return "Analytics";
  if (title.includes("hr")) return "HR";
  if (["developer", "engineer", "python", "web", "software"].some((word) => title.includes(word))) return "IT";
  return "General";
}

function metricCard(label, value, color, hint = "") {
  return `<article class="metric-card" style="--accent:${color}"><p class="metric-label">${label}</p><p class="metric-value">${value}</p>${hint ? `<p class="metric-hint">${hint}</p>` : ""}</article>`;
}

function panel(title, body, subtitle = "") {
  return `<section class="panel"><div class="panel-heading"><div><h2>${title}</h2>${subtitle ? `<p class="panel-subtitle">${subtitle}</p>` : ""}</div></div>${body}</section>`;
}

function bars(items) {
  const max = Math.max(1, ...items.map((item) => item.value));
  if (!items.length) return '<p class="empty-state">No data to display yet.</p>';
  return `<div class="bar-list">${items.map((item) => `<div class="bar-row"><span class="bar-label">${escapeHTML(item.label)}</span><div class="bar-track"><div class="bar-fill" style="width:${item.value ? Math.max(2, item.value / max * 100) : 0}%;background:${item.color}"></div></div><span class="bar-value">${item.value}</span></div>`).join("")}</div>`;
}

function statusPill(status) {
  const color = STATUS_COLORS[status] || "#64748b";
  return `<span class="status-pill" style="color:${color}">${escapeHTML(status)}</span>`;
}

function candidateTable(candidates, selectable = false) {
  if (!candidates.length) return '<div class="empty-state">No candidates match these filters.</div>';
  return `<div class="table-wrap"><table><thead><tr><th>ID</th><th>Candidate</th><th>Job Position</th><th>Education</th><th>Experience</th><th>Status</th></tr></thead><tbody>${candidates.map((candidate) => `<tr data-candidate-id="${candidate.id}" class="${selectable && candidate.id === selectedCandidateId ? "selected-row" : ""}"><td>${candidate.id}</td><td class="primary-cell">${escapeHTML(candidate.name)}</td><td>${escapeHTML(candidate.job)}</td><td>${escapeHTML(candidate.edu)}</td><td>${escapeHTML(candidate.exp)}</td><td>${statusPill(candidate.status)}</td></tr>`).join("")}</tbody></table></div>`;
}

function interviewTable(interviews) {
  if (!interviews.length) return '<div class="empty-state">No interviews scheduled yet.</div>';
  return `<div class="table-wrap"><table><thead><tr><th>Candidate</th><th>Job Position</th><th>Date</th><th>Time</th><th>Mode</th></tr></thead><tbody>${interviews.map((interview) => `<tr data-interview-id="${interview.id}" class="${interview.id === selectedInterviewId ? "selected-row" : ""}"><td class="primary-cell">${escapeHTML(interview.name)}</td><td>${escapeHTML(interview.job)}</td><td>${dateLabel(interview.date)}</td><td>${escapeHTML(interview.time)}</td><td>${escapeHTML(interview.mode)}</td></tr>`).join("")}</tbody></table></div>`;
}

function employeeTable(employees) {
  if (!employees.length) return '<div class="empty-state">No employees in the records yet.</div>';
  return `<div class="table-wrap"><table><thead><tr><th>Employee Name</th><th>Position</th><th>Joining Date</th><th>Department</th></tr></thead><tbody>${employees.map((employee) => `<tr data-employee-id="${employee.id}" class="${employee.id === selectedEmployeeId ? "selected-row" : ""}"><td class="primary-cell">${escapeHTML(employee.name)}</td><td>${escapeHTML(employee.job)}</td><td>${dateLabel(employee.joined)}</td><td>${escapeHTML(employee.dept)}</td></tr>`).join("")}</tbody></table></div>`;
}

function renderDashboard() {
  const candidateCount = db.candidates.length;
  const hiredCount = db.candidates.filter((candidate) => ["Selected", "Hired"].includes(candidate.status)).length;
  const pipeline = STATUSES.map((status) => ({
    label: status,
    value: db.candidates.filter((candidate) => candidate.status === status).length,
    color: STATUS_COLORS[status],
  }));
  const upcoming = [...db.interviews].sort((a, b) => a.date.localeCompare(b.date)).slice(0, 8);
  const interviewRows = upcoming.length
    ? `<div class="table-wrap"><table><thead><tr><th>Candidate</th><th>Date</th><th>Time</th></tr></thead><tbody>${upcoming.map((interview) => `<tr><td class="primary-cell">${escapeHTML(interview.name)}</td><td>${dateLabel(interview.date)}</td><td>${escapeHTML(interview.time)}</td></tr>`).join("")}</tbody></table></div>`
    : '<div class="empty-state">No interviews scheduled yet.</div>';
  return `<div class="cards">${metricCard("TOTAL CANDIDATES", candidateCount, "#2563eb")}${metricCard("INTERVIEWS", db.interviews.length, "#d97706")}${metricCard("EMPLOYEES", db.employees.length, "#16a34a")}${metricCard("SELECTED / HIRED", hiredCount, "#7c3aed")}</div><div class="dashboard-grid">${panel("Hiring Pipeline", bars(pipeline), "Candidate applications by status")}${panel("Upcoming Interviews", interviewRows, "Your next scheduled interviews")}</div>`;
}

function renderCandidates() {
  const query = (document.querySelector("#candidate-search")?.value || "").trim().toLowerCase();
  const status = document.querySelector("#candidate-filter")?.value || "All";
  const filtered = db.candidates.filter((candidate) => {
    const matchesText = `${candidate.name} ${candidate.job} ${candidate.edu}`.toLowerCase().includes(query);
    return matchesText && (status === "All" || candidate.status === status);
  });
  const statusOptions = ["All", ...STATUSES].map((item) => `<option${item === status ? " selected" : ""}>${item}</option>`).join("");
  return `<div class="toolbar"><input id="candidate-search" class="field-control search-control" type="search" placeholder="Search name, job, education…" value="${escapeHTML(query)}" aria-label="Search candidates"><select id="candidate-filter" class="field-control" aria-label="Filter by status">${statusOptions}</select><span class="toolbar-spacer"></span><button class="button button-primary" data-action="add-candidate">+ Add</button><button class="button button-purple" data-action="update-status">Update Status</button><button class="button button-orange" data-action="schedule-selected">Schedule</button><button class="button button-green" data-action="hire-selected">Hire</button><button class="button button-danger" data-action="delete-candidate">Delete</button><button class="button button-muted" data-action="export-csv">Export CSV</button></div>${panel("Candidate Applications", `${candidateTable(filtered, true)}<p class="selection-note">Select a row to update, schedule, hire, or delete. Double-click a candidate to edit details.</p>`)}`;
}

function renderInterviews() {
  const sorted = [...db.interviews].sort((a, b) => a.date.localeCompare(b.date));
  return `<div class="toolbar"><button class="button button-orange" data-action="new-interview">+ Schedule Interview</button><button class="button button-danger" data-action="delete-interview">Delete selected</button></div>${panel("Scheduled Interviews", interviewTable(sorted))}`;
}

function renderEmployees() {
  return `<div class="toolbar"><button class="button button-danger" data-action="remove-employee">Remove selected employee</button></div>${panel("Employee Records", employeeTable(db.employees))}`;
}

function renderAnalytics() {
  const total = db.candidates.length || 1;
  const count = (...statuses) => db.candidates.filter((candidate) => statuses.includes(candidate.status)).length;
  const departments = new Map();
  db.employees.forEach((employee) => departments.set(employee.dept, (departments.get(employee.dept) || 0) + 1));
  const colors = ["#2563eb", "#16a34a", "#d97706", "#7c3aed", "#dc2626", "#64748b"];
  const departmentBars = [...departments.entries()].sort(([a], [b]) => a.localeCompare(b))
    .map(([label, value], index) => ({ label, value, color: colors[index % colors.length] }));
  const statusBars = STATUSES.map((status) => ({ label: status, value: count(status), color: STATUS_COLORS[status] }));
  return `<div class="cards">${metricCard("SELECTION RATE", `${(count("Selected", "Hired") / total * 100).toFixed(1)}%`, "#7c3aed")}${metricCard("HIRE RATE", `${(count("Hired") / total * 100).toFixed(1)}%`, "#16a34a")}${metricCard("REJECTION RATE", `${(count("Rejected") / total * 100).toFixed(1)}%`, "#dc2626")}${metricCard("IN PIPELINE", count("Applied", "Shortlisted", "Interview"), "#2563eb")}</div><div class="analytics-grid">${panel("Candidates by Status", bars(statusBars))}${panel("Employees by Department", bars(departmentBars))}</div>`;
}

const renderers = {
  Dashboard: renderDashboard,
  Candidates: renderCandidates,
  Interviews: renderInterviews,
  Employees: renderEmployees,
  Analytics: renderAnalytics,
};

function render() {
  const titles = { Dashboard: "HR Dashboard" };
  pageTitle.textContent = titles[currentPage] || currentPage;
  document.querySelectorAll(".nav-link").forEach((button) => {
    const active = button.dataset.page === currentPage;
    button.classList.toggle("active", active);
    button.setAttribute("aria-current", active ? "page" : "false");
  });
  pageContent.innerHTML = renderers[currentPage]();
  notice.hidden = !storageNotice;
  notice.textContent = storageNotice;
  bindPageEvents();
}

function bindPageEvents() {
  document.querySelectorAll("[data-candidate-id]").forEach((row) => {
    row.addEventListener("click", () => {
      selectedCandidateId = Number(row.dataset.candidateId);
      render();
    });
    row.addEventListener("dblclick", () => editCandidate(Number(row.dataset.candidateId)));
  });
  document.querySelectorAll("[data-interview-id]").forEach((row) => {
    row.addEventListener("click", () => {
      selectedInterviewId = Number(row.dataset.interviewId);
      render();
    });
  });
  document.querySelectorAll("[data-employee-id]").forEach((row) => {
    row.addEventListener("click", () => {
      selectedEmployeeId = Number(row.dataset.employeeId);
      render();
    });
  });
  const search = document.querySelector("#candidate-search");
  if (search) search.addEventListener("input", () => {
    const start = search.selectionStart;
    render();
    const updatedSearch = document.querySelector("#candidate-search");
    updatedSearch.focus();
    updatedSearch.setSelectionRange(start, start);
  });
  const filter = document.querySelector("#candidate-filter");
  if (filter) filter.addEventListener("change", render);
  document.querySelectorAll("[data-action]").forEach((button) => button.addEventListener("click", () => {
    handleAction(button.dataset.action);
  }));
}

function openForm(title, fields, initialValues, onSubmit) {
  document.querySelector("#dialog-title").textContent = title;
  dialogFields.innerHTML = fields.map((field) => {
    const value = initialValues[field.name] ?? "";
    const required = field.required ? " required" : "";
    let control;
    if (field.options) {
      control = `<select class="form-control" name="${escapeHTML(field.name)}"${required}>${field.options.map((option) => `<option value="${escapeHTML(option.value)}"${option.value === value ? " selected" : ""}>${escapeHTML(option.label)}</option>`).join("")}</select>`;
    } else {
      control = `<input class="form-control" name="${escapeHTML(field.name)}" type="${field.type || "text"}" value="${escapeHTML(value)}"${field.placeholder ? ` placeholder="${escapeHTML(field.placeholder)}"` : ""}${required}>`;
    }
    return `<label class="form-field">${escapeHTML(field.label)}${control}</label>`;
  }).join("");
  form.onsubmit = (event) => {
    event.preventDefault();
    const values = Object.fromEntries(new FormData(form).entries());
    if (onSubmit(values) !== false) dialog.close();
  };
  dialog.showModal();
  dialog.querySelector("input,select")?.focus();
}

function closeDialog() {
  dialog.close();
}

function getSelectedCandidate() {
  const candidate = db.candidates.find((item) => item.id === selectedCandidateId);
  if (!candidate) showToast("Select a candidate first.", true);
  return candidate;
}

function addCandidate() {
  openForm("Add candidate", [
    { name: "name", label: "Candidate name", required: true },
    { name: "job", label: "Job position", required: true },
    { name: "edu", label: "Education" },
    { name: "exp", label: "Experience" },
  ], {}, (values) => {
    db.candidates.push({ id: nextId(db.candidates), name: values.name.trim(), job: values.job.trim(), edu: values.edu.trim(), exp: values.exp.trim(), status: "Applied" });
    const saved = persist();
    render();
    if (saved) showToast("Candidate added.");
  });
}

function editCandidate(id) {
  const candidate = db.candidates.find((item) => item.id === id);
  if (!candidate) return;
  openForm("Edit candidate", [
    { name: "name", label: "Candidate name", required: true },
    { name: "job", label: "Job position", required: true },
    { name: "edu", label: "Education" },
    { name: "exp", label: "Experience" },
  ], candidate, (values) => {
    Object.assign(candidate, { name: values.name.trim(), job: values.job.trim(), edu: values.edu.trim(), exp: values.exp.trim() });
    const saved = persist();
    render();
    if (saved) showToast("Candidate updated.");
  });
}

function updateCandidateStatus() {
  const candidate = getSelectedCandidate();
  if (!candidate) return;
  const options = STATUSES.filter((status) => status !== "Hired");
  openForm("Update candidate status", [
    { name: "status", label: "Status", options: options.map((status) => ({ value: status, label: status })) },
  ], { status: candidate.status === "Hired" ? "Selected" : candidate.status }, (values) => {
    candidate.status = values.status;
    const saved = persist();
    render();
    if (saved) showToast(`${candidate.name} moved to ${candidate.status}.`);
  });
}

function scheduleInterview(candidate) {
  openForm(`Schedule interview · ${candidate.name}`, [
    { name: "date", label: "Date", type: "date", required: true },
    { name: "time", label: "Time", placeholder: "e.g. 10:00 AM", required: true },
    { name: "mode", label: "Mode", options: ["Online", "Offline"].map((mode) => ({ value: mode, label: mode })) },
  ], { date: new Date().toISOString().slice(0, 10), time: "10:00 AM", mode: "Online" }, (values) => {
    db.interviews.push({ id: nextId(db.interviews), name: candidate.name, job: candidate.job, date: values.date, time: values.time.trim(), mode: values.mode });
    if (["Applied", "Shortlisted"].includes(candidate.status)) candidate.status = "Interview";
    const saved = persist();
    render();
    if (saved) showToast(`Interview scheduled for ${candidate.name}.`);
  });
}

function newInterview() {
  const available = db.candidates.filter((candidate) => candidate.status !== "Rejected");
  if (!available.length) {
    showToast("No candidates are available to schedule.", true);
    return;
  }
  openForm("Choose a candidate", [
    { name: "candidateId", label: "Candidate", options: available.map((candidate) => ({ value: String(candidate.id), label: `${candidate.name} · ${candidate.job}` })) },
  ], {}, (values) => {
    const candidate = available.find((item) => item.id === Number(values.candidateId));
    closeDialog();
    if (candidate) scheduleInterview(candidate);
    return false;
  });
}

function hireCandidate() {
  const candidate = getSelectedCandidate();
  if (!candidate) return;
  if (candidate.status !== "Selected") {
    showToast("Only selected candidates can be hired. Update the status to Selected first.", true);
    return;
  }
  db.employees.push({
    id: nextId(db.employees),
    name: candidate.name,
    job: candidate.job,
    joined: new Date().toISOString().slice(0, 10),
    dept: guessDepartment(candidate.job),
  });
  candidate.status = "Hired";
  const saved = persist();
  render();
  if (saved) showToast(`${candidate.name} hired successfully.`);
}

function exportCSV() {
  const quote = (value) => `"${String(value ?? "").replace(/"/g, '""')}"`;
  const rows = [
    ["ID", "Candidate", "Job Position", "Education", "Experience", "Status"],
    ...db.candidates.map((candidate) => [candidate.id, candidate.name, candidate.job, candidate.edu, candidate.exp, candidate.status]),
  ];
  const csv = `\uFEFF${rows.map((row) => row.map(quote).join(",")).join("\r\n")}`;
  const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = "candidates.csv";
  link.click();
  URL.revokeObjectURL(url);
  showToast("Candidate list exported.");
}

function handleAction(action) {
  if (action === "add-candidate") return addCandidate();
  if (action === "update-status") return updateCandidateStatus();
  if (action === "schedule-selected") {
    const candidate = getSelectedCandidate();
    if (candidate) scheduleInterview(candidate);
    return;
  }
  if (action === "hire-selected") return hireCandidate();
  if (action === "export-csv") return exportCSV();
  if (action === "new-interview") return newInterview();
  if (action === "delete-candidate") {
    const candidate = getSelectedCandidate();
    if (!candidate || !window.confirm(`Delete candidate ${candidate.name}?`)) return;
    db.candidates = db.candidates.filter((item) => item.id !== candidate.id);
    selectedCandidateId = null;
    const saved = persist();
    render();
    if (saved) showToast("Candidate deleted.");
    return;
  }
  if (action === "delete-interview") {
    if (!selectedInterviewId) return showToast("Select an interview first.", true);
    if (!window.confirm("Delete the selected interview?")) return;
    db.interviews = db.interviews.filter((item) => item.id !== selectedInterviewId);
    selectedInterviewId = null;
    const saved = persist();
    render();
    if (saved) showToast("Interview removed.");
    return;
  }
  if (action === "remove-employee") {
    if (!selectedEmployeeId) return showToast("Select an employee first.", true);
    if (!window.confirm("Remove this employee record?")) return;
    db.employees = db.employees.filter((item) => item.id !== selectedEmployeeId);
    selectedEmployeeId = null;
    const saved = persist();
    render();
    if (saved) showToast("Employee removed.");
  }
}

function updateClock() {
  document.querySelector("#clock").textContent = new Intl.DateTimeFormat("en", {
    weekday: "short", day: "2-digit", month: "short", year: "numeric",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  }).format(new Date());
}

document.querySelectorAll(".nav-link").forEach((button) => {
  button.addEventListener("click", () => {
    currentPage = button.dataset.page;
    selectedCandidateId = null;
    selectedInterviewId = null;
    selectedEmployeeId = null;
    render();
  });
});
document.querySelectorAll("[data-close-dialog]").forEach((button) => button.addEventListener("click", closeDialog));
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) closeDialog();
});
updateClock();
window.setInterval(updateClock, 1000);
render();
