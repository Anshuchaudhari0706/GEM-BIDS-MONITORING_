import json
from curl_cffi import requests
import fitz
import re

with open('../database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

tenders = db.get("tenders", [])

test_ids = [
    "GEM/2026/B/8060177",
    "GEM/2026/B/8032101",
    "GEM/2026/B/7963352",
    "GEM/2026/B/8056284",
    "GEM/2026/B/8059769",
    "GEM/2026/B/8065509",
    "GEM/2026/B/7965384",
    "GEM/2026/B/7942333"
]

def clean_val(val):
    if not val:
        return ""
    val = re.sub(r'[\r\n]+', ' ', val).strip()
    cut_tokens = [
        "Specialization", "विशेषज्ञता", "Educational Qualification", "शैक्षिक योग्यता",
        "Type of Function", "कार्य का प्रकार", "Core", "कोर", "Post Graduation", "स्नातकोत्तर",
        "Experience", "अनुभव", "District", "Zipcode", "State", "मूल्य", "Values", "Specification", "विवरण",
        "Title for Optional", "Designation", "पदनाम", "Minimum Floor Price", "Additional Details", "Addon"
    ]
    for tok in cut_tokens:
        tok_idx = val.lower().find(tok.lower())
        if tok_idx > 0:
            val = val[:tok_idx].strip()
    val = re.sub(r'^[\|\:\-\s\.\,]+|[\|\:\-\s\.\,]+$', '', val).strip()
    return val

def extract_multi_role_breakdown(full_text):
    # Clean text from all pages, stripping footer page numbers
    cleaned_text = re.sub(r'\n\s*\d+\s*\/\s*\d+\s*\n', '\n', full_text)
    cleaned_text = re.sub(r'\(\s*\n\s*(\d+)\s*\)', r'(\1)', cleaned_text)
    
    # 1. Schedule headers
    schedule_pattern = r'([A-Za-z\s\-\;\,]+(?:Manpower|Security|Sanitation|Housekeeping|Cleaning|Driver|Staff|Services|Fixed)[A-Za-z0-9\s\-\;\,\/]*)\s*\(\s*(\d+)\s*\)\s*\n\s*(?:[\?]+|[^\n\r]{0,30}?(?:Technical\s+Specifications|\/Technical\s+Specifications|\u0924\u0915\u0928\u0940\u0915\u0940))'
    matches = list(re.finditer(schedule_pattern, cleaned_text, re.I))
    
    roles = []
    if matches:
        for idx, m in enumerate(matches):
            start_pos = m.start()
            end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(cleaned_text)
            block = cleaned_text[start_pos:end_pos]
            
            hdr_category = m.group(1).strip()
            hdr_qty = int(m.group(2))
            
            prof_m = re.search(r'(?:List\s+of\s+Profiles|\u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932\s*\u0915\u0940\s*\u0938\u0942\u091a\u0940)\s*[:\|\-]?\s*([^\n\r\|]{2,80})', block, re.I)
            desig_m = re.search(r'(?:Designation|\u092a\u0926\u0928\u093e\u092e)\s*[:\|\-]?\s*([^\n\r\|]{2,80})', block, re.I)
            skill_m = re.search(r'(?:Skill\s+Category|\u0915\u094c\u0936\u0932\s*\u0936\u094d\u0930\u0947\u0923\u0940)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
            edu_m = re.search(r'(?:Educational\s+Qualification|\u0936\u0948\u0915\u094d\u0937\u093f\u0915\s*\u092f\u094b\u0917\u094d\u092f\u0924\u093e)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
            func_m = re.search(r'(?:Type\s+of\s+Function|\u0915\u093e\u0930\u094d\u092f\s*\u0915\u093e\s*\u092a\u094d\u0930\u0915\u093e\u0930)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
            
            table_qty_m = re.search(r'(?:Number\s+of\s+Resources\s+to\s+be\s+hired|\u0938\u0902\u0938\u093e\u0927\u0928\u094b\u0902\s*\u0915\u0940\s*\u092e\u093e\u0924\u094d\u0930\u093e)[\s\S]*?\n\s*(\d+)\s*\n\s*[^\n\r]+\n\s*[^\n\r]+\n\s*(\d+)\s*\n\s*Minimum\s+daily', block, re.I)
            
            qty = hdr_qty
            if table_qty_m:
                qty = int(table_qty_m.group(2))
                
            raw_prof = clean_val(prof_m.group(1)) if prof_m else ""
            raw_desig = clean_val(desig_m.group(1)) if desig_m else ""
            
            designation = raw_desig or raw_prof or "Outsourced Staff"
            profile = raw_prof or raw_desig or designation
            skill = clean_val(skill_m.group(1)) if skill_m else "Unskilled"
            edu = clean_val(edu_m.group(1)) if edu_m else "Secondary School"
            func = clean_val(func_m.group(1)) if func_m else "Others"
            
            # Map canonical and duty
            role_lower = f"{designation} {profile}".lower()
            if any(k in role_lower for k in ["data entry", "deo", "computer", "typist"]):
                canonical = "Data Entry Operator (DEO)"
                duty_sum = "Computer Data Entry & Records Management"
            elif any(k in role_lower for k in ["khansama", "cook", "chef", "kitchen", "cater"]):
                canonical = "Khansama / Cook"
                duty_sum = "Meal Preparation & Kitchen Management"
            elif any(k in role_lower for k in ["safai", "sweeper", "clean", "sanitation", "housekeep"]):
                canonical = "Safaiwala / Sanitation Worker"
                duty_sum = "Premises Cleaning & Sanitation"
            elif any(k in role_lower for k in ["mali", "gardener", "gardner", "horticulture"]):
                canonical = "Mali / Gardener"
                duty_sum = "Gardening & Plantation Upkeep"
            elif any(k in role_lower for k in ["security", "guard", "watchman", "gate man", "un-armed security"]):
                canonical = "Security Guard"
                duty_sum = "Watch & Ward / Premises Security"
            elif any(k in role_lower for k in ["driver", "chauffeur"]):
                canonical = "Driver / Chauffeur"
                duty_sum = "Vehicle Driving & Logbook Maintenance"
            elif any(k in role_lower for k in ["electrician", "wireman"]):
                canonical = "Electrician / Wireman"
                duty_sum = "Electrical Wiring & Equipment Maintenance"
            elif any(k in role_lower for k in ["plumber"]):
                canonical = "Plumber / Pipe Fitter"
                duty_sum = "Sanitary Pipelines & Water Supply"
            elif any(k in role_lower for k in ["mts", "peon", "helper", "office boy"]):
                canonical = "Multi-Tasking Staff (MTS) / Peon"
                duty_sum = "Office Maintenance & Document Movement"
            else:
                canonical = designation
                duty_sum = "Operational Support & Deliverables"

            roles.append({
                "designation": designation,
                "canonical_designation": canonical,
                "profile": profile,
                "quantity": qty,
                "skill_category": skill,
                "educational_qualification": edu,
                "type_of_function": func,
                "duty_summary": duty_sum
            })
            
    return roles

for t_id in test_ids:
    raw_id = t_id.split("/")[-1]
    # Check if we have b_id in db
    t_obj = next((x for x in tenders if x.get("id") == t_id), None)
    b_id = None
    if t_obj:
        raw_doc = t_obj.get("raw_doc") or {}
        b_id_list = raw_doc.get("b_id") or []
        if b_id_list:
            b_id = str(b_id_list[0])
            
    target_id = b_id or raw_id
    url = f"https://bidplus.gem.gov.in/showbidDocument/{target_id}"
    try:
        r = requests.get(url, verify=False, impersonate="chrome120", timeout=8)
        if r.status_code == 200 and len(r.content) > 1000:
            doc = fitz.open(stream=r.content, filetype="pdf")
            full_text = "\n".join([page.get_text() for page in doc])
            roles = extract_multi_role_breakdown(full_text)
            print(f"\n==========================================")
            print(f"TENDER: {t_id} (Target ID: {target_id}) - Found {len(roles)} roles:")
            for role in roles:
                print(f"  - {role['quantity']}x {role['designation']} ({role['skill_category']}, {role['educational_qualification']}) -> Duty: {role['duty_summary']}")
            print(f"  Total Staff: {sum(r['quantity'] for r in roles)}")
        else:
            print(f"Fetch failed for {t_id} (Status: {r.status_code}, len: {len(r.content)})")
    except Exception as e:
        print(f"Error for {t_id}: {e}")
