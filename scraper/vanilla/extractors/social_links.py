def extract_social_links(page):
    social_domains = {
        "linkedin.com": "linkedin",
        "facebook.com": "facebook",
        "twitter.com": "twitter",
        "x.com": "twitter",
        "instagram.com": "instagram",
        "github.com": "github",
        "crunchbase.com": "crunchbase",
        "angel.co": "angellist",
        "wellfound.com": "wellfound"
        # add more
    }

    anchors = page.eval_on_selector_all("a", "els => els.map(e => e.href)")
    results = {}

    for href in anchors:
        for domain, name in social_domains.items():
            if domain in href.lower():
                results[name] = href
                break

    return results
