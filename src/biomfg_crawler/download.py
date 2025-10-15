import requests
import time
import biomfg_extractor as bme

# Input: url (str), whitelist (set), blacklist (set), post_sleep (int), whitelist_sleep (int), force (bool)
# Output: dict with keys 'link', 'status', and 'content'
def download(url, whitelist, blacklist, post_sleep=10, whitelist_sleep=30, force=False):
    try:
        parent_domain = url.split("/")[2]
        if parent_domain in blacklist and force == False:
            print(f"Parent domain blacklisted: {url}")
            return {"link": url, "status": "blacklist", "content": None}
        if parent_domain in whitelist:
            time.sleep(whitelist_sleep)
        response = requests.get(url)
        status = response.status_code
        if status == 200:
            whitelist.add(parent_domain)
            time.sleep(post_sleep)
            return {"link": url, "status": status, "content": response.text}
        else:
            blacklist.add(parent_domain)
            print(f"Failed to download file: {url}: {status}")
            time.sleep(post_sleep)
            return {"link": url, "status": status, "content": response.text}
    except Exception as e:
        blacklist.add(parent_domain)
        print(f"Error downloading file: {url}: {e}")
        time.sleep(post_sleep)
        return {"link": url, "status": "error", "content": "None"}

# Input: a JSON object with 'link', 'status', and 'content' keys
# Output: the same JSON object with added 'ai_response' and 'llm_trim' keys
def submit_to_ai(result, user_prompt, system_prompt, patterns, language, post_sleep=60):
    if result['status'] == 200 and result['content'] != "None":
        if result['link'].endswith(".pdf") or result['content'].strip().startswith("%PDF"):
            print(f"Skipping PDF content from {result['link']}")
        else:
            try:
                llm_trim = bme.html_to_llm(
                    result['content'], patterns, language)
                ai_response = bme.extract_source(
                    url=result['link'], user_prompt=user_prompt, system_prompt=system_prompt, source_data=llm_trim)
                result['llm_trim'] = llm_trim
                result['ai_response'] = bme.biomfg_to_json(ai_response)
                time.sleep(post_sleep)
            except Exception as e:
                result['ai_response'] = "NA"
                result['llm_trim'] = "NA"
                print(
                    f"Error extracting or summarizing content from {result['link']}: {e}")
                time.sleep(post_sleep)
    else:
        result['ai_response'] = None
        result['llm_trim'] = None