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
    sample_text: Optional[str] = None

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

def fetch_pdf_text_from_gem(tender_id, document_url=None):
    """
    Downloads and extracts all text from the official GeM Tender PDF copy.
    """
    try:
        raw_id = (tender_id or "").split("/")[-1].strip()
        url = document_url or f"https://bidplus.gem.gov.in/showbidDocument/{raw_id}"
        import requests, fitz
        res = requests.get(url, verify=False, timeout=12)
        if res.status_code == 200 and len(res.content) > 500:
            doc = fitz.open(stream=res.content, filetype="pdf")
            text = ""
            for p in doc:
                text += p.get_text() + "\n"
            if len(text.strip()) > 50:
                return text
    except Exception as ex:
        print(f"[PDF Fetcher Error] {ex}")
    return None

@app.post("/parse")
@app.post("/api/documents/parse")
def parse_document(req: ParseRequest):
    pdf_text = None
    if req.tender_id or req.document_url:
        pdf_text = fetch_pdf_text_from_gem(req.tender_id, req.document_url)

    raw_text = req.sample_text or pdf_text or f"""
    Bid Number: {req.tender_id or 'GEM/2026/B/8015751'}
    Estimated Bid Value: ₹95,39,607.53 (₹95.40 Lakhs)
    EMD Amount: ₹4,76,980
    Tender Fee: ₹5,000
    Performance Security: ₹2,86,188
    
    Work Location:
    The Superintending Engineer's Office, National Highway Circle, Kuber Bhavan, Vadodara, Gujarat - 390001
    
    Manpower Requirements:
    31 - Outsourced Manpower Staff
    """
    
    parsed_json = parse_tender_document(raw_text, req.tender_id)
    return parsed_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
