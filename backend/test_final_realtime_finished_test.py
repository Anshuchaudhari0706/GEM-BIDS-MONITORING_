import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, unwrap_val

def run_finished_realtime_test():
    target_date = "2026-08-13"
    print("==================================================")
    print(f"FINAL REAL-TIME FINISHED-TENDER TEST ({target_date})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=target_date, scan_type="finished", state_filter="ALL", max_pages=10)

    bids = res.get("data", [])
    total = len(bids)

    print(f"Total Raw Records Retrieved: {res.get('recordsRetrieved', 0)}")
    print(f"Date Matches: {res.get('dateMatches', 0)}")
    print(f"Date Mismatches: {res.get('dateMismatches', 0)}")
    print(f"Total Filtered Bids Returned: {total}\n")

    if total == 0:
        print("--------------------------------------------------")
        print("No live tenders are scheduled to close today.")
        print("--------------------------------------------------")
        print("\n--- METRICS REPORT ---")
        print(f"Total Finished Today: 0")
        print(f"Closing Today: 0")
        print(f"Already Ended: 0")
        print(f"Date Mismatches: {res.get('dateMismatches', 0)}")
        print(f"Unknown Closing Time: 0")
        return

    now_dt = datetime.now()
    closing_today_count = 0
    ended_count = 0
    date_mismatches_count = 0
    unknown_time_count = 0

    limit = min(20, total)
    print(f"Showing Details for First {limit} Records:\n")

    for i in range(total):
        b = bids[i]
        doc = b.get("raw_doc", {})
        end_solr = unwrap_val(doc.get("final_end_date_sort"))
        end_solr_str = str(end_solr) if end_solr else ""

        pub_date = b.get("publishedDate")
        deadline_date = b.get("deadline")
        deadline_time = "Unknown"
        deadline_datetime_str = "Unknown"
        deadline_dt = None

        if 'T' in end_solr_str:
            try:
                clean_iso = end_solr_str.replace('Z', '')
                deadline_dt = datetime.fromisoformat(clean_iso)
                deadline_time = deadline_dt.strftime("%I:%M %p")
                deadline_datetime_str = deadline_dt.isoformat()
            except Exception:
                deadline_dt = None

        if not deadline_dt and deadline_date:
            try:
                deadline_dt = datetime.strptime(deadline_date, "%Y-%m-%d")
                deadline_time = "11:59 PM"
                deadline_datetime_str = deadline_dt.isoformat()
            except Exception:
                deadline_dt = None

        if deadline_date != target_date:
            date_mismatches_count += 1

        if deadline_dt:
            if deadline_dt > now_dt:
                status = "CLOSING_TODAY"
                closing_today_count += 1
            else:
                status = "ENDED"
                ended_count += 1
        else:
            status = "ENDED"
            ended_count += 1
            unknown_time_count += 1

        if i < limit:
            print(f"[{i+1}]")
            print(f"Bid ID:           {b.get('id')}")
            print(f"publishedDate:    {pub_date}")
            print(f"deadlineDate:     {deadline_date}")
            print(f"deadlineTime:     {deadline_time}")
            print(f"deadlineDateTime: {deadline_datetime_str}")
            print(f"status:           {status}\n")

    print("==================================================")
    print("                METRICS REPORT")
    print("==================================================")
    print(f"Total Finished Today: {total}")
    print(f"Closing Today:        {closing_today_count}")
    print(f"Already Ended:        {ended_count}")
    print(f"Date Mismatches:      {date_mismatches_count}")
    print(f"Unknown Closing Time: {unknown_time_count}")
    print("==================================================")

    math_verified = (total == closing_today_count + ended_count)
    date_verified = (date_mismatches_count == 0)

    print(f"Total = Closing Today + Ended Verification : {'PASS' if math_verified else 'FAIL'}")
    print(f"All Records Have deadlineDate == {target_date} : {'PASS' if date_verified else 'FAIL'}")

if __name__ == "__main__":
    run_finished_realtime_test()
