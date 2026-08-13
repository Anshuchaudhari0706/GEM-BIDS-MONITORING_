import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, unwrap_val, normalize_gem_date

def test_official_filter_structure_in_scraper():
    print("==================================================")
    print("TESTING OFFICIAL GeM FILTER STRUCTURE IN SCRAPER")
    print("==================================================")

    scraper = GeMLiveScraper()
    driver = scraper._init_driver()
    csrf_key, csrf_val, cookies_dict = scraper.acquire_session_tokens(driver)

    from curl_cffi import requests
    s = requests.Session(impersonate="chrome110")
    for k, v in cookies_dict.items():
        s.cookies.set(k, v)

    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://bidplus.gem.gov.in/bidlists',
        'X-Requested-With': 'XMLHttpRequest'
    })

    # Test 1: Date 2026-08-13 with OFFICIAL filter payload
    target_date = "2026-08-13"
    dt_obj = datetime.strptime(target_date, "%Y-%m-%d")
    gem_date_formatted = dt_obj.strftime("%d/%m/%Y")

    payload_official = {
        "param": {
            "searchBid": "",
            "searchType": "fullText"
        },
        "filter": {
            "bidStatusType": "ended_bids",
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
        'payload': json.dumps(payload_official),
        csrf_key: csrf_val
    }

    print(f"\n--- SENDING OFFICIAL PAYLOAD FOR DATE {target_date} ---")
    print(json.dumps(payload_official, indent=2))

    res = s.post('https://bidplus.gem.gov.in/all-bids-data', data=post_data, verify=False, timeout=12)
    print(f"HTTP Status: {res.status_code}")

    if res.status_code == 200:
        j = res.json()
        resp_inner = j.get('response', {}).get('response', {}) or j.get('response', {})
        num_found = resp_inner.get('numFound', 0)
        docs = resp_inner.get('docs', []) or j.get('docs', [])

        print(f"SOURCE FILTERED numFound: {num_found}")
        print(f"DOCS RETURNED IN PAGE 1:  {len(docs)}")

        if docs:
            print("\nFIRST 10 RESULT END DATES:")
            for idx, d in enumerate(docs[:10]):
                end_solr = unwrap_val(d.get('final_end_date_sort'))
                norm_end = normalize_gem_date(end_solr)
                print(f"  [{idx+1}] bid={d.get('b_bid_number')} raw_end={end_solr} norm_end={norm_end}")

    driver.quit()

if __name__ == "__main__":
    test_official_filter_structure_in_scraper()
