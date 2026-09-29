import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from curl_cffi import requests
import fitz
from tender_parser import parse_tender_document

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database.json")

with open(DB_PATH, "r", encoding="utf-8") as f:
    db = json.load(f)

tenders = db.get("tenders", [])
print(f"Total tenders in DB: {len(tenders)}")

def enrich_single(t):
    t_id = t.get("id") or t.get("bid_number")
    raw_doc = t.get("raw_doc") or {}
    b_id_list = raw_doc.get("b_id") or []
    b_id = str(b_id_list[0]) if b_id_list else None
    raw_num = t_id.split("/")[-1] if t_id else None
    
    target_id = b_id or raw_num
    if not target_id:
        return None
        
    url = f"https://bidplus.gem.gov.in/showbidDocument/{target_id}"
    try:
        r = requests.get(url, verify=False, impersonate="chrome120", timeout=8)
        if r.status_code == 200 and len(r.content) > 1000:
            doc = fitz.open(stream=r.content, filetype="pdf")
            full_text = "\n".join([page.get_text() for page in doc])
            
            parsed = parse_tender_document(full_text, t_id)
            if parsed:
                if parsed.get("staff_details") and len(parsed.get("staff_details")) > 0:
                    t["staff_details"] = parsed["staff_details"]
                    t["manpower"] = parsed["staff_details"]
                    t["primary_designation"] = parsed["primary_designation"]
                    t["duty_summary"] = parsed["duty_summary"]
                    t["duty_description"] = parsed["duty_description"]
                    t["employees"] = parsed["totalStaffCount"]
                    t["quantity"] = str(parsed["totalStaffCount"])
                    t["quantity_display"] = str(parsed["totalStaffCount"])
                    return (t_id, "MULTI/ROLES", parsed["primary_designation"], parsed["totalStaffCount"])
                elif parsed.get("primary_designation") and "Outsourced Manpower Staff" not in parsed.get("primary_designation"):
                    t["primary_designation"] = parsed["primary_designation"]
                    t["duty_summary"] = parsed["duty_summary"]
                    t["duty_description"] = parsed["duty_description"]
                    return (t_id, "SINGLE", parsed["primary_designation"], t.get("quantity"))
    except Exception as ex:
        return (t_id, "ERROR", str(ex), None)
    return (t_id, "SKIPPED", None, None)

print("Running fast multi-threaded PDF reader enrichment...")
with ThreadPoolExecutor(max_workers=16) as pool:
    futures = [pool.submit(enrich_single, t) for t in tenders]
    for fut in as_completed(futures):
        res = fut.result()
        if res and res[1] in ("MULTI/ROLES", "SINGLE"):
            print(f"[OK] {res[0]}: {str(res[2]).encode('ascii', 'replace').decode('ascii')} (Count: {res[3]})")

with open(DB_PATH, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2)

print("\nSaved updated database.json successfully!")
