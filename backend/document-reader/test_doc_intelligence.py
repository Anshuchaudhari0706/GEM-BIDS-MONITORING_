import json
from tender_parser import parse_tender_document
from pdf_reader import extract_text_from_pdf_bytes

def test_document_intelligence():
    print("==================================================")
    print("      TESTING TENDER DOCUMENT INTELLIGENCE")
    print("==================================================")

    sample_text = """
    GeM Bid Number: GEM/2026/B/7821202
    Tender Title: Custom Bid for Services - Security Guard and Peon Requirements
    
    Estimated Tender Value: Rs. 25,00,000 (INR 25 Lakhs)
    Earnest Money Deposit (EMD): ₹50,000
    
    Office Address & Work Location:
    District Collector Office, Station Road, Palanpur, Banaskantha, Gujarat - 385001
    
    Schedule of Manpower Requirements:
    1. Security Guard - 10 Nos.
    2. Security Supervisor - 2 Nos.
    3. Peon - 3 Nos.
    4. Housekeeping Staff - 5 Nos.
    
    Closing Date: 12/08/2026
    """

    res = parse_tender_document(sample_text, "GEM/2026/B/7821202")
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    test_document_intelligence()
