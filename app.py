import os
import threading
from flask import Flask, render_template, request, jsonify


from utils.enrichment       import enrich_company_data
from utils.report_generator import generate_report
from utils.pdf_generator    import generate_pdf
from utils.email_sender     import send_report_email as send_email


app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    try:
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip()
        company  = request.form.get('company', '').strip()
        website  = request.form.get('website', '').strip()
        industry = request.form.get('industry', '').strip()
        size     = request.form.get('size', '').strip()

        if not all([name, email, company, website, industry, size]):
            return jsonify({"success": False, "message": "All fields are required."}), 400

        if '@' not in email or '.' not in email.split('@')[-1]:
            return jsonify({"success": False, "message": "Invalid email address."}), 400

        if not website.startswith(("http://", "https://")):
            website = "https://" + website

        lead = {
            "name":     name,
            "email":    email,
            "company":  company,
            "website":  website,
            "industry": industry,
            "size":     size,
        }

        thread = threading.Thread(target=run_pipeline, args=(lead,))
        thread.daemon = True
        thread.start()

        return jsonify({
            "success": True,
            "message": f"Thank you {name}! Your audit for {company} will arrive in your inbox shortly."
        })

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


def run_pipeline(lead: dict):
    company = lead['company']
    print(f"\n{'='*55}")
    print(f"[pipeline] Starting: {company}")
    print(f"{'='*55}")
    status = "failed"

    try:
        print("[pipeline] Step 1: Enriching...")
        enriched = enrich_company_data(company, lead['website'])
        print("[pipeline]   ✓ Done")

        print("[pipeline] Step 2: Generating report...")
        report_data = generate_report(lead, enriched)
        print("[pipeline]   ✓ Done")

        print("[pipeline] Step 3: Building PDF...")
        pdf_path = generate_pdf(lead, report_data)
        if not pdf_path:
            raise Exception("PDF generation failed")
        print(f"[pipeline]   ✓ Saved: {pdf_path}")

        print(f"[pipeline] Step 4: Sending email to {lead['email']}...")
        success = send_email(lead, pdf_path)
        if success:
            print("[pipeline]   ✓ Email sent")
            status = "sent"
        else:
            print("[pipeline]   ✗ Email failed")
            status = "failed: email"

        


    except Exception as e:
        status = f"failed: {e}"
        print(f"[pipeline] ✗ Error: {e}")
        try:
            if pdf_path and os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"[pipeline] Cleaned up PDF: {pdf_path}")
        except Exception:
            pass

    print(f"[pipeline] Done — {status}\n")


if __name__ == "__main__":
    app.run(debug=True)