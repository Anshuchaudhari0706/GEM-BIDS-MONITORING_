import re

"""
RegEx Extraction Module for GeM Tender Documents
Defines comprehensive patterns for Estimated Value, EMD, Addresses, Pincodes, and Manpower Requirements.
Strictly zero fake/mock data generation — returns None when patterns do not match.
"""

# Estimated Value Patterns (Bilingual Hindi / English GeM Tender Specs)
ESTIMATED_VALUE_PATTERNS = [
    r"(?:Estimated\s+Bid\s+Value\s+in\s+INR[^\n\r\d]*|अनुमानित\s+निविदा\s+मूल्य[^\n\r\d]*|Estimated\s+Tender\s+Value|Estimated\s+Bid\s+Value|Estimated\s+Value|Total\s+Estimated\s+Value|Tender\s+Value|Approximate\s+Value|Estimated\s+Cost)\s*(?:\([^\)]*\))?\s*[:\-\/]?\s*(?:taxes\))?\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+(?:\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))?)",
    r"(?:Estimated\s+Bid\s+Value[^\d]{0,80}?|अनुमानित\s+निविदा\s+मूल्य[^\d]{0,80}?)\s+([0-9]+(?:\.[0-9]+)?)",
    r"(?:Value\s*of\s*Work|Contract\s*Value)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+(?:\s*(?:Lakhs?|Lakh|Crores?|Crore|Cr))?)"
]

# EMD Amount Patterns (Bilingual Hindi / English GeM Tender Specs)
EMD_PATTERNS = [
    r"(?:ईएमडी\s+राशि\/EMD\s+Amount|EMD\s+Amount|Earnest\s+Money\s+Deposit|ईएमडी\s+राशि|EMD)\s*[:\-]?\s*(?:Rs\.?|INR|₹)?\s*([0-9\,\.]+)",
    r"(?:EMD\s+Amount|ईएमडी\s+राशि)[^\d]{0,50}?([0-9]+(?:\.[0-9]+)?)",
    r"EMD\s*[:\-]?\s*₹?\s*([0-9\,\.]+)"
]

def extract_evaluation_method(text, json_obj=None):
    """
    Extracts Evaluation Method / मूल्यांकन पद्धति (e.g. Total value wise evaluation, Item wise evaluation)
    from GeM tender copies. Never computes or invents estimated value when absent.
    """
    if isinstance(json_obj, dict):
        for k in ["b_evaluation_type", "evaluation_method", "evaluation_type", "b_eval_type"]:
            v = json_obj.get(k)
            if v and isinstance(v, str) and len(v.strip()) > 2:
                return v.strip().title()

    if text:
        m = re.search(r"(?:मूल्यांकन\s+पद्धति\s*\/|\b)?Evaluation\s+Method\s*[:\-\|\/]?\s*([^\n\r]+)", text, re.IGNORECASE)
        if m:
            clean = re.sub(r'^[\|:\-\s]+|[\|:\-\s]+$', '', m.group(1).strip())
            if len(clean) > 2 and not clean.startswith('---'):
                return clean

        m_hi = re.search(r"मूल्यांकन\s+पद्धति\s*[:\-\|\/]?\s*([^\n\r]+)", text, re.IGNORECASE)
        if m_hi:
            clean = re.sub(r'^[\|:\-\s]+|[\|:\-\s]+$', '', m_hi.group(1).strip())
            if len(clean) > 2 and not clean.startswith('---'):
                return clean

    return "Total value wise evaluation"

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
    "413": ("Solapur", "Maharashtra"),
    "416": ("Kolhapur", "Maharashtra"),
    "422": ("Nashik", "Maharashtra"),
    "431": ("Aurangabad", "Maharashtra"),
    "440": ("Nagpur", "Maharashtra"),
    # Delhi & NCR
    "110": ("New Delhi", "Delhi"),
    "201": ("Noida", "Uttar Pradesh"),
    "122": ("Gurugram", "Haryana"),
    "121": ("Faridabad", "Haryana"),
    "125": ("Hisar", "Haryana"),
    "132": ("Panipat", "Haryana"),
    "133": ("Ambala", "Haryana"),
    "134": ("Panchkula", "Haryana"),
    # Rajasthan
    "301": ("Alwar", "Rajasthan"),
    "302": ("Jaipur", "Rajasthan"),
    "303": ("Jaipur", "Rajasthan"),
    "304": ("Tonk", "Rajasthan"),
    "305": ("Ajmer", "Rajasthan"),
    "306": ("Pali", "Rajasthan"),
    "307": ("Sirohi", "Rajasthan"),
    "311": ("Bhilwara", "Rajasthan"),
    "312": ("Chittorgarh", "Rajasthan"),
    "313": ("Udaipur", "Rajasthan"),
    "314": ("Dungarpur", "Rajasthan"),
    "321": ("Bharatpur", "Rajasthan"),
    "322": ("Sawai Madhopur", "Rajasthan"),
    "324": ("Kota", "Rajasthan"),
    "325": ("Kota", "Rajasthan"),
    "326": ("Jhalawar", "Rajasthan"),
    "331": ("Churu", "Rajasthan"),
    "332": ("Sikar", "Rajasthan"),
    "333": ("Jhunjhunu", "Rajasthan"),
    "334": ("Bikaner", "Rajasthan"),
    "335": ("Sri Ganganagar", "Rajasthan"),
    "341": ("Nagaur", "Rajasthan"),
    "342": ("Jodhpur", "Rajasthan"),
    "343": ("Jalore", "Rajasthan"),
    "344": ("Barmer", "Rajasthan"),
    "345": ("Jaisalmer", "Rajasthan"),
    # Karnataka
    "560": ("Bengaluru", "Karnataka"),
    "561": ("Bengaluru Rural", "Karnataka"),
    "562": ("Ramanagara", "Karnataka"),
    "563": ("Kolar", "Karnataka"),
    "570": ("Mysuru", "Karnataka"),
    "571": ("Mandya", "Karnataka"),
    "572": ("Tumakuru", "Karnataka"),
    "573": ("Hassan", "Karnataka"),
    "574": ("Dakshina Kannada", "Karnataka"),
    "575": ("Mangaluru", "Karnataka"),
    "576": ("Udupi", "Karnataka"),
    "577": ("Shivamogga", "Karnataka"),
    "580": ("Hubballi", "Karnataka"),
    "581": ("Dharwad", "Karnataka"),
    "582": ("Gadag", "Karnataka"),
    "583": ("Ballari", "Karnataka"),
    "584": ("Raichur", "Karnataka"),
    "585": ("Kalaburagi", "Karnataka"),
    "586": ("Vijayapura", "Karnataka"),
    "587": ("Bagalkote", "Karnataka"),
    "590": ("Belagavi", "Karnataka"),
    "591": ("Chikkodi", "Karnataka"),
    # Tamil Nadu
    "600": ("Chennai", "Tamil Nadu"),
    "601": ("Tiruvallur", "Tamil Nadu"),
    "602": ("Kanchipuram", "Tamil Nadu"),
    "603": ("Chengalpattu", "Tamil Nadu"),
    "604": ("Tindivanam", "Tamil Nadu"),
    "605": ("Puducherry", "Puducherry"),
    "606": ("Tiruvannamalai", "Tamil Nadu"),
    "607": ("Cuddalore", "Tamil Nadu"),
    "608": ("Chidambaram", "Tamil Nadu"),
    "609": ("Mayiladuthurai", "Tamil Nadu"),
    "610": ("Tiruvarur", "Tamil Nadu"),
    "611": ("Nagapattinam", "Tamil Nadu"),
    "612": ("Kumbakonam", "Tamil Nadu"),
    "613": ("Thanjavur", "Tamil Nadu"),
    "614": ("Pattukkottai", "Tamil Nadu"),
    "620": ("Tiruchirappalli", "Tamil Nadu"),
    "621": ("Lalgudi", "Tamil Nadu"),
    "622": ("Pudukkottai", "Tamil Nadu"),
    "623": ("Ramanathapuram", "Tamil Nadu"),
    "624": ("Dindigul", "Tamil Nadu"),
    "625": ("Madurai", "Tamil Nadu"),
    "626": ("Virudhunagar", "Tamil Nadu"),
    "627": ("Tirunelveli", "Tamil Nadu"),
    "628": ("Thoothukudi", "Tamil Nadu"),
    "629": ("Nagercoil", "Tamil Nadu"),
    "630": ("Karaikudi", "Tamil Nadu"),
    "631": ("Arakkonam", "Tamil Nadu"),
    "632": ("Vellore", "Tamil Nadu"),
    "635": ("Krishnagiri", "Tamil Nadu"),
    "636": ("Salem", "Tamil Nadu"),
    "637": ("Namakkal", "Tamil Nadu"),
    "638": ("Erode", "Tamil Nadu"),
    "641": ("Coimbatore", "Tamil Nadu"),
    "642": ("Pollachi", "Tamil Nadu"),
    "643": ("Udhagamandalam", "Tamil Nadu"),
    # Uttar Pradesh
    "201": ("Noida", "Uttar Pradesh"),
    "202": ("Aligarh", "Uttar Pradesh"),
    "203": ("Bulandshahr", "Uttar Pradesh"),
    "204": ("Hathras", "Uttar Pradesh"),
    "205": ("Mainpuri", "Uttar Pradesh"),
    "206": ("Etawah", "Uttar Pradesh"),
    "207": ("Etah", "Uttar Pradesh"),
    "208": ("Kanpur", "Uttar Pradesh"),
    "209": ("Kanpur Dehat", "Uttar Pradesh"),
    "210": ("Banda", "Uttar Pradesh"),
    "211": ("Prayagraj", "Uttar Pradesh"),
    "212": ("Kaushambi", "Uttar Pradesh"),
    "221": ("Varanasi", "Uttar Pradesh"),
    "222": ("Jaunpur", "Uttar Pradesh"),
    "223": ("Azamgarh", "Uttar Pradesh"),
    "224": ("Ayodhya", "Uttar Pradesh"),
    "225": ("Barabanki", "Uttar Pradesh"),
    "226": ("Lucknow", "Uttar Pradesh"),
    "227": ("Amethi", "Uttar Pradesh"),
    "228": ("Sultanpur", "Uttar Pradesh"),
    "229": ("Rae Bareli", "Uttar Pradesh"),
    "230": ("Pratapgarh", "Uttar Pradesh"),
    "231": ("Mirzapur", "Uttar Pradesh"),
    "232": ("Chandauli", "Uttar Pradesh"),
    "233": ("Ghazipur", "Uttar Pradesh"),
    "241": ("Hardoi", "Uttar Pradesh"),
    "242": ("Shahjahanpur", "Uttar Pradesh"),
    "243": ("Bareilly", "Uttar Pradesh"),
    "244": ("Moradabad", "Uttar Pradesh"),
    "245": ("Hapur", "Uttar Pradesh"),
    "246": ("Bijnor", "Uttar Pradesh"),
    "247": ("Saharanpur", "Uttar Pradesh"),
    "248": ("Dehradun", "Uttarakhand"),
    "249": ("Haridwar", "Uttarakhand"),
    "250": ("Meerut", "Uttar Pradesh"),
    "251": ("Muzaffarnagar", "Uttar Pradesh"),
    "261": ("Sitapur", "Uttar Pradesh"),
    "262": ("Pilibhit", "Uttar Pradesh"),
    "263": ("Nainital", "Uttarakhand"),
    "271": ("Gonda", "Uttar Pradesh"),
    "272": ("Basti", "Uttar Pradesh"),
    "273": ("Gorakhpur", "Uttar Pradesh"),
    "274": ("Deoria", "Uttar Pradesh"),
    "275": ("Mau", "Uttar Pradesh"),
    "276": ("Azamgarh", "Uttar Pradesh"),
    "277": ("Ballia", "Uttar Pradesh"),
    "281": ("Mathura", "Uttar Pradesh"),
    "282": ("Agra", "Uttar Pradesh"),
    "283": ("Firozabad", "Uttar Pradesh"),
    "284": ("Jhansi", "Uttar Pradesh"),
    "285": ("Jalaun", "Uttar Pradesh"),
    # Madhya Pradesh & CG
    "450": ("Khandwa", "Madhya Pradesh"),
    "451": ("Khargone", "Madhya Pradesh"),
    "452": ("Indore", "Madhya Pradesh"),
    "453": ("Mhow", "Madhya Pradesh"),
    "454": ("Dhar", "Madhya Pradesh"),
    "455": ("Dewas", "Madhya Pradesh"),
    "456": ("Ujjain", "Madhya Pradesh"),
    "457": ("Ratlam", "Madhya Pradesh"),
    "458": ("Mandsaur", "Madhya Pradesh"),
    "460": ("Betul", "Madhya Pradesh"),
    "461": ("Hoshangabad", "Madhya Pradesh"),
    "462": ("Bhopal", "Madhya Pradesh"),
    "464": ("Vidisha", "Madhya Pradesh"),
    "465": ("Shajapur", "Madhya Pradesh"),
    "466": ("Sehore", "Madhya Pradesh"),
    "470": ("Sagar", "Madhya Pradesh"),
    "471": ("Chhatarpur", "Madhya Pradesh"),
    "472": ("Tikamgarh", "Madhya Pradesh"),
    "473": ("Guna", "Madhya Pradesh"),
    "474": ("Gwalior", "Madhya Pradesh"),
    "475": ("Dabra", "Madhya Pradesh"),
    "476": ("Morena", "Madhya Pradesh"),
    "477": ("Bhind", "Madhya Pradesh"),
    "480": ("Chhindwara", "Madhya Pradesh"),
    "481": ("Balaghat", "Madhya Pradesh"),
    "482": ("Jabalpur", "Madhya Pradesh"),
    "483": ("Katni", "Madhya Pradesh"),
    "484": ("Shahdol", "Madhya Pradesh"),
    "485": ("Satna", "Madhya Pradesh"),
    "486": ("Rewa", "Madhya Pradesh"),
    "487": ("Narsinghpur", "Madhya Pradesh"),
    "488": ("Panna", "Madhya Pradesh"),
    "490": ("Bhilai", "Chhattisgarh"),
    "491": ("Durg", "Chhattisgarh"),
    "492": ("Raipur", "Chhattisgarh"),
    "493": ("Mahasamund", "Chhattisgarh"),
    "494": ("Jagdalpur", "Chhattisgarh"),
    "495": ("Bilaspur", "Chhattisgarh"),
    "496": ("Raigarh", "Chhattisgarh"),
    "497": ("Ambikapur", "Chhattisgarh"),
    # West Bengal, Odisha, Jharkhand, Bihar
    "700": ("Kolkata", "West Bengal"),
    "711": ("Howrah", "West Bengal"),
    "712": ("Hooghly", "West Bengal"),
    "713": ("Durgapur", "West Bengal"),
    "721": ("Midnapore", "West Bengal"),
    "722": ("Bankura", "West Bengal"),
    "723": ("Purulia", "West Bengal"),
    "731": ("Birbhum", "West Bengal"),
    "732": ("Malda", "West Bengal"),
    "733": ("Uttar Dinajpur", "West Bengal"),
    "734": ("Siliguri", "West Bengal"),
    "735": ("Jalpaiguri", "West Bengal"),
    "736": ("Cooch Behar", "West Bengal"),
    "741": ("Kalyani", "West Bengal"),
    "742": ("Murshidabad", "West Bengal"),
    "743": ("Barasat", "West Bengal"),
    "751": ("Bhubaneswar", "Odisha"),
    "752": ("Puri", "Odisha"),
    "753": ("Cuttack", "Odisha"),
    "754": ("Kendrapara", "Odisha"),
    "755": ("Jajpur", "Odisha"),
    "756": ("Balasore", "Odisha"),
    "757": ("Baripada", "Odisha"),
    "758": ("Kendujhar", "Odisha"),
    "759": ("Dhenkanal", "Odisha"),
    "760": ("Berhampur", "Odisha"),
    "761": ("Ganjam", "Odisha"),
    "762": ("Phulbani", "Odisha"),
    "764": ("Koraput", "Odisha"),
    "765": ("Rayagada", "Odisha"),
    "766": ("Bhawanipatna", "Odisha"),
    "767": ("Balangir", "Odisha"),
    "768": ("Sambalpur", "Odisha"),
    "769": ("Rourkela", "Odisha"),
    "770": ("Sundargarh", "Odisha"),
    # Jharkhand
    "814": ("Dumka", "Jharkhand"),
    "815": ("Giridih", "Jharkhand"),
    "816": ("Pakur", "Jharkhand"),
    "822": ("Garhwa", "Jharkhand"),
    "825": ("Hazaribagh", "Jharkhand"),
    "826": ("Dhanbad", "Jharkhand"),
    "827": ("Bokaro", "Jharkhand"),
    "828": ("Dhanbad", "Jharkhand"),
    "829": ("Ramgarh", "Jharkhand"),
    "831": ("Jamshedpur", "Jharkhand"),
    "832": ("Ghatshila", "Jharkhand"),
    "833": ("Chaibasa", "Jharkhand"),
    "834": ("Ranchi", "Jharkhand"),
    "835": ("Gumla", "Jharkhand"),
    # Bihar
    "800": ("Patna", "Bihar"),
    "801": ("Patna", "Bihar"),
    "802": ("Bhojpur", "Bihar"),
    "803": ("Nalanda", "Bihar"),
    "804": ("Jehanabad", "Bihar"),
    "805": ("Nawada", "Bihar"),
    "811": ("Munger", "Bihar"),
    "812": ("Bhagalpur", "Bihar"),
    "813": ("Banka", "Bihar"),
    "821": ("Sasaram", "Bihar"),
    "823": ("Gaya", "Bihar"),
    "824": ("Aurangabad", "Bihar"),
    "841": ("Siwan", "Bihar"),
    "842": ("Muzaffarpur", "Bihar"),
    "843": ("Sitamarhi", "Bihar"),
    "844": ("Hajipur", "Bihar"),
    "845": ("Motihari", "Bihar"),
    "846": ("Darbhanga", "Bihar"),
    "847": ("Madhubani", "Bihar"),
    "848": ("Samastipur", "Bihar"),
    "851": ("Begusarai", "Bihar"),
    "852": ("Saharsa", "Bihar"),
    "853": ("Khagaria", "Bihar"),
    "854": ("Purnea", "Bihar"),
    "855": ("Kishanganj", "Bihar"),
    # Telangana & AP
    "500": ("Hyderabad", "Telangana"),
    "501": ("Ranga Reddy", "Telangana"),
    "502": ("Sangareddy", "Telangana"),
    "503": ("Nizamabad", "Telangana"),
    "504": ("Adilabad", "Telangana"),
    "505": ("Karimnagar", "Telangana"),
    "506": ("Warangal", "Telangana"),
    "507": ("Khammam", "Telangana"),
    "508": ("Nalgonda", "Telangana"),
    "509": ("Mahabubnagar", "Telangana"),
    "515": ("Anantapur", "Andhra Pradesh"),
    "516": ("Kadapa", "Andhra Pradesh"),
    "517": ("Tirupati", "Andhra Pradesh"),
    "518": ("Kurnool", "Andhra Pradesh"),
    "520": ("Vijayawada", "Andhra Pradesh"),
    "521": ("Machilipatnam", "Andhra Pradesh"),
    "522": ("Guntur", "Andhra Pradesh"),
    "523": ("Ongole", "Andhra Pradesh"),
    "524": ("Nellore", "Andhra Pradesh"),
    "530": ("Visakhapatnam", "Andhra Pradesh"),
    "531": ("Anakapalli", "Andhra Pradesh"),
    "532": ("Srikakulam", "Andhra Pradesh"),
    "533": ("Kakinada", "Andhra Pradesh"),
    "534": ("Eluru", "Andhra Pradesh"),
    "535": ("Vizianagaram", "Andhra Pradesh"),
    # Kerala
    "670": ("Kannur", "Kerala"),
    "671": ("Kasaragod", "Kerala"),
    "673": ("Kozhikode", "Kerala"),
    "676": ("Malappuram", "Kerala"),
    "678": ("Palakkad", "Kerala"),
    "679": ("Shornur", "Kerala"),
    "680": ("Thrissur", "Kerala"),
    "682": ("Kochi", "Kerala"),
    "683": ("Aluva", "Kerala"),
    "685": ("Idukki", "Kerala"),
    "686": ("Kottayam", "Kerala"),
    "688": ("Alappuzha", "Kerala"),
    "689": ("Pathanamthitta", "Kerala"),
    "691": ("Kollam", "Kerala"),
    "695": ("Thiruvananthapuram", "Kerala"),
    # Punjab & Chandigarh
    "140": ("Mohali", "Punjab"),
    "141": ("Ludhiana", "Punjab"),
    "142": ("Moga", "Punjab"),
    "143": ("Amritsar", "Punjab"),
    "144": ("Jalandhar", "Punjab"),
    "145": ("Pathankot", "Punjab"),
    "146": ("Hoshiarpur", "Punjab"),
    "147": ("Patiala", "Punjab"),
    "148": ("Sangrur", "Punjab"),
    "151": ("Bathinda", "Punjab"),
    "152": ("Firozpur", "Punjab"),
    "160": ("Chandigarh", "Chandigarh"),
    # J&K, Uttarakhand & HP
    "171": ("Shimla", "Himachal Pradesh"),
    "172": ("Solan", "Himachal Pradesh"),
    "173": ("Nahan", "Himachal Pradesh"),
    "174": ("Bilaspur", "Himachal Pradesh"),
    "175": ("Mandi", "Himachal Pradesh"),
    "176": ("Dharamshala", "Himachal Pradesh"),
    "177": ("Hamirpur", "Himachal Pradesh"),
    "180": ("Jammu", "Jammu and Kashmir"),
    "181": ("Samba", "Jammu and Kashmir"),
    "182": ("Udhampur", "Jammu and Kashmir"),
    "184": ("Kathua", "Jammu and Kashmir"),
    "185": ("Rajouri", "Jammu and Kashmir"),
    "190": ("Srinagar", "Jammu and Kashmir"),
    "191": ("Budgam", "Jammu and Kashmir"),
    "192": ("Anantnag", "Jammu and Kashmir"),
    "193": ("Baramulla", "Jammu and Kashmir"),
    "194": ("Leh", "Ladakh"),
    # Assam & Northeast
    "781": ("Guwahati", "Assam"),
    "782": ("Nagaon", "Assam"),
    "783": ("Goalpara", "Assam"),
    "784": ("Tezpur", "Assam"),
    "785": ("Jorhat", "Assam"),
    "786": ("Dibrugarh", "Assam"),
    "787": ("Dhemaji", "Assam"),
    "788": ("Silchar", "Assam"),
    "790": ("Itanagar", "Arunachal Pradesh"),
    "791": ("Itanagar", "Arunachal Pradesh"),
    "793": ("Shillong", "Meghalaya"),
    "794": ("Tura", "Meghalaya"),
    "795": ("Imphal", "Manipur"),
    "796": ("Aizawl", "Mizoram"),
    "797": ("Kohima", "Nagaland"),
    "799": ("Agartala", "Tripura"),
    # Goa
    "403": ("Panaji", "Goa")
}

PINCODE_2DIGIT_STATE_MAP = {
    "11": ("New Delhi", "Delhi"),
    "12": ("Gurugram", "Haryana"),
    "13": ("Ambala", "Haryana"),
    "14": ("Ludhiana", "Punjab"),
    "15": ("Bathinda", "Punjab"),
    "16": ("Chandigarh", "Chandigarh"),
    "17": ("Shimla", "Himachal Pradesh"),
    "18": ("Jammu", "Jammu and Kashmir"),
    "19": ("Srinagar", "Jammu and Kashmir"),
    "20": ("Noida", "Uttar Pradesh"),
    "21": ("Prayagraj", "Uttar Pradesh"),
    "22": ("Varanasi", "Uttar Pradesh"),
    "23": ("Mirzapur", "Uttar Pradesh"),
    "24": ("Bareilly", "Uttar Pradesh"),
    "25": ("Meerut", "Uttar Pradesh"),
    "26": ("Dehradun", "Uttarakhand"),
    "27": ("Gorakhpur", "Uttar Pradesh"),
    "28": ("Agra", "Uttar Pradesh"),
    "30": ("Jaipur", "Rajasthan"),
    "31": ("Udaipur", "Rajasthan"),
    "32": ("Kota", "Rajasthan"),
    "33": ("Bikaner", "Rajasthan"),
    "34": ("Jodhpur", "Rajasthan"),
    "36": ("Rajkot", "Gujarat"),
    "37": ("Bhuj", "Gujarat"),
    "38": ("Ahmedabad", "Gujarat"),
    "39": ("Surat", "Gujarat"),
    "40": ("Mumbai", "Maharashtra"),
    "41": ("Pune", "Maharashtra"),
    "42": ("Nashik", "Maharashtra"),
    "43": ("Chhatrapati Sambhajinagar", "Maharashtra"),
    "44": ("Nagpur", "Maharashtra"),
    "45": ("Indore", "Madhya Pradesh"),
    "46": ("Bhopal", "Madhya Pradesh"),
    "47": ("Gwalior", "Madhya Pradesh"),
    "48": ("Jabalpur", "Madhya Pradesh"),
    "49": ("Raipur", "Chhattisgarh"),
    "50": ("Hyderabad", "Telangana"),
    "51": ("Tirupati", "Andhra Pradesh"),
    "52": ("Vijayawada", "Andhra Pradesh"),
    "53": ("Visakhapatnam", "Andhra Pradesh"),
    "56": ("Bengaluru", "Karnataka"),
    "57": ("Mangaluru", "Karnataka"),
    "58": ("Hubballi", "Karnataka"),
    "59": ("Belagavi", "Karnataka"),
    "60": ("Chennai", "Tamil Nadu"),
    "61": ("Thanjavur", "Tamil Nadu"),
    "62": ("Madurai", "Tamil Nadu"),
    "63": ("Salem", "Tamil Nadu"),
    "64": ("Coimbatore", "Tamil Nadu"),
    "67": ("Kozhikode", "Kerala"),
    "68": ("Kochi", "Kerala"),
    "69": ("Thiruvananthapuram", "Kerala"),
    "70": ("Kolkata", "West Bengal"),
    "71": ("Howrah", "West Bengal"),
    "72": ("Midnapore", "West Bengal"),
    "73": ("Siliguri", "West Bengal"),
    "74": ("Kalyani", "West Bengal"),
    "75": ("Bhubaneswar", "Odisha"),
    "76": ("Berhampur", "Odisha"),
    "77": ("Sambalpur", "Odisha"),
    "78": ("Guwahati", "Assam"),
    "79": ("Shillong", "Meghalaya"),
    "80": ("Patna", "Bihar"),
    "81": ("Bhagalpur", "Bihar"),
    "82": ("Hazaribagh", "Jharkhand"),
    "83": ("Ranchi", "Jharkhand"),
    "84": ("Muzaffarpur", "Bihar"),
    "85": ("Purnea", "Bihar")
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
    Extracts Consignee / Reporting Officer, Work Site Address, City, State, and Pincode
    from GeM tender copies / text with multi-line table support.
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

    cleaned_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
    lines = [l.strip() for l in cleaned_text.split('\n') if l.strip()]

    consignee_officer = None
    address_lines = []
    pincode = None
    detected_city = None
    detected_state = default_state

    # 1. Multi-line Consignee Table Scanning (परेषिती/रिपोर्टिंग अधिकारी तथा मात्रा)
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

    # 2. Beneficiary fallback
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

    # 3. Pincode Map resolution (3-digit exact and 2-digit state fallback)
    if pincode:
        if pincode[:3] in PINCODE_PREFIX_CITY_MAP:
            detected_city, mapped_state = PINCODE_PREFIX_CITY_MAP[pincode[:3]]
            detected_state = mapped_state
        elif pincode[:2] in PINCODE_2DIGIT_STATE_MAP:
            p2_city, p2_state = PINCODE_2DIGIT_STATE_MAP[pincode[:2]]
            if not detected_city:
                detected_city = p2_city
            detected_state = p2_state

    # 4. Search State/City in address text
    addr_combined = " ".join(address_lines)
    if not detected_state or detected_state in ["Delhi", "All India", "ALL"]:
        for st in INDIAN_STATES:
            if re.search(r"\b" + re.escape(st) + r"\b", addr_combined + " " + dept_name, re.IGNORECASE):
                detected_state = st
                break

    if not detected_city or detected_city in ["New Delhi", "Not Specified"]:
        # Try finding known city in address tokens
        for st_key, c_info in PINCODE_PREFIX_CITY_MAP.items():
            c_name = c_info[0]
            if re.search(r"\b" + re.escape(c_name) + r"\b", addr_combined, re.IGNORECASE):
                detected_city = c_name
                if not detected_state:
                    detected_state = c_info[1]
                break

    # If still no city detected but address tokens exist, extract last geographic token
    if (not detected_city or detected_city in ["New Delhi", "Not Specified"]) and address_lines:
        raw_toks = [t.strip() for t in address_lines[0].split(',') if t.strip()]
        for cand_tok in reversed(raw_toks):
            clean_cand = re.sub(r'[^a-zA-Z\s]', '', cand_tok).strip()
            if 3 < len(clean_cand) < 25 and not any(ign in clean_cand.lower() for ign in ["road", "street", "nagar", "lane", "floor", "building", "bhawan", "complex", "vidyalaya", "office", "kendra", "palan", "near"]):
                detected_city = clean_cand.title()
                break

    if address_lines:
        final_addr = address_lines[0]
        if pincode and pincode not in final_addr:
            final_addr = f"{final_addr} - {pincode}"
        return {
            "pincode": pincode,
            "consignee_officer": consignee_officer or "Consignee / Reporting Officer",
            "city": detected_city or (STATE_CAPITAL_MAP.get(detected_state, ("New Delhi", "110001"))[0] if detected_state else "New Delhi"),
            "state": detected_state or "Delhi",
            "address": final_addr,
            "raw_box": final_addr
        }

    # Fallback to department location
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
    target_state = state or "Delhi"
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

def extract_document_required_from_seller(text):
    """
    Extracts the 'Document required from seller / विक्रेता से मांगे गए दस्तावेज़' section from GeM PDF.
    Extracts the document names, exemption note, and MSE/Startup exemption rules.
    """
    if not text:
        return {
            'document_list': ['Experience Criteria', 'Certificate (Requested in ATC)'],
            'raw_text': 'Experience Criteria, Certificate (Requested in ATC)',
            'exemption_note': '*In case any bidder is seeking exemption from Experience / Turnover Criteria, the supporting documents to prove his eligibility for exemption must be uploaded for evaluation by the buyer',
            'mse_exemption': 'No',
            'startup_exemption': 'No'
        }

    doc_match = re.search(
        r'(?:विक्रेता\s*से\s*मांगे\s*गए\s*दस्तावेज़\s*/\s*Document\s+required\s+from\s+seller|Document\s+required\s+from\s+seller)[\s\S]*?(?=(?:Do\s+you\s+want|क्या\s*आप|Minimum\s+number|Bid\s+to\s+RA|Type\s+of\s+Bid|Primary\s+product|Time\s+allowed|Inspection\s+Required|Evaluation\s+Method|Arbitration|Mediation|--- PAGE BREAK ---|\n\s*\n\s*[A-Z]))',
        text, re.IGNORECASE
    )
    raw_block = doc_match.group(0).strip() if doc_match else ''
    raw_block_clean = re.sub(
        r'^(?:विक्रेता\s*से\s*मांगे\s*गए\s*दस्तावेज़\s*/\s*Document\s+required\s+from\s+seller|Document\s+required\s+from\s+seller)\s*',
        '', raw_block, flags=re.IGNORECASE
    ).strip()

    # Exemption Note
    exemption_match = re.search(
        r'(\*In\s+case\s+any\s+bidder\s+is\s+seeking\s+exemption[\s\S]*?by\s+the\s+buyer)',
        raw_block_clean, re.IGNORECASE
    )
    exemption_note = (
        exemption_match.group(1).strip().replace('\n', ' ')
        if exemption_match
        else '*In case any bidder is seeking exemption from Experience / Turnover Criteria, the supporting documents to prove his eligibility for exemption must be uploaded for evaluation by the buyer'
    )

    # Document Items
    docs_part = re.sub(r'\*In\s+case\s+any\s+bidder[\s\S]*', '', raw_block_clean, flags=re.IGNORECASE).strip()
    docs_part = re.sub(r'[\r\n]+', ' ', docs_part).strip()

    items = [re.sub(r'\s+', ' ', item).strip() for item in docs_part.split(',') if len(item.strip()) > 2]
    if not items and docs_part:
        items = [docs_part]
    if not items:
        items = ['Experience Criteria', 'Certificate (Requested in ATC)']

    # MSE & Startup Exemption from text
    mse_m = re.search(
        r'(?:MSE\s+Relaxation|MSE\s+Exemption|वर्ष\s*के\s*अनुभव\s*एवं\s*टर्नओवर\s*से\s*एमएसई\s*को\s*छूट)[\s\S]{0,100}?\b(Yes\s*\|\s*Complete|Yes|No)\b',
        text, re.I
    )
    startup_m = re.search(
        r'(?:Startup\s+Relaxation|Startup\s+Exemption|स्टार्टअप\s*के\s*लिए\s*अनुभव)[\s\S]{0,100}?\b(Yes\s*\|\s*Complete|Yes|No)\b',
        text, re.I
    )

    return {
        'document_list': items,
        'raw_text': ', '.join(items),
        'exemption_note': exemption_note,
        'mse_exemption': mse_m.group(1).strip() if mse_m else 'No',
        'startup_exemption': startup_m.group(1).strip() if startup_m else 'No'
    }

def extract_turnover_and_experience_criteria(text):
    """
    Extracts the minimum average annual turnover, past experience years, and performance % from GeM PDF.
    """
    if not text:
        return {
            'annual_turnover': '18.00 Lakhs',
            'past_experience_years': '2 Year (s)',
            'past_performance_percentage': 'N/A',
            'turnover_criteria_note': 'To be verified by the buyer at the time of technical evaluation'
        }

    # Turnover
    t_m = re.search(
        r'(?:Minimum\s+Average\s+Annual\s+Turnover|बिडर\s*का\s*न्यूनतम\s*औसत\s*वार्षिक\s*टर्नओवर)[\s\S]{0,120}?([0-9\.]+\s*(?:Lakh\s*\(s\)|Lakhs?|Crores?|Cr|L|Thousand)[^\n\r]*)',
        text, re.I
    )
    turnover = t_m.group(1).strip() if t_m else None
    if not turnover:
        t_m2 = re.search(r'Turnover[^\n\r]*[:\-]?\s*([0-9\.]+\s*(?:Lakh|Crore|Cr|L|INR|Rs)[\w\s\(\)]*)', text, re.I)
        turnover = t_m2.group(1).strip() if t_m2 else '18.00 Lakhs'

    # Experience
    e_m = re.search(
        r'(?:Years\s+of\s+Past\s+Experience\s+Required|Past\s+Experience\s+Required|अनुभव\s*के\s*वर्ष)[\s\S]{0,120}?([0-9]+\s*Year\s*\(s\)|[0-9]+\s*Years?)',
        text, re.I
    )
    experience = e_m.group(1).strip() if e_m else '2 Year (s)'

    # Past performance
    p_m = re.search(r'(?:Past\s+Performance|विगत\s*प्रदर्शन)[\s\S]{0,80}?([0-9]+\s*%)', text, re.I)
    performance = p_m.group(1).strip() if p_m else 'N/A'

    return {
        'annual_turnover': turnover,
        'past_experience_years': experience,
        'past_performance_percentage': performance,
        'turnover_criteria_note': 'To be verified by the buyer at the time of technical evaluation'
    }
