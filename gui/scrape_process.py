import json
import re

from utils.dict_tools import filter_unknown_fields


def find_linkedin_url(data):
    searlized = json.dumps(data)
    match = re.search(r"https?://(:?www\.)?linkedin\.com/company/[^\"' ]+", searlized, re.I)
    return match.group(0) if match else None

def scrape_url_with_logs(url, log_queue, result_queue, llm_client_name=None, llm_model_name=None, force_llm = False):
    from scraper.vanilla.website import WebsiteScraper as VanillaWebsiteScraper
    from scraper.llm.website import WebsiteScraper as LLMWebsiteScraper
    from scraper.llm.linkedin import LinkedInScraper

    if llm_client_name == "OpenAI":
        from llm_clients.openai_client import OpenAIClient
        llm_client = OpenAIClient(model_name=llm_model_name)
    elif llm_client_name == "Transformers":
        from llm_clients.custom_client import CustomClient
        llm_client = CustomClient(model_name=llm_model_name)
    elif llm_client_name == "Groq":
        from llm_clients.groq_client import GroqAIClient
        llm_client = GroqAIClient(model_name=llm_model_name)
    
    try:
        log_queue.put(f"Visiting {url}...")
        if force_llm and llm_client_name and llm_model_name:
            scraper = LLMWebsiteScraper(url, llm_client, log_queue)
        else:
            if force_llm:
                log_queue.put("LLM client not provided, using vanilla. Configure LLMs in the settings.")
            scraper = VanillaWebsiteScraper(url, log_queue)
        scraper.scrape()
        log_queue.put(f"Visit completed {url}")
        
        results = scraper.results
        results["URL"] = url

        try:
            linkedin_url = find_linkedin_url(results)
        
            if linkedin_url and llm_client_name and llm_model_name:
                log_queue.put(f"Scraping LinkedIn profile: {linkedin_url}")

                linkedin_scraper = LinkedInScraper(linkedin_url, llm_client, log_queue)
                linkedin_results = linkedin_scraper.scrape()

                results.update(linkedin_results)
        except Exception as e:
            log_queue.put(f"Error scraping LinkedIn profile: {e}")
                
        result_queue.put(filter_unknown_fields(results))
        log_queue.put(f"Finished scraping {url}.")
    except Exception as e:
        log_queue.put(f"Error scraping {url}: {e}")
