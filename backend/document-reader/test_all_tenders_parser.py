import sys
import os
import json

doc_dir = os.path.dirname(__file__)
sys.path.insert(0, doc_dir)
from tender_parser import parse_tender_document

test_samples = [
    {
        "id": "GEM/2026/B/8015751",
        "name": "Official Bilingual GeM Tender (Patan / Bank of Baroda)",
        "text": """
        बिड विवरण/Bid Details
        मूल्य दर्शाने वाला वित्तीय दस्तावेज ब्रेकअप आवश्यक है / Financial Document Indicating Price Breakup Required Yes
        अनुमानित निविदा मूल्य (सभी करों सहित) भारतीय रुपये में / Estimated Bid Value in INR (Inclusive of all taxes) 2182197
        ईएमडी विवरण/EMD Detail
        एडवाइजरी बैंक/Advisory Bank Bank Of Baroda
        ईएमडी राशि/EMD Amount 65466

        परेषिती/रिपोर्टिंग अधिकारी /Consignees/Reporting Officer and Quantity
        क्र.सं./S.No. परेषिती/रिपोर्टिंग अधिकारी /Consignee Reporting/Officer पता/Address संसाधनों की मात्रा / Area in Sq. Metre अतिरिक्त आवश्यकता /Additional Requirement
        1
        Parth Mahendrakumar Patel
        384265,District Deputy Director(Cl-I), Scheduled Caste Welfare's Office, Block No.2, 1st Floor, Central Office Bhavan, Rajmahal Rd., Patan, Dist. Patan Phone:02766-226782
        1250
        """
    },
    {
        "id": "GEM/2026/B/7981122",
        "name": "Standard PWD GeM Tender (Jaipur / SBI)",
        "text": """
        Bid Number: GEM/2026/B/7981122
        Estimated Bid Value in INR (Inclusive of all taxes): Rs. 45,50,000
        Advisory Bank: State Bank of India
        EMD Amount: Rs. 1,36,500
        Consignee Reporting/Officer: Ramesh Chandra Sharma
        Address: 302005,Executive Engineer, PWD Office, Tonk Road, Jaipur, Rajasthan Phone:0141-2740001
        """
    },
    {
        "id": "GEM/2026/B/7821202",
        "name": "Vadodara National Highway Tender (Punjab National Bank)",
        "text": """
        Bid Number: GEM/2026/B/7821202
        Estimated Bid Value: 9539607.53
        Advisory Bank: Punjab National Bank
        EMD Amount: 286188
        390001,The Superintending Engineer's Office,National Highway Circle,712 & 713,7th floor, E-block,Kuber Bhavan,Kothi char rasta,Raopura,vadodara
        """
    }
]

results = []
for s in test_samples:
    res = parse_tender_document(s["text"], s["id"])
    results.append({
        "name": s["name"],
        "bidNumber": res["bidNumber"],
        "consignee_officer": res["consignee_officer"],
        "city": res["city"],
        "state": res["state"],
        "pincode": res["pincode"],
        "address": res["address"],
        "estimatedValue": res["estimatedValue"]["value"],
        "emdAmount": res["emdAmount"]["value"],
        "advisoryBank": res["advisoryBank"]
    })

print(json.dumps(results, indent=2))
