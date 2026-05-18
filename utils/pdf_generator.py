from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

def generate_pdf(lead, report_data):
    # Extract lead info
    name    = lead["name"]
    company = lead["company"]
    website = lead["website"]
    industry = lead["industry"]
    size    = lead["size"]

    # Get project base folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Create reports folder
    folder = os.path.join(base_dir, "reports")
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Safe filename
    safe_company = company.replace(" ", "_").replace("/", "-")
    file_path = os.path.join(folder, f"{safe_company}_SimplifIQ_Audit.pdf")

    # Page setup
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    def new_page():
        c.showPage()
        c.setFont("Helvetica", 10)

    def draw_text(text, x, y, font="Helvetica", size=11, max_width=400):
        """Draw text with word wrap."""
        c.setFont(font, size)
        words = str(text).split()
        line  = ""
        for word in words:
            test = line + " " + word if line else word
            if c.stringWidth(test, font, size) < max_width:
                line = test
            else:
                c.drawString(x, y, line)
                y -= size + 4
                line = word
        if line:
            c.drawString(x, y, line)
        return y - size - 6

    y = height - 60

    # ── HEADER ───────────────────────────────────────────────
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.rect(0, height - 80, width, 80, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(50, height - 50, "SimplifIQ")
    c.setFont("Helvetica", 11)
    c.drawString(50, height - 68, "Personalised Business Audit Report")

    y = height - 110

    # ── COMPANY TITLE ─────────────────────────────────────────
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, company)
    y -= 20
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.drawString(50, y, f"{industry}  |  {size}  |  {website}")
    y -= 30

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Executive Summary")
    y -= 18
    c.setFillColorRGB(0.2, 0.2, 0.2)
    y = draw_text(report_data.get("executive_summary", ""), 50, y, max_width=500)
    y -= 14

    # ── COMPANY OVERVIEW ──────────────────────────────────────
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Company Overview")
    y -= 18

    overview = report_data.get("company_overview", {})
    for label, key in [
        ("What They Do",      "what_they_do"),
        ("Market Position",   "market_position"),
        ("Digital Footprint", "digital_footprint"),
    ]:
        c.setFillColorRGB(0.06, 0.07, 0.14)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{label}:")
        y -= 14
        c.setFillColorRGB(0.2, 0.2, 0.2)
        y = draw_text(overview.get(key, "N/A"), 60, y, max_width=490)
        y -= 6

    y -= 10

    # ── DIGITAL PRESENCE AUDIT ────────────────────────────────
    if y < 200:
        new_page()
        y = height - 60

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Digital Presence Audit")
    y -= 18

    audit = report_data.get("digital_presence_audit", {})
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.drawString(50, y, f"Website Score: {audit.get('website_score', 'N/A')}  —  {audit.get('score_reason', '')}")
    y -= 18

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Strengths:")
    y -= 14
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.05, 0.45, 0.47)
    for s in audit.get("strengths", []):
        c.drawString(65, y, f"✓  {s}")
        y -= 14
    y -= 4

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Gaps:")
    y -= 14
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(0.79, 0.25, 0.25)
    for g in audit.get("gaps", []):
        c.drawString(65, y, f"⚠  {g}")
        y -= 14
    y -= 4

    c.setFillColorRGB(0.2, 0.2, 0.2)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.drawString(50, y, "Messaging Clarity:")
    y -= 14
    c.setFillColorRGB(0.2, 0.2, 0.2)
    y = draw_text(audit.get("messaging_clarity", ""), 60, y, max_width=490)
    y -= 14

    # ── INDUSTRY INSIGHTS ─────────────────────────────────────
    if y < 200:
        new_page()
        y = height - 60

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Industry Insights")
    y -= 18

    for i, insight in enumerate(report_data.get("industry_insights", []), 1):
        if y < 120:
            new_page()
            y = height - 60
        c.setFillColorRGB(0.06, 0.07, 0.14)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"{i}. {insight.get('trend', '')}")
        y -= 14
        c.setFillColorRGB(0.2, 0.2, 0.2)
        y = draw_text(insight.get("relevance", ""), 65, y, max_width=480)
        c.setFillColorRGB(0.05, 0.45, 0.47)
        y = draw_text(f"→ {insight.get('action', '')}", 65, y, max_width=480)
        y -= 8

    y -= 10

    # ── OPPORTUNITY AREAS ─────────────────────────────────────
    if y < 200:
        new_page()
        y = height - 60

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Opportunity Areas")
    y -= 18

    for opp in report_data.get("opportunity_areas", []):
        if y < 120:
            new_page()
            y = height - 60
        c.setFillColorRGB(0.06, 0.07, 0.14)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"• {opp.get('title', '')}")
        y -= 14
        c.setFillColorRGB(0.2, 0.2, 0.2)
        y = draw_text(opp.get("description", ""), 65, y, max_width=480)
        c.setFont("Helvetica", 9)
        c.drawString(65, y, f"Impact: {opp.get('potential_impact','')}   Effort: {opp.get('effort','')}")
        y -= 18

    y -= 10

    # ── RECOMMENDATION ────────────────────────────────────────
    if y < 150:
        new_page()
        y = height - 60

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "SimplifIQ Recommendation")
    y -= 18
    c.setFillColorRGB(0.2, 0.2, 0.2)
    y = draw_text(report_data.get("simplifiq_recommendation", ""), 50, y, max_width=500)
    y -= 14

    # ── NEXT STEPS ────────────────────────────────────────────
    if y < 150:
        new_page()
        y = height - 60

    c.setFillColorRGB(0.06, 0.07, 0.14)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Next Steps")
    y -= 18

    for i, step in enumerate(report_data.get("next_steps", []), 1):
        c.setFillColorRGB(0.2, 0.2, 0.2)
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"{i}.")
        y = draw_text(step, 70, y, max_width=480)
        y -= 6

    # ── FOOTER ────────────────────────────────────────────────
    c.setFillColorRGB(0.6, 0.6, 0.6)
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, f"SimplifIQ · Confidential · Generated for {company}")
    c.drawString(width - 150, 30, "simplifiq.com")

    c.save()
    return file_path