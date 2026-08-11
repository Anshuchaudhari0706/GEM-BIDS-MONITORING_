"""
Validator & Confidence Score Module for GeM Tender Extraction
Calculates confidence levels (HIGH, MEDIUM, LOW, NOT_FOUND) for all extracted fields.
Ensures zero fake data generation — returns NOT_FOUND if field is absent.
"""

def evaluate_field_confidence(val, raw_matched=None, is_numeric=False):
    if val is None or val == "" or val == "Not Specified" or val == "Not Available":
        return "NOT_FOUND"

    if is_numeric and isinstance(val, (int, float)) and val > 0:
        return "HIGH"

    if raw_matched and len(str(raw_matched)) > 5:
        return "HIGH"

    if isinstance(val, str) and len(val) > 10:
        return "MEDIUM"

    if isinstance(val, list) and len(val) > 0:
        return "HIGH"

    return "LOW"
