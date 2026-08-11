import re

"""
Normalizer Module for GeM Tender Documents
Normalizes numeric currency strings (Lakhs, Crores, INR) into pure numeric integers.
Normalizes state names, addresses, and manpower quantities.
"""

def normalize_currency_to_number(raw_val_str):
    if not raw_val_str:
        return None, None

    cleaned = raw_val_str.replace('₹', '').replace('Rs.', '').replace('Rs', '').replace('INR', '').replace(',', '').strip()
    
    # Check for Lakhs / Crore multipliers
    multiplier = 1
    if re.search(r"Lakhs?|Lakh", cleaned, re.IGNORECASE):
        multiplier = 100000
        cleaned = re.sub(r"Lakhs?|Lakh", "", cleaned, flags=re.IGNORECASE).strip()
    elif re.search(r"Crores?|Crore|Cr", cleaned, re.IGNORECASE):
        multiplier = 10000000
        cleaned = re.sub(r"Crores?|Crore|Cr", "", cleaned, flags=re.IGNORECASE).strip()

    num_match = re.search(r"([0-9\.]+)", cleaned)
    if num_match:
        try:
            val_float = float(num_match.group(1))
            final_num = int(val_float * multiplier)
            formatted_display = f"₹{final_num:,.0f}" if final_num < 100000 else f"₹{final_num/100000:.2f} Lakhs"
            return final_num, formatted_display
        except ValueError:
            pass

    return None, raw_val_str

def normalize_manpower_list(raw_manpower_list):
    normalized = []
    seen = set()

    for item in raw_manpower_list:
        desig = item.get("designation", "").strip()
        qty = item.get("quantity", 0)

        if desig and qty > 0 and desig.lower() not in seen:
            seen.add(desig.lower())
            normalized.append({
                "designation": desig,
                "quantity": int(qty)
            })

    return normalized
