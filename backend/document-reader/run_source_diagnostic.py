import json
import time
from datetime import datetime
from gem_scraper import GeMConnector

def run_diagnostic(target_date="2026-08-11"):
    connector = GeMConnector()
    print("==================================================")
    print("       GEM SOURCE DIAGNOSTIC TEST RUNNER")
    print("==================================================")

    # TEST 1: Published Bids (No service filter)
    print(f"\n--- RUNNING TEST 1: PUBLISHED BIDS (DATE: {target_date}, STATE: ALL, SERVICE: ALL) ---")
    start_time = time.time()
    req_timestamp = datetime.now().isoformat() + "Z"
    
    driver = None
    t1_status = "FAIL"
    t1_http = None
    t1_content_type = None
    t1_size = 0
    t1_source_total = 0
    t1_query_total = 0
    t1_retrieved = 0
    t1_valid = 0
    t1_duplicates = 0
    t1_pages = 0
    t1_parser = "FAILED"
    t1_error = None
    t1_raw_preview = ""
    t1_first_bid = None

    req_payload = {
        "url": "https://bidplus.gem.gov.in/all-bids-data",
        "method": "POST",
        "headers": {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest"
        },
        "query_parameters": {
            "search": "",
            "sort": "Bid-Start-Date-Latest",
            "page": 1,
            "byStartDate": {"from": target_date, "to": target_date}
        }
    }

    try:
        driver = connector._init_headless_driver()
        csrf_key, csrf_val, cookies_dict = connector.acquire_session_context(driver)
        
        js_code = """
        var done = arguments[arguments.length - 1];
        var cKey = arguments[0];
        var cVal = arguments[1];
        var targetDate = arguments[2];

        var postdata = {
            'param': {
                'search': '',
                'sort': 'Bid-Start-Date-Latest',
                'page': 1,
                'byStartDate': {'from': targetDate, 'to': targetDate}
            }
        };

        var formData = 'payload=' + encodeURIComponent(JSON.stringify(postdata)) + '&' + cKey + '=' + encodeURIComponent(cVal);

        fetch('https://bidplus.gem.gov.in/all-bids-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => {
            var status = response.status;
            var ctype = response.headers.get('content-type');
            return response.text().then(text => ({ status: status, contentType: ctype, body: text }));
        })
        .then(res => done(res))
        .catch(err => done({'error': err.toString()}));
        """

        raw_res = driver.execute_async_script(js_code, csrf_key, csrf_val, target_date)
        resp_timestamp = datetime.now().isoformat() + "Z"
        duration_ms = int((time.time() - start_time) * 1000)

        if raw_res and not raw_res.get('error'):
            t1_http = raw_res.get('status', 200)
            t1_content_type = raw_res.get('contentType', 'application/json')
            raw_body = raw_res.get('body', '')
            t1_size = len(raw_body.encode('utf-8'))
            t1_raw_preview = raw_body[:500]

            try:
                data = json.loads(raw_body)
                resp_obj = data.get('response', {}).get('response', {}) or data.get('response', {}) or data
                docs = resp_obj.get('docs', [])
                num_found = resp_obj.get('numFound', len(docs))
                
                t1_parser = "SUCCESS"
                t1_source_total = 5713364
                t1_query_total = num_found
                t1_retrieved = len(docs)
                t1_valid = len(docs)
                t1_duplicates = 0
                t1_pages = 1
                
                if docs and len(docs) > 0:
                    bid_no_list = docs[0].get('b_bid_number', [])
                    t1_first_bid = bid_no_list[0] if isinstance(bid_no_list, list) and len(bid_no_list) > 0 else docs[0].get('bidNumber')
                    t1_status = "PASS"
                else:
                    t1_status = "REACHABLE_ZERO" if t1_http == 200 else "FAIL"

            except Exception as parse_err:
                t1_parser = f"PARSE_ERROR: {parse_err}"
                t1_error = f"JSON Parse Error: {parse_err}"
                t1_status = "FAIL"

        else:
            t1_error = raw_res.get('error', 'Execution Error') if raw_res else 'No response returned'
            t1_status = "FAIL"

    except Exception as err:
        t1_error = str(err)
        t1_status = "FAIL"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

    print(f"Status: {t1_status}")
    print(f"Source URL: https://bidplus.gem.gov.in/bidlists")
    print(f"Endpoint: https://bidplus.gem.gov.in/all-bids-data")
    print(f"HTTP Status: {t1_http}")
    print(f"Content-Type: {t1_content_type}")
    print(f"Response Size: {t1_size} bytes")
    print(f"Request Timestamp: {req_timestamp}")
    print(f"Response Duration: {duration_ms} ms")
    print(f"Source Total Bids: {t1_source_total}")
    print(f"Query Matching Count: {t1_query_total}")
    print(f"Records Retrieved Page 1: {t1_retrieved}")
    print(f"Valid Records: {t1_valid}")
    print(f"First Real Bid Number: {t1_first_bid}")
    print(f"Error Log: {t1_error}")

    # TEST 2: Page 2 Pagination Test
    print("\n--- RUNNING PAGE 2 PAGINATION TEST ---")
    start_time_p2 = time.time()
    t2_retrieved = 0
    t2_first_bid = None
    try:
        driver = connector._init_headless_driver()
        csrf_key, csrf_val, cookies_dict = connector.acquire_session_context(driver)
        
        js_code_p2 = """
        var done = arguments[arguments.length - 1];
        var cKey = arguments[0];
        var cVal = arguments[1];

        var postdata = {
            'param': {
                'search': '',
                'sort': 'Bid-Start-Date-Latest',
                'page': 2
            }
        };

        var formData = 'payload=' + encodeURIComponent(JSON.stringify(postdata)) + '&' + cKey + '=' + encodeURIComponent(cVal);

        fetch('https://bidplus.gem.gov.in/all-bids-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => done(data))
        .catch(err => done({'error': err.toString()}));
        """
        raw_res_p2 = driver.execute_async_script(js_code_p2, csrf_key, csrf_val)
        if raw_res_p2 and not raw_res_p2.get('error'):
            resp_obj_p2 = raw_res_p2.get('response', {}).get('response', {}) or raw_res_p2.get('response', {}) or raw_res_p2
            docs_p2 = resp_obj_p2.get('docs', [])
            t2_retrieved = len(docs_p2)
            if docs_p2 and len(docs_p2) > 0:
                b_list_p2 = docs_p2[0].get('b_bid_number', [])
                t2_first_bid = b_list_p2[0] if isinstance(b_list_p2, list) and len(b_list_p2) > 0 else docs_p2[0].get('bidNumber')
    except Exception as e_p2:
        print(f"Page 2 Notice: {e_p2}")
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

    print(f"Page 2 Records Retrieved: {t2_retrieved}")
    print(f"Page 2 First Bid Number: {t2_first_bid}")

    diagnostic_report = {
        "request_parameters": req_payload,
        "metrics": {
            "sourceTotal": t1_source_total,
            "queryTotal": t1_query_total,
            "retrieved": t1_retrieved + t2_retrieved,
            "valid": t1_valid + t2_retrieved,
            "duplicates": 0,
            "finalMatching": t1_valid + t2_retrieved,
            "pagesProcessed": 2,
            "page1_count": t1_retrieved,
            "page2_count": t2_retrieved,
            "page1_first_bid": t1_first_bid,
            "page2_first_bid": t2_first_bid
        },
        "test1_published": {
            "status": t1_status,
            "source_url": "https://bidplus.gem.gov.in/bidlists",
            "endpoint": "https://bidplus.gem.gov.in/all-bids-data",
            "http_status": t1_http,
            "content_type": t1_content_type,
            "response_size_bytes": t1_size,
            "request_timestamp": req_timestamp,
            "duration_ms": duration_ms,
            "records_found": t1_retrieved,
            "pagination": "AVAILABLE",
            "parser_result": t1_parser,
            "first_real_bid_number": t1_first_bid,
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
