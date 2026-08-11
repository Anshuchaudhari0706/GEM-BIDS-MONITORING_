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

def extract_office_address(text):
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
