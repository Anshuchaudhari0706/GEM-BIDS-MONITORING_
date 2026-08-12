import json
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from curl_cffi import requests

GEM_BIDLISTS_URL = "https://bidplus.gem.gov.in/bidlists"
GEM_ALL_BIDS_DATA_URL = "https://bidplus.gem.gov.in/all-bids-data"

options = Options()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)
try:
    driver.get(GEM_BIDLISTS_URL)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cname_elem = soup.find('input', {'id': 'cname'})
    csrf_key = cname_elem.get('value') if cname_elem else 'csrf_bd_gem_nk'
    csrf_match = re.search(r"['\"]" + csrf_key + r"['\"]\s*:\s*['\"]([^'\"]+)['\"]", driver.page_source)
    csrf_val = csrf_match.group(1) if csrf_match else ''
    cookies_dict = {c['name']: c['value'] for c in driver.get_cookies()}
finally:
    driver.quit()

s = requests.Session(impersonate="chrome110")
for k, v in cookies_dict.items():
    s.cookies.set(k, v)

s.headers.update({
    'User-Agent': 'Mozilla/5.0',
    'Referer': GEM_BIDLISTS_URL,
    'X-Requested-With': 'XMLHttpRequest'
})

res = s.post(GEM_ALL_BIDS_DATA_URL, data={'payload': json.dumps({"page": 1, "param": {"search": "", "sort": "Bid-Start-Date-Latest"}}), csrf_key: csrf_val})
docs = res.json().get('response', {}).get('response', {}).get('docs', [])

print("Sample Solr Doc 1:")
for k, v in docs[0].items():
    print(f"  {k}: {v}")

print("\nSample Solr Doc 2:")
for k, v in docs[1].items():
    print(f"  {k}: {v}")
