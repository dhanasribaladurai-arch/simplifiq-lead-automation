import os

FOLDER_ID  = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
CREDS_PATH = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "credentials/google_service_account.json")


def upload_pdf(pdf_path: str, company_name: str) -> str | None:
    if not FOLDER_ID:
        print("[google_drive] Skipped — GOOGLE_DRIVE_FOLDER_ID not set in .env")
        return None
    if not os.path.exists(CREDS_PATH):
        print(f"[google_drive] Skipped — credentials not found at: {CREDS_PATH}")
        return None
    if not os.path.exists(pdf_path):
        print(f"[google_drive] Skipped — PDF not found at: {pdf_path}")
        return None
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = service_account.Credentials.from_service_account_file(
            CREDS_PATH,
            scopes=["https://www.googleapis.com/auth/drive.file"],
        )
        service = build("drive", "v3", credentials=creds)

        safe     = company_name.replace(" ", "_").replace("/", "-")
        filename = f"{safe}_SimplifIQ_Audit.pdf"

        file = service.files().create(
            body={"name": filename, "parents": [FOLDER_ID]},
            media_body=MediaFileUpload(pdf_path, mimetype="application/pdf"),
            fields="id,webViewLink"
        ).execute()

        link = file.get("webViewLink", "")
        print(f"[google_drive] ✓ Uploaded → {link}")
        return link

    except Exception as e:
        print(f"[google_drive] ✗ Error: {e}")
        return None