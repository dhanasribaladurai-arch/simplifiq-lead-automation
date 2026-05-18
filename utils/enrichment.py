def enrich_company_data(company, website):
    return {
        "company_name": company,
        "website": website,
        "industry": "Software Development",
        "summary": f"{company} is a growing company focused on innovation and digital transformation.",
        "recommendation": "Improving digital presence and automating lead generation can help business growth."
    }