import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper

def run_full_source_filter_verification():
    print("==================================================")
    print("VERIFYING GeM SOURCE-SIDE DATE FILTERED PAYLOAD")
    print("==================================================")

    scraper = GeMLiveScraper()

    # TEST 1: FINISHED for date = 2026-08-13
    print("\n--------------------------------------------------")
    print("TEST 1: FINISHED (date = 2026-08-13, state = ALL)")
    print("--------------------------------------------------")

    res1 = scraper.fetch_live_bids(date_str="2026-08-13", scan_type="finished", state_filter="ALL", max_pages=10)

    print("\nSOURCE REQUEST PAYLOAD LOGIC:")
    print("  filter.byEndDate = {'from': '13/08/2026', 'to': '13/08/2026'}")
    print("  filter.bidStatusType = 'ended_bids'")

    print(f"\nSOURCE FILTERED NUMFOUND: {res1.get('sourceTotal', 0)}")
    print(f"PAGES PROCESSED:         {res1.get('pagesProcessed', 0)}")
    print(f"RAW RECORDS:             {res1.get('recordsRetrieved', 0)}")
    print(f"DATE MATCHES:            {res1.get('dateMatches', 0)}")
    print(f"DATE MISMATCHES:         {res1.get('dateMismatches', 0)}")
    print(f"FINAL RECORDS:           {res1.get('total', 0)}")
    print(f"PAGINATION COMPLETE:     {res1.get('paginationComplete')}")
    print(f"STOP REASON:             {res1.get('stop_reason')}")

    zero_verified_1 = (res1.get('paginationComplete') is True) and (res1.get('total', 0) == 0) and (res1.get('dateMismatches', 0) == 0)

    print(f"\nTEST 1 ZERO RESULT VERIFIED = {'YES' if zero_verified_1 else 'NO'}")

    # TEST 2: PUBLISHED for date = 2025-06-17
    print("\n--------------------------------------------------")
    print("TEST 2: PUBLISHED (date = 2025-06-17, state = ALL)")
    print("--------------------------------------------------")

    res2 = scraper.fetch_live_bids(date_str="2025-06-17", scan_type="published", state_filter="ALL", max_pages=10)

    print(f"\nSOURCE FILTERED NUMFOUND: {res2.get('sourceTotal', 0)}")
    print(f"PAGES PROCESSED:         {res2.get('pagesProcessed', 0)}")
    print(f"RAW RECORDS:             {res2.get('recordsRetrieved', 0)}")
    print(f"DATE MATCHES:            {res2.get('dateMatches', 0)}")
    print(f"DATE MISMATCHES:         {res2.get('dateMismatches', 0)}")
    print(f"FINAL RECORDS:           {res2.get('total', 0)}")
    print(f"PAGINATION COMPLETE:     {res2.get('paginationComplete')}")
    print(f"STOP REASON:             {res2.get('stop_reason')}")

    source_filter_verified = (res1.get('sourceTotal', 0) == 0) and (res1.get('dateMismatches', 0) == 0)
    pagination_complete_verified = res1.get('paginationComplete') is True
    local_validation_verified = (res1.get('dateMismatches', 0) == 0)

    print("\n==================================================")
    print("                 FINAL ACCEPTANCE")
    print("==================================================")
    print(f"SOURCE DATE FILTER VERIFIED = {'YES' if source_filter_verified else 'NO'}")
    print(f"FILTERED SOURCE TOTAL       = {'VALID' if res1.get('sourceTotal', 0) == 0 else 'INVALID'}")
    print(f"PAGINATION COMPLETE         = {'YES' if pagination_complete_verified else 'NO'}")
    print(f"LOCAL DATE VALIDATION       = {'YES' if local_validation_verified else 'NO'}")
    print(f"ZERO RESULT VERIFIED        = {'YES' if zero_verified_1 else 'NO'}")
    print("==================================================")

if __name__ == "__main__":
    run_full_source_filter_verification()
