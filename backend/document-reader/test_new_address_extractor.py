import json
import requests
import fitz
import re
import sys

# Pincode 3-digit prefix mapping
PINCODE_PREFIX_CITY_MAP = {
    # UP
    "246": ("Bijnor", "Uttar Pradesh"),
    "226": ("Lucknow", "Uttar Pradesh"),
    "208": ("Kanpur", "Uttar Pradesh"),
    "201": ("Noida", "Uttar Pradesh"),
    "250": ("Meerut", "Uttar Pradesh"),
    "282": ("Agra", "Uttar Pradesh"),
    "221": ("Varanasi", "Uttar Pradesh"),
    "211": ("Prayagraj", "Uttar Pradesh"),
    # Bihar
    "854": ("Katihar", "Bihar"),
    "800": ("Patna", "Bihar"),
    "812": ("Bhagalpur", "Bihar"),
    "842": ("Muzaffarpur", "Bihar"),
    "823": ("Gaya", "Bihar"),
    # TN
    "620": ("Tiruchirappalli", "Tamil Nadu"),
    "600": ("Chennai", "Tamil Nadu"),
    "641": ("Coimbatore", "Tamil Nadu"),
    "625": ("Madurai", "Tamil Nadu"),
    # Karnataka
    "580": ("Hubballi", "Karnataka"),
    "560": ("Bengaluru", "Karnataka"),
    "570": ("Mysuru", "Karnataka"),
    # AP & Telangana
    "530": ("Visakhapatnam", "Andhra Pradesh"),
    "520": ("Vijayawada", "Andhra Pradesh"),
    "500": ("Hyderabad", "Telangana"),
    # Maharashtra
    "400": ("Mumbai", "Maharashtra"),
    "401": ("Thane", "Maharashtra"),
    "411": ("Pune", "Maharashtra"),
    "440": ("Nagpur", "Maharashtra"),
    # MP
    "462": ("Bhopal", "Madhya Pradesh"),
    "452": ("Indore", "Madhya Pradesh"),
    "482": ("Jabalpur", "Madhya Pradesh"),
    # Gujarat
    "380": ("Ahmedabad", "Gujarat"),
    "382": ("Gandhinagar", "Gujarat"),
    "390": ("Vadodara", "Gujarat"),
    "395": ("Surat", "Gujarat"),
    "360": ("Rajkot", "Gujarat"),
    # Bengal & Odisha
    "700": ("Kolkata", "West Bengal"),
    "751": ("Bhubaneswar", "Odisha"),
    "760": ("Berhampur", "Odisha"),
    # Delhi
    "110": ("New Delhi", "Delhi")
}

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Chandigarh", "Jammu and Kashmir", "Ladakh"
]

def clean_text_for_parsing(text):
    # Normalize broken unicode or control characters that sometimes appear in PyMuPDF
    t = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    return t

def extract_real_tender_address(pdf_text, dept_name="", buyer_email=""):
    """
    Ultra-robust extraction of real Consignee Officer, Full Work/Office Address,
    City, State, and Pincode from GeM PDF document text.
    """
    if not pdf_text:
        return None

    cleaned_text = clean_text_for_parsing(pdf_text)
    lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()]

    consignee_officer = None
    address_lines = []
    pincode = None
    city = None
    state = None

    # STRATEGY 1: Look for Consignees / Reporting Officer Table (परेषिती/रिपोर्टिंग अधिकारी / Consignees/Reporting Officer)
    # The table in GeM PDF typically has:
    # 1. Header: Consignee / Reporting Officer and Quantity
    # 2. Columns: S.No. | Consignee/Reporting Officer | Address | Quantity | Delivery Days
    # 3. Row: 1 | <Officer Name> | <Multi-line Address> | <Quantity> | <Days>
    
    consignee_header_indices = []
    for idx, l in enumerate(lines):
        if re.search(r"Consignee.*Reporting|Consignee.*Officer|परे.*षती.*अिधकार|Consignees/Reporting Officer and Quantity", l, re.IGNORECASE):
            consignee_header_indices.append(idx)

    for h_idx in consignee_header_indices:
        # Search subsequent lines up to 35 lines ahead for row item '1'
        search_window = lines[h_idx:min(len(lines), h_idx + 35)]
        
        # Look for the row starting with '1' (first consignee)
        row_start_rel = None
        for r_idx, w_line in enumerate(search_window):
            if w_line == "1" or w_line == "1." or re.match(r"^1\s*$", w_line):
                # Ensure it's not a page number or item quantity by checking context
                row_start_rel = r_idx
                break
        
        if row_start_rel is not None:
            data_lines = search_window[row_start_rel + 1:]
            if len(data_lines) >= 2:
                # First line is usually the officer name
                officer_candidate = data_lines[0]
                if len(officer_candidate) > 2 and not officer_candidate.isdigit():
                    consignee_officer = officer_candidate.replace('*', '').strip() or officer_candidate
                
                # Subsequent lines up to quantity number or ATC section are address lines
                raw_addr_tokens = []
                for d_line in data_lines[1:]:
                    # If line is pure integer (e.g. quantity like "1", "120", "60", or delivery days "25", "180") or ATC header
                    if d_line.isdigit() and len(d_line) < 5:
                        # Could be quantity or delivery days - end of address block
                        if raw_addr_tokens:
                            break
                        continue
                    if any(k in d_line.lower() for k in ["buyer added", "special terms", "specification", "technical specifications", "advisory", "clause", "page "]):
                        break
                    raw_addr_tokens.append(d_line)
                
                if raw_addr_tokens:
                    full_addr_str = " ".join(raw_addr_tokens)
                    # Clean masking characters *********** if any
                    full_addr_str = re.sub(r'\*+', '', full_addr_str).strip()
                    
                    # Check for 6-digit Pincode in full_addr_str
                    pin_m = re.search(r"\b[1-9][0-9]{5}\b", full_addr_str)
                    if pin_m:
                        pincode = pin_m.group(0)
                    
                    # Split into clean address components
                    clean_addr = full_addr_str
                    # Remove leading or trailing commas/spaces
                    clean_addr = re.sub(r'^[,\s]+|[,\s]+$', '', clean_addr)
                    clean_addr = re.sub(r'\s+', ' ', clean_addr)
                    
                    if len(clean_addr) > 5:
                        address_lines.append(clean_addr)
                        break

    # STRATEGY 2: If Consignee Table wasn't found or masked, check "Beneficiary" block
    if not address_lines:
        for idx, l in enumerate(lines):
            if re.search(r"Beneficiary\s*:|लाभाथ_\s*:", l, re.IGNORECASE):
                ben_lines = lines[idx+1:min(len(lines), idx+6)]
                cleaned_ben = []
                for b_l in ben_lines:
                    if any(k in b_l.lower() for k in ["splitting", "purchase preference", "msme", "mii", "yes", "no", "page "]):
                        break
                    cleaned_ben.append(b_l)
                if cleaned_ben:
                    ben_str = ", ".join(cleaned_ben)
                    ben_str = re.sub(r'\*+', '', ben_str).strip()
                    if len(ben_str) > 10:
                        address_lines.append(ben_str)
                        pin_m = re.search(r"\b[1-9][0-9]{5}\b", ben_str)
                        if pin_m and not pincode:
                            pincode = pin_m.group(0)
                        break

    # STRATEGY 3: Check "Office Name" and "Buyer Email" from Page 1
    office_name = None
    buyer_loc = None
    for idx, l in enumerate(lines):
        if "Office Name" in l or "काया%लय का नाम" in l:
            if idx + 1 < len(lines):
                val = lines[idx+1]
                if not val.startswith("*") and len(val) > 2:
                    office_name = val
        if "Buyer Email" in l or "ेता ईमेल" in l:
            if idx + 1 < len(lines):
                buyer_email = lines[idx+1]

    # Resolve City & State from Pincode first
    if pincode and pincode[:3] in PINCODE_PREFIX_CITY_MAP:
        city, state = PINCODE_PREFIX_CITY_MAP[pincode[:3]]

    # If city or state still missing, search in extracted address string
    addr_combined = " ".join(address_lines)
    if not state:
        for st in INDIAN_STATES:
            if re.search(r"\b" + re.escape(st) + r"\b", addr_combined + " " + dept_name, re.IGNORECASE):
                state = st
                break

    if not city:
        # Check known cities
        for st_key, c_list in PINCODE_PREFIX_CITY_MAP.items():
            c_name = c_list[0]
            if re.search(r"\b" + re.escape(c_name) + r"\b", addr_combined, re.IGNORECASE):
                city = c_name
                if not state:
                    state = c_list[1]
                break

    # If still missing city, check office name or tokens
    if not city and office_name:
        for token in reversed(office_name.split()):
            token_clean = re.sub(r'[^a-zA-Z]', '', token).strip().title()
            if len(token_clean) > 3:
                city = token_clean
                break

    # Format the final clean real address
    if address_lines:
        final_address = address_lines[0]
        # Append pincode if not in address
        if pincode and pincode not in final_address:
            final_address = f"{final_address} - {pincode}"
    else:
        final_address = None

    return {
        "consignee_officer": consignee_officer or "Consignee Officer",
        "address": final_address,
        "city": city,
        "state": state,
        "pincode": pincode,
        "office_name": office_name
    }

# Run test on all downloaded analysis entries
with open("pdf_address_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"\n=======================================================")
print(f"TESTING NEW REAL ADDRESS EXTRACTOR ON {len(data)} REAL GeM PDFs:")
print(f"=======================================================")

for item in data:
    t_id = item["id"]
    full_sample = item["full_sample"]
    res = extract_real_tender_address(full_sample)
    print(f"\n[TENDER {t_id}]")
    print(f"  OLD WRONG ADDR: {item['stored_address']}")
    print(f"  NEW REAL ADDR : {res.get('address')}")
    print(f"  REAL OFFICER  : {res.get('consignee_officer')}")
    print(f"  REAL CITY     : {res.get('city')}")
    print(f"  REAL STATE    : {res.get('state')}")
    print(f"  REAL PINCODE  : {res.get('pincode')}")
