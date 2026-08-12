import os

def create_codebase_text_file():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(root_dir, "FULL_PROJECT_CODEBASE.txt")

    files_to_include = [
        ("backend/document-reader/gem_scraper.py", "PYTHON LIVE GE M SCRAPER & PARSER ENGINE"),
        ("backend/document-reader/main.py", "FASTAPI DOCUMENT READER & SCANNER MICROSERVICE"),
        ("backend/document-reader/tender_parser.py", "MASTER TENDER DOCUMENT PARSER"),
        ("backend/document-reader/pdf_reader.py", "PDF TEXT EXTRACTION & OCR FALLBACK ENGINE"),
        ("backend/document-reader/regex_parser.py", "REGEX FIELD EXTRACTION MODULE"),
        ("backend/document-reader/normalizer.py", "VALUE & CURRENCY NORMALIZER MODULE"),
        ("backend/document-reader/validators.py", "EXTRACTION CONFIDENCE VALIDATOR"),
        ("backend/server.js", "NODE EXPRESS API SERVER"),
        ("backend/test_gem_live_scanner.py", "LIVE GE M SCANNER DEBUG TEST SUITE"),
        ("backend/test_gem_payload_investigation.py", "GE M API PAGINATION PAYLOAD TEST"),
        ("backend/test_inspect_real_bids.py", "REAL GE M BIDS MULTI-PAGE AUDIT TEST"),
        ("backend/test_api_bids_suite.py", "API /bids, /scan, /status SUITE TEST"),
        ("backend/test_post_scan.py", "POST /api/scan LIVE TRIGGER TEST"),
        ("frontend/src/config/constants.js", "FRONTEND CONSTANTS & MAPPINGS"),
        ("frontend/src/services/api.js", "FRONTEND API CLIENT SERVICE")
    ]

    with open(output_path, "w", encoding="utf-8") as out:
        out.write("================================================================================\n")
        out.write("             GeM TENDER INTELLIGENCE — FULL PROJECT CODEBASE TEXT FILE\n")
        out.write("================================================================================\n")
        out.write("Repository: https://github.com/Anshuchaudhari0706/GEM-BIDS-MONITORING_.git\n")
        out.write("Branch:     23012011008_Anshu\n")
        out.write("Generated:  2026-08-12\n")
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
