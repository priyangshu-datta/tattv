BASE_PROMPT = """From the following webpage text, extract:

- Company Name
- Tagline or Description
- Website (if mentioned)
- Industry or field
- Estimated Employee Count
- Location (Headquarters or City)
- Country (if mentioned)
- Contact Email (if mentioned)
- Social Media Links (LinkedIn, Twitter, etc.)
- Phone Number (if mentioned)
- Address (if mentioned)
- Year Founded (if mentioned)
- Key People (CEO, Founders, etc.)
- Any other relevant information

Respond ONLY in raw JSON like:
{"company_name": "...", "description": "...", "website": "...", ...}

Text:
{{content}}
"""
