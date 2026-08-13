import os
import sys
import json
from datetime import datetime
from curl_cffi import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, unwrap_val, normalize_gem_date

def test_official_payload_with_filter_object():
    target_date = "2026-08-13"
    dt_obj = datetime.strptime(target_date, "%Y-%m-%d")
    gem_date_formatted = dt_obj.strftime("%d/%m/%Y")

    print("==================================================")
    print("COMPARING OFFICIAL GeM PAYLOAD VS CURRENT PYTHON PAYLOAD")
    print("==================================================")

    scraper = GeMLiveScraper()
    driver = scraper._init_driver()
    csrf_key, csrf_val, cookies_dict = scraper.acquire_session_tokens(driver)

    s = requests.Session(impersonate="chrome110")
    for k, v in cookies_dict.items():
        s.cookies.set(k, v)

    s.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Referer': 'https://bidplus.gem.gov.in/bidlists',
        'X-Requested-With': 'XMLHttpRequest'
    })

    # PAYLOAD 1: Official GeM Structure with "filter" object
    payload_official = {
        "page": 1,
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

    post_data_official = {
        'payload': json.dumps(payload_official),
        csrf_key: csrf_val
    }

    print("\n--- OFFICIAL BROWSER REQUEST PAYLOAD ---")
    print(json.dumps(payload_official, indent=2))

    for target_url in ['https://bidplus.gem.gov.in/all-bids-data', 'https://bidplus.gem.gov.in/getbidlists']:
        res_off = s.post(target_url, data=post_data_official, verify=False, timeout=12)
        print(f"\nTarget URL: {target_url} -> Status: {res_off.status_code}")

        if res_off.status_code == 200:
            try:
                j_off = res_off.json()
                resp_inner = j_off.get('response', {}).get('response', {}) or j_off.get('response', {})
                num_found_off = resp_inner.get('numFound', 0)
                docs_off = resp_inner.get('docs', []) or j_off.get('docs', [])

                print("\n--- OFFICIAL PAYLOAD RESULT ---")
                print(f"SOURCE FILTERED numFound: {num_found_off}")
                print(f"DOCS RETURNED IN PAGE 1:  {len(docs_off)}")

                if docs_off:
                    print("\nFIRST 10 RESULT END DATES:")
                    for idx, d in enumerate(docs_off[:10]):
                        end_solr = d.get('final_end_date_sort')
                        if isinstance(end_solr, list) and len(end_solr) > 0:
                            end_solr = end_solr[0]
                        norm_end = normalize_gem_date(end_solr)
                        print(f"  [{idx+1}] bid={d.get('b_bid_number')} raw_end={end_solr} norm_end={norm_end}")
            except Exception as ex:
                print(f"Error parsing response: {ex}")

    driver.quit()

if __name__ == "__main__":
    test_official_payload_with_filter_object()
