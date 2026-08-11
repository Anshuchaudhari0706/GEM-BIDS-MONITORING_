import re

"""
Table Parser Module for GeM Tender Documents
Extracts structured manpower rows and schedule of requirements from tabular strings or PDF table blocks.
"""

def extract_tables_from_text(raw_text):
    rows = []
    lines = raw_text.split('\n')

    # Look for tabular patterns with columns (Sr No | Designation | Quantity)
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
