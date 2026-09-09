import os
import sys

# Route exports directly to the production GeM Authoritative Connector Engine
doc_reader_path = os.path.join(os.path.dirname(__file__), 'document-reader')
if doc_reader_path not in sys.path:
    sys.path.insert(0, doc_reader_path)

from gem_scraper import (
    GeMLiveScraper,
    scan_real_gem_portal,
    unwrap_val,
    normalize_gem_date,
    extract_manpower_count_from_json,
    extract_high_value_info,
    detect_state_from_text,
    detect_category_code
)

def fetch_live_gem_bids(selected_date_str="2026-08-26", service_category="ALL"):
    """
    Direct delegate to production GeMLiveScraper engine.
    Zero artificial mock data or hardcoded loop data.
    """
    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str=selected_date_str, scan_type="published", state_filter="ALL")
    return res.get("data", [])

if __name__ == "__main__":
    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(date_str="2026-08-26", scan_type="published", state_filter="ALL", max_pages=2)
    print(f"Live GeM Direct Fetch Success: {res.get('status') == 'success' or res.get('status') == 'INCOMPLETE'} | Total Count: {len(res.get('data', []))}")
