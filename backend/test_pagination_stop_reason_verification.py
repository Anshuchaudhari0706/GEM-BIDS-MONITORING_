import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper

def run_stop_reason_verification():
    target_date = "2026-08-13"
    print("==================================================")
    print(f"FINAL PAGINATION STOP-REASON VERIFICATION ({target_date})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=target_date, scan_type="finished", state_filter="ALL", max_pages=10)

    stop_reason = res.get("stop_reason")
    last_page = res.get("lastPage", 0)
    records_on_last_page = res.get("recordsOnLastPage", 0)
    gem_num_found = res.get("gemNumFound", 0)
    total_unique_records = res.get("totalUniqueRecords", 0)
    safety_max_pages = res.get("safetyMaxPages", 50)
    pagination_complete = res.get("paginationComplete", False)

    source_total = res.get("sourceTotal", 0)
    records_retrieved = res.get("recordsRetrieved", 0)
    pages_processed = res.get("pagesProcessed", 0)
    final_matching_records = res.get("total", 0)
    date_matches = res.get("dateMatches", 0)
    date_mismatches = res.get("dateMismatches", 0)

    print("\n--------------------------------------------------")
    print("EXACT STOP METRICS REPORT")
    print("--------------------------------------------------")
    print(f"STOP_REASON:          {stop_reason}")
    print(f"LAST_PAGE:            {last_page}")
    print(f"RECORDS_ON_LAST_PAGE: {records_on_last_page}")
    print(f"GEM_NUM_FOUND:        {gem_num_found}")
    print(f"TOTAL_UNIQUE_RECORDS: {total_unique_records}")
    print(f"SAFETY_MAX_PAGES:     {safety_max_pages}")
    print(f"PAGINATION_COMPLETE:  {pagination_complete}")

    print("\n--------------------------------------------------")
    print("SUMMARY DATASET METRICS")
    print("--------------------------------------------------")
    print(f"source_total / numFound: {source_total}")
    print(f"records_retrieved:       {records_retrieved}")
    print(f"pages_processed:         {pages_processed}")
    print(f"final_matching_records:  {final_matching_records}")
    print(f"date_matches:            {date_matches}")
    print(f"date_mismatches:         {date_mismatches}")

    # Valid stop reasons list
    valid_stop_reasons = [
        "GE M SOURCE RETURNED ZERO RECORDS",
        "ALL GE M numFound RECORDS RETRIEVED",
        "SAFETY_MAX_PAGES_REACHED",
        "NO_NEW_UNIQUE_RECORDS"
    ]

    is_valid_enum = stop_reason in valid_stop_reasons
    print(f"\nSTOP_REASON IN VALID ENUM SET: {'PASS' if is_valid_enum else 'FAIL'}")

    if stop_reason == "SAFETY_MAX_PAGES_REACHED":
        zero_result_verified = False
        print("SCAN WAS LIMITED BY SAFETY_MAX_PAGES_REACHED (INCOMPLETE SCAN)")
    else:
        zero_result_verified = (pagination_complete is True) and (final_matching_records == 0)

    print("\n==================================================")
    print("                 FINAL ACCEPTANCE")
    print("==================================================")
    print(f"ZERO RESULT VERIFIED = {'YES' if zero_result_verified else 'NO'}")
    print("==================================================")

if __name__ == "__main__":
    run_stop_reason_verification()
