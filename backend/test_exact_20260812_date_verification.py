import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, normalize_gem_date, unwrap_val

TARGET_DATE = "2026-08-12"

def test_1_published_all():
    print("==================================================")
    print(f"TEST 1 — PUBLISHED ALL INDIA ({TARGET_DATE})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=TARGET_DATE, scan_type="published", state_filter="ALL", max_pages=10)

    bids = res.get("data", [])
    total_returned = len(bids)
    print(f"\nTotal Records Returned: {total_returned}")
    print(f"GeM Source Total (numFound): {res.get('sourceTotal', 0)}")
    print(f"Pages Processed: {res.get('pagesProcessed', 0)}")
    print(f"Raw Records Retrieved: {res.get('recordsRetrieved', 0)}")

    if total_returned == 0:
        print("\nZERO REAL GE M BIDS FOUND FOR THIS DATE")
        return "ZERO REAL GE M BIDS FOUND FOR THIS DATE", bids

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

    correct_date = 0
    wrong_date = 0
    unknown_date = 0
    replacement_detected = False

    for b in bids:
        pub_date = b.get("publishedDate")
        raw_doc = b.get("raw_doc", {})
        raw_start = unwrap_val(raw_doc.get("final_start_date_sort"))
        norm_start = normalize_gem_date(raw_start)

        if norm_start is None and pub_date == TARGET_DATE:
            replacement_detected = True

        if pub_date == TARGET_DATE:
            correct_date += 1
        elif pub_date is None:
            unknown_date += 1
        else:
            wrong_date += 1

    print("--- METRICS ---")
    print(f"Total returned: {total_returned}")
    print(f"Date = {TARGET_DATE}: {correct_date}")
    print(f"Date != {TARGET_DATE}: {wrong_date}")
    print(f"Unknown date: {unknown_date}")
    print(f"Date replacement detected: {replacement_detected}")

    is_pass = (correct_date == total_returned) and (wrong_date == 0) and (unknown_date == 0) and not replacement_detected
    return "PASS" if is_pass else "FAIL", bids

def test_2_published_gujarat():
    print("\n==================================================")
    print(f"TEST 2 — PUBLISHED GUJARAT ({TARGET_DATE})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=TARGET_DATE, scan_type="published", state_filter="Gujarat", max_pages=10)

    bids = res.get("data", [])
    total_returned = len(bids)
    print(f"\nTotal Records Returned: {total_returned}")

    if total_returned == 0:
        print("\nZERO REAL GE M BIDS FOUND FOR THIS DATE")
        return "ZERO REAL GE M BIDS FOUND FOR THIS DATE"

    correct_date = 0
    wrong_date = 0
    unknown_date = 0
    gujarat_count = 0
    pan_india_count = 0
    other_states_count = 0

    for b in bids:
        pub_date = b.get("publishedDate")
        st = str(b.get("state") or "").lower()

        if pub_date == TARGET_DATE:
            correct_date += 1
        elif pub_date is None:
            unknown_date += 1
        else:
            wrong_date += 1

        if "gujarat" in st:
            gujarat_count += 1
        elif "all india" in st or "pan india" in st or "india" in st:
            pan_india_count += 1
        else:
            other_states_count += 1

    print("--- METRICS ---")
    print(f"Total: {total_returned}")
    print(f"Correct date: {correct_date}")
    print(f"Wrong date: {wrong_date}")
    print(f"Unknown date: {unknown_date}")
    print(f"Gujarat: {gujarat_count}")
    print(f"Pan India: {pan_india_count}")
    print(f"Other states: {other_states_count}")

    is_pass = (correct_date == total_returned) and (wrong_date == 0) and (unknown_date == 0)
    return "PASS" if is_pass else "FAIL"

def test_3_finished_all():
    print("\n==================================================")
    print(f"TEST 3 — FINISHED ALL INDIA ({TARGET_DATE})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=TARGET_DATE, scan_type="finished", state_filter="ALL", max_pages=10)

    bids = res.get("data", [])
    total_returned = len(bids)
    print(f"\nTotal Records Returned: {total_returned}")

    if total_returned == 0:
        print("\nZERO REAL GE M BIDS FOUND FOR THIS DATE")
        return "ZERO REAL GE M BIDS FOUND FOR THIS DATE"

    correct_deadline = 0
    wrong_deadline = 0
    unknown_deadline = 0

    for b in bids:
        deadline = b.get("deadline")

        if deadline == TARGET_DATE:
            correct_deadline += 1
        elif deadline is None:
            unknown_deadline += 1
        else:
            wrong_deadline += 1

    print("--- METRICS ---")
    print(f"Total: {total_returned}")
    print(f"Correct deadline: {correct_deadline}")
    print(f"Wrong deadline: {wrong_deadline}")
    print(f"Unknown deadline: {unknown_deadline}")

    is_pass = (correct_deadline == total_returned) and (wrong_deadline == 0) and (unknown_deadline == 0)
    return "PASS" if is_pass else "FAIL"

def main():
    print("==================================================")
    print(f"      EXACT DATE ({TARGET_DATE}) VERIFICATION SUITE")
    print("==================================================")

    res1, _ = test_1_published_all()
    res2 = test_2_published_gujarat()
    res3 = test_3_finished_all()

    print("\n==================================================")
    print("                FINAL RESULT SUMMARY")
    print("==================================================")
    print(f"PUBLISHED ALL INDIA {TARGET_DATE} = {res1}")
    print(f"PUBLISHED GUJARAT {TARGET_DATE}   = {res2}")
    print(f"FINISHED ALL INDIA {TARGET_DATE}  = {res3}")
    print("==================================================")

if __name__ == "__main__":
    main()
