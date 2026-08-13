import json
from curl_cffi import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

def test_gem_date_formatting():
    # Target date: July 8, 2025 (2025-07-08)
    # If GeM expects MM/DD/YYYY: "07/08/2025"
    mm_dd_yyyy = "07/08/2025"

    print("==================================================")
    print(f"TESTING MM/DD/YYYY FORMAT ({mm_dd_yyyy}) FOR 2025-07-08")
    print("==================================================")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://bidplus.gem.gov.in/bidlists')

    cookies_dict = {c['name']: c['value'] for c in driver.get_cookies()}
    csrf_key, csrf_val = "csrf_bd_gem_nk", None
    try:
        elem = driver.find_element("xpath", "//input[contains(@name, 'csrf')]")
        csrf_key = elem.get_attribute("name")
        csrf_val = elem.get_attribute("value")
    except:
        pass
    driver.quit()

    s = requests.Session(impersonate="chrome110")
    for k, v in cookies_dict.items():
        s.cookies.set(k, v)
    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://bidplus.gem.gov.in/bidlists',
        'X-Requested-With': 'XMLHttpRequest'
    })

    payload_obj = {
        "page": 1,
        "param": {
            "searchBid": "",
            "searchType": "fullText"
        },
        "filter": {
            "bidStatusType": "ended_bids",
            "byType": "all",
            "highBidValue": "",
            "byEndDate": {
                "from": mm_dd_yyyy,
                "to": mm_dd_yyyy
            },
            "sort": "Bid-End-Date-Oldest"
        }
    }

    res = s.post('https://bidplus.gem.gov.in/all-bids-data', data={'payload': json.dumps(payload_obj), csrf_key: csrf_val}, verify=False, timeout=12)
    print(f"HTTP Status: {res.status_code}")

    if res.status_code == 200:
        j = res.json()
        resp_inner = j.get('response', {}).get('response', {}) or j.get('response', {})
        num_found = resp_inner.get('numFound', 0)
        docs = resp_inner.get('docs', []) or j.get('docs', [])

        print(f"SOURCE numFound: {num_found}")
        print(f"DOCS RETURNED IN PAGE 1: {len(docs)}")

        if docs:
            print("\nFIRST 10 RETURNED RECORDS:")
            for idx, d in enumerate(docs[:10]):
                end_solr = d.get('final_end_date_sort')
                if isinstance(end_solr, list) and len(end_solr) > 0:
                    end_solr = end_solr[0]
                print(f"  [{idx+1}] bid={d.get('b_bid_number')} raw_end={end_solr}")

if __name__ == "__main__":
    test_gem_date_formatting()
