import os

def create_codebase_text_file():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_dir, "FULL_PROJECT_CODEBASE.txt")

    files_to_include = [
        # --- BACKEND CONNECTOR & SCRAPER ---
        ("backend/document-reader/gem_scraper.py", "PYTHON LIVE GE M SCRAPER, SESSION TOKEN & DATE VALIDATION ENGINE"),
        ("backend/document-reader/main.py", "FASTAPI DOCUMENT READER & SCANNER MICROSERVICE"),
        ("backend/document-reader/tender_parser.py", "UNIFIED MASTER TENDER DOCUMENT PARSER"),
        ("backend/document-reader/pdf_reader.py", "PDF TEXT EXTRACTION & TESSERACT OCR ENGINE"),
        ("backend/document-reader/regex_parser.py", "REGEX FIELD EXTRACTION MODULE"),
        ("backend/document-reader/normalizer.py", "NUMERIC & CURRENCY NORMALIZER MODULE"),
        ("backend/document-reader/validators.py", "EXTRACTION CONFIDENCE EVALUATOR"),
        ("backend/server.js", "NODE EXPRESS PRODUCTION API SERVER"),

        # --- TEST & VERIFICATION SUITES ---
        ("backend/test_exact_20260812_date_verification.py", "EXACT 2026-08-12 DATE VERIFICATION SUITE"),
        ("backend/test_final_real_data_verification.py", "FINAL REAL-DATA VERIFICATION SUITE"),
        ("backend/test_gem_live_scraper.py", "LIVE GE M SCANNER DEBUG TEST SUITE"),
        ("backend/test_gem_payload_investigation.py", "PAGINATION PAYLOAD INVESTIGATION SUITE"),
        ("backend/test_inspect_real_bids.py", "MULTI-PAGE 1,000 REAL BIDS AUDIT SUITE"),
        ("backend/test_inspect_raw_keys.py", "SOLR RAW DOCUMENT KEYS INSPECTOR"),
        ("backend/test_api_bids_suite.py", "API /bids, /scan, /status SUITE TEST"),
        ("backend/test_post_scan.py", "POST /api/scan LIVE TRIGGER TEST"),

        # --- FRONTEND REACT APP ---
        ("frontend/src/App.jsx", "REACT ROOT APPLICATION COMPONENT & ROUTER"),
        ("frontend/src/main.jsx", "REACT VITE ENTRY POINT"),
        ("frontend/src/index.css", "GLOBAL TAILWIND & VANILLA CSS DESIGN SYSTEM"),
        ("frontend/src/config/constants.js", "INDIAN STATES & MANPOWER CONSTANTS"),
        ("frontend/src/services/api.js", "AXIOS API CLIENT SERVICE"),
        ("frontend/src/components/Navbar.jsx", "NAVBAR NAVIGATION HEADER"),
        ("frontend/src/components/TenderCard.jsx", "TENDER CARD COMPONENT WITH MANPOWER & PDF STATUS"),
        ("frontend/src/components/TenderFilters.jsx", "TENDER FILTERS PANEL (DATE, STATE, MANPOWER)"),
        ("frontend/src/components/TenderModal.jsx", "TENDER DETAILS MODAL POPUP"),
        ("frontend/src/components/StatsOverview.jsx", "DASHBOARD STATS OVERVIEW CARDS"),
        ("frontend/src/pages/Dashboard.jsx", "MAIN DASHBOARD PAGE"),
        ("frontend/src/pages/Login.jsx", "AUTHENTICATION LOGIN PAGE")
    ]

    with open(output_path, "w", encoding="utf-8") as out:
        out.write("================================================================================\n")
        out.write("             GeM TENDER INTELLIGENCE — COMPLETE APPLICATION CODEBASE\n")
        out.write("================================================================================\n")
        out.write("Repository: https://github.com/Anshuchaudhari0706/GEM-BIDS-MONITORING_.git\n")
        out.write("Branch:     23012011008_Anshu\n")
        out.write("Generated:  2026-08-13\n")
        out.write("================================================================================\n\n")

        for rel_path, desc in files_to_include:
            abs_path = os.path.join(root_dir, rel_path)
            out.write("--------------------------------------------------------------------------------\n")
            out.write(f"FILE: {rel_path}\n")
            out.write(f"DESCRIPTION: {desc}\n")
            out.write("--------------------------------------------------------------------------------\n")

            if os.path.exists(abs_path):
                with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                out.write(content)
            else:
                out.write(f"[FILE NOT FOUND: {abs_path}]\n")

            out.write("\n\n")

        out.write("================================================================================\n")
        out.write("                         END OF FULL CODEBASE TEXT FILE\n")
        out.write("================================================================================\n")

    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_codebase_text_file()
