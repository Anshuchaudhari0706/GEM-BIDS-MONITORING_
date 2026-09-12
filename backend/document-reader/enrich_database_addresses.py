import json
import requests
import fitz
import re
import sys
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

# Comprehensive Pincode 3-digit prefix mapping
PINCODE_PREFIX_CITY_MAP = {
    # UP
    "201": ("Noida", "Uttar Pradesh"),
    "208": ("Kanpur", "Uttar Pradesh"),
    "211": ("Prayagraj", "Uttar Pradesh"),
    "221": ("Varanasi", "Uttar Pradesh"),
    "223": ("Azamgarh", "Uttar Pradesh"),
    "226": ("Lucknow", "Uttar Pradesh"),
    "243": ("Bareilly", "Uttar Pradesh"),
    "246": ("Bijnor", "Uttar Pradesh"),
    "250": ("Meerut", "Uttar Pradesh"),
    "273": ("Gorakhpur", "Uttar Pradesh"),
    "282": ("Agra", "Uttar Pradesh"),
    # Bihar
    "800": ("Patna", "Bihar"),
    "812": ("Bhagalpur", "Bihar"),
    "823": ("Gaya", "Bihar"),
    "842": ("Muzaffarpur", "Bihar"),
    "846": ("Darbhanga", "Bihar"),
    "854": ("Katihar", "Bihar"),
    # Tamil Nadu
    "600": ("Chennai", "Tamil Nadu"),
    "620": ("Tiruchirappalli", "Tamil Nadu"),
    "625": ("Madurai", "Tamil Nadu"),
    "636": ("Salem", "Tamil Nadu"),
    "641": ("Coimbatore", "Tamil Nadu"),
    # Karnataka
    "560": ("Bengaluru", "Karnataka"),
    "570": ("Mysuru", "Karnataka"),
    "575": ("Mangaluru", "Karnataka"),
    "580": ("Hubballi", "Karnataka"),
    "585": ("Kalaburagi", "Karnataka"),
    # Maharashtra
    "400": ("Mumbai", "Maharashtra"),
    "401": ("Thane", "Maharashtra"),
    "411": ("Pune", "Maharashtra"),
    "422": ("Nashik", "Maharashtra"),
    "431": ("Aurangabad", "Maharashtra"),
    "440": ("Nagpur", "Maharashtra"),
    # Gujarat
    "360": ("Rajkot", "Gujarat"),
    "361": ("Jamnagar", "Gujarat"),
    "364": ("Bhavnagar", "Gujarat"),
    "370": ("Bhuj", "Gujarat"),
    "380": ("Ahmedabad", "Gujarat"),
    "382": ("Gandhinagar", "Gujarat"),
    "384": ("Mehsana", "Gujarat"),
    "388": ("Anand", "Gujarat"),
    "390": ("Vadodara", "Gujarat"),
    "395": ("Surat", "Gujarat"),
    "396": ("Valsad", "Gujarat"),
    # Delhi & Haryana
    "110": ("New Delhi", "Delhi"),
    "121": ("Faridabad", "Haryana"),
    "122": ("Gurugram", "Haryana"),
    "125": ("Hisar", "Haryana"),
    "132": ("Panipat", "Haryana"),
    "133": ("Ambala", "Haryana"),
    "134": ("Panchkula", "Haryana"),
    # Punjab & Chandigarh
    "160": ("Chandigarh", "Chandigarh"),
    "141": ("Ludhiana", "Punjab"),
    "143": ("Amritsar", "Punjab"),
    "144": ("Jalandhar", "Punjab"),
    # Rajasthan
    "301": ("Alwar", "Rajasthan"),
    "302": ("Jaipur", "Rajasthan"),
    "305": ("Ajmer", "Rajasthan"),
    "313": ("Udaipur", "Rajasthan"),
    "324": ("Kota", "Rajasthan"),
    "334": ("Bikaner", "Rajasthan"),
    "342": ("Jodhpur", "Rajasthan"),
    # MP & CG
    "452": ("Indore", "Madhya Pradesh"),
    "462": ("Bhopal", "Madhya Pradesh"),
    "474": ("Gwalior", "Madhya Pradesh"),
    "482": ("Jabalpur", "Madhya Pradesh"),
    "492": ("Raipur", "Chhattisgarh"),
    # Bengal, Odisha, Jharkhand
    "700": ("Kolkata", "West Bengal"),
    "711": ("Howrah", "West Bengal"),
    "713": ("Durgapur", "West Bengal"),
    "741": ("Kalyani", "West Bengal"),
    "751": ("Bhubaneswar", "Odisha"),
    "753": ("Cuttack", "Odisha"),
    "760": ("Berhampur", "Odisha"),
    "769": ("Rourkela", "Odisha"),
    "826": ("Dhanbad", "Jharkhand"),
    "831": ("Jamshedpur", "Jharkhand"),
    "834": ("Ranchi", "Jharkhand"),
    # AP & Telangana
    "500": ("Hyderabad", "Telangana"),
    "506": ("Warangal", "Telangana"),
    "520": ("Vijayawada", "Andhra Pradesh"),
    "530": ("Visakhapatnam", "Andhra Pradesh"),
    # Kerala
    "682": ("Kochi", "Kerala"),
    "695": ("Thiruvananthapuram", "Kerala"),
    # Assam & NE
    "781": ("Guwahati", "Assam"),
    # J&K, Uttarakhand & HP
    "184": ("Kathua", "Jammu and Kashmir"),
    "180": ("Jammu", "Jammu and Kashmir"),
    "190": ("Srinagar", "Jammu and Kashmir"),
    "248": ("Dehradun", "Uttarakhand"),
    "171": ("Shimla", "Himachal Pradesh"),
    # Goa
    "403": ("Panaji", "Goa")
}

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Chandigarh", "Jammu and Kashmir", "Ladakh"
]

def clean_gem_text(text):
    if not text:
        return ""
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

def parse_full_gem_pdf_for_address(pdf_bytes, dept_name="", ministry_name=""):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        return None

    full_text = clean_gem_text("\n".join([p.get_text() for p in doc]))
    lines = [l.strip() for l in full_text.split('\n') if l.strip()]

    consignee_officer = None
    address_lines = []
    pincode = None
    city = None
    state = None
    office_name = None

    # Step 1: Check Page 1 metadata
    for idx, l in enumerate(lines[:120]):
        if any(k in l.lower() for k in ["ministry/state name", "मं ालय/रा!य का नाम", "ministry/state"]):
            if idx + 1 < len(lines):
                val = lines[idx+1].strip()
                for st in INDIAN_STATES:
                    if st.lower() == val.lower() or st.lower() in val.lower():
                        state = st
                        break
        if any(k in l.lower() for k in ["office name", "काया%लय का नाम"]):
            if idx + 1 < len(lines):
                val = lines[idx+1].strip()
                if not val.startswith("*") and len(val) > 2:
                    office_name = val

    # Step 2: Search for Consignees / Reporting Officer Table
    for idx, l in enumerate(lines):
        if re.search(r"Consignee.*Reporting|Consignee.*Officer|परे.*षती.*अिधकार|Consignees/Reporting Officer", l, re.IGNORECASE):
            window = lines[idx:min(len(lines), idx + 40)]
            row_idx = None
            for w_i, w_l in enumerate(window):
                if re.match(r"^1\.?$", w_l):
                    row_idx = w_i
                    break
            
            if row_idx is not None and row_idx + 1 < len(window):
                row_content = window[row_idx + 1:]
                officer_line = row_content[0].replace('*', '').strip()
                if len(officer_line) > 1 and not officer_line.isdigit():
                    consignee_officer = officer_line
                
                raw_addr_tokens = []
                for a_l in row_content[1:]:
                    tok_lower = a_l.lower().strip()
                    # Terminate when hitting service columns, delivery days, quantity, or next section
                    if any(term in tok_lower for term in [
                        "project /", "lumpsum", "based", "monthly basis", "delivery days", "डिलीवरी",
                        "s.no", "सं.", "additional requirement", "अतिरिक्त आवश्यकता", "buyer added", "special terms",
                        "advisory", "clause", "specification", "terms and conditions", "eligibility", "view file"
                    ]):
                        break
                    
                    if a_l.isdigit() and len(a_l) < 5:
                        if raw_addr_tokens:
                            break
                        continue
                    
                    if tok_lower in ["n/a", "na", "-", "/", "\\"]:
                        continue

                    clean_l = a_l.replace('*', '').strip()
                    if clean_l:
                        raw_addr_tokens.append(clean_l)
                
                if raw_addr_tokens:
                    combined_addr = ", ".join(raw_addr_tokens)
                    combined_addr = re.sub(r'^[,\s]+|[,\s]+$', '', combined_addr)
                    combined_addr = re.sub(r',\s*,', ',', combined_addr)
                    
                    pin_m = re.search(r"\b[1-9][0-9]{5}\b", combined_addr)
                    if pin_m:
                        pincode = pin_m.group(0)
                        combined_addr = re.sub(r'^' + pincode + r'\s*,\s*', '', combined_addr)
                    
                    if len(combined_addr) > 3:
                        address_lines.append(combined_addr)
                        break

    # Step 3: Beneficiary fallback
    if not address_lines:
        for idx, l in enumerate(lines):
            if re.search(r"Beneficiary\s*:|लाभाथ_\s*:", l, re.IGNORECASE):
                ben_window = lines[idx+1:min(len(lines), idx+8)]
                ben_tokens = []
                for b_l in ben_window:
                    if any(k in b_l.lower() for k in ["splitting", "purchase preference", "msme", "mii", "yes", "no", "page "]):
                        break
                    clean_b = b_l.replace('*', '').strip()
                    if clean_b and not clean_b.startswith("("):
                        ben_tokens.append(clean_b)
                if ben_tokens:
                    ben_str = ", ".join(ben_tokens)
                    ben_str = re.sub(r'^[,\s]+|[,\s]+$', '', ben_str)
                    if len(ben_str) > 10:
                        pin_m = re.search(r"\b[1-9][0-9]{5}\b", ben_str)
                        if pin_m:
                            pincode = pin_m.group(0)
                        address_lines.append(ben_str)
                        break

    # Step 4: Resolve City & State from Pincode map
    if pincode and pincode[:3] in PINCODE_PREFIX_CITY_MAP:
        mapped_city, mapped_state = PINCODE_PREFIX_CITY_MAP[pincode[:3]]
        city = mapped_city
        if not state:
            state = mapped_state

    # Step 5: Check city/state in address string
    addr_str = " ".join(address_lines)
    if not state:
        for st in INDIAN_STATES:
            if re.search(r"\b" + re.escape(st) + r"\b", addr_str + " " + dept_name + " " + ministry_name, re.IGNORECASE):
                state = st
                break

    if not city:
        for st_k, c_info in PINCODE_PREFIX_CITY_MAP.items():
            c_n = c_info[0]
            if re.search(r"\b" + re.escape(c_n) + r"\b", addr_str, re.IGNORECASE):
                city = c_n
                if not state:
                    state = c_info[1]
                break

    # Format final official address
    if address_lines:
        clean_final = address_lines[0]
        if pincode and pincode not in clean_final:
            clean_final = f"{clean_final} - {pincode}"
    elif office_name:
        clean_final = f"{office_name}, {city or ''}, {state or ''} - {pincode or ''}".strip(" ,-")
    else:
        clean_final = None

    return {
        "consignee_officer": consignee_officer or "Consignee / Reporting Officer",
        "address": clean_final,
        "city": city or "Not Specified",
        "state": state or "Not Specified",
        "pincode": pincode or "Not Specified",
        "office_name": office_name
    }

def process_single_tender(t):
    t_id = t.get("id")
    raw_doc = t.get("raw_doc", {})
    b_id_val = None
    if isinstance(raw_doc, dict):
        b_ids = raw_doc.get("b_id", [])
        if isinstance(b_ids, list) and len(b_ids) > 0:
            b_id_val = str(b_ids[0])
    
    candidates = []
    if b_id_val:
        candidates.append(b_id_val)
    candidates.append(t_id.split("/")[-1])
    
    for cid in candidates:
        try:
            url = f"https://bidplus.gem.gov.in/showbidDocument/{cid}"
            r = requests.get(url, verify=False, timeout=8)
            if r.status_code == 200 and len(r.content) > 1000:
                parsed = parse_full_gem_pdf_for_address(
                    r.content,
                    t.get("department", ""),
                    raw_doc.get("ba_official_details_minName", [""])[0] if isinstance(raw_doc, dict) and isinstance(raw_doc.get("ba_official_details_minName"), list) else ""
                )
                if parsed and parsed.get("address"):
                    return t_id, parsed
        except Exception:
            pass
    return t_id, None

import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database.json'))

# Load DB and process all tenders
with open(db_path, "r", encoding="utf-8") as f:
    db = json.load(f)

tenders = db.get("tenders", [])
print(f"Enriching {len(tenders)} tenders from GeM official PDFs using ThreadPool...")

with ThreadPoolExecutor(max_workers=8) as executor:
    results = list(executor.map(process_single_tender, tenders))

updated_count = 0
for t_id, parsed in results:
    if parsed and parsed.get("address"):
        for t in tenders:
            if t.get("id") == t_id:
                t["address"] = parsed["address"]
                t["office_address"] = parsed["address"]
                if parsed["consignee_officer"] != "Consignee / Reporting Officer":
                    t["consignee_officer"] = parsed["consignee_officer"]
                if parsed["city"] != "Not Specified":
                    t["city"] = parsed["city"]
                if parsed["state"] != "Not Specified":
                    t["state"] = parsed["state"]
                if parsed["pincode"] != "Not Specified":
                    t["pincode"] = parsed["pincode"]
                
                if "work_location" in t and isinstance(t["work_location"], dict):
                    t["work_location"]["address"] = parsed["address"]
                    t["work_location"]["city"] = t["city"]
                    t["work_location"]["state"] = t["state"]
                    t["work_location"]["pincode"] = t["pincode"]
                    t["work_location"]["consignee_officer"] = t["consignee_officer"]
                updated_count += 1
                print(f"✅ {t_id} -> {parsed['address']} ({t['city']}, {t['state']})")
                break

print(f"\n=======================================================")
print(f"Successfully enriched {updated_count}/{len(tenders)} tenders with REAL GeM PDF Addresses!")
print(f"=======================================================")

with open(db_path, "w", encoding="utf-8") as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("Saved updated database.json successfully!")
