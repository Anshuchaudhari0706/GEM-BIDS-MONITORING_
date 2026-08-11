import json
import time
from gem_scraper import GeMConnector

def test_pagination():
    connector = GeMConnector()
    print("==================================================")
    print("      GEM PAGINATION PROTOCOL INSPECTOR")
    print("==================================================")

    driver = connector._init_headless_driver()
    try:
        csrf_key, csrf_val, cookies_dict = connector.acquire_session_context(driver)
        
        # Test 5 different payload variations for Page 2:
        variations = [
            {"name": "param.page=2", "payload": {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "page": 2}}},
            {"name": "param.pageNo=2", "payload": {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "pageNo": 2}}},
            {"name": "param.start=10", "payload": {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "start": 10}}},
            {"name": "param.offset=10", "payload": {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "offset": 10}}},
            {"name": "param.page=2,start=10", "payload": {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "page": 2, "start": 10}}}
        ]

        js_code = """
        var done = arguments[arguments.length - 1];
        var postObj = arguments[0];
        var cKey = arguments[1];
        var cVal = arguments[2];

        var formData = 'payload=' + encodeURIComponent(JSON.stringify(postObj)) + '&' + cKey + '=' + encodeURIComponent(cVal);

        fetch('https://bidplus.gem.gov.in/all-bids-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(r => r.json())
        .then(data => done(data))
        .catch(err => done({'error': err.toString()}));
        """

        # First get Page 1
        page1_res = driver.execute_async_script(js_code, {"param": {"search": "", "sort": "Bid-Start-Date-Latest", "page": 1}}, csrf_key, csrf_val)
        docs1 = page1_res.get('response', {}).get('response', {}).get('docs', []) or page1_res.get('docs', [])
        p1_first = docs1[0].get('b_bid_number', [None])[0] if docs1 else "EMPTY"
        p1_last = docs1[-1].get('b_bid_number', [None])[0] if docs1 else "EMPTY"
        print(f"\nPAGE 1 (Default): Count={len(docs1)}, First={p1_first}, Last={p1_last}")

        for var in variations:
            res = driver.execute_async_script(js_code, var["payload"], csrf_key, csrf_val)
            docs = res.get('response', {}).get('response', {}).get('docs', []) or res.get('docs', [])
            p2_first = docs[0].get('b_bid_number', [None])[0] if docs else "EMPTY"
            p2_last = docs[-1].get('b_bid_number', [None])[0] if docs else "EMPTY"
            is_advanced = p2_first != p1_first if docs else False
            print(f"Variation [{var['name']}]: Count={len(docs)}, First={p2_first}, Advanced={is_advanced}")

    except Exception as err:
        print(f"Pagination Test Error: {err}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_pagination()
