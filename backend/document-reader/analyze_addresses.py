import json
import requests
import fitz
import re

with open("../database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

tenders = db.get("tenders", [])

results = []

for t in tenders[:15]:
    t_id = t.get("id")
    raw_id = t_id.split("/")[-1]
    url = f"https://bidplus.gem.gov.in/showbidDocument/{raw_id}"
    try:
        r = requests.get(url, verify=False, timeout=8)
        content_type = r.headers.get("content-type", "")
        print(f"Tender {t_id} -> HTTP {r.status_code}, length={len(r.content)}, type={content_type}")
        if r.status_code == 200 and ("pdf" in content_type or len(r.content) > 1000):
            try:
                doc = fitz.open(stream=r.content, filetype="pdf")
                full_text = "\n".join([f"[PAGE {i+1}]\n" + p.get_text() for i, p in enumerate(doc)])
                
                # Let's find all occurrences of Consignee / Address / Beneficiary in full_text
                consignee_matches = []
                lines = full_text.split("\n")
                for i, line in enumerate(lines):
                    # Check for address-related headings or pincodes
                    if re.search(r"consignee|reporting\s*officer|परे\s*षती|पता/address|address|पिनकोड|pincode|beneficiary|लाभाथ_", line, re.IGNORECASE):
                        snippet = lines[max(0, i-1):min(len(lines), i+12)]
                        consignee_matches.append({
                            "line_num": i,
                            "heading": line,
                            "snippet": snippet
                        })
                
                results.append({
                    "id": t_id,
                    "stored_address": t.get("address"),
                    "stored_city": t.get("city"),
                    "stored_state": t.get("state"),
                    "matches": consignee_matches[:5],
                    "full_sample": full_text[:4000]
                })
            except Exception as pe:
                print(f"PDF Parse error for {t_id}: {pe}")
    except Exception as e:
        print(f"Fetch error for {t_id}: {e}")

with open("pdf_address_analysis.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nAnalysis complete! Processed {len(results)} PDFs. Output saved to pdf_address_analysis.json")
