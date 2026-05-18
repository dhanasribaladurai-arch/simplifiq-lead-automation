import smtplib
from email.message import EmailMessage
import os

def send_report_email(lead, pdf_path):
    try:
        receiver_email = lead["email"]
        sender_email   = "test@mailtrap.io"

        smtp_host     = "sandbox.smtp.mailtrap.io"
        smtp_port     = 2525
        smtp_username = "1857e6fdea9348"
        smtp_password = "909354a6e5313a"

        msg            = EmailMessage()
        msg["Subject"] = f"Your Business Audit — {lead['company']}"
        msg["From"]    = sender_email
        msg["To"]      = receiver_email

        msg.set_content(
            f"Hi {lead['name']},\n\n"
            f"Please find your personalised audit report for {lead['company']} attached.\n\n"
            f"Thank you.\n\nSimplifIQ Team"
        )

        if not os.path.exists(pdf_path):
            print("PDF not found:", pdf_path)
            return False

        with open(pdf_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(pdf_path)

        msg.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename=file_name
        )

        with smtplib.SMTP(smtp_host, smtp_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.send_message(msg)

        print(f"[email_sender] ✓ Email sent to {receiver_email}")
        return True

    except Exception as e:
        print(f"[email_sender] ✗ Error: {e}")
        return False