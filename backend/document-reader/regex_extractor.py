import re

# Comprehensive Regex Extraction Patterns for GeM Tender Documents
PATTERNS = {
    "bid_number": [
        r"Bid\s*(?:No|Number|ID|Reference)\s*[:\-]?\s*([A-Z0-9\/\-]+)",
        r"GEM\/\d{4}\/[AB]\/\d+",
        r"Tender\s*(?:No|ID|Ref)\s*[:\-]?\s*([A-Z0-9\/\-]+)"
    ],
    "title": [
        r"(?:Title|Name\s+of\s+Work|Subject|Work|Service)\s*[:\-]?\s*([^\n\r]{10,120})",
        r"([A-Za-z0-9\s,&-]+(?:Service|Contract|Outsourcing|Supply|Maintenance|Guard)[^\n\r]{5,80})"
    ],
    "organization": [
        r"(?:Organization|Department|Ministry|Buyer|Authority)\s*[:\-]?\s*([^\n\r]{5,100})",
        r"(Ministry\s+of\s+[A-Za-z\s]+|National\s+[A-Za-z\s]+|Indian\s+Institute\s+of\s+[A-Za-z\s]+)"
    ],
    "estimated_value": [
        r"(?:Estimated\s+(?:Bid|Tender|Contract)?\s*Value|Total\s+Estimated\s+Value|Approx\.?\s+Value)\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)\s*(Lakhs?|Lakh|Crores?|Crore)?",
        r"(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d+)?)\s*(Lakhs?|Lakh|Crores?|Crore)?\s*(?:Estimated|Value|Total)"
    ],
    "emd_amount": [
        r"(?:EMD|Earnest\s+Money\s+Deposit)\s*(?:Amount)?\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)",
        r"EMD\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)"
    ],
    "tender_fee": [
        r"(?:Tender|Document)\s+Fee\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)",
        r"Cost\s+of\s+Tender\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+)"
    ],
    "performance_security": [
        r"(?:Performance\s+Security|Security\s+Deposit|ePBG)\s*[:\-]?\s*(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)"
    ],
    "dates": {
        "published_date": [r"(?:Published|Issue|Start)\s+Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"],
        "closing_date": [r"(?:Closing|End|Submission)\s+Date\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})"],
        "closing_time": [r"(?:Closing|End)\s+Time\s*[:\-]?\s*(\d{1,2}:\d{2}(?:\s*[APMapm]{2})?)"]
    },
    "location": [
        r"(?:Work\s+Location|Place\s+of\s+Work|Site\s+Address|Consignee\s+Address)\s*[:\-]?\s*([^\n\r]{10,150})",
        r"([A-Za-z0-9\s,.-]+,\s*(?:Gujarat|Delhi|Karnataka|Maharashtra|Rajasthan|Uttarakhand|Telangana|Uttar Pradesh)\s*-\s*\d{6})"
    ]
}

MANPOWER_PATTERNS = [
    r"(\d+)\s*[\-\:]?\s*(Security\s+Guard|Security\s+Supervisor|Peon|Housekeeping\s+Staff|Data\s+Entry\s+Operator|Driver|Electrician|Plumber|Supervisor)",
    r"(Security\s+Guard|Security\s+Supervisor|Peon|Housekeeping\s+Staff|Data\s+Entry\s+Operator|Driver|Electrician|Plumber|Supervisor)\s*[\-\:]?\s*(\d+)",
    r"(\d+)\s+([A-Za-z\s]+(?:Guard|Peon|Staff|Operator|Driver|Supervisor|Helper|Technician))"
]

def parse_indian_number(val_str, unit_str=None):
    """Converts Indian numbering (Lakhs/Crores) into numeric integer."""
    if not val_str:
        return 0, "₹0"
    
    clean_val = str(val_str).replace(',', '').strip()
    try:
        num = float(clean_val)
    except ValueError:
        return 0, str(val_str)
    
    unit = (unit_str or '').lower().strip()
    if 'crore' in unit:
        num *= 10000000
    elif 'lakh' in unit:
        num *= 100000
    
    formatted = f"₹{int(num):,}"
    return int(num), formatted
