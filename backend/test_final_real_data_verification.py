import os
import sys
import json
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, normalize_gem_date, unwrap_val

def run_test_case(test_name, target_date, scan_type, state_filter, max_pages=3):
    print(f"\n==================================================")
    print(f"  RUNNING TEST: {test_name}")
    print(f"  Type={scan_type} Date={target_date} State={state_filter}")
    print(f"==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=target_date, scan_type=scan_type, state_filter=state_filter, max_pages=max_pages)

    bids = res.get("data", [])
    total_returned = len(bids)
    print(f"Total Records Returned: {total_returned}")
    print(f"Records Retrieved: {res.get('recordsRetrieved', 0)}")
    print(f"Date Matches: {res.get('dateMatches', 0)}")
    print(f"Date Mismatches: {res.get('dateMismatches', 0)}")

    # Print first 20 records
    print("\n--- FIRST 20 RETURNED RECORDS ---")
    limit = min(20, total_returned)
    for i in range(limit):
        b = bids[i]
        print(f"[{i+1}]")
        print(f"Bid ID: {b.get('id')}")
        print(f"publishedDate: {b.get('publishedDate')}")
        print(f"deadline: {b.get('deadline')}")
        print(f"state: {b.get('state')}")
        print(f"category: {b.get('category')}")
        print(f"employees: {b.get('employees')}")
        print(f"value: {b.get('value')}")
        print(f"isHighValue: {b.get('isHighValue')}\n")

    date_matches = 0
    date_mismatches = 0
    unknown_dates = 0
    date_replacement_detected = False

    for b in bids:
        raw_doc = b.get("raw_doc", {})
        raw_start = unwrap_val(raw_doc.get("final_start_date_sort"))
        raw_end = unwrap_val(raw_doc.get("final_end_date_sort"))

        norm_raw_start = normalize_gem_date(raw_start)
        norm_raw_end = normalize_gem_date(raw_end)

        if scan_type.upper() == "PUBLISHED":
            target_field_norm = norm_raw_start
            actual_date = b.get("publishedDate")
        else:
            target_field_norm = norm_raw_end
            actual_date = b.get("deadline")

        # Verify no replacement occurred if raw date was missing/invalid
        if target_field_norm is None and actual_date == target_date:
            date_replacement_detected = True

        if actual_date == target_date:
            date_matches += 1
        elif actual_date is None:
            unknown_dates += 1
        else:
            date_mismatches += 1

    print("--- METRICS ---")
    print(f"Total returned: {total_returned}")
    print(f"Date = {target_date}: {date_matches}")
    print(f"Date != {target_date}: {date_mismatches}")
    print(f"Unknown date: {unknown_dates}")
    print(f"Date Replacement Detected: {date_replacement_detected}")

    is_pass = (date_matches == total_returned) and (date_mismatches == 0) and not date_replacement_detected
    print(f"TEST RESULT: {'PASS' if is_pass else 'FAIL'}")
    return is_pass

def main():
    print("==================================================")
    print("      FINAL REAL-DATA VERIFICATION TEST SUITE")
    print("==================================================")

    # Test 1: PUBLISHED ALL INDIA (Real date 2025-06-17)
    pass1 = run_test_case("PUBLISHED ALL INDIA (Real GeM Date 2025-06-17)", "2025-06-17", "PUBLISHED", "ALL", max_pages=3)

    # Test 2: PUBLISHED GUJARAT (Real date 2025-06-17)
    pass2 = run_test_case("PUBLISHED GUJARAT (Real GeM Date 2025-06-17)", "2025-06-17", "PUBLISHED", "Gujarat", max_pages=3)

    # Test 3: FINISHED ALL INDIA (Real date 2025-07-08)
    pass3 = run_test_case("FINISHED ALL INDIA (Real GeM Date 2025-07-08)", "2025-07-08", "FINISHED", "ALL", max_pages=3)

    all_passed = pass1 and pass2 and pass3

    print("\n==================================================")
    print("            FINAL VERIFICATION SUMMARY")
    print("==================================================")
    print(f"LIVE DATE VALIDATION = {'PASS' if all_passed else 'FAIL'}")
    print(f"PUBLISHED ALL INDIA = {'PASS' if pass1 else 'FAIL'}")
    print(f"PUBLISHED GUJARAT  = {'PASS' if pass2 else 'FAIL'}")
    print(f"FINISHED ALL INDIA  = {'PASS' if pass3 else 'FAIL'}")
    print("==================================================")

if __name__ == "__main__":
    main()
