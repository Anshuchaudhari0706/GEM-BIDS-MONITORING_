import fitz
import re
import json

doc = fitz.open('test_9919881.pdf')

# Clean text from all pages, stripping footer page numbers like "4 / 14"
cleaned_pages = []
for p in range(len(doc)):
    p_text = doc[p].get_text()
    # Strip page number footer like "\n4 / 14\n"
    p_text = re.sub(r'\n\s*\d+\s*\/\s*\d+\s*\n', '\n', p_text)
    cleaned_pages.append(p_text)

full_cleaned_text = "\n".join(cleaned_pages)
# Normalize multiline parentheses like "(\n 5 )"
full_cleaned_text = re.sub(r'\(\s*\n\s*(\d+)\s*\)', r'(\1)', full_cleaned_text)

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

# Identify all schedule items in the document
# Method 1: Find all occurrences of "<Category / Service Name> ( <QTY> )"
schedule_pattern = r'([A-Za-z\s\-\;\,]+(?:Manpower|Security|Sanitation|Housekeeping|Cleaning|Driver|Staff|Services)[A-Za-z0-9\s\-\;\,\/]*)\s*\(\s*(\d+)\s*\)\s*\n\s*(?:[\?]+|[^\n\r]{0,30}?(?:Technical\s+Specifications|\/Technical\s+Specifications|\u0924\u0915\u0928\u0940\u0915\u0940))'

matches = list(re.finditer(schedule_pattern, full_cleaned_text, re.I))
print(f"Schedule headers found: {len(matches)}")

extracted_roles = []

if matches:
    for idx, m in enumerate(matches):
        start_pos = m.start()
        end_pos = matches[idx+1].start() if idx + 1 < len(matches) else len(full_cleaned_text)
        block = full_cleaned_text[start_pos:end_pos]
        
        hdr_category = m.group(1).strip()
        hdr_qty = int(m.group(2))
        
        # 1. Profile & Designation
        prof_m = re.search(r'(?:List\s+of\s+Profiles|\u092a\u094d\u0930\u094b\u092b\u093e\u0907\u0932\s*\u0915\u0940\s*\u0938\u0942\u091a\u0940)\s*[:\|\-]?\s*([^\n\r\|]{2,80})', block, re.I)
        desig_m = re.search(r'(?:Designation|\u092a\u0926\u0928\u093e\u092e)\s*[:\|\-]?\s*([^\n\r\|]{2,80})', block, re.I)
        
        # 2. Skill Category & Education
        skill_m = re.search(r'(?:Skill\s+Category|\u0915\u094c\u0936\u0932\s*\u0936\u094d\u0930\u0947\u0923\u0940)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
        edu_m = re.search(r'(?:Educational\s+Qualification|\u0936\u0948\u0915\u094d\u0937\u093f\u0915\s*\u092f\u094b\u0917\u094d\u092f\u0924\u093e)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
        func_m = re.search(r'(?:Type\s+of\s+Function|\u0915\u093e\u0930\u094d\u092f\s*\u0915\u093e\s*\u092a\u094d\u0930\u0915\u093e\u0930)\s*[:\|\-]?\s*([^\n\r\|]{2,60})', block, re.I)
        
        # 3. Consignee / Resources Table
        # Extract row from table: e.g. 1\n*****\n*****Cachar\n5\nMinimum daily wage
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
        
        # Determine specific duty description
        role_lower = f"{designation} {profile}".lower()
        if any(k in role_lower for k in ["data entry", "deo", "computer", "typist"]):
            canonical_desig = "Data Entry Operator (DEO)"
            duty_sum = "Computer Data Entry & Records Management"
            duty_desc = "Data entry into government portals, office record keeping, document scanning & desk support."
        elif any(k in role_lower for k in ["khansama", "cook", "chef", "kitchen", "cater"]):
            canonical_desig = "Khansama / Cook"
            duty_sum = "Meal Preparation, Kitchen Management & Cooking"
            duty_desc = "Hygienic cooking, pantry service, meal preparation and kitchen cleanliness."
        elif any(k in role_lower for k in ["safai", "sweeper", "clean", "sanitation", "housekeep"]):
            canonical_desig = "Safaiwala / Sanitation Worker"
            duty_sum = "Premises Cleaning, Sweeping & Waste Disposal"
            duty_desc = "Daily sweeping, wet mopping, waste disposal and facility sanitization."
        elif any(k in role_lower for k in ["mali", "gardener", "gardner", "horticulture"]):
            canonical_desig = "Mali / Gardener"
            duty_sum = "Lawn Mowing, Gardening & Plantation Upkeep"
            duty_desc = "Gardening, lawn maintenance, tree trimming, soil fertilization and daily lawn watering."
        elif any(k in role_lower for k in ["security", "guard", "watchman"]):
            canonical_desig = "Security Guard"
            duty_sum = "Watch & Ward / 24x7 Premises Security"
            duty_desc = "24x7 premises guarding, access control, visitor logbook checking and night patrolling."
        elif any(k in role_lower for k in ["driver", "chauffeur"]):
            canonical_desig = "Driver / Chauffeur"
            duty_sum = "Official Vehicle Driving & Logbook Maintenance"
            duty_desc = "Safe driving of departmental light motor vehicles (LMV), routine maintenance and logbook upkeep."
        elif any(k in role_lower for k in ["electrician", "wireman"]):
            canonical_desig = "Electrician / Wireman"
            duty_sum = "Electrical Wiring & Equipment Maintenance"
            duty_desc = "Routine electrical maintenance, wiring inspection, panel checking and equipment troubleshooting."
        elif any(k in role_lower for k in ["plumber"]):
            canonical_desig = "Plumber / Pipe Fitter"
            duty_sum = "Sanitary Pipelines & Water Supply Upkeep"
            duty_desc = "Pipeline maintenance, tap repairs, drainage clearance and water line upkeep."
        elif any(k in role_lower for k in ["mts", "peon", "helper", "office boy"]):
            canonical_desig = "Multi-Tasking Staff (MTS) / Peon"
            duty_sum = "Office Maintenance & Document Dispatch"
            duty_desc = "Physical movement of office files, tea/water service for meetings and desk support."
        else:
            canonical_desig = designation
            duty_sum = "Operational Support & Deliverables"
            duty_desc = "Execution of operational tasks and contractual deliverables as specified by the buyer."

        extracted_roles.append({
            "schedule_no": idx + 1,
            "designation": designation,
            "canonical_designation": canonical_desig,
            "profile": profile,
            "quantity": qty,
            "skill_category": skill,
            "educational_qualification": edu,
            "type_of_function": func,
            "duty_summary": duty_sum,
            "duty": duty_desc
        })

print("Extracted Multi-Role Staff Breakdown:")
print(json.dumps(extracted_roles, indent=2))
print("Total Staff Count:", sum(r["quantity"] for r in extracted_roles))
