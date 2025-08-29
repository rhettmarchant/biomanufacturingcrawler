from biomanufacturingtracker.src.extractors.sourceExtract import extract_source
import json

user_prompt = "biomanufacturingtracker/src/ai_prompts/userPrompt.txt"
system_prompt = "biomanufacturingtracker/src/ai_prompts/prompt_getRecords.md"

def bulk_ai_search(links):
    results = []
    for url in links:
        json = extract_source(url, system_prompt, user_prompt)
        results.append(json)
    return results

if __name__ == "__main__":
    links = [
        "https://www.natureworksllc.com/about-natureworks/news/press-releases/2023/2023-10-18-natureworks-announces-next-phase-of-construction-thailand",
        "https://www.linkedin.com/company/henan-jindan-lactic-acid-technology-co-ltd/about/",
        "https://www.lenzing.com/technology-production/biorefinery/",
        "https://www.foodnavigator.com/Article/2005/06/21/Ajinomoto-ramps-up-MSG-production-on-market-growth/"
    ]  # Populate this list with the URLs you want to process
    results = bulk_ai_search(links)
    print(json.dumps(results, indent=2))