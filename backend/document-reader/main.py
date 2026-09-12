from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from tender_parser import parse_tender_document
from gem_scraper import scan_real_gem_portal

app = FastAPI(title="GeM Intel Document Intelligence Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ParseRequest(BaseModel):
    document_url: Optional[str] = None
    tender_id: Optional[str] = None
    b_id: Optional[str] = None
    sample_text: Optional[str] = None
    consignee_box: Optional[str] = None
    existing_consignee: Optional[str] = None
    existing_city: Optional[str] = None
    existing_state: Optional[str] = None
    existing_pincode: Optional[str] = None
    existing_address: Optional[str] = None
    existing_department: Optional[str] = None
    existing_value: Optional[float] = None
    existing_emd: Optional[float] = None

class ScanRequest(BaseModel):
    date: Optional[str] = None
    type: Optional[str] = "published" # 'published' | 'finished'
    state: Optional[str] = "ALL"

@app.get("/")
def read_root():
    return {"status": "ACTIVE", "service": "GeMIntel Python Document Reader & Live Scraper Microservice"}

@app.get("/api/diagnostic")
@app.post("/api/diagnostic")
def run_diagnostic_endpoint():
    try:
        import json
        from run_source_diagnostic import run_diagnostic
        run_diagnostic()
        with open("gem_source_diagnostic_results.json", "r") as f:
            data = json.load(f)
        return {"success": True, "diagnostic": data}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/scan")
@app.post("/api/scan")
def scan_tenders_endpoint(req: ScanRequest):
    scan_type = (req.type or "published").lower()
    res = scan_real_gem_portal(req.date, req.state, None, scan_type.upper())

    return {
        "success": res.get("status") in ("success", "SOURCE_REACHABLE_ZERO"),
        "type": scan_type,
        "date": req.date,
        "state": req.state,

        "status": res.get("status"),
        "sourceVerified": res.get("sourceVerified", res.get("status") in ("success", "SOURCE_REACHABLE_ZERO")),
        "queryVerified": res.get("queryVerified", False),
        "paginationComplete": res.get("paginationComplete", False),
        "dateFilterVerified": res.get("dateFilterVerified", False),

        "sourceTotal": res.get("sourceTotal"),
        "queryTotal": res.get("total", 0),

        "pagesProcessed": res.get("pagesProcessed", 0),
        "recordsRetrieved": res.get("recordsRetrieved", 0),
        "validRecords": res.get("validRecords", 0),
        "duplicatesRemoved": res.get("duplicatesRemoved", 0),
        "dateMatches": res.get("dateMatches", 0),
        "dateMismatches": res.get("dateMismatches", 0),

        "finalMatchingRecords": res.get("total", 0),
        "stop_reason": res.get("stop_reason"),
        "gemNumFound": res.get("gemNumFound"),
        "safetyMaxPages": res.get("safetyMaxPages"),
        "closingTodayCount": res.get("closingTodayCount", 0),
        "endedCount": res.get("endedCount", 0),
        "count": len(res.get("data", [])),
        "bids": res.get("data", []),

        "scan_error": res.get("scan_error")
    }

def fetch_pdf_text_from_gem(tender_id, document_url=None, b_id=None):
    """
    Downloads and extracts all text from the official GeM Tender PDF copy.
    Tries document_url, b_id (internal ID), and tender_id tail.
    """
    try:
        import requests, fitz
        raw_id = (tender_id or "").split("/")[-1].strip()
        candidates = []
        if document_url:
            candidates.append(document_url)
        if b_id:
            candidates.append(f"https://bidplus.gem.gov.in/showbidDocument/{b_id}")
        if raw_id:
            candidates.append(f"https://bidplus.gem.gov.in/showbidDocument/{raw_id}")

        for url in candidates:
            try:
                res = requests.get(url, verify=False, timeout=10)
                if res.status_code == 200 and len(res.content) > 1000:
                    doc = fitz.open(stream=res.content, filetype="pdf")
                    text = ""
                    for p in doc:
                        text += p.get_text() + "\n"
                    if len(text.strip()) > 50:
                        return text
            except Exception:
                pass
    except Exception as ex:
        print(f"[PDF Fetcher Error] {ex}")
    return None

@app.post("/parse")
@app.post("/api/documents/parse")
def parse_document(req: ParseRequest):
    pdf_text = None
    if req.tender_id or req.document_url or req.b_id:
        pdf_text = fetch_pdf_text_from_gem(req.tender_id, req.document_url, req.b_id)

    raw_text = req.sample_text or pdf_text
    if not raw_text:
        box_str = req.consignee_box or f"{req.existing_consignee or 'Consignee Officer'}, {req.existing_address or 'Government Office'}"
        raw_text = f"""
        Bid Number: {req.tender_id or 'GEM/2026/B/8015751'}
        Estimated Bid Value: {req.existing_value or 'As per Minimum Wages'}
        EMD Amount: {req.existing_emd or 'As per GeM Portal Rules'}
        Consignee Reporting/Officer: {req.existing_consignee or 'Consignee Officer'}
        Address: {req.existing_pincode or '382010'},{req.existing_address or 'Government Office'}
        {box_str}
        """

    parsed_json = parse_tender_document(raw_text, req.tender_id)

    # Preserve high-confidence verified existing tender fields if not present in partial parse
    if req.existing_consignee and req.existing_consignee != 'Consignee / Reporting Officer' and (not parsed_json.get('consignee_officer') or parsed_json.get('consignee_officer') == 'Consignee / Reporting Officer'):
        parsed_json['consignee_officer'] = req.existing_consignee
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['consignee_officer'] = req.existing_consignee
        if parsed_json.get('workLocation'): parsed_json['workLocation']['consignee_officer'] = req.existing_consignee

    if req.existing_city and (not parsed_json.get('city') or parsed_json.get('city') in ('Not Specified', 'Gandhinagar', 'New Delhi')):
        parsed_json['city'] = req.existing_city
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['city'] = req.existing_city
        if parsed_json.get('workLocation'): parsed_json['workLocation']['city'] = req.existing_city

    if req.existing_state and (not parsed_json.get('state') or parsed_json.get('state') in ('Not Specified', 'Gujarat', 'Delhi')):
        parsed_json['state'] = req.existing_state
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['state'] = req.existing_state
        if parsed_json.get('workLocation'): parsed_json['workLocation']['state'] = req.existing_state

    if req.existing_pincode and (not parsed_json.get('pincode') or parsed_json.get('pincode') == 'Not Specified'):
        parsed_json['pincode'] = req.existing_pincode
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['pincode'] = req.existing_pincode
        if parsed_json.get('workLocation'): parsed_json['workLocation']['pincode'] = req.existing_pincode

    if req.existing_address and (not parsed_json.get('address') or 'Central Procurement' in str(parsed_json.get('address'))):
        parsed_json['address'] = req.existing_address
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['value'] = req.existing_address
        if parsed_json.get('workLocation'): parsed_json['workLocation']['address'] = req.existing_address

    if req.consignee_box:
        if parsed_json.get('officeAddress'): parsed_json['officeAddress']['raw_consignee_box'] = req.consignee_box
        if parsed_json.get('workLocation'): parsed_json['workLocation']['raw_consignee_box'] = req.consignee_box

    return parsed_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
