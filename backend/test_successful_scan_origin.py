import requests

def test_successful_scan_origin():
    print("==================================================")
    print("      TESTING SUCCESSFUL SCAN DATA ORIGIN & METRICS")
    print("==================================================")

    login_url = "http://localhost:5000/api/auth/login"
    login_payload = {"email": "chaudharianshu0706@gmail.com", "password": "Anshu@2746"}
    sess = requests.Session()
    res = sess.post(login_url, json=login_payload)
    if res.status_code != 200:
        login_payload = {"email": "admin@gemintel.com", "password": "admin123"}
        res = sess.post(login_url, json=login_payload)

    token = res.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}

    # Query current scan: Date: 2026-08-11, PUBLISHED, ALL, ALL
    url = "http://localhost:5000/api/tenders?selectedDate=2026-08-11&status=PUBLISHED&state=ALL&services=ALL"
    r = sess.get(url, headers=headers).json()

    print("--- SUCCESSFUL SCAN RESPONSE METRICS ---")
    print(f"Scan ID: {r.get('scan', {}).get('scanId')}")
    print(f"Scan Status: {r.get('scan', {}).get('status')}")
    print(f"Source Verified: {r.get('scan', {}).get('sourceVerified')}")
    print(f"Source Query Total: {r.get('sourceQueryTotal')}")
    print(f"Records Retrieved: {r.get('recordsRetrieved')}")
    print(f"Valid Records: {r.get('validRecords')}")
    print(f"Duplicates Removed: {r.get('duplicatesRemoved')}")
    print(f"Current Query Matching Count: {r.get('matchingCount')}")
    print(f"Preserved Historical Database Count: {r.get('historicalCount')}")
    print(f"Returned Tenders Array Length: {len(r.get('tenders', []))}\n")

    tenders = r.get('tenders', [])
    if tenders:
        print(f"First Tender Bid Number: {tenders[0].get('id')}")
        print(f"First Tender Data Origin: {tenders[0].get('dataOrigin')}")
        print(f"First Tender Scan ID: {tenders[0].get('scanId')}\n")

    assert r.get('scan', {}).get('status') == 'COMPLETED'
    assert r.get('matchingCount') == 187
    assert len(tenders) == 187
    assert r.get('historicalCount') == 380
    assert r.get('matchingCount') != r.get('historicalCount')

    print("==================================================")
    print("  SUCCESSFUL SCAN METRICS TEST PASSED (MATCHING: 187, HISTORICAL: 380)")
    print("==================================================")

if __name__ == "__main__":
    test_successful_scan_origin()
