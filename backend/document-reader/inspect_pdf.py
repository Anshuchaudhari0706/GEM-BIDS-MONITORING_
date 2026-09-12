import requests
import fitz
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://bidplus.gem.gov.in/showbidDocument/7927224', verify=False, timeout=10)
doc = fitz.open(stream=r.content, filetype='pdf')
text = '\n'.join([p.get_text() for p in doc])
print(f"Total pages: {len(doc)}, Total chars: {len(text)}")

# Look for Consignee / Reporting Officer and Address lines
lines = text.split('\n')
for i, line in enumerate(lines):
    if any(k in line.lower() for k in ['consignee', 'reporting officer', 'परेषिती', 'address', 'पता', 'pin code', 'pincode', 'buyer']):
        start = max(0, i - 2)
        end = min(len(lines), i + 8)
        print(f"--- MATCH AT LINE {i} ---")
        for j in range(start, end):
            print(f"  {j}: {lines[j]}")
