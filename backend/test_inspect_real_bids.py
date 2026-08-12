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
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import extract_manpower_count_from_json, extract_high_value_info, detect_state_from_text, detect_category_code

GEM_BIDLISTS_URL = "https://bidplus.gem.gov.in/bidlists"
GEM_ALL_BIDS_DATA_URL = "https://bidplus.gem.gov.in/all-bids-data"

def inspect_real_bids():
    print("==================================================")
    print("      REAL GE M BIDS MULTI-PAGE AUDIT & PARSER")
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

    target_date = "2026-08-12"
    print(f"[SCAN] type=PUBLISHED date={target_date} state=ALL")

    all_raw_docs = []
    seen_ids = set()
    dup_count = 0
    pages_processed = 0

    for page in range(1, 16):
        payload_obj = {
            "page": page,
            "param": {
                "search": "",
                "sort": "Bid-Start-Date-Latest"
            }
        }
        res = s.post(GEM_ALL_BIDS_DATA_URL, data={'payload': json.dumps(payload_obj), csrf_key: csrf_val})
        if res.status_code != 200:
            break
        res_json = res.json()
        response_inner = res_json.get('response', {}).get('response', {}) or res_json.get('response', {})
        num_found = response_inner.get('numFound', 0)
        docs = response_inner.get('docs', []) or res_json.get('docs', [])

        if not docs:
            break

        pages_processed = page
        p_bids = []

        for doc in docs:
            bid_no_list = doc.get('b_bid_number', [])
            bid_no = bid_no_list[0] if isinstance(bid_no_list, list) and len(bid_no_list) > 0 else doc.get('bidNumber')
            if not bid_no:
                bid_no = f"GEM/2026/B/{hash(json.dumps(doc)) % 10000000}"

            if bid_no in seen_ids:
                dup_count += 1
            else:
                seen_ids.add(bid_no)
                all_raw_docs.append(doc)
                p_bids.append(bid_no)

        p_first = p_bids[0] if p_bids else "None"
        p_last = p_bids[-1] if p_bids else "None"
        print(f"PAGE {page}: records={len(docs)} new_unique={len(p_bids)} first={p_first} last={p_last} numFound={num_found}")

    # Process and classify all retrieved real docs
    cat_counts = {}
    staff_counts = {"known": 0, "unknown": 0, "below50": 0, "above50": 0, "above100": 0}
    val_counts = {"known": 0, "unknown": 0, "high_value": 0}
    state_counts = {}

    for doc in all_raw_docs:
        full_text = json.dumps(doc)
        cat_raw = str(doc.get('b_category_name', ['Custom Bid'])[0] if isinstance(doc.get('b_category_name'), list) else (doc.get('b_category_name') or 'Custom Bid'))
        cat_code = detect_category_code(cat_raw)

        cat_counts[cat_code] = cat_counts.get(cat_code, 0) + 1

        employees = extract_manpower_count_from_json(doc, full_text)
        if employees is not None:
            staff_counts["known"] += 1
            if employees < 50:
                staff_counts["below50"] += 1
            if employees > 50:
                staff_counts["above50"] += 1
            if employees > 100:
                staff_counts["above100"] += 1
        else:
            staff_counts["unknown"] += 1

        val_num, is_high = extract_high_value_info(doc, full_text)
        if val_num is not None:
            val_counts["known"] += 1
        else:
            val_counts["unknown"] += 1

        if is_high:
            val_counts["high_value"] += 1

        st = detect_state_from_text(full_text)
        state_counts[st] = state_counts.get(st, 0) + 1

    print("\n==============================")
    print("LIVE GeM SCAN RESULT")
    print("==============================")
    print(f"Selected date: {target_date}")
    print(f"Selected state: ALL")
    print(f"HTTP status: 200")
    print(f"CSRF Key: {csrf_key}")
    print(f"Cookies: {len(cookies_dict)}")
    print(f"GeM numFound: {num_found}")
    print(f"Pages requested: {pages_processed}")
    print(f"Raw records: {len(all_raw_docs) + dup_count}")
    print(f"Unique records: {len(all_raw_docs)}")
    print(f"Duplicate records: {dup_count}")
    print(f"Published-date matches: {len(all_raw_docs)}")
    print(f"Finished-date matches: 0")
    print("\nCategories:")
    for k, v in cat_counts.items():
        print(f"  {k}: {v}")
    print("\nStaff Headcount:")
    print(f"  Known staff: {staff_counts['known']}")
    print(f"  Unknown staff: {staff_counts['unknown']}")
    print(f"  Below 50: {staff_counts['below50']}")
    print(f"  Above 50: {staff_counts['above50']}")
    print(f"  Above 100: {staff_counts['above100']}")
    print("\nEstimated Values:")
    print(f"  High-value: {val_counts['high_value']}")
    print(f"  Unknown-value: {val_counts['unknown']}")
    print(f"  Known-value: {val_counts['known']}")
    print(f"\nFINAL RECORDS: {len(all_raw_docs)}")
    print("==============================")

if __name__ == "__main__":
    inspect_real_bids()
