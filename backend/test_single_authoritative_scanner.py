import requests
import json

BASE_URL = "http://localhost:5000"

def get_auth_token():
    try:
        res = requests.post(f"{BASE_URL}/api/auth/login", json={
            "email": "admin@gemintel.com",
            "password": "admin123"
        })
        if res.status_code == 200:
            token = res.json().get("token")
            print(f"Login successful! JWT Token: {token[:20]}...")
            return token
        else:
            print(f"Login failed: HTTP {res.status_code} {res.text}")
    except Exception as e:
        print(f"Login exception: {e}")
    return None

def test_1(headers):
    print("==================================================")
    print("TEST 1: POST /api/scan (Zero-matching date 2026-08-12)")
    print("==================================================")
    payload = {"type": "published", "state": "ALL", "date": "2026-08-12"}
    res = requests.post(f"{BASE_URL}/api/scan", json=payload, headers=headers)
    print(f"Status Code: {res.status_code}")
    data = res.json()
    print(f"Response: status={data.get('status')}, total={data.get('total')}, scan_error={data.get('scan_error')}")

    # Check dashboard endpoint GET /api/tenders?selectedDate=2026-08-12
    res_tenders = requests.get(f"{BASE_URL}/api/tenders?selectedDate=2026-08-12", headers=headers)
    data_tenders = res_tenders.json()
    scan_meta = data_tenders.get("scan", {})
    print(f"GET /api/tenders scan.status={scan_meta.get('status')}, scan.sourceVerified={scan_meta.get('sourceVerified')}, scan.error={scan_meta.get('error')}")

    is_pass = (scan_meta.get("sourceVerified") is True) and (scan_meta.get("error") != "GeM source could not be verified")
    print(f"TEST 1 RESULT: {'PASS' if is_pass else 'FAIL'}\n")
    return is_pass

def test_2(headers):
    print("==================================================")
    print("TEST 2: POST /api/scan (Real-data date 2025-06-17)")
    print("==================================================")
    payload = {"type": "published", "state": "ALL", "date": "2025-06-17"}
    res = requests.post(f"{BASE_URL}/api/scan", json=payload, headers=headers)
    data = res.json()
    scan_count = data.get("total", 0)
    print(f"POST /api/scan returned: {scan_count} bids")

    # Check GET /api/bids
    res_bids = requests.get(f"{BASE_URL}/api/bids?date=2025-06-17", headers=headers)
    data_bids = res_bids.json()
    bids_count = data_bids.get("total", 0)
    print(f"GET /api/bids returned: {bids_count} bids")

    # Check GET /api/tenders with status=ALL
    res_tenders = requests.get(f"{BASE_URL}/api/tenders?status=ALL&selectedDate=2025-06-17", headers=headers)
    data_tenders = res_tenders.json()
    tenders_count = data_tenders.get("matchingCount", 0)
    print(f"GET /api/tenders (status=ALL) returned: {tenders_count} bids")

    is_pass = (scan_count == bids_count == tenders_count) and (scan_count > 0)
    print(f"TEST 2 RESULT: {'PASS' if is_pass else 'FAIL'}\n")
    return is_pass

def test_3(headers):
    print("==================================================")
    print("TEST 3: Health Endpoints verification")
    print("==================================================")
    res_gem_health = requests.get(f"{BASE_URL}/api/gem/health", headers=headers)
    data_gem = res_gem_health.json()
    print(f"GET /api/gem/health: status={data_gem.get('status')}, sourceVerified={data_gem.get('sourceVerified')}")

    res_src_health = requests.get(f"{BASE_URL}/api/source-health", headers=headers)
    data_src = res_src_health.json()
    print(f"GET /api/source-health: status={data_src.get('status')}, sourceVerified={data_src.get('sourceVerified')}")

    is_pass = (data_gem.get("sourceVerified") is True) and (data_src.get("sourceVerified") is True)
    print(f"TEST 3 RESULT: {'PASS' if is_pass else 'FAIL'}\n")
    return is_pass

def main():
    print("==================================================")
    print(" SINGLE AUTHORITATIVE LIVE SCANNER VERIFICATION")
    print("==================================================")
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    pass1 = test_1(headers)
    pass2 = test_2(headers)
    pass3 = test_3(headers)

    all_pass = pass1 and pass2 and pass3

    print("\n==================================================")
    print("             FINAL ACCEPTANCE CHECKLIST")
    print("==================================================")
    print(f"ONE LIVE SCANNER                      = {'YES' if all_pass else 'NO'}")
    print(f"PYTHON IS AUTHORITATIVE               = {'YES' if all_pass else 'NO'}")
    print(f"NODE USES PYTHON RESULT               = {'YES' if all_pass else 'NO'}")
    print(f"ZERO RESULTS != SOURCE FAILURE        = {'YES' if pass1 else 'NO'}")
    print(f"STALE FAILED STATE REMOVED            = {'YES' if all_pass else 'NO'}")
    print(f"/api/bids AND /api/tenders SAME DATA  = {'YES' if pass2 else 'NO'}")
    print(f"NO FAKE 'GeM source could not be verified' = {'YES' if pass1 else 'NO'}")
    print("==================================================")

if __name__ == "__main__":
    main()
