# 🐍 Python for DevOps & SRE

## 🌟 Introduction
Python is the Swiss Army knife for SREs. It's used for automation, API interaction, and data processing.

## 🟢 Level 0: Basics for Ops
- Scripts vs Modules.
- Pip and Virtualenvs (`venv`).
- **Standard Library:** `os`, `sys`, `json`, `subprocess`, `datetime`.

## 🟡 Level 1: API & Automation
- **Requests:** Interacting with REST APIs (GitHub, AWS, Jira).
- **Boto3:** The AWS SDK for Python (Creating S3 buckets, starting EC2s).
- **BeautifulSoup/Selenium:** Web scraping and UI testing.

## 🟠 Level 2: SRE Tooling (Mid-Level)
- **FastAPI/Flask:** Creating internal tools and dashboards.
- **PyTest:** Writing tests for your infrastructure scripts.
- **AsyncIO:** Handling concurrent tasks (e.g., checking 1000 server healths).
- **Pandas:** Analyzing CSV logs or cost reports.

## 💻 Example: Simple Health Check
```python
import requests

def check_site(url):
    try:
        r = requests.get(url)
        return r.status_code == 200
    except:
        return False

print(f"Site is Up: {check_site('https://google.com')}")
```
