import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def inspect_js_functions():
    print("==================================================")
    print("      INSPECTING GEM FRONTEND JS FUNCTIONS")
    print("==================================================")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://bidplus.gem.gov.in/bidlists")
        time.sleep(3)

        # Inspect global window JS functions or pagination event handlers
        js_inspect = """
        var funcs = [];
        for (var prop in window) {
            if (typeof window[prop] === 'function' && (prop.toLowerCase().includes('bid') || prop.toLowerCase().includes('page') || prop.toLowerCase().includes('search') || prop.toLowerCase().includes('load'))) {
                funcs.push(prop);
            }
        }
        return {
            funcs: funcs,
            pageSourceLength: document.body.innerHTML.length,
            firstCardBefore: document.querySelector('.card, .bid-card, #bid_list, .bid-id, p.bid_no')?.innerText
        };
        """
        res1 = driver.execute_script(js_inspect)
        print(f"Discovered matching global JS functions: {res1.get('funcs')}")
        print(f"First bid text before click: {res1.get('firstCardBefore')}")

        # Try executing GeM's pagination script or location hash
        print("\nTesting window.location.hash = '#page-2'...")
        driver.execute_script("window.location.hash = '#page-2';")
        time.sleep(3)

        first_card_after_hash = driver.execute_script("return document.querySelector('.card, .bid-card, #bid_list, .bid-id, p.bid_no')?.innerText;")
        print(f"First bid text after hash = '#page-2': {first_card_after_hash}")

        # Try clicking page 2 link directly via jQuery or native click
        print("\nTesting direct click on pagination link '2'...")
        driver.execute_script("""
            var links = document.querySelectorAll('a');
            for (var i=0; i<links.length; i++) {
                if (links[i].innerText.trim() === '2') {
                    links[i].click();
                    break;
                }
            }
        """)
        time.sleep(4)

        first_card_after_click = driver.execute_script("return document.querySelector('.card, .bid-card, #bid_list, .bid-id, p.bid_no, a.bidUrl')?.innerText;")
        print(f"First bid text after link click '2': {first_card_after_click}")

        # Extract all bid numbers currently rendered on Page 2
        bid_numbers_p2 = driver.execute_script("""
            var nodes = document.querySelectorAll('a.bidUrl, p.bid_no, .bid-number');
            var list = [];
            for (var i=0; i<nodes.length; i++) {
                list.push(nodes[i].innerText.trim());
            }
            return list;
        """)
        print(f"\nRendered Bid Numbers on Page 2 ({len(bid_numbers_p2)} total):")
        for b in bid_numbers_p2[:5]:
            print(f"  - {b}")

    except Exception as err:
        print(f"JS inspection error: {err}")
    finally:
        driver.quit()

if __name__ == "__main__":
    inspect_js_functions()
