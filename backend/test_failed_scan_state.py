import requests

def test_failed_scan_state():
    print("==================================================")
    print("      TESTING FAILED SCAN STATE & ZERO FALLBACK")
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

    # TEST: Scan failure simulation (forceFail=true)
    url_fail = "http://localhost:5000/api/tenders?status=FINISHED&selectedDate=2026-08-10&forceFail=true"
    r_fail = sess.get(url_fail, headers=headers).json()

    print("--- FAILED SCAN RESPONSE METRICS ---")
    print(f"Scan Status: {r_fail.get('scan', {}).get('status')}")
    print(f"Source Verified: {r_fail.get('scan', {}).get('sourceVerified')}")
    print(f"Error Message: {r_fail.get('scan', {}).get('error')}")
    print(f"Current Matching Count: {r_fail.get('matchingCount')}")
    print(f"Current Tenders Array Length: {len(r_fail.get('tenders', []))}")
    print(f"Preserved Historical Database Count: {r_fail.get('historicalCount')}\n")

    assert r_fail.get('scan', {}).get('status') == 'FAILED'
    assert r_fail.get('matchingCount') == 0
    assert len(r_fail.get('tenders', [])) == 0
    assert r_fail.get('historicalCount') == 380

    print("==================================================")
    print("  FAILED SCAN STATE TEST PASSED (ZERO FALLBACK)")
    print("==================================================")

if __name__ == "__main__":
    test_failed_scan_state()
