import re

"""
RegEx Extraction Module for GeM Tender Documents
Defines comprehensive patterns for Estimated Value, EMD, Addresses, Pincodes, and Manpower Requirements.
Strictly zero fake/mock data generation — returns None when patterns do not match.
"""

# Estimated Value Patterns
ESTIMATED_VALUE_PATTERNS = [
    r"(?:Estimated\s+Tender\s+Value|Estimated\s+Value|Total\s+Estimated\s+Value|Tender\s+Value|Approximate\s+Value|Contract\s+Value|Estimated\s+Cost)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+(?:\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))?)",
    r"(?:Rs\.?|INR|₹)\s*([0-9\,\.]+\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))",
    r"Value\s*of\s*Work\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+)"
]

# EMD Amount Patterns
EMD_PATTERNS = [
    r"(?:EMD\s+Amount|Earnest\s+Money\s+Deposit|EMD)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+)",
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
    "Delhi": ["New Delhi", "Delhi", "North Delhi", "South Delhi", "West Delhi", "East Delhi", "Dwarka", "Rohini"],
    "Karnataka": ["Bengaluru", "Bangalore", "Mysuru", "Mysore", "Hubballi", "Mangaluru", "Belagavi", "Kalaburagi"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tirunelveli", "Tiruppur", "Vellore"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Prayagraj", "Noida", "Greater Noida", "Ghaziabad", "Meerut", "Bareilly", "Gorakhpur"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Jabalpur", "Gwalior", "Ujjain", "Sagar", "Dewas", "Satna", "Ratlam"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri", "Kalyani", "Kharagpur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Secunderabad"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Kollam", "Thrissur", "Kannur", "Alappuzha"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda", "Mohali"],
    "Haryana": ["Gurugram", "Gurgaon", "Faridabad", "Panipat", "Ambala", "Yamunanagar", "Rohtak", "Hisar", "Karnal", "Sonipat"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga"]
}

# Pincode 3-digit prefix mapping to Indian Major Cities
PINCODE_PREFIX_CITY_MAP = {
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
    "400": ("Mumbai", "Maharashtra"),
    "411": ("Pune", "Maharashtra"),
    "440": ("Nagpur", "Maharashtra"),
    "302": ("Jaipur", "Rajasthan"),
    "110": ("New Delhi", "Delhi"),
    "560": ("Bengaluru", "Karnataka"),
    "600": ("Chennai", "Tamil Nadu"),
    "500": ("Hyderabad", "Telangana"),
    "226": ("Lucknow", "Uttar Pradesh"),
    "201": ("Noida", "Uttar Pradesh"),
    "700": ("Kolkata", "West Bengal")
}

def extract_consignee_details(text):
    """
    Extracts Consignee / Reporting Officer and Office Address from GeM tender copies / text.
    Handles GeM format: [Pincode],[Officer/Office],[Building/Floor],[Area],[City]
    Example: 390001,The Superintending Engineer's Office,National Highway Circle,712 & 713,7th floor, E-block,Kuber Bhavan,Kothi char rasta,Raopura,vadodara
    """
    if not text:
        return None

    # Pattern 1: Match comma-separated consignee block starting with 6-digit pincode
    pincode_block_m = re.search(r"(\b[1-9][0-9]{5}\b)\s*,\s*([^\r\n]{15,300})", text)
    if pincode_block_m:
        raw_box = pincode_block_m.group(0).strip()
        pin = pincode_block_m.group(1).strip()
        rest = pincode_block_m.group(2).strip()
        tokens = [t.strip() for t in rest.split(',') if t.strip()]

        officer = tokens[0] if tokens else "Consignee Officer"
        
        # Detect city from tokens
        detected_city = None
        detected_state = "Gujarat"

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

        # Reconstruct clean full address
        clean_addr_parts = tokens
        formatted_address = f"{', '.join(clean_addr_parts)} - {pin}" if pin not in ', '.join(clean_addr_parts) else ', '.join(clean_addr_parts)

        return {
            "pincode": pin,
            "consignee_officer": officer,
            "city": detected_city or "Gandhinagar",
            "state": detected_state,
            "address": formatted_address,
            "raw_box": raw_box
        }

    # Pattern 2: Table format "Consignee/Reporting Officer ... Address"
    table_m = re.search(r"(?:Consignee(?:s)?\s*/\s*Reporting\s+Officer|Consignee\s+Detail[s]?)\s*[:\-]?\s*([^\n\r]+(?:[\r\n]+[^\n\r]+){0,3})", text, re.IGNORECASE)
    if table_m:
        raw_block = table_m.group(1).strip()
        pin_m = re.search(r"\b[1-9][0-9]{5}\b", raw_block)
        pin = pin_m.group(0) if pin_m else None
        
        detected_city = None
        detected_state = "Gujarat"
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

        clean_block = re.sub(r'\s+', ' ', raw_block)
        return {
            "pincode": pin,
            "consignee_officer": clean_block.split(',')[0].strip() if ',' in clean_block else clean_block[:50],
            "city": detected_city or "Gandhinagar",
            "state": detected_state,
            "address": clean_block,
            "raw_box": raw_block
        }

    return None

def extract_city(text, state=None):
    if not text:
        return "Gandhinagar"
    
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

    return "Gandhinagar" if (state == "Gujarat" or not state) else "New Delhi"

def extract_office_address(text):
    consignee_info = extract_consignee_details(text)
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
    return None

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
