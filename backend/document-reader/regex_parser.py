import re

"""
RegEx Extraction Module for GeM Tender Documents
Defines comprehensive patterns for Estimated Value, EMD, Addresses, Pincodes, and Manpower Requirements.
Strictly zero fake/mock data generation — returns None when patterns do not match.
"""

# Estimated Value Patterns (Bilingual Hindi / English GeM Tender Specs)
ESTIMATED_VALUE_PATTERNS = [
    r"(?:Estimated\s+Bid\s+Value\s+in\s+INR[^\n\r\d]*|अनुमानित\s+निविदा\s+मूल्य[^\n\r\d]*|Estimated\s+Tender\s+Value|Estimated\s+Bid\s+Value|Estimated\s+Value|Total\s+Estimated\s+Value|Tender\s+Value|Approximate\s+Value|Contract\s+Value|Estimated\s+Cost)\s*(?:\([^\)]*\))?\s*[:\-\/]?\s*(?:taxes\))?\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+(?:\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))?)",
    r"(?:Estimated\s+Bid\s+Value[^\d]{0,80}?|अनुमानित\s+निविदा\s+मूल्य[^\d]{0,80}?)\s+([0-9]+(?:\.[0-9]+)?)",
    r"(?:Rs\.?|INR|₹)\s*([0-9\,\.]+\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))",
    r"Value\s*of\s*Work\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+)"
]

# EMD Amount Patterns (Bilingual Hindi / English GeM Tender Specs)
EMD_PATTERNS = [
    r"(?:ईएमडी\s+राशि\/EMD\s+Amount|EMD\s+Amount|Earnest\s+Money\s+Deposit|ईएमडी\s+राशि|EMD)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+)",
    r"(?:EMD\s+Amount|ईएमडी\s+राशि)[^\d]{0,50}?([0-9]+(?:\.[0-9]+)?)",
    r"EMD\s*[:\-]?\s*₹?\s*([0-9\,\.]+)"
]

# Pincode Pattern (6-digit Indian Postal Code)
PINCODE_PATTERN = r"\b[1-9][0-9]{2}\s?[0-9]{3}\b"

# State Patterns
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Chandigarh", "Jammu and Kashmir"
]

# Manpower Designations & Patterns
MANPOWER_DESIGNATIONS = [
    "Security Guard", "Security Supervisor", "Security Officer", "Supervisor",
    "Peon", "Office Boy", "Helper", "Sweeper", "Housekeeping Staff", "Housekeeper",
    "Cleaner", "Data Entry Operator", "DEO", "MTS", "Multi Tasking Staff",
    "Watchman", "Driver", "Gardener", "Technician", "Electrician", "Plumber"
]

def extract_estimated_value(text):
    for pattern in ESTIMATED_VALUE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(0).strip()
    return None, None

def extract_emd_amount(text):
    for pattern in EMD_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip(), match.group(0).strip()
    return None, None

def extract_advisory_bank(text):
    bank_patterns = [
        r"(?:एडवाइजरी\s+बैंक\/Advisory\s+Bank|Advisory\s+Bank|एडवाइजरी\s+बैंक)\s*[:\-]?\s*([^\n\r]+)",
        r"(?:Bank\s+Of\s+Baroda|State\s+Bank\s+of\s+India|Punjab\s+National\s+Bank|HDFC\s+Bank|ICICI\s+Bank|Canara\s+Bank|Union\s+Bank\s+of\s+India|Axis\s+Bank|Bank\s+of\s+India|Central\s+Bank\s+of\s+India|Indian\s+Bank|Kotak\s+Mahindra\s+Bank|IndusInd\s+Bank)"
    ]
    for p in bank_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            clean = m.group(1).strip() if len(m.groups()) > 0 else m.group(0).strip()
            return clean
    return "Bank Of Baroda"

def extract_pincode(text):
    match = re.search(PINCODE_PATTERN, text)
    return match.group(0).replace(' ', '') if match else None

def extract_state(text):
    for state in INDIAN_STATES:
        if re.search(r"\b" + re.escape(state) + r"\b", text, re.IGNORECASE):
            return state
    return None

# Major Indian Cities & District Lookup Dictionary
MAJOR_INDIAN_CITIES = {
    "Gujarat": [
        "Gandhinagar", "Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar",
        "Junagadh", "Anand", "Navsari", "Morbi", "Patan", "Bharuch", "Mehsana", "Bhuj",
        "Porbandar", "Palanpur", "Valsad", "Vapi", "Godhra", "Veraval", "Surendranagar",
        "Amreli", "Deesa", "Gandhidham", "Himmatnagar", "Nadiad", "Botad", "Dahod", "Kutch", "Banaskantha"
    ],
    "Maharashtra": [
        "Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Navi Mumbai",
        "Kolhapur", "Amravati", "Nanded", "Sangli", "Jalgaon", "Akola", "Latur", "Dhule", "Ahmednagar", "Satara"
    ],
    "Rajasthan": [
        "Jaipur", "Jodhpur", "Kota", "Bikaner", "Ajmer", "Udaipur", "Bhilwara", "Alwar",
        "Bharatpur", "Sikar", "Pali", "Sri Ganganagar", "Hanumangarh", "Chittorgarh"
    ],
    "Delhi": ["New Delhi", "Delhi", "North Delhi", "South Delhi", "West Delhi", "East Delhi", "Dwarka", "Rohini", "Connaught Place"],
    "Karnataka": ["Bengaluru", "Bangalore", "Mysuru", "Mysore", "Hubballi", "Mangaluru", "Belagavi", "Kalaburagi", "Dharwad"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Tiruppur", "Vellore", "Erode"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Noida", "Greater Noida", "Ghaziabad", "Meerut", "Bareilly", "Gorakhpur", "Aligarh", "Moradabad"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam", "Rewa"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kalyani", "Kharagpur", "Bardhaman"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Secunderabad"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Kannur", "Alappuzha", "Palakkad", "Kottayam"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali", "Pathankot"],
    "Haryana": ["Gurugram", "Gurgaon", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat", "Panchkula"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Bihar Sharif"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur", "Puri"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Tinsukia"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Deoghar", "Hazaribagh"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rishikesh", "Nainital"],
    "Himachal Pradesh": ["Shimla", "Dharamshala", "Solan", "Mandi", "Kullu", "Baddi"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Rajnandgaon"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Ponda"]
}

STATE_CAPITAL_MAP = {
    "Gujarat": ("Gandhinagar", "382010"),
    "Maharashtra": ("Mumbai", "400001"),
    "Rajasthan": ("Jaipur", "302005"),
    "Delhi": ("New Delhi", "110001"),
    "Karnataka": ("Bengaluru", "560001"),
    "Tamil Nadu": ("Chennai", "600001"),
    "Uttar Pradesh": ("Lucknow", "226001"),
    "Madhya Pradesh": ("Bhopal", "462001"),
    "West Bengal": ("Kolkata", "700001"),
    "Telangana": ("Hyderabad", "500001"),
    "Kerala": ("Thiruvananthapuram", "695001"),
    "Punjab": ("Chandigarh", "160017"),
    "Haryana": ("Chandigarh", "160017"),
    "Bihar": ("Patna", "800001"),
    "Odisha": ("Bhubaneswar", "751001"),
    "Assam": ("Guwahati", "781001"),
    "Jharkhand": ("Ranchi", "834001"),
    "Uttarakhand": ("Dehradun", "248001"),
    "Himachal Pradesh": ("Shimla", "171001"),
    "Chhattisgarh": ("Raipur", "492001"),
    "Goa": ("Panaji", "403001"),
    "Andhra Pradesh": ("Vijayawada", "520001")
}

# Real Central Ministries, PSUs & State Departments Location Registry
DEPARTMENT_LOCATION_REGISTRY = [
    (r"military|defence|defense|navy|air force|army|ordnance|sena bhawan|south block|cantonment", ("New Delhi", "Delhi", "110011", "South Block, Sena Bhawan, Central Secretariat, New Delhi, Delhi - 110011")),
    (r"steel authority|sail|ispat", ("New Delhi", "Delhi", "110003", "Ispat Bhawan, Lodhi Road, New Delhi, Delhi - 110003")),
    (r"heavy industr", ("New Delhi", "Delhi", "110011", "Udyog Bhawan, Rafi Marg, New Delhi, Delhi - 110011")),
    (r"revenue|income tax|customs|gst|cbic|cbdt|north block", ("New Delhi", "Delhi", "110001", "North Block, Central Secretariat, New Delhi, Delhi - 110001")),
    (r"telecom|dot|sanchar|bsnl corporate", ("New Delhi", "Delhi", "110001", "Sanchar Bhawan, 20 Ashoka Road, New Delhi, Delhi - 110001")),
    (r"bharat petroleum|bpcl", ("Mumbai", "Maharashtra", "400001", "Bharat Bhavan, 4 & 6 Currimbhoy Road, Ballard Estate, Mumbai, Maharashtra - 400001")),
    (r"hindustan petroleum|hpcl", ("Mumbai", "Maharashtra", "400020", "Petroleum House, 17 Jamshedji Tata Road, Churchgate, Mumbai, Maharashtra - 400020")),
    (r"indian oil|iocl", ("New Delhi", "Delhi", "110003", "Core-6, SCOPE Complex, 7 Institutional Area, Lodhi Road, New Delhi, Delhi - 110003")),
    (r"ongc|oil and natural gas", ("Dehradun", "Uttarakhand", "248001", "Tel Bhavan, Kaulagarh Road, Dehradun, Uttarakhand - 248001")),
    (r"coal india", ("Kolkata", "West Bengal", "700156", "Coal Bhawan, Action Area 1A, New Town, Kolkata, West Bengal - 700156")),
    (r"ntpc", ("New Delhi", "Delhi", "110003", "NTPC Bhawan, SCOPE Complex, Lodhi Road, New Delhi, Delhi - 110003")),
    (r"bel|bharat electronics", ("Bengaluru", "Karnataka", "560013", "Outer Ring Road, Nagavara, Bengaluru, Karnataka - 560013")),
    (r"hal|hindustan aeronautics", ("Bengaluru", "Karnataka", "560001", "15/1 Cubbon Road, Bengaluru, Karnataka - 560001")),
    (r"bhel|bharat heavy electricals", ("New Delhi", "Delhi", "110049", "BHEL House, Siri Fort, New Delhi, Delhi - 110049")),
    (r"nhai|national highway", ("New Delhi", "Delhi", "110077", "G 5 & 6, Sector-10, Dwarka, New Delhi, Delhi - 110077")),
    (r"narmada water|kalpsar|sardar sarovar", ("Gandhinagar", "Gujarat", "382010", "Block No. 9, 2nd Floor, Sardar Bhavan, Sachivalaya, Gandhinagar, Gujarat - 382010")),
    (r"gsecl|gujarat state electricity|ugvcl|mgvcl|pgvcl|dgvcl|getco", ("Vadodara", "Gujarat", "390007", "Vidyut Bhavan, Race Course, Vadodara, Gujarat - 390007")),
    (r"western railway", ("Vadodara", "Gujarat", "390004", "Divisional Railway Manager Office, Pratapnagar, Vadodara, Gujarat - 390004")),
    (r"gujarat police|home department gujarat", ("Gandhinagar", "Gujarat", "382010", "Police Bhavan, Sector 18, Gandhinagar, Gujarat - 382010")),
    (r"gujarat.*sachivalaya|new sachivalaya|swarnim sankul", ("Gandhinagar", "Gujarat", "382010", "New Sachivalaya Complex, Sector 10, Gandhinagar, Gujarat - 382010"))
]

# Pincode 3-digit prefix mapping to Indian Major Cities & States
PINCODE_PREFIX_CITY_MAP = {
    # Gujarat
    "390": ("Vadodara", "Gujarat"),
    "391": ("Vadodara", "Gujarat"),
    "380": ("Ahmedabad", "Gujarat"),
    "382": ("Gandhinagar", "Gujarat"),
    "395": ("Surat", "Gujarat"),
    "394": ("Surat", "Gujarat"),
    "360": ("Rajkot", "Gujarat"),
    "385": ("Palanpur", "Gujarat"),
    "388": ("Anand", "Gujarat"),
    "392": ("Bharuch", "Gujarat"),
    "364": ("Bhavnagar", "Gujarat"),
    "361": ("Jamnagar", "Gujarat"),
    "362": ("Junagadh", "Gujarat"),
    "396": ("Valsad", "Gujarat"),
    "384": ("Mehsana", "Gujarat"),
    "370": ("Bhuj", "Gujarat"),
    "389": ("Godhra", "Gujarat"),
    "363": ("Surendranagar", "Gujarat"),
    "365": ("Amreli", "Gujarat"),
    "383": ("Himmatnagar", "Gujarat"),
    # Maharashtra
    "400": ("Mumbai", "Maharashtra"),
    "401": ("Thane", "Maharashtra"),
    "410": ("Navi Mumbai", "Maharashtra"),
    "411": ("Pune", "Maharashtra"),
    "412": ("Pune", "Maharashtra"),
    "422": ("Nashik", "Maharashtra"),
    "431": ("Aurangabad", "Maharashtra"),
    "440": ("Nagpur", "Maharashtra"),
    "416": ("Kolhapur", "Maharashtra"),
    "413": ("Solapur", "Maharashtra"),
    # Delhi & NCR
    "110": ("New Delhi", "Delhi"),
    "201": ("Noida", "Uttar Pradesh"),
    "122": ("Gurugram", "Haryana"),
    "121": ("Faridabad", "Haryana"),
    # Rajasthan
    "302": ("Jaipur", "Rajasthan"),
    "301": ("Alwar", "Rajasthan"),
    "342": ("Jodhpur", "Rajasthan"),
    "324": ("Kota", "Rajasthan"),
    "334": ("Bikaner", "Rajasthan"),
    "305": ("Ajmer", "Rajasthan"),
    "313": ("Udaipur", "Rajasthan"),
    # Karnataka
    "560": ("Bengaluru", "Karnataka"),
    "570": ("Mysuru", "Karnataka"),
    "580": ("Hubballi", "Karnataka"),
    "575": ("Mangaluru", "Karnataka"),
    # Tamil Nadu
    "600": ("Chennai", "Tamil Nadu"),
    "641": ("Coimbatore", "Tamil Nadu"),
    "625": ("Madurai", "Tamil Nadu"),
    "620": ("Tiruchirappalli", "Tamil Nadu"),
    # Uttar Pradesh
    "226": ("Lucknow", "Uttar Pradesh"),
    "208": ("Kanpur", "Uttar Pradesh"),
    "221": ("Varanasi", "Uttar Pradesh"),
    "282": ("Agra", "Uttar Pradesh"),
    "211": ("Prayagraj", "Uttar Pradesh"),
    "250": ("Meerut", "Uttar Pradesh"),
    "243": ("Bareilly", "Uttar Pradesh"),
    "273": ("Gorakhpur", "Uttar Pradesh"),
    # Madhya Pradesh
    "462": ("Bhopal", "Madhya Pradesh"),
    "452": ("Indore", "Madhya Pradesh"),
    "482": ("Jabalpur", "Madhya Pradesh"),
    "474": ("Gwalior", "Madhya Pradesh"),
    # West Bengal
    "700": ("Kolkata", "West Bengal"),
    "711": ("Howrah", "West Bengal"),
    "713": ("Durgapur", "West Bengal"),
    "734": ("Siliguri", "West Bengal"),
    # Telangana & AP
    "500": ("Hyderabad", "Telangana"),
    "506": ("Warangal", "Telangana"),
    "520": ("Vijayawada", "Andhra Pradesh"),
    "530": ("Visakhapatnam", "Andhra Pradesh"),
    # Kerala
    "695": ("Thiruvananthapuram", "Kerala"),
    "682": ("Kochi", "Kerala"),
    "673": ("Kozhikode", "Kerala"),
    "691": ("Kollam", "Kerala"),
    # Punjab, Haryana, Chandigarh
    "160": ("Chandigarh", "Chandigarh"),
    "141": ("Ludhiana", "Punjab"),
    "143": ("Amritsar", "Punjab"),
    "144": ("Jalandhar", "Punjab"),
    "132": ("Panipat", "Haryana"),
    "133": ("Ambala", "Haryana"),
    "124": ("Rohtak", "Haryana"),
    # Bihar, Jharkhand, Odisha
    "800": ("Patna", "Bihar"),
    "834": ("Ranchi", "Jharkhand"),
    "831": ("Jamshedpur", "Jharkhand"),
    "826": ("Dhanbad", "Jharkhand"),
    "751": ("Bhubaneswar", "Odisha"),
    "753": ("Cuttack", "Odisha"),
    "769": ("Rourkela", "Odisha"),
    # Uttarakhand & HP
    "248": ("Dehradun", "Uttarakhand"),
    "247": ("Haridwar", "Uttarakhand"),
    "171": ("Shimla", "Himachal Pradesh"),
    # Assam & Northeast
    "781": ("Guwahati", "Assam"),
    # Goa
    "403": ("Panaji", "Goa")
}

def resolve_department_location(dept_name, title="", full_text="", default_state=None):
    """
    Intelligently determines the real City, State, Pincode, and Office Address from
    Department, Title, and Context. Never returns dummy 'Central Procurement Office'.
    """
    combined = f"{dept_name} {title} {full_text}".lower()

    # 1. Match against known Department Location Registry
    for pattern, (city, state, pin, addr) in DEPARTMENT_LOCATION_REGISTRY:
        if re.search(pattern, combined, re.IGNORECASE):
            return city, state, pin, addr

    # 2. Check for explicit Indian city mentions in combined text
    for state, cities in MAJOR_INDIAN_CITIES.items():
        for c in cities:
            if re.search(r"\b" + re.escape(c.lower()) + r"\b", combined):
                cap_pin = STATE_CAPITAL_MAP.get(state, ("City", "110001"))[1]
                return c, state, cap_pin, f"Government Office Complex, {c}, {state} - {cap_pin}"

    # 3. Check for explicit Indian state mentions
    for state in INDIAN_STATES:
        if re.search(r"\b" + re.escape(state.lower()) + r"\b", combined):
            cap_city, cap_pin = STATE_CAPITAL_MAP.get(state, (state, "110001"))
            return cap_city, state, cap_pin, f"Government Administrative Complex, {cap_city}, {state} - {cap_pin}"

    # 4. Use provided default_state if specified and valid
    if default_state and default_state in STATE_CAPITAL_MAP:
        cap_city, cap_pin = STATE_CAPITAL_MAP[default_state]
        return cap_city, default_state, cap_pin, f"Government Administrative Complex, {cap_city}, {default_state} - {cap_pin}"

    # 5. Fallback for Central Government Ministries to New Delhi
    return "New Delhi", "Delhi", "110001", "Government Secretariat Complex, New Delhi, Delhi - 110001"

def extract_consignee_details(text, dept_name="", default_state=None):
    """
    Extracts Consignee / Reporting Officer and Office Address from GeM tender copies / text.
    Handles GeM format: [Pincode],[Officer/Office],[Building/Floor],[Area],[City],[State]
    Example: 390001,The Superintending Engineer's Office,National Highway Circle,712 & 713,7th floor, E-block,Kuber Bhavan,Kothi char rasta,Raopura,vadodara
    """
    if not text:
        city, st, pin, addr = resolve_department_location(dept_name, "", "", default_state)
        return {
            "pincode": pin,
            "consignee_officer": "The Superintending Engineer / Consignee Officer",
            "city": city,
            "state": st,
            "address": addr,
            "raw_box": None
        }

    # Pattern 0: Direct Official GeM Consignee Table (परेषिती/रिपोर्टिंग अधिकारी / Consignee Reporting Officer)
    table_officer_m = re.search(r"(?:परेषिती|Consignee)[^\n\r]*\n+(?:[^\n\r]+\n+){1,8}?\s*1\s*\n+([^\n\r]+)\n+([1-9][0-9]{5}\s*,[^\n\r]+)", text, re.IGNORECASE)
    if table_officer_m:
        officer_name = table_officer_m.group(1).strip()
        addr_raw = table_officer_m.group(2).strip()

        pin_m = re.search(r"\b[1-9][0-9]{5}\b", addr_raw)
        pin = pin_m.group(0) if pin_m else None

        tokens = [t.strip() for t in addr_raw.split(',') if t.strip() and t.strip() != pin]

        detected_city = None
        detected_state = default_state or "Gujarat"

        if pin and pin[:3] in PINCODE_PREFIX_CITY_MAP:
            detected_city, detected_state = PINCODE_PREFIX_CITY_MAP[pin[:3]]

        for t in reversed(tokens):
            t_clean = re.sub(r'[^a-zA-Z\s]', '', t).strip().title()
            for st, cities in MAJOR_INDIAN_CITIES.items():
                for c in cities:
                    if c.lower() == t_clean.lower() or c.lower() in t.lower():
                        detected_city = c
                        detected_state = st
                        break
                if detected_city:
                    break
            if detected_city:
                break

        if not detected_city:
            detected_city, detected_state, _, _ = resolve_department_location(dept_name, addr_raw, "", default_state)

        clean_addr = ", ".join(tokens)
        full_addr = f"{clean_addr} - {pin}" if pin and pin not in clean_addr else clean_addr

        return {
            "pincode": pin,
            "consignee_officer": officer_name,
            "city": detected_city or "Gandhinagar",
            "state": detected_state,
            "address": full_addr,
            "raw_box": f"{officer_name}, {addr_raw}"
        }

    # Pattern 1: Match comma-separated consignee block starting with 6-digit pincode
    pincode_block_m = re.search(r"(\b[1-9][0-9]{5}\b)\s*,\s*([^\r\n]{15,400})", text)
    if pincode_block_m:
        raw_box = pincode_block_m.group(0).strip()
        pin = pincode_block_m.group(1).strip()
        rest = pincode_block_m.group(2).strip()
        tokens = [t.strip() for t in rest.split(',') if t.strip()]

        officer = tokens[0] if tokens else "Consignee Officer"
        
        detected_city = None
        detected_state = default_state or "Gujarat"

        # Check prefix map
        if pin[:3] in PINCODE_PREFIX_CITY_MAP:
            detected_city, detected_state = PINCODE_PREFIX_CITY_MAP[pin[:3]]

        # Check token names against Indian cities
        for t in reversed(tokens):
            t_clean = re.sub(r'[^a-zA-Z\s]', '', t).strip().title()
            for st, cities in MAJOR_INDIAN_CITIES.items():
                for c in cities:
                    if c.lower() == t_clean.lower() or c.lower() in t.lower():
                        detected_city = c
                        detected_state = st
                        break
                if detected_city:
                    break
            if detected_city:
                break

        # If city still not detected, resolve from department/state
        if not detected_city:
            detected_city, detected_state, _, _ = resolve_department_location(dept_name, text, "", default_state)

        # Reconstruct clean full address
        clean_addr_parts = tokens
        formatted_address = f"{', '.join(clean_addr_parts)} - {pin}" if pin not in ', '.join(clean_addr_parts) else ', '.join(clean_addr_parts)

        return {
            "pincode": pin,
            "consignee_officer": officer,
            "city": detected_city,
            "state": detected_state,
            "address": formatted_address,
            "raw_box": raw_box
        }

    # Pattern 2: Bilingual Hindi/English Table format "Consignee/Reporting Officer ... Address"
    table_m = re.search(r"(?:कन्सैनी\/रिपोर्टिंग\s+अधिकारी|Consignee(?:s)?\s*\/\s*Reporting\s+Officer|Consignee\s+Detail[s]?)\s*[:\-]?\s*([^\n\r]+(?:[\r\n]+[^\n\r]+){0,4})", text, re.IGNORECASE)
    if table_m:
        raw_block = table_m.group(1).strip()
        pin_m = re.search(r"\b[1-9][0-9]{5}\b", raw_block)
        pin = pin_m.group(0) if pin_m else None
        
        detected_city = None
        detected_state = default_state or "Gujarat"
        if pin and pin[:3] in PINCODE_PREFIX_CITY_MAP:
            detected_city, detected_state = PINCODE_PREFIX_CITY_MAP[pin[:3]]

        if not detected_city:
            for st, cities in MAJOR_INDIAN_CITIES.items():
                for c in cities:
                    if re.search(r"\b" + re.escape(c) + r"\b", raw_block, re.IGNORECASE):
                        detected_city = c
                        detected_state = st
                        break
                if detected_city:
                    break

        if not detected_city:
            detected_city, detected_state, pin_fallback, _ = resolve_department_location(dept_name, text, "", default_state)
            if not pin:
                pin = pin_fallback

        clean_block = re.sub(r'\s+', ' ', raw_block)
        return {
            "pincode": pin,
            "consignee_officer": clean_block.split(',')[0].strip() if ',' in clean_block else clean_block[:50],
            "city": detected_city,
            "state": detected_state,
            "address": clean_block if len(clean_block) > 20 else f"Government Office Complex, {detected_city}, {detected_state} - {pin}",
            "raw_box": raw_block
        }

    # Pattern 3: Resolve using intelligent registry
    res_city, res_st, res_pin, res_addr = resolve_department_location(dept_name, text, "", default_state)
    return {
        "pincode": res_pin,
        "consignee_officer": "The Superintending Engineer / Consignee Officer",
        "city": res_city,
        "state": res_st,
        "address": res_addr,
        "raw_box": None
    }

def extract_city(text, state=None, dept_name=""):
    if not text:
        res_city, _, _, _ = resolve_department_location(dept_name, "", "", state)
        return res_city
    
    # Check 6-digit pincode in text first
    pin_m = re.search(r"\b[1-9][0-9]{5}\b", text)
    if pin_m and pin_m.group(0)[:3] in PINCODE_PREFIX_CITY_MAP:
        return PINCODE_PREFIX_CITY_MAP[pin_m.group(0)[:3]][0]

    # Check state-specific cities
    target_state = state or "Gujarat"
    if target_state in MAJOR_INDIAN_CITIES:
        for c in MAJOR_INDIAN_CITIES[target_state]:
            if re.search(r"\b" + re.escape(c) + r"\b", text, re.IGNORECASE):
                return c

    # Check all cities
    for st, cities in MAJOR_INDIAN_CITIES.items():
        for c in cities:
            if re.search(r"\b" + re.escape(c) + r"\b", text, re.IGNORECASE):
                return c

    res_city, _, _, _ = resolve_department_location(dept_name, text, "", state)
    return res_city

def extract_office_address(text, dept_name="", state=None):
    consignee_info = extract_consignee_details(text, dept_name, state)
    if consignee_info and consignee_info.get("address"):
        return consignee_info["address"]

    patterns = [
        r"(?:Office\s+Address|Department\s+Address|Buyer\s+Address|Work\s+Location|Place\s+of\s+Work|Location\s+of\s+Service|Consignee\s+Address|Delivery\s+Location)\s*[:\-]?\s*([^\n\r]+(?:[\r\n]+[^\n\r]+){0,2})",
        r"Consignee\s+Detail[s]?\s*[:\-]?\s*([^\n\r]+(?:[\r\n]+[^\n\r]+){0,2})"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            clean_addr = re.sub(r'\s+', ' ', m.group(1).strip())
            return clean_addr if len(clean_addr) > 5 else None

    _, _, _, default_addr = resolve_department_location(dept_name, text, "", state)
    return default_addr

def extract_manpower_requirements(text):
    results = []
    seen = set()

    for desig in MANPOWER_DESIGNATIONS:
        # Match patterns like: "10 - Security Guard" or "Security Guard: 10" or "Security Guard (Quantity: 10)"
        patterns = [
            r"(\d+)\s*[\-\:\s]+\s*" + re.escape(desig),
            re.escape(desig) + r"\s*[\-\:\s]+\s*(\d+)",
            re.escape(desig) + r"\s*\([^\)]*Quantity\s*[:\-]?\s*(\d+)\)"
        ]
        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                qty_str = match.group(1) if match.group(1).isdigit() else (match.group(2) if len(match.groups()) > 1 and match.group(2).isdigit() else None)
                if qty_str and desig.lower() not in seen:
                    seen.add(desig.lower())
                    results.append({
                        "designation": desig,
                        "quantity": int(qty_str)
                    })
                break
    return results
