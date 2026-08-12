import json
import requests
import sys
import os

# Ensure backend/document-reader is in path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))

from gem_scraper import GeMLiveScraper, extract_manpower_count_from_json, extract_high_value_info, detect_state_from_text, detect_category_code

def run_gem_live_test():
    print("==================================================")
    print("      LIVE GE M SCANNER & PARSER DEBUG SUITE")
    print("==================================================")

    scraper = GeMLiveScraper()
    
    print("\n[STEP 1 & 2] Opening GeM Portal & Acquiring CSRF Tokens...")
    try:
        csrf_key, csrf_val, cookies_dict = scraper.acquire_session_tokens()
        print(f"  CSRF Key: {csrf_key}")
        print(f"  CSRF Token Value Length: {len(csrf_val)}")
        print(f"  Acquired Session Cookies Count: {len(cookies_dict)}")
    except Exception as e:
        print(f"  [ERROR] Failed to acquire CSRF tokens: {e}")
        return

    print("\n[STEP 3 & 4] Executing Live Scan API Request to /all-bids-data...")
    res_dict = scraper.fetch_live_bids(date_str="2026-08-12", scan_type="published", state_filter="ALL", max_pages=2)

    print(f"\n[STEP 5 & 6] Response Status: {res_dict.get('status')}")
    print(f"  Scan Error (if any): {res_dict.get('scan_error')}")
    print(f"  Total Valid Records Parsed: {res_dict.get('total')}")

    data = res_dict.get("data", [])

    if not data:
        print("  [NOTICE] 0 records returned. Verifying if scan_error was reported correctly.")
        if res_dict.get("status") == "error":
            print(f"  [SUCCESS] Scan failure accurately reported: {res_dict.get('scan_error')}")
        return

    first_bid = data[0]
    raw_doc = first_bid.get("raw_doc", {})

    print("\n[STEP 8 & 9 & 10] First Bid Details:")
    print(f"  Bid Number: {first_bid.get('id')}")
    print(f"  Title / Category Raw: {first_bid.get('title')}")
    print(f"  Department: {first_bid.get('department')}")
    print(f"  JSON Keys in Raw Document: {list(raw_doc.keys())[:10] if isinstance(raw_doc, dict) else 'String'}")

    full_text = json.dumps(raw_doc)

    print("\n[STEP 11] Testing Manpower Extraction:")
    mp_count = extract_manpower_count_from_json(raw_doc, full_text)
    print(f"  Extracted Employees Headcount: {mp_count} (Type: {type(mp_count).__name__})")

    print("\n[STEP 12] Testing High-Value Extraction:")
    val_num, is_high = extract_high_value_info(raw_doc, full_text)
    print(f"  Extracted Value: {val_num} | Is High Value: {is_high}")

    print("\n[STEP 13] Testing State Detection:")
    state = detect_state_from_text(full_text)
    print(f"  Detected Location/State: {state}")

    print("\n[STEP 14] Testing Category Code Detection:")
    cat = detect_category_code(first_bid.get('title'))
    print(f"  Mapped Category Code: {cat}")

    print("\n==================================================")
    print("      LIVE GE M SCANNER DEBUG TEST PASSED")
    print("==================================================")

if __name__ == "__main__":
    run_gem_live_test()
