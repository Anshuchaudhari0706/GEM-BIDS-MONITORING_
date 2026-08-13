import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def capture_official_gem_payload():
    print("==================================================")
    print("CAPTURING OFFICIAL GeM BIDLISTS NETWORK REQUESTS")
    print("==================================================")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get('https://bidplus.gem.gov.in/all-bids')
        time.sleep(4)

        # Trigger network actions or inspect requests captured
        logs = driver.get_log('performance')

        all_bids_requests = []
        for entry in logs:
            try:
                log_data = json.loads(entry['message'])
                message = log_data.get('message', {})
                method = message.get('method', '')

                if method == 'Network.requestWillBeSent':
                    request = message.get('params', {}).get('request', {})
                    url = request.get('url', '')
                    if 'all-bids-data' in url or 'bidlists' in url:
                        post_data = request.get('postData', '')
                        headers = request.get('headers', {})
                        all_bids_requests.append({
                            'url': url,
                            'method': request.get('method'),
                            'postData': post_data,
                            'headers': headers
                        })
            except Exception:
                pass

        print(f"Captured {len(all_bids_requests)} network requests matching GeM bid endpoints:\n")

        for idx, req in enumerate(all_bids_requests):
            print(f"--- REQUEST [{idx+1}] ---")
            print(f"URL: {req['url']}")
            print(f"METHOD: {req['method']}")
            print(f"POST DATA: {req['postData']}\n")

    except Exception as e:
        print(f"Error capturing payload: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_official_gem_payload()
