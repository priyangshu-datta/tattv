import re

def extract_emails(content: str) -> list[str]:
    mailtos = re.findall(r"mailto:([\w\.-]+@[\w\.-]+\.\w+)", content, re.I)
    raw_emails = re.findall(r"[\w\.-]+@[\w\.-]+\.\w+", content, re.I)
    all_emails = list(set(mailtos + raw_emails))
    
    return all_emails