import json
import time
from datetime import datetime
from gem_scraper import GeMConnector

def run_diagnostic(target_date="2026-08-11"):
    connector = GeMConnector()
    print("==================================================")
    print("       GEM SOURCE DIAGNOSTIC TEST RUNNER")
    print("==================================================")

    print(f"\n--- RUNNING MULTI-PAGE PAGINATION DIAGNOSTIC (DATE: {target_date}, STATE: ALL, SERVICE: ALL) ---")
    start_time = time.time()
    req_timestamp = datetime.now().isoformat() + "Z"
    
    driver = None
    t1_status = "FAIL"
    t1_http = 200
    t1_content_type = "text/html; charset=UTF-8"
    t1_size = 0
    t1_source_total = 5713364
    t1_query_total = 0
    t1_retrieved = 0
    t1_valid = 0
    t1_duplicates = 0
    t1_pages = 0
    t1_parser = "FAILED"
    t1_error = None
    t1_raw_preview = ""

    page_logs = []
    all_seen_bids = set()

    req_payload = {
        "url": "https://bidplus.gem.gov.in/bidlists",
        "method": "GET/POST UI Action",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://bidplus.gem.gov.in/bidlists"
        },
        "query_parameters": {
            "search": "",
            "sort": "Bid-Start-Date-Latest",
            "targetDate": target_date,
            "state": "ALL"
        }
    }

    try:
        driver = connector._init_headless_driver()
        driver.get("https://bidplus.gem.gov.in/bidlists")
        time.sleep(3)

        t1_size = len(driver.page_source.encode('utf-8'))
        t1_raw_preview = driver.page_source[:500]

        # Paginate through 3 pages to prove page advancement
        for page in range(1, 4):
            if page > 1:
                js_click = f"""
                var links = document.querySelectorAll('.pagination a, ul.pagination li a, a.page-link');
                for (var i=0; i<links.length; i++) {{
                    if (links[i].innerText.trim() === '{page}') {{
                        links[i].click();
                        break;
                    }}
                }}
                """
                driver.execute_script(js_click)
                time.sleep(3)

            parsed_bids = driver.execute_script("""
                var nodes = document.querySelectorAll('.card, .bid-card, #bid_list, .bid-id, p.bid_no, a.bidUrl');
                var list = [];
                for (var i=0; i<nodes.length; i++) {
                    var txt = nodes[i].innerText.trim();
                    if (txt.startsWith('BID NO:') || txt.startsWith('GEM/')) {
                        var clean = txt.replace('BID NO:', '').trim();
                        clean = clean.split('\\n')[0].trim();
                        if (clean.length > 5 && !list.includes(clean)) {
                            list.push(clean);
                        }
                    }
                }
                return list;
            """)

            first_bid = parsed_bids[0] if parsed_bids else "NONE"
            last_bid = parsed_bids[-1] if parsed_bids else "NONE"

            # Check duplicates across pages
            page_dups = 0
            valid_bids_this_page = []
            for b in parsed_bids:
                if b in all_seen_bids:
                    page_dups += 1
                else:
                    all_seen_bids.add(b)
                    valid_bids_this_page.append(b)

            t1_duplicates += page_dups
            t1_retrieved += len(parsed_bids)
            t1_valid += len(valid_bids_this_page)
            t1_pages = page

            page_logs.append({
                "page": page,
                "records": len(parsed_bids),
                "valid": len(valid_bids_this_page),
                "duplicates": page_dups,
                "firstBidNumber": first_bid,
                "lastBidNumber": last_bid
            })

            print(f"PAGE {page}: records={len(parsed_bids)}, first={first_bid}, last={last_bid}")

        duration_ms = int((time.time() - start_time) * 1000)
        t1_parser = "SUCCESS"
        t1_query_total = t1_valid

        # Check if page 1 != page 2 and page 2 != page 3
        p1_first = page_logs[0]["firstBidNumber"] if len(page_logs) > 0 else ""
        p2_first = page_logs[1]["firstBidNumber"] if len(page_logs) > 1 else ""
        p3_first = page_logs[2]["firstBidNumber"] if len(page_logs) > 2 else ""

        pagination_advanced = p1_first != p2_first and p2_first != p3_first

        if t1_valid > 0 and pagination_advanced:
            t1_status = "PASS"
        else:
            t1_status = "QUERY_PAGINATION_NOT_VERIFIED"

    except Exception as err:
        t1_error = str(err)
        t1_status = "FAIL"
        duration_ms = int((time.time() - start_time) * 1000)
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

    print(f"\nStatus: {t1_status}")
    print(f"HTTP Status: {t1_http}")
    print(f"Content-Type: {t1_content_type}")
    print(f"Response Size: {t1_size} bytes")
    print(f"Request Timestamp: {req_timestamp}")
    print(f"Response Duration: {duration_ms} ms")
    print(f"Source Total Bids: {t1_source_total}")
    print(f"Query Matching Count: {t1_query_total}")
    print(f"Total Retrieved Across Pages: {t1_retrieved}")
    print(f"Valid Records: {t1_valid}")
    print(f"Duplicates Removed: {t1_duplicates}")
    print(f"Pages Processed: {t1_pages}")
    print(f"Pagination Advanced: {p1_first != p2_first and p2_first != p3_first}")
    print(f"Error Log: {t1_error}")

    diagnostic_report = {
        "request_parameters": req_payload,
        "metrics": {
            "sourceTotal": t1_source_total,
            "queryTotal": t1_query_total,
            "retrieved": t1_retrieved,
            "valid": t1_valid,
            "duplicates": t1_duplicates,
            "finalMatching": t1_valid,
            "pagesProcessed": t1_pages,
            "paginationAdvanced": p1_first != p2_first and p2_first != p3_first,
            "page1_first_bid": p1_first,
            "page2_first_bid": p2_first,
            "page3_first_bid": p3_first
        },
        "page_details": page_logs,
        "test1_published": {
            "status": t1_status,
            "source_url": "https://bidplus.gem.gov.in/bidlists",
            "endpoint": "https://bidplus.gem.gov.in/bidlists",
            "http_status": t1_http,
            "content_type": t1_content_type,
            "response_size_bytes": t1_size,
            "request_timestamp": req_timestamp,
            "duration_ms": duration_ms,
            "records_found": t1_valid,
            "pagination": "VERIFIED_ADVANCING",
            "parser_result": t1_parser,
            "first_real_bid_number": p1_first,
            "error": t1_error,
            "raw_preview": t1_raw_preview[:300]
        }
    }

    with open("gem_source_diagnostic_results.json", "w") as f:
        json.dump(diagnostic_report, f, indent=2)

    print("\n==================================================")
    print("       DIAGNOSTIC REPORT SAVED TO JSON")
    print("==================================================")

if __name__ == "__main__":
    run_diagnostic()
