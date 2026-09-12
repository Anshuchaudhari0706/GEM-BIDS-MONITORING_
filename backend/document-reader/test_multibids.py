import json
import requests
import fitz

with open("../database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

tenders = db.get("tenders", [])
print(f"Total tenders in DB: {len(tenders)}")

for t in tenders[:10]:
    t_id = t.get("id")
    raw_id = t_id.split("/")[-1]
    url = f"https://bidplus.gem.gov.in/showbidDocument/{raw_id}"
    try:
        r = requests.get(url, verify=False, timeout=8)
        if r.status_code == 200 and len(r.content) > 500:
            doc = fitz.open(stream=r.content, filetype="pdf")
            text = "\n".join([p.get_text() for p in doc])
            
            # Search for Beneficiary and Consignee block
            print(f"\n==========================================")
            print(f"TENDER {t_id} (Length: {len(text)} chars)")
            print(f"Stored Address: {t.get('address')}")
            
            # Find Consignee or Beneficiary lines
            lines = text.split("\n")
            for i, line in enumerate(lines):
                if any(k in line.lower() for k in ["consignees/reporting", "consignee reporting", "परे षती//रपो@टbग", "लाभाथ_", "beneficiary :", "beneficiary:"]):
                    snippet = "\n".join(lines[i:min(len(lines), i+15)])
                    print(f"--- MATCH AT LINE {i} ---")
                    print(snippet)
                    break
        else:
            print(f"Tender {t_id} fetch failed: {r.status_code}")
    except Exception as e:
        print(f"Tender {t_id} error: {e}")
