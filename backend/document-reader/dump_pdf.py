import requests
import fitz

r = requests.get('https://bidplus.gem.gov.in/showbidDocument/7927224', verify=False, timeout=10)
doc = fitz.open(stream=r.content, filetype='pdf')
text = '\n'.join([f"--- PAGE {i+1} ---\n" + p.get_text() for i, p in enumerate(doc)])
with open("pdf_dump_7927224.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Saved pdf_dump_7927224.txt successfully!")
