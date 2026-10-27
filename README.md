# Recruitment & HR Analytics Portal

A recruitment management portal for tracking candidates, scheduling interviews, managing employee records, and reviewing hiring analytics. The project includes a Python desktop application and a browser-based version published with GitHub Pages.

## Features

- **Dashboard:** Candidate, interview, employee, and selected/hired totals, plus a hiring pipeline and upcoming interviews.
- **Candidate management:** Add, edit, search, and filter candidates; update application statuses; schedule interviews; and export candidate records to CSV.
- **Interview management:** Schedule interviews for candidates and remove scheduled interviews.
- **Employee management:** Review employee records and remove records when needed.
- **Analytics:** Review selection, hire, and rejection rates, candidates by status, and employees by department.

## Browser app

Open the [Recruitment & HR Analytics Portal](https://manthan-0907.github.io/Recruitment-HR-Analytics-Portal/). The web app is built with HTML, CSS, and JavaScript and runs without a server-side database.

Browser records are saved in that browser's local storage. They are private to the browser and are not shared with other users or synchronized with the desktop app.

## Desktop app

Run `hr recuritment_portal.py` with Python and Tkinter installed. The desktop app saves its records to `hr_data.json` beside the script.

## Deployment

The static website is deployed to GitHub Pages by `.github/workflows/pages.yml` whenever changes are pushed to `main`. In the repository settings, configure **Settings → Pages → Build and deployment → Source** to **GitHub Actions**.

The website consists of `index.html`, `styles.css`, and `app.js`.
