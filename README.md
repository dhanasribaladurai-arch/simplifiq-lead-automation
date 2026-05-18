# SimplifIQ — Lead Automation Pipeline

An AI-powered system that automates the entire lead intake to report delivery workflow.

## What It Does
1. Prospect submits a form with company details
2. System scrapes and enriches company data
3. Generates a personalised PDF audit report
4. Sends the report to the prospect via email
5. Logs the lead to Google Sheets (bonus)
6. Archives the PDF to Google Drive (bonus)

## Tech Stack
- **Backend:** Python + Flask
- **Data Enrichment:** BeautifulSoup + Hunter.io
- **PDF Generation:** ReportLab
- **Email:** Mailtrap SMTP
- **Bonus:** Google Sheets API + Google Drive API

## Project Structure
LEAD_AUTOMATION/
├── app.py                  # Flask app + pipeline
├── templates/
│   └── index.html          # Lead intake form
├── utils/
│   ├── enrichment.py       # Web scraping + Hunter.io
│   ├── report_generator.py # Report generation
│   ├── pdf_generator.py    # PDF builder
│   ├── email_sender.py     # Email delivery
│   ├── google_sheets.py    # Sheets logging (bonus)
│   └── google_drive.py     # Drive archiving (bonus)
├── requirements.txt
└── .gitignore

## Setup Instructions
1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/simplifiq-lead-automation.git
cd simplifiq-lead-automation
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Create `.env` file
GOOGLE_SHEET_ID=your-sheet-id
GOOGLE_DRIVE_FOLDER_ID=your-folder-id
GOOGLE_SERVICE_ACCOUNT_JSON=credentials/google_service_account.json

4. Run the app
```bash
python app.py
```

5. Open browser
   [http://localhost:5000](http://127.0.0.1:5000)

## Design Decisions
- **Background threading** — form returns instantly, pipeline runs async
- **Graceful fallbacks** — enrichment failures don't stop the pipeline
- **ReportLab** — no headless browser needed for PDF generation
- **Mailtrap** — safe email testing without hitting real inboxes

## Assumptions & Limitations
- Mailtrap used for email (sandbox testing environment)
- Hunter.io optional — pipeline works without it
- Google APIs optional — skipped gracefully if not configured
