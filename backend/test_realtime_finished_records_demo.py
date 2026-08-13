import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'document-reader'))
from gem_scraper import GeMLiveScraper, unwrap_val

def run_finished_realtime_demo():
    target_date = "2025-07-08"
    print("==================================================")
    print(f"REAL-TIME FINISHED TENDER CLASSIFICATION DEMO ({target_date})")
    print("==================================================")

    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=target_date, scan_type="finished", state_filter="ALL", max_pages=10)

    bids = res.get("data", [])
    total = len(bids)

    print(f"Total Filtered Bids Returned: {total}\n")

    now_dt = datetime.now()
    closing_today_count = 0
    ended_count = 0

    limit = min(20, total)
    print(f"Showing Details for First {limit} Records:\n")

    for i in range(limit):
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

        status = b.get("status")

        print(f"[{i+1}]")
        print(f"Bid ID:           {b.get('id')}")
        print(f"publishedDate:    {pub_date}")
        print(f"deadlineDate:     {deadline_date}")
        print(f"deadlineTime:     {deadline_time}")
        print(f"deadlineDateTime: {deadline_datetime_str}")
        print(f"status:           {status}\n")

if __name__ == "__main__":
    run_finished_realtime_demo()
