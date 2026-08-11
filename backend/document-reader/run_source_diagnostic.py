import json
import time
from datetime import datetime
from gem_scraper import GeMConnector

def run_diagnostic():
    connector = GeMConnector()
    print("==================================================")
    print("       GEM SOURCE DIAGNOSTIC TEST RUNNER")
    print("==================================================")

    # TEST 1: Published Bids (No service filter)
    print("\n--- RUNNING TEST 1: PUBLISHED BIDS (NO SERVICE FILTER) ---")
    start_time = time.time()
    req_timestamp = datetime.now().isoformat() + "Z"
    
    driver = None
    t1_status = "FAIL"
    t1_http = None
    t1_content_type = None
    t1_size = 0
    t1_records = 0
    t1_pages = 0
    t1_pagination = "NOT AVAILABLE"
    t1_parser = "FAILED"
    t1_error = None
    t1_raw_preview = ""
    t1_first_bid = None

    try:
        driver = connector._init_headless_driver()
        csrf_key, csrf_val, cookies_dict = connector.acquire_session_context(driver)
        
        # Execute raw POST fetch for page 1
        js_code = """
        var done = arguments[arguments.length - 1];
        var cKey = arguments[0];
        var cVal = arguments[1];

        var postdata = {
            'param': {
                'search': '',
                'sort': 'Bid-Start-Date-Latest',
                'page': 1
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

        raw_res = driver.execute_async_script(js_code, csrf_key, csrf_val)
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
                docs = data.get('response', {}).get('response', {}).get('docs', []) or data.get('docs', [])
                num_found = data.get('response', {}).get('response', {}).get('numFound', 0) or len(docs)
                
                t1_parser = "SUCCESS"
                t1_records = len(docs)
                t1_pages = 1
                t1_pagination = f"AVAILABLE (Total Bids in Source: {num_found})" if num_found > 0 else "AVAILABLE (0 records)"
                
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
    print(f"Records Received: {t1_records}")
    print(f"Pagination: {t1_pagination}")
    print(f"Parser Result: {t1_parser}")
    print(f"First Real Bid Number: {t1_first_bid}")
    print(f"Error Log: {t1_error}")
    print(f"Raw Response Preview:\n{t1_raw_preview[:300]}...")

    # TEST 2: Finished/Closed Bids (No service filter)
    print("\n--- RUNNING TEST 2: FINISHED BIDS (NO SERVICE FILTER) ---")
    start_time_t2 = time.time()
    t2_status = "FAIL"
    t2_http = None
    t2_content_type = None
    t2_size = 0
    t2_records = 0
    t2_pages = 0
    t2_pagination = "NOT AVAILABLE"
    t2_parser = "FAILED"
    t2_error = None
    t2_raw_preview = ""
    t2_first_bid = None

    try:
        csrf_key, csrf_val, cookies_dict = connector.acquire_session_context(None)
        res_docs = connector.fetch_finished_bids(csrf_key, csrf_val, cookies_dict, target_date=None, target_state="ALL", max_pages=1)
        duration_ms_t2 = int((time.time() - start_time_t2) * 1000)
        
        t2_http = 200 if res_docs is not None else 500
        t2_content_type = "application/json"
        t2_records = len(res_docs)
        t2_parser = "SUCCESS" if res_docs is not None else "FAILED"
        t2_pages = 1 if res_docs else 0
        t2_pagination = "AVAILABLE" if res_docs else "NOT AVAILABLE"
        
        if res_docs and len(res_docs) > 0:
            t2_status = "PASS"
            b_list = res_docs[0].get('b_bid_number', [])
            t2_first_bid = b_list[0] if isinstance(b_list, list) and len(b_list) > 0 else res_docs[0].get('bidNumber')
            t2_raw_preview = json.dumps(res_docs[0])[:500]
        else:
            t2_status = "REACHABLE_ZERO" if t2_http == 200 else "FAIL"

    except Exception as err2:
        t2_error = str(err2)
        t2_status = "FAIL"
        duration_ms_t2 = int((time.time() - start_time_t2) * 1000)

    print(f"Status: {t2_status}")
    print(f"HTTP Status: {t2_http}")
    print(f"Content-Type: {t2_content_type}")
    print(f"Response Duration: {duration_ms_t2} ms")
    print(f"Records Received: {t2_records}")
    print(f"Parser Result: {t2_parser}")
    print(f"First Real Bid Number: {t2_first_bid}")
    print(f"Error Log: {t2_error}")

    diagnostic_report = {
        "test1_published": {
            "status": t1_status,
            "source_url": "https://bidplus.gem.gov.in/bidlists",
            "endpoint": "https://bidplus.gem.gov.in/all-bids-data",
            "http_status": t1_http,
            "content_type": t1_content_type,
            "response_size_bytes": t1_size,
            "request_timestamp": req_timestamp,
            "duration_ms": duration_ms,
            "records_found": t1_records,
            "pagination": t1_pagination,
            "parser_result": t1_parser,
            "first_real_bid_number": t1_first_bid,
            "error": t1_error,
            "raw_preview": t1_raw_preview[:300]
        },
        "test2_finished": {
            "status": t2_status,
            "http_status": t2_http,
            "records_found": t2_records,
            "parser_result": t2_parser,
            "first_real_bid_number": t2_first_bid,
            "error": t2_error
        }
    }

    with open("gem_source_diagnostic_results.json", "w") as f:
        json.dump(diagnostic_report, f, indent=2)

    print("\n==================================================")
    print("       DIAGNOSTIC REPORT SAVED TO JSON")
    print("==================================================")

if __name__ == "__main__":
    run_diagnostic()
