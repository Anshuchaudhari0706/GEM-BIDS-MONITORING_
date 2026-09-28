import re

"""
Table & Specification Parser Module for GeM Tender Documents
Extracts:
1. विवरण/ Specification | मूल्य/ Values (कोर / Core)
2. संसाधनों की मात्रा / Number of Resources to be hired & अतिरिक्त आवश्यकता / Additional Requirement
"""

CANONICAL_GEM_PROFILES = [
    (r"security\s+guard\s*(?:\(without\s+arms\)|without\s+arms)", "Security Guard (Without Arms)"),
    (r"security\s+guard\s*(?:\(with\s+arms\)|with\s+arms|armed)", "Security Guard (With Arms)"),
    (r"security\s+supervisor", "Security Supervisor"),
    (r"security\s+officer", "Security Officer"),
    (r"security\s+guard|watchman|gate\s+guard", "Security Guard"),
    (r"fire\s*safety\s*guard|fireman|fire\s+fighter", "Fire Safety Guard / Fireman"),
    (r"sanitation\s+supervisor|housekeeping\s+supervisor", "Sanitation / Housekeeping Supervisor"),
    (r"sanitation\s+worker|safai\s*karamchari|safai\s*karmi|safai\s*karmachari", "Sanitation Worker / Safai Karamchari"),
    (r"housekeeper|housekeeping\s+staff|house\s*keeping|cleaning\s+staff|cleaner", "Housekeeping Staff / Cleaner"),
    (r"sweeper", "Sweeper"),
    (r"data\s+entry\s+operator|deo\b|computer\s+operator|data\s+entry", "Data Entry Operator (DEO)"),
    (r"multi\s*tasking\s*staff|mts\b|office\s+peon|peon|office\s+boy|office\s+attendant", "Multi Tasking Staff (MTS)"),
    (r"office\s+assistant|lower\s+division\s+clerk|ldc\b|udc\b|clerk", "Office Assistant / Clerk"),
    (r"accountant|account\s+assistant|accounts\s+executive", "Accountant / Account Assistant"),
    (r"store\s+keeper|warehouse\s+assistant|material\s+handler", "Store Keeper / Material Handler"),
    (r"electrician|wireman|electrical\s+technician", "Electrician / Wireman"),
    (r"plumber|pipe\s+fitter", "Plumber"),
    (r"carpenter", "Carpenter"),
    (r"painter", "Painter"),
    (r"mason", "Mason"),
    (r"lift\s+operator", "Lift Operator"),
    (r"dg\s+operator|generator\s+operator|pump\s+operator", "DG Set / Pump Operator"),
    (r"technician|mechanic", "Technician / Mechanic"),
    (r"driver\s*(?:\(lmv\s*\/\s*hmv\)|lmv\s*\/\s*hmv)?|chauffeur|ambulance\s+driver|vehicle\s+driver", "Driver (LMV / HMV)"),
    (r"gardener|mali\b|horticulture\s+worker|horticulture\s+staff", "Gardener / Mali"),
    (r"cook|chef|kitchen\s+helper|catering\s+staff", "Cook / Catering Staff"),
    (r"staff\s+nurse|nurse\b", "Staff Nurse"),
    (r"nursing\s+assistant|hospital\s+attendant|ward\s+boy|aya\b", "Nursing Assistant / Hospital Attendant"),
    (r"pharmacist", "Pharmacist"),
    (r"lab\s+technician|laboratory\s+assistant", "Lab Technician")
]

def clean_extracted_profile(raw_val):
    if not raw_val:
        return None
    val = re.sub(r'^[\|\:\-\s\.\,]+|[\|\:\-\s\.\,]+$', '', raw_val).strip()
    cut_tokens = [
        "Specialization", "विशेषज्ञता", "Educational Qualification", "शैक्षिक योग्यता",
        "Type of Function", "कार्य का प्रकार", "Core", "कोर", "Post Graduation", "स्नातकोत्तर",
        "Experience", "अनुभव", "District", "Zipcode", "State", "मूल्य", "Values", "Specification", "विवरण"
    ]
    for tok in cut_tokens:
        tok_idx = val.lower().find(tok.lower())
        if tok_idx > 0:
            val = val[:tok_idx].strip()
    val = re.sub(r'^[\|\:\-\s\.\,]+|[\|\:\-\s\.\,]+$', '', val).strip()
    return val if len(val) >= 2 else None

def extract_list_of_profiles(raw_text, tender_title="", tender_category=""):
    """
    Precisely extracts the 'List of Profiles' field from GeM Tender Documents,
    Core Specifications tables, SOR, or Service definitions.
    """
    text = raw_text or ""
    combined_context = f"{text} {tender_title} {tender_category}".lower()

    # 1. Direct Regex Match from Table Row / Specification Section
    direct_patterns = [
        r"(?:List\s+of\s+Profiles|प्रोफाइल\s*की\s*सूची)\s*[:\|\-]?\s*([^\n\r\|]{2,80})",
        r"\|\s*(?:List\s+of\s+Profiles|प्रोफाइल\s*की\s*सूची)\s*\|\s*([^\|\n\r]{2,80})\|",
        r"(?:List\s+of\s+Profiles|प्रोफाइल\s*की\s*सूची)[\s\S]{0,40}?\n\s*([A-Za-z0-9\s\(\)\/\-\,\&]{3,80})",
        r"(?:Designation\s*of\s*Manpower|Profile\s*Name|Category\s*of\s*Manpower)\s*[:\|\-]?\s*([^\n\r\|]{2,80})"
    ]

    for p in direct_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            cand = clean_extracted_profile(m.group(1))
            if cand and not any(ign in cand.lower() for ign in ["not required", "not applicable", "others", "specification", "values"]):
                # Check canonical mapping first for clean standard designation
                for pat, canon in CANONICAL_GEM_PROFILES:
                    if re.search(pat, cand, re.IGNORECASE):
                        return canon
                return cand.title()

    # 2. Match from Canonical Profiles in context (title, category, text)
    for pat, canon in CANONICAL_GEM_PROFILES:
        if re.search(r"\b" + pat + r"\b", combined_context, re.IGNORECASE):
            return canon

    # 3. Contextual Keyword Fallbacks
    if any(k in combined_context for k in ["guard", "security", "watchman", "patrolling"]):
        return "Security Guard"
    elif any(k in combined_context for k in ["sanitation", "sweeper", "safai", "cleaning", "housekeeping"]):
        return "Sanitation Worker / Housekeeping Staff"
    elif any(k in combined_context for k in ["data entry", "deo", "computer operator", "typist"]):
        return "Data Entry Operator (DEO)"
    elif any(k in combined_context for k in ["driver", "chauffeur"]):
        return "Driver (LMV / HMV)"
    elif any(k in combined_context for k in ["mali", "gardener", "horticulture"]):
        return "Gardener / Mali"
    elif any(k in combined_context for k in ["mts", "peon", "attendant", "office boy"]):
        return "Multi Tasking Staff (MTS)"
    elif any(k in combined_context for k in ["electrician", "wireman"]):
        return "Electrician / Wireman"
    elif any(k in combined_context for k in ["plumber"]):
        return "Plumber"
    elif any(k in combined_context for k in ["nurse", "nursing", "healthcare", "hospital"]):
        return "Nursing Assistant / Hospital Attendant"
    elif any(k in combined_context for k in ["cook", "catering"]):
        return "Cook / Catering Staff"

    return "Security Guard"

def extract_tables_from_text(raw_text):
    rows = []
    lines = raw_text.split('\n')
    table_line_pattern = r"^(\d+)\s+([A-Za-z\s]+)\s+(\d+)\b"

    for line in lines:
        match = re.search(table_line_pattern, line.strip())
        if match:
            sr_no = match.group(1)
            desig = match.group(2).strip()
            qty = match.group(3)

            if len(desig) > 3 and qty.isdigit():
                rows.append({
                    "sr_no": int(sr_no),
                    "designation": desig,
                    "quantity": int(qty)
                })

    return rows

def extract_core_specifications(raw_text, tender_title="", tender_category="", tender_state="Gujarat"):
    """
    Parses the 'विवरण/ Specification | मूल्य/ Values' (कोर / Core) table from GeM PDF.
    """
    text = raw_text or ""
    combined_context = f"{text} {tender_title} {tender_category}".lower()

    # 1. Skill Category
    skill_m = re.search(r"(?:Skill\s+Category|कौशल\s*श्रेणी)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    if skill_m:
        skill_cat = skill_m.group(1).strip()
    else:
        if any(k in combined_context for k in ["highly skilled", "high skilled", "doctor", "specialist", "engineer"]):
            skill_cat = "Highly Skilled"
        elif any(k in combined_context for k in ["skilled", "driver", "electrician", "computer operator", "deo", "data entry", "nurse"]):
            skill_cat = "Skilled"
        elif any(k in combined_context for k in ["semi-skilled", "semi skilled", "security supervisor", "plumber", "painter", "mason"]):
            skill_cat = "Semi-Skilled"
        else:
            skill_cat = "Unskilled"

    # 2. Educational Qualification
    edu_m = re.search(r"(?:Educational\s+Qualification|शैक्षिक\s*योग्यता)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    if edu_m:
        edu_qual = edu_m.group(1).strip()
    else:
        if any(k in combined_context for k in ["graduate", "bachelor", "degree", "post graduate", "pg"]):
            edu_qual = "Graduate"
        elif any(k in combined_context for k in ["intermediate", "12th", "higher secondary", "hsc"]):
            edu_qual = "Higher Secondary"
        elif any(k in combined_context for k in ["secondary", "10th", "ssc", "matriculation", "high school"]):
            edu_qual = "Secondary School"
        elif any(k in combined_context for k in ["driver", "security guard", "sweeper", "safai", "cleaner"]):
            edu_qual = "Secondary School"
        else:
            edu_qual = "Secondary School"

    # 3. Type of Function
    func_m = re.search(r"(?:Type\s+of\s+Function|कार्य\s*का\s*प्रकार)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    if func_m:
        type_of_func = func_m.group(1).strip()
    else:
        if "security" in combined_context:
            type_of_func = "Security Operations / Watch & Ward"
        elif "cleaning" in combined_context or "sanitation" in combined_context or "housekeeping" in combined_context:
            type_of_func = "Sanitation & Facility Maintenance"
        elif "driver" in combined_context:
            type_of_func = "Transport & Fleet Operations"
        elif "data entry" in combined_context or "it" in combined_context:
            type_of_func = "Administrative & Computer Operations"
        else:
            type_of_func = "Others"

    # 4. List of Profiles / Designation (High Precision Extractor)
    profile_name = extract_list_of_profiles(raw_text, tender_title=tender_title, tender_category=tender_category)

    # 5. Experience
    exp_m = re.search(r"(?:Experience\s*\(years\)|Years\s+of\s+Past\s+Experience|Experience|अनुभव)\s*[:\-]?\s*([0-9\sto\-\+Years\(\)]+)", text, re.I)
    if exp_m and len(exp_m.group(1).strip()) > 0:
        exp_req = exp_m.group(1).strip()
    else:
        exp_req = "0 to 3 Years"

    # 6. Specialization & PG
    spec_m = re.search(r"(?:Specialization|विशेषज्ञता)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    specialization = spec_m.group(1).strip() if spec_m else "Not Required"

    pg_m = re.search(r"(?:Post\s+Graduation|स्नातकोत्तर)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    post_grad = pg_m.group(1).strip() if pg_m else "Not Required"

    pg_spec_m = re.search(r"(?:Specialization\s+for\s+PG|पीजी\s*के\s*लिए\s*विशेषज्ञता)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    spec_for_pg = pg_spec_m.group(1).strip() if pg_spec_m else "Not Applicable"

    # 7. Geographical Presence
    geo_pres_m = re.search(r"(?:Is\s+the\s+Geographical\s+presence.*?in\s+the\s+consignee.*?State|Geographical\s+presence\s+required)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    geo_presence = geo_pres_m.group(1).strip() if geo_pres_m else "Yes"
    if "no" in geo_presence.lower():
        geo_presence = "No"
    else:
        geo_presence = "Yes"

    geo_state_m = re.search(r"(?:Name\s+of\s+states\/\s*UT\s+for\s+geographical\s+presence.*?required|State.*?geographical\s+presence)\s*[:\-]?\s*([^\n\r\|]+)", text, re.I)
    geo_state = geo_state_m.group(1).strip() if geo_state_m else (tender_state or "Gujarat")

    return {
        "section_title": "कोर / Core",
        "skill_category": skill_cat,
        "educational_qualification": edu_qual,
        "type_of_function": type_of_func,
        "list_of_profiles": profile_name,
        "specialization": specialization,
        "post_graduation": post_grad,
        "specialization_for_pg": spec_for_pg,
        "experience": exp_req,
        "state": "NA",
        "zipcode": "NA",
        "district": "NA",
        "geographical_presence_required": geo_presence,
        "geographical_presence_state": geo_state
    }

def extract_wage_and_resource_breakdown(raw_text, resource_count=None, profile_name="Security Guard"):
    """
    Parses the 'संसाधनों की मात्रा / Number of Resources to be hired' &
    'अतिरिक्त आवश्यकता /Additional Requirement' table from GeM PDF.
    """
    text = raw_text or ""

    # 1. Number of Resources
    res_m = re.search(r"(?:Number\s+of\s+Resources\s+to\s+be\s+hired|संसाधनों\s*की\s*मात्रा)\s*[:\-]?\s*(\d+)", text, re.I)
    if res_m:
        num_resources = int(res_m.group(1))
    elif resource_count and int(resource_count) > 0:
        num_resources = int(resource_count)
    else:
        num_resources = 8

    # 2. Minimum daily wage (INR) exclusive of GST
    wage_m = re.search(r"(?:Minimum\s+daily\s+wage.*?exclusive\s+of\s+GST|दैनिक\s*मजदूरी)\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    if wage_m:
        min_daily_wage = float(wage_m.group(1))
    else:
        min_daily_wage = 512.50

    # 3. Bonus (INR per day)
    bonus_m = re.search(r"(?:Bonus\s*\(INR\s+per\s+day\)|बोनस)\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    if bonus_m:
        bonus_daily = float(bonus_m.group(1))
    else:
        bonus_daily = round(min_daily_wage * 0.0833, 2) if min_daily_wage > 0 else 42.69

    # 4. EDLI & EPF Admin Charge
    edli_m = re.search(r"(?:EDLI\s*\(INR\s+per\s+day\))\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    edli_daily = float(edli_m.group(1)) if edli_m else 0.0

    epf_adm_m = re.search(r"(?:EPF\s+Admin\s+Charge\s*\(INR\s+per\s+day\))\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    epf_admin_daily = float(epf_adm_m.group(1)) if epf_adm_m else 0.0

    # 5. Optional Allowances 1, 2, 3
    opt1_m = re.search(r"(?:Optional\s+Allowances\s+1\s*\(INR\s+per\s+day\))\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    opt1_daily = float(opt1_m.group(1)) if opt1_m else 0.0

    opt2_m = re.search(r"(?:Optional\s+Allowances\s+2\s*\(INR\s+per\s+day\))\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    opt2_daily = float(opt2_m.group(1)) if opt2_m else 0.0

    opt3_m = re.search(r"(?:Optional\s+Allowances\s+3\s*\(INR\s+per\s+day\))\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    opt3_daily = float(opt3_m.group(1)) if opt3_m else 0.0

    # 6. Overtime details
    ot_hrs_m = re.search(r"(?:Estimated\s+Number\s+of\s+Overtime\s+Hours.*?Month)\s*[:\-]?\s*(\d+)", text, re.I)
    ot_hours_monthly = int(ot_hrs_m.group(1)) if ot_hrs_m else 0

    ot_rate_m = re.search(r"(?:Remuneration\s+per\s+resource\s+per\s+hour\s+for\s+Overtime)\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    ot_rate_hourly = float(ot_rate_m.group(1)) if ot_rate_m else 0.0

    # 7. ESI & Provident Fund
    esi_m = re.search(r"(?:ESI\s*\(INR\s+per\s+day\)|ईएसआई)\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    if esi_m:
        esi_daily = float(esi_m.group(1))
    else:
        esi_daily = round(min_daily_wage * 0.0325, 2) if min_daily_wage > 0 else 16.66

    pf_m = re.search(r"(?:Provident\s+Fund\s*\(INR\s+per\s+day\)|भविष्य\s*निधि)\s*[:\-]?\s*([0-9\.]+)", text, re.I)
    if pf_m:
        pf_daily = float(pf_m.group(1))
    else:
        pf_daily = round(min_daily_wage * 0.13, 2) if min_daily_wage > 0 else 66.63

    # 8. Working Days & Duration
    days_m = re.search(r"(?:Number\s+of\s+working\s+days\s+in\s+a\s+month|कार्य\s*दिवस)\s*[:\-]?\s*(\d+)", text, re.I)
    working_days_month = int(days_m.group(1)) if days_m else 26

    tenure_m = re.search(r"(?:Tenure\/\s*Duration\s+of\s+Employment\s*\(in\s+months\)|रोजगार\s*की\s*अवधि)\s*[:\-]?\s*(\d+)", text, re.I)
    tenure_months = int(tenure_m.group(1)) if tenure_m else 11

    # Calculations
    daily_cost_per_resource = min_daily_wage + bonus_daily + edli_daily + epf_admin_daily + opt1_daily + opt2_daily + opt3_daily + esi_daily + pf_daily
    monthly_cost_per_resource = daily_cost_per_resource * working_days_month
    total_contract_estimate = monthly_cost_per_resource * num_resources * tenure_months

    return {
        "number_of_resources": num_resources,
        "minimum_daily_wage": min_daily_wage,
        "bonus_daily": bonus_daily,
        "edli_daily": edli_daily,
        "epf_admin_charge_daily": epf_admin_daily,
        "optional_allowances_1": opt1_daily,
        "optional_allowances_2": opt2_daily,
        "optional_allowances_3": opt3_daily,
        "overtime_hours_monthly": ot_hours_monthly,
        "overtime_rate_hourly": ot_rate_hourly,
        "esi_daily": esi_daily,
        "provident_fund_daily": pf_daily,
        "working_days_in_month": working_days_month,
        "tenure_duration_months": tenure_months,
        "daily_cost_per_resource": round(daily_cost_per_resource, 2),
        "monthly_cost_per_resource": round(monthly_cost_per_resource, 2),
        "total_contract_estimate": round(total_contract_estimate, 2)
    }
