import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_load_bids():
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

        pages = []
        for page in range(1, 4):
            # Click pagination element page link
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

            bids = driver.execute_script("""
                var nodes = document.querySelectorAll('a.bidUrl, p.bid_no, .bid-number');
                var list = [];
                for (var i=0; i<nodes.length; i++) {
                    var txt = nodes[i].innerText.trim();
                    if (txt.startsWith('BID NO:') || txt.startsWith('GEM/')) {
                        list.push(txt);
                    }
                }
                return list;
            """)
            first_bid = bids[0] if bids else "NONE"
            last_bid = bids[-1] if bids else "NONE"
            pages.append({"page": page, "count": len(bids), "first": first_bid, "last": last_bid})
            print(f"PAGE {page}: count={len(bids)}, first={first_bid}, last={last_bid}")

        # Check if page 1 != page 2 and page 2 != page 3
        p1_first = pages[0]["first"]
        p2_first = pages[1]["first"]
        p3_first = pages[2]["first"]
        print(f"\nPagination Verification:")
        print(f"Page 1 != Page 2: {p1_first != p2_first} ({p1_first} vs {p2_first})")
        print(f"Page 2 != Page 3: {p2_first != p3_first} ({p2_first} vs {p3_first})")

    finally:
        driver.quit()

if __name__ == "__main__":
    test_load_bids()
