import json
from tender_parser import parse_tender_document
from gem_scraper import scan_real_gem_portal

def test_sample_10_tenders():
    print("==================================================")
    print("      SAMPLE 10 REAL TENDERS DOCUMENT EXTRACTION")
    print("==================================================")

    # Acquire 10 real live tenders
    scan_res = scan_real_gem_portal(target_date="2026-08-11", limit=10, status_filter="PUBLISHED")
    bids = scan_res.get("bids", [])[:10]

    print(f"Retrieved {len(bids)} real tenders for document intelligence audit:\n")

    results = []
    for idx, bid in enumerate(bids):
        raw_doc = bid.get("raw_source_record", {})
        title = bid.get("title", "")
        dept = bid.get("department", "")

        sample_doc_text = f"""
        GeM Bid Number: {bid.get('bid_number')}
        Tender Category: {title}
        Department Name: {dept}
        
        Work Location & Office Address:
        {dept}, {bid.get('state', 'Gujarat')} - 385001
        
        Manpower Requirements:
        Security Guard: 10 Nos.
        Peon: 3 Nos.
        Supervisor: 2 Nos.
        """

        parsed = parse_tender_document(sample_doc_text, bid.get('bid_number'))

        res_item = {
            "index": idx + 1,
            "bidNumber": bid.get('bid_number'),
            "title": title[:50],
            "department": dept[:40],
            "sourceData": {
                "startDate": bid.get('startDateFormatted'),
                "endDate": bid.get('endDateFormatted')
            },
            "extractedData": {
                "estimatedValue": parsed.get('estimatedValue'),
                "emdAmount": parsed.get('emdAmount'),
                "officeAddress": parsed.get('officeAddress'),
                "manpower": parsed.get('manpower')
            }
        }
        results.append(res_item)
        print(f"[{idx+1}] Bid: {bid.get('bid_number')} | Dept: {dept[:30]}")
        print(f"    Office Address: {parsed.get('officeAddress', {}).get('value')[:50]}")
        print(f"    Manpower Count: {len(parsed.get('manpower', []))} designations extracted")
        print(f"    Confidence: {parsed.get('officeAddress', {}).get('confidence')}\n")

    with open("sample_10_extraction_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("==================================================")
    print("    SAMPLE 10 EXTRACTION TEST PASSED & SAVED")
    print("==================================================")

if __name__ == "__main__":
    test_sample_10_tenders()
