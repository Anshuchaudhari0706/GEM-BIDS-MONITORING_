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
    res = scan_real_gem_portal(req.date, req.state, 500, scan_type.upper())

    return {
        "success": res.get("status") == "success",
        "type": scan_type,
        "date": req.date,
        "state": req.state,

        "status": res.get("status"),
        "sourceVerified": res.get("sourceVerified", False),
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
        "count": len(res.get("data", [])),
        "bids": res.get("data", []),

        "scan_error": res.get("scan_error")
    }

@app.post("/parse")
@app.post("/api/documents/parse")
def parse_document(req: ParseRequest):
    raw_text = req.sample_text or f"""
    Bid Number: {req.tender_id or 'GEM/2026/B/7821202'}
    Estimated Bid Value: ₹25,00,000 (₹25 Lakhs)
    EMD Amount: ₹50,000
    Tender Fee: ₹5,000
    Performance Security: ₹1,25,000
    
    Work Location:
    District Collector Office, Station Road, Palanpur, Banaskantha, Gujarat - 385001
    
    Manpower Requirements:
    10 - Security Guard (3 Shift, 8 Hours)
    2 - Security Supervisor (General, 8 Hours)
    3 - Peon (General, 8 Hours)
    5 - Housekeeping Staff (2 Shift, 8 Hours)
    
    Closing Date: 10/08/2026
    Closing Time: 18:00
    """
    
    parsed_json = parse_tender_document(raw_text, req.tender_id)
    return parsed_json

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
