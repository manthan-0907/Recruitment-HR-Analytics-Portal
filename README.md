# Recruitment-HR-Analytics-Portal

Recruitment and HR analytics portal with a Python desktop version and a browser-based version for GitHub Pages.

## GitHub Pages website

The static website is made up of `index.html`, `styles.css`, and `app.js`. A push to `main` deploys it using the GitHub Actions workflow in `.github/workflows/pages.yml`.

To enable deployment, open the repository's **Settings → Pages** and set the build and deployment source to **GitHub Actions**. The first workflow run will publish the site at:

`https://manthan-0907.github.io/Recruitment-HR-Analytics-Portal/`

The browser version includes the dashboard, candidates, interviews, employees, analytics, and candidate CSV export. Its records are saved in the current browser's local storage; they are not shared across browsers or users and are separate from the Python app's `hr_data.json` file.

## Desktop version

Run `hr recuritment_portal.py` with Python and Tkinter installed.
