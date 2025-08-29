- 👋 Hi, I’m @HarrisonChris
- 👀 I am wanting to migrate to .net Core platform from ASP.net 4 VB.
- 🌱 I’m currently learning PHP and MySQL in order to host Wordpress site on our windows server..
- 💞️ I’m looking to collaborate on WAMP Server or the best hosting solution for Wordpress sites on Windows server OS.
- 📫 I can be reached via email at harrisonchri@gmail.com

<!---
HarrisonChris/HarrisonChris is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->

## Accountant Time & Invoicing Desktop App

A cross-platform Python desktop application (PySide6) for accountants to track time, manage clients/projects, and generate/send invoices backed by Microsoft SQL Server.

### Features
- Clients and projects management
- Time tracking (manual entries; timer planned)
- Invoice generation from unbilled time entries
- Print to PDF and email invoices
- Configurable SQL Server and SMTP settings

### Prerequisites
- Python 3.10+
- Microsoft ODBC Driver 18 for SQL Server installed on your OS
- SQL Server instance accessible from your machine

### Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configure
The app stores settings in `~/.accountant_app/config.json`.
You can set up DB/SMTP via the Settings dialog (gear icon) inside the app.

Alternatively, you can set environment variable `DB_URL` to a full SQLAlchemy URL, e.g.:
```
mssql+pyodbc://USERNAME:PASSWORD@SERVER/DATABASE?driver=ODBC+Driver+18+for+SQL+Server&trustservercertificate=yes
```

### Run
```bash
python -m accountant_app
```

### Notes
- On first run, the database schema will be created automatically.
- Printing uses Qt's print framework; PDF export works on all platforms even without a printer.
