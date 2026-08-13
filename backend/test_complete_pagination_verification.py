import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper

def run_complete_pagination_verification():
    print("==================================================")
    print("FINAL COMPLETE PAGINATION & STOP-REASON VERIFICATION")
    print("==================================================")

    scraper = GeMLiveScraper()

    # --------------------------------------------------
    # TEST 1: KNOWN POSITIVE DATE (2025-07-08)
    # --------------------------------------------------
    print("\n--------------------------------------------------")
    print("TEST 1: FINISHED POSITIVE DATE (2025-07-08)")
    print("--------------------------------------------------")

    # Pass max_pages=15 to test multi-page dynamic pagination logs and filtering
    res1 = scraper.fetch_live_bids(date_str="2025-07-08", scan_type="finished", state_filter="ALL", max_pages=15)

    source_total_1 = res1.get("sourceTotal", 0)
    pages_processed_1 = res1.get("pagesProcessed", 0)
    raw_records_1 = res1.get("recordsRetrieved", 0)
    unique_records_1 = res1.get("totalUniqueRecords", 0)
    dup_removed_1 = res1.get("duplicatesRemoved", 0)
    date_matches_1 = res1.get("dateMatches", 0)
    date_mismatches_1 = res1.get("dateMismatches", 0)
    final_records_1 = res1.get("total", 0)
    pag_complete_1 = res1.get("paginationComplete")
    stop_reason_1 = res1.get("stop_reason")

    print("\n--- TEST 1 REPORT ---")
    print(f"sourceTotal:        {source_total_1}")
    print(f"pagesProcessed:     {pages_processed_1}")
    print(f"rawRecords:         {raw_records_1}")
    print(f"uniqueRecords:      {unique_records_1}")
    print(f"duplicatesRemoved:  {dup_removed_1}")
    print(f"dateMatches:        {date_matches_1}")
    print(f"dateMismatches:     {date_mismatches_1}")
    print(f"finalRecords:       {final_records_1}")
    print(f"paginationComplete: {pag_complete_1}")
    print(f"stopReason:         {stop_reason_1}")

    bids_1 = res1.get("data", [])
    cond1_1 = (source_total_1 > 0 and source_total_1 < 5000000)
    cond1_2 = (date_mismatches_1 == 0)
    cond1_3 = all(b.get("deadline") == "2025-07-08" for b in bids_1)

    t1_pass = cond1_1 and cond1_2 and cond1_3

    # --------------------------------------------------
    # TEST 2: TODAY (2026-08-13) REAL-TIME COMPLETE PAGINATION
    # --------------------------------------------------
    print("\n--------------------------------------------------")
    print("TEST 2: FINISHED TODAY REAL-TIME TEST (2026-08-13)")
    print("--------------------------------------------------")

    res2 = scraper.fetch_live_bids(date_str="2026-08-13", scan_type="finished", state_filter="ALL", max_pages=None)

    source_total_2 = res2.get("sourceTotal", 0)
    pages_processed_2 = res2.get("pagesProcessed", 0)
    raw_records_2 = res2.get("recordsRetrieved", 0)
    unique_records_2 = res2.get("totalUniqueRecords", 0)
    dup_removed_2 = res2.get("duplicatesRemoved", 0)
    date_matches_2 = res2.get("dateMatches", 0)
    date_mismatches_2 = res2.get("dateMismatches", 0)
    final_records_2 = res2.get("total", 0)
    pag_complete_2 = res2.get("paginationComplete")
    stop_reason_2 = res2.get("stop_reason")

    print("\n--- TEST 2 REPORT ---")
    print(f"sourceTotal:        {source_total_2}")
    print(f"pagesProcessed:     {pages_processed_2}")
    print(f"rawRecords:         {raw_records_2}")
    print(f"uniqueRecords:      {unique_records_2}")
    print(f"duplicatesRemoved:  {dup_removed_2}")
    print(f"dateMatches:        {date_matches_2}")
    print(f"dateMismatches:     {date_mismatches_2}")
    print(f"finalRecords:       {final_records_2}")
    print(f"paginationComplete: {pag_complete_2}")
    print(f"stopReason:         {stop_reason_2}")

    t2_pass = (pag_complete_2 is True) and (unique_records_2 + dup_removed_2 == source_total_2) and (date_mismatches_2 == 0) and (stop_reason_2 in ["ALL_GE_M_NUMFOUND_RECORDS_RETRIEVED", "GE M SOURCE RETURNED ZERO RECORDS"])

    # --------------------------------------------------
    # TEST 3: ZERO DATE CASE (2030-01-01)
    # --------------------------------------------------
    print("\n--------------------------------------------------")
    print("TEST 3: FINISHED ZERO DATE CASE (2030-01-01)")
    print("--------------------------------------------------")

    res3 = scraper.fetch_live_bids(date_str="2030-01-01", scan_type="finished", state_filter="ALL", max_pages=None)

    source_total_3 = res3.get("sourceTotal", 0)
    pages_processed_3 = res3.get("pagesProcessed", 0)
    final_records_3 = res3.get("total", 0)
    pag_complete_3 = res3.get("paginationComplete")
    stop_reason_3 = res3.get("stop_reason")

    print("\n--- TEST 3 REPORT ---")
    print(f"sourceTotal:        {source_total_3}")
    print(f"pagesProcessed:     {pages_processed_3}")
    print(f"finalRecords:       {final_records_3}")
    print(f"paginationComplete: {pag_complete_3}")
    print(f"stopReason:         {stop_reason_3}")

    t3_pass = (pag_complete_3 is True) and (final_records_3 == 0) and (stop_reason_3 == "GE M SOURCE RETURNED ZERO RECORDS")

    print("\n==================================================")
    print("                 FINAL ACCEPTANCE")
    print("==================================================")
    print(f"SOURCE DATE FILTER             = {'PASS' if cond1_1 else 'FAIL'}")
    print(f"FILTERED NUMFOUND              = {'PASS (' + str(source_total_1) + ')' if cond1_1 else 'FAIL'}")
    print(f"FULL PAGINATION (TODAY)        = {'PASS (' + str(pages_processed_2) + ' pages)' if t2_pass else 'FAIL'}")
    print(f"ALL FILTERED RECORDS RETRIEVED = {'PASS (' + str(unique_records_2) + '/' + str(source_total_2) + ')' if t2_pass else 'FAIL'}")
    print(f"DATE VALIDATION                = {'PASS' if cond1_2 and cond1_3 and date_mismatches_2 == 0 else 'FAIL'}")
    print(f"ZERO-DATE CASE (2030-01-01)    = {'PASS' if t3_pass else 'FAIL'}")
    print("--------------------------------------------------")
    print(f"OVERALL FINAL ACCEPTANCE       = {'PASS' if t1_pass and t2_pass and t3_pass else 'FAIL'}")
    print("==================================================")

if __name__ == "__main__":
    run_complete_pagination_verification()
