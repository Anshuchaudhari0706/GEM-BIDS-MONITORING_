import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def inspect_browser_pagination():
    print("==================================================")
    print("      INSPECTING REAL BROWSER PAGINATION CLICK")
    print("==================================================")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://bidplus.gem.gov.in/bidlists")
        time.sleep(3)

        # Inject performance logger to catch all fetch/XHR request payloads
        js_interceptor = """
        window.__capturedRequests = [];
        var origFetch = window.fetch;
        window.fetch = function() {
            var url = arguments[0];
            var opts = arguments[1] || {};
            window.__capturedRequests.push({ url: url, body: opts.body });
            return origFetch.apply(this, arguments);
        };
        """
        driver.execute_script(js_interceptor)

        # Find and click Page 2 button or pagination link in GeM UI
        page2_links = driver.find_elements("css selector", ".pagination a, ul.pagination li a, a.page-link, [data-page='2']")
        print(f"Found {len(page2_links)} pagination links on page")

        clicked = False
        for link in page2_links:
            text = link.text.strip()
            page_attr = link.get_attribute("data-page") or link.get_attribute("href") or ""
            print(f"Link text: '{text}', page_attr: '{page_attr}'")
            if text == "2" or "page=2" in page_attr or "2" in text:
                print(f"Clicking Page 2 link: {text}...")
                driver.execute_script("arguments[0].click();", link)
                clicked = True
                time.sleep(3)
                break

        captured = driver.execute_script("return window.__capturedRequests;")
        print(f"\nCaptured {len(captured)} network requests:")
        for idx, req in enumerate(captured):
            print(f"[{idx+1}] URL: {req.get('url')}")
            print(f"    Body: {req.get('body')}")

    except Exception as err:
        print(f"Browser click notice: {err}")
    finally:
        driver.quit()

if __name__ == "__main__":
    inspect_browser_pagination()
