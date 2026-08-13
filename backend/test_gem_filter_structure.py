import json
import requests
from curl_cffi import requests as cffi_requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def test_gem_filter_structure():
    target_date = "2026-08-13"
    dt_obj = datetime.strptime(target_date, "%Y-%m-%d")
    gem_date_formatted = dt_obj.strftime("%d/%m/%Y")

    print("==================================================")
    print(f"TESTING OFFICIAL GeM FILTER STRUCTURE (date = {target_date})")
    print("==================================================")

    # Initialize Selenium to get CSRF + cookies
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://bidplus.gem.gov.in/all-bids')

    cookies_dict = {c['name']: c['value'] for c in driver.get_cookies()}

    # Get CSRF
    csrf_key = "csrf_bd_gem_nk"
    csrf_val = None
    try:
        elem = driver.find_element("xpath", "//input[contains(@name, 'csrf')]")
        csrf_key = elem.get_attribute("name")
        csrf_val = elem.get_attribute("value")
    except:
        pass

    driver.quit()

    s = cffi_requests.Session(impersonate="chrome110")
    for k, v in cookies_dict.items():
        s.cookies.set(k, v)

    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://bidplus.gem.gov.in/all-bids',
        'X-Requested-With': 'XMLHttpRequest'
    })

    # Official Payload structure with "filter" object:
    payload_obj = {
        "param": {
            "searchBid": "",
            "searchType": "fullText"
        },
        "filter": {
            "bidStatusType": "all_bids",
            "byType": "all",
            "highBidValue": "",
            "byEndDate": {
                "from": gem_date_formatted,
                "to": gem_date_formatted
            },
            "sort": "Bid-End-Date-Oldest"
        }
    }

    post_data = {
        'payload': json.dumps(payload_obj),
        csrf_key: csrf_val
    }

    print("\n--- OFFICIAL G e M PAYLOAD SENT ---")
    print(json.dumps(payload_obj, indent=2))

    res = s.post('https://bidplus.gem.gov.in/all-bids-data', data=post_data, verify=False, timeout=12)
    print(f"\nHTTP Status: {res.status_code}")

    res_json = res.json()
    resp_inner = res_json.get('response', {}).get('response', {}) or res_json.get('response', {})
    num_found = resp_inner.get('numFound', 0)
    docs = resp_inner.get('docs', []) or res_json.get('docs', [])

    print("\n--- G e M SOURCE RESPONSE ---")
    print(f"SOURCE FILTERED numFound: {num_found}")
    print(f"DOCS RETURNED IN PAGE 1:  {len(docs)}")

    if docs:
        print("\nFIRST 10 RESULT END DATES:")
        for idx, d in enumerate(docs[:10]):
            end_solr = d.get('final_end_date_sort')
            if isinstance(end_solr, list) and len(end_solr) > 0:
                end_solr = end_solr[0]
            print(f"  [{idx+1}] bid={d.get('b_bid_number')} end_date={end_solr}")

if __name__ == "__main__":
    test_gem_filter_structure()
