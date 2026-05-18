def generate_report(lead: dict, enriched: dict) -> dict:
    company  = lead["company"]
    industry = lead["industry"]
    size     = lead["size"]
    website  = lead["website"]

    page_text        = enriched.get("page_text", "")
    meta_description = enriched.get("meta_description", "")
    page_title       = enriched.get("page_title", "")

    # ── Executive Summary ─────────────────────────────────────
    if meta_description:
        summary = f"{company} is a {industry} company — {meta_description[:200]}. This audit covers their digital presence, industry trends, and key opportunities for growth."
    else:
        summary = f"{company} operates in the {industry} sector with a team of {size}. This personalised audit outlines their current digital standing and actionable recommendations to accelerate growth."

    # ── Website Score ─────────────────────────────────────────
    score = 5
    if page_title:        score += 1
    if meta_description:  score += 1
    if len(page_text) > 500: score += 1
    if "contact" in page_text.lower(): score += 1
    if "about" in page_text.lower():   score += 1
    score = min(score, 10)

    strengths = []
    gaps      = []

    if page_title:
        strengths.append("Clear page title present")
    else:
        gaps.append("Missing page title")

    if meta_description:
        strengths.append("Meta description found — good for SEO")
    else:
        gaps.append("No meta description — hurts SEO ranking")

    if "about" in page_text.lower():
        strengths.append("About section present — builds trust")
    else:
        gaps.append("No About section found")

    if "contact" in page_text.lower():
        strengths.append("Contact information visible")
    else:
        gaps.append("Contact information not easily found")

    if len(page_text) > 1000:
        strengths.append("Good amount of website content")
    else:
        gaps.append("Thin website content — add more pages")

    # Keep max 3 each
    strengths = strengths[:3]
    gaps      = gaps[:3]

    if not strengths:
        strengths = ["Active online presence", "Website is live and accessible", "Business information available"]
    if not gaps:
        gaps = ["SEO optimisation needed", "Content marketing opportunity", "Conversion optimisation"]

    # ── Industry Insights ─────────────────────────────────────
    industry_insights_map = {
        "SaaS / Software": [
            {"trend": "AI-Powered Features", "relevance": f"SaaS companies like {company} are integrating AI to increase retention and reduce churn.", "action": "Identify one manual workflow that AI can automate in your product."},
            {"trend": "Product-Led Growth", "relevance": "Letting the product drive acquisition is becoming the dominant SaaS go-to-market strategy.", "action": "Add a free trial or freemium tier to reduce sales friction."},
            {"trend": "Customer Success Automation", "relevance": f"Automated onboarding sequences help {company} scale without proportional headcount.", "action": "Build an automated onboarding email sequence for new users."},
        ],
        "Finance & Fintech": [
            {"trend": "Open Banking APIs", "relevance": f"{company} can leverage open banking to offer richer, more personalised financial services.", "action": "Evaluate open banking API providers this quarter."},
            {"trend": "AI Fraud Detection", "relevance": "AI-based fraud prevention is becoming table stakes in fintech.", "action": "Audit your current fraud detection capabilities and identify gaps."},
            {"trend": "Embedded Finance", "relevance": f"Embedding financial products into non-financial platforms creates new revenue for companies like {company}.", "action": "Explore partnership opportunities with complementary platforms."},
        ],
        "E-commerce & Retail": [
            {"trend": "Personalisation at Scale", "relevance": f"Customers expect personalised experiences — {company} can use data to deliver them.", "action": "Implement product recommendation engine on your store."},
            {"trend": "Social Commerce", "relevance": "Shopping via Instagram and TikTok is growing 3x faster than traditional e-commerce.", "action": "Set up a shop on Instagram or TikTok this month."},
            {"trend": "Same-Day Delivery Expectations", "relevance": f"Logistics speed is now a competitive differentiator for {company}.", "action": "Review your fulfilment strategy and identify speed improvements."},
        ],
        "Healthcare & MedTech": [
            {"trend": "Telemedicine Growth", "relevance": f"{company} can expand reach by offering remote consultation or digital health services.", "action": "Evaluate telemedicine platform integrations this quarter."},
            {"trend": "AI Diagnostics", "relevance": "AI is improving diagnostic accuracy and reducing costs across healthcare.", "action": "Research AI diagnostic tools relevant to your specialty."},
            {"trend": "Patient Data Security", "relevance": f"Data privacy compliance is critical for {company} to maintain patient trust.", "action": "Conduct a HIPAA/data compliance audit this quarter."},
        ],
        "Consulting & Professional Services": [
            {"trend": "AI-Augmented Consulting", "relevance": f"{company} can deliver faster, deeper insights by using AI research and analysis tools.", "action": "Pilot an AI research tool on your next client engagement."},
            {"trend": "Productised Services", "relevance": "Packaging consulting into fixed-price products increases scalability.", "action": "Create one productised service offering this quarter."},
            {"trend": "Thought Leadership Content", "relevance": f"Publishing insights positions {company} as the go-to expert in your niche.", "action": "Publish one in-depth article or case study per month."},
        ],
    }

    insights = industry_insights_map.get(industry, [
        {"trend": "Digital Transformation", "relevance": f"{company} can gain competitive advantage by automating key business processes.", "action": "Map your top 3 manual processes and prioritise automation."},
        {"trend": "Data-Driven Decisions", "relevance": "Companies using analytics dashboards make faster, better decisions.", "action": "Set up a KPI dashboard tracking your core business metrics."},
        {"trend": "Customer Experience", "relevance": f"Personalised experiences drive loyalty and revenue for businesses like {company}.", "action": "Survey your top 10 customers this month to find friction points."},
    ])

    # ── Opportunity Areas ─────────────────────────────────────
    opportunities = [
        {
            "title": "Process Automation",
            "description": f"Automate repetitive manual workflows at {company} to save time and reduce errors. Focus on lead intake, reporting, and client communication first.",
            "potential_impact": "High",
            "effort": "Medium",
        },
        {
            "title": "SEO & Content Marketing",
            "description": f"Strengthen {company}'s organic search presence with targeted content. Companies in {industry} that publish regularly get 3x more inbound leads.",
            "potential_impact": "High",
            "effort": "Medium",
        },
        {
            "title": "Lead Nurturing Sequences",
            "description": f"Build automated email follow-up sequences to convert prospects into clients without manual effort from the {company} team.",
            "potential_impact": "Medium",
            "effort": "Low",
        },
    ]

    # ── Next Steps ────────────────────────────────────────────
    next_steps = [
        f"Share this report with your leadership team at {company} and align on top priorities.",
        f"Pick ONE opportunity area and assign an owner with a 30-day deadline.",
        "Book a free 30-minute consultation with SimplifIQ to discuss implementation.",
    ]

    return {
        "executive_summary": summary,
        "company_overview": {
            "what_they_do": f"{company} is a {industry} business serving customers via {website}. With a team size of {size}, they are positioned to scale with the right systems in place.",
            "market_position": f"Operating in the {industry} space, {company} competes in a market that is rapidly adopting automation and AI-driven tools.",
            "digital_footprint": f"{'Strong' if score >= 7 else 'Developing'} online presence with a website score of {score}/10. {'Good foundational signals detected.' if score >= 7 else 'Several key improvements identified below.'}",
        },
        "digital_presence_audit": {
            "website_score": f"{score}/10",
            "score_reason": f"Based on page content, SEO signals, and site structure analysis.",
            "strengths": strengths,
            "gaps": gaps,
            "messaging_clarity": f"{'The value proposition is reasonably clear from the homepage.' if score >= 7 else 'The value proposition needs to be stronger and more immediately visible to visitors.'}",
        },
        "industry_insights": insights,
        "opportunity_areas": opportunities,
        "simplifiq_recommendation": f"SimplifIQ can help {company} automate their lead intake, reporting, and client communication workflows — saving 10+ hours per week and enabling the team to focus on growth. Our AI-powered tools are built specifically for {industry} businesses at the {size} stage.",
        "next_steps": next_steps,
    }