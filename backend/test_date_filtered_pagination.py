import json
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from curl_cffi import requests

GEM_BIDLISTS_URL = "https://bidplus.gem.gov.in/bidlists"
GEM_ALL_BIDS_DATA_URL = "https://bidplus.gem.gov.in/all-bids-data"

def test_date_filtered_pagination():
    print("==================================================")
    print("   TESTING DATE-FILTERED PAGINATION & NUMFOUND")
    print("==================================================")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(options=options)
    csrf_key = 'csrf_bd_gem_nk'
    csrf_val = ''
    cookies_dict = {}

    try:
        driver.get(GEM_BIDLISTS_URL)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cname_elem = soup.find('input', {'id': 'cname'})
        if cname_elem and cname_elem.get('value'):
            csrf_key = cname_elem.get('value')
        csrf_match = re.search(r"['\"]" + csrf_key + r"['\"]\s*:\s*['\"]([^'\"]+)['\"]", driver.page_source)
        if csrf_match:
            csrf_val = csrf_match.group(1)
        for c in driver.get_cookies():
            cookies_dict[c['name']] = c['value']
    finally:
        driver.quit()

    s = requests.Session(impersonate="chrome110")
    for k, v in cookies_dict.items():
        s.cookies.set(k, v)
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': GEM_BIDLISTS_URL,
        'X-Requested-With': 'XMLHttpRequest'
    })

    # Test Date Filter 12/08/2026 across multiple pages
    target_date = "12/08/2026"
    print(f"\n--- Testing Date Filter: {target_date} ---")
    seen_bids = set()
    total_raw = 0

    for page in range(1, 10):
        payload_obj = {
            "page": page,
            "param": {
                "search": "",
                "sort": "Bid-Start-Date-Latest",
                "byStartDate": {
                    "from": target_date,
                    "to": target_date
                }
            }
        }

        res = s.post(GEM_ALL_BIDS_DATA_URL, data={'payload': json.dumps(payload_obj), csrf_key: csrf_val})
        res_json = res.json()
        response_inner = res_json.get('response', {}).get('response', {}) or res_json.get('response', {})
        num_found = response_inner.get('numFound', 0)
        docs = response_inner.get('docs', []) or res_json.get('docs', [])

        bids = [d.get('b_bid_number', [''])[0] if isinstance(d.get('b_bid_number'), list) else d.get('bidNumber') for d in docs]
        
        if not bids:
            print(f"PAGE {page}: 0 records returned. Pagination finished.")
            break

        new_in_page = 0
        for b in bids:
            if b and b not in seen_bids:
                seen_bids.add(b)
                new_in_page += 1

        total_raw += len(bids)
        first_bid = bids[0] if bids else "None"
        last_bid = bids[-1] if bids else "None"

        print(f"PAGE {page}: records={len(bids)} new_unique={new_in_page} first={first_bid} last={last_bid} numFound={num_found}")

        if new_in_page == 0:
            print(f"PAGE {page}: 0 new unique records. Stopping pagination.")
            break

    print(f"\nSummary for Date {target_date}:")
    print(f"  Total Raw Records Retrieved: {total_raw}")
    print(f"  Total Unique Bids Collected: {len(seen_bids)}")
    print(f"  Duplicates Across Pages: {total_raw - len(seen_bids)}")

if __name__ == "__main__":
    test_date_filtered_pagination()
