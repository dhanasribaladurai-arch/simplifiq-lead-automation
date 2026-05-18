import os
from datetime import datetime

SHEET_ID   = os.getenv("https://docs.google.com/spreadsheets/d/1iO41UsjX5lgWUlclZBHgeITnsvohAP1jGwAJlkof2Nc/edit?gid=0#gid=0", "")
CREDS_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/google_service_account.json")


def log_lead(lead: dict, status: str) -> bool:
    if not SHEET_ID:
        print("[google_sheets] Skipped — GOOGLE_SHEET_ID not set in .env")
        return False
    if not os.path.exists(CREDS_PATH):
        print(f"[google_sheets] Skipped — credentials not found at: {CREDS_PATH}")
        return False
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_file(
            CREDS_PATH,
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        service = build("sheets", "v4", credentials=creds)

        existing = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range="Sheet1!A1:H1"
        ).execute()

        if not existing.get("values"):
            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body={"values": [["Name","Email","Company","Website","Industry","Size","Timestamp","Status"]]},
            ).execute()

        service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A:H",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [[
                lead.get("name",""),
                lead.get("email",""),
                lead.get("company",""),
                lead.get("website",""),
                lead.get("industry",""),
                lead.get("size",""),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                status,
            ]]},
        ).execute()

        print(f"[google_sheets] ✓ Logged: {lead.get('company')} → {status}")
        return True

    except Exception as e:
        print(f"[google_sheets] ✗ Error: {e}")
        return False