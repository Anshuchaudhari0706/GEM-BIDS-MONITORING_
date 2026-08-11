from curl_cffi import requests
import re
import json

s = requests.Session(impersonate="chrome120")

r1 = s.get('https://bidplus.gem.gov.in/bidlists')
print(f"GET Status: {r1.status_code}")

cname_match = re.search(r'id=["\']cname["\']\s+value=["\']([^"\']+)["\']', r1.text)
csrf_key = cname_match.group(1) if cname_match else 'csrf_bd_gem_nk'

csrf_val_match = re.search(r"['\"]" + csrf_key + r"['\"]\s*:\s*['\"]([^'\"]+)['\"]", r1.text)
csrf_val = csrf_val_match.group(1) if csrf_val_match else ''

print(f"Extracted CSRF Key: {csrf_key}")
print(f"Extracted CSRF Value: {csrf_val}")

payload = json.dumps({"param": {"search": "", "sort": "Bid-Start-Date-Latest"}})
post_data = {
    'payload': payload,
    csrf_key: csrf_val
}

r2 = s.post('https://bidplus.gem.gov.in/all-bids-data', data=post_data)
print(f"POST Status: {r2.status_code}")
data = r2.json()
docs = data.get('response', {}).get('response', {}).get('docs', [])
print(f"✅ SUCCESS! FETCHED {len(docs)} REAL LIVE OFFICIAL GE M BIDS!")
for d in docs[:10]:
    bno = (d.get('b_bid_number') or ['N/A'])[0]
    cat = (d.get('b_category_name') or ['N/A'])[0]
    print(f"REAL BID: {bno} | {cat[:60]}")
