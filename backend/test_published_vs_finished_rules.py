import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def get_auth_token():
    try:
        res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "admin@gemintel.com",
            "password": "admin123"
        })
        if res.status_code == 200:
            return res.json().get("token")
    except Exception as e:
        print(f"Login failed: {e}")
    return None

def test_published_rules(headers):
    print("==================================================")
    print("PUBLISHED TENDERS RULE TEST (date = 2025-06-17)")
    print("==================================================")
    scan_res = requests.post(f"{BASE_URL}/api/scan", json={
        "type": "published", "state": "ALL", "date": "2025-06-17"
    }, headers=headers)
    scan_data = scan_res.json()
    print(f"POST /api/scan (published) status={scan_data.get('status')}, total={scan_data.get('total')}")

    res = requests.get(f"{BASE_URL}/api/tenders?status=PUBLISHED&selectedDate=2025-06-17", headers=headers)
    data = res.json()
    tenders = data.get("tenders", [])
    print(f"GET /api/tenders (PUBLISHED) returned: {len(tenders)} bids")

    date_mismatches = [t for t in tenders if t.get("publishedDate") != "2025-06-17"]
    print(f"Published Date Mismatches: {len(date_mismatches)}")

    is_pass = (len(tenders) > 0) and (len(date_mismatches) == 0)
    print(f"PUBLISHED RULE RESULT: {'PASS' if is_pass else 'FAIL'}\n")
    return is_pass

def test_finished_rules(headers):
    print("==================================================")
    print("FINISHED TENDERS RULE TEST (date = 2025-07-08)")
    print("==================================================")
    scan_res = requests.post(f"{BASE_URL}/api/scan", json={
        "type": "finished", "state": "ALL", "date": "2025-07-08"
    }, headers=headers)
    scan_data = scan_res.json()
    print(f"POST /api/scan (finished) status={scan_data.get('status')}, total={scan_data.get('total')}")

    res = requests.get(f"{BASE_URL}/api/tenders?status=FINISHED&selectedDate=2025-07-08", headers=headers)
    data = res.json()
    tenders = data.get("tenders", [])
    scan_meta = data.get("scan", {})
    print(f"GET /api/tenders (FINISHED) returned: {len(tenders)} bids")

    deadline_mismatches = [t for t in tenders if t.get("deadline") != "2025-07-08"]
    print(f"Deadline Mismatches: {len(deadline_mismatches)}")

    closing_today = [t for t in tenders if t.get("status") == "CLOSING_TODAY"]
    ended = [t for t in tenders if t.get("status") == "ENDED"]

    print(f"CLOSING TODAY:  {len(closing_today)}")
    print(f"ALREADY ENDED:  {len(ended)}")
    print(f"FINISHED TOTAL: {len(tenders)}")

    is_pass = (len(tenders) > 0) and (len(deadline_mismatches) == 0) and (len(closing_today) + len(ended) == len(tenders))
    print(f"FINISHED RULE RESULT: {'PASS' if is_pass else 'FAIL'}\n")
    return is_pass

def main():
    print("==================================================")
    print("   PUBLISHED vs FINISHED TENDERS BUSINESS RULES TEST")
    print("==================================================")
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    pass_pub = test_published_rules(headers)
    pass_fin = test_finished_rules(headers)

    all_pass = pass_pub and pass_fin

    print("==================================================")
    print("             FINAL ACCEPTANCE CHECKLIST")
    print("==================================================")
    print(f"PUBLISHED TENDERS RULE (publishedDate == selectedDate) = {'PASS' if pass_pub else 'FAIL'}")
    print(f"FINISHED TENDERS RULE (deadlineDate == selectedDate)  = {'PASS' if pass_fin else 'FAIL'}")
    print(f"CLOSING TODAY & ENDED CLASSIFICATION                 = {'PASS' if pass_fin else 'FAIL'}")
    print(f"FINISHED TOTAL = CLOSING TODAY + ENDED               = {'PASS' if pass_fin else 'FAIL'}")
    print("==================================================")

if __name__ == "__main__":
    main()
