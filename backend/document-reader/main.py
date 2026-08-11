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

@app.post("/scan")
@app.post("/api/scan")
def scan_tenders_endpoint(req: ScanRequest):
    scan_type = (req.type or "published").lower()
    bids = scan_real_gem_portal(req.date, req.state, 50, scan_type.upper())

    return {
        "success": True,
        "type": scan_type,
        "date": req.date,
        "state": req.state,
        "count": len(bids),
        "bids": bids
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
