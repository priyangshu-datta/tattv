def extract_company_name(page, domain):
        title = page.title()
        if title and '|' in title:
            name = title.split('|')[0].strip()
            if name:
                return name

        # Meta tags
        meta_names = [
            'meta[property="og:site_name"]',
            'meta[name="application-name"]',
            'meta[name="og:site_name"]',
            'meta[name="twitter:site"]'
        ]
        for selector in meta_names:
            try:
                content = page.locator(selector).get_attribute("content")
                if content:
                    return content.strip()
            except:
                continue

        # First h1 is usually the company name
        try:
            h1 = page.locator("h1").first.text_content()
            if h1 and len(h1.strip()) < 50:
                return h1.strip()
        except:
            pass

        # Alt attribute of logo
        try:
            logos = page.locator("img[alt*='logo'], img[title*='logo']")
            for i in range(min(logos.count(), 3)):
                alt = logos.nth(i).get_attribute("alt") or logos.nth(i).get_attribute("title")
                if alt and len(alt.strip()) > 1:
                    return alt.strip()
        except:
            pass

        # Fallback to domain name
        return domain.replace("www.", "").split(".")[0].capitalize()