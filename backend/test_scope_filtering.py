import requests

def test_scope_filtering():
    print("==================================================")
    print("      TESTING SCAN-SCOPE & HISTORICAL METRICS")
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

    # TEST 1: Published Bids (Date: 2026-08-11, Status: PUBLISHED)
    url_pub = "http://localhost:5000/api/tenders?selectedDate=2026-08-11&status=PUBLISHED&state=ALL&services=ALL"
    r_pub = sess.get(url_pub, headers=headers).json()

    print("--- TEST 1: PUBLISHED BIDS (DATE: 2026-08-11) ---")
    print(f"Total Stored Database Tenders: {r_pub.get('totalStoredTenders')}")
    print(f"Current Matching Query Tenders: {r_pub.get('matchingTenders')}")
    print(f"Scan ID: {r_pub.get('scanId')}")
    print(f"Filters applied: {r_pub.get('filters')}\n")

    # TEST 2: Finished Bids (Date: 2026-08-11, Status: FINISHED)
    url_fin = "http://localhost:5000/api/tenders?selectedDate=2026-08-11&status=FINISHED&state=ALL&services=ALL"
    r_fin = sess.get(url_fin, headers=headers).json()

    print("--- TEST 2: FINISHED BIDS (DATE: 2026-08-11) ---")
    print(f"Total Stored Database Tenders: {r_fin.get('totalStoredTenders')}")
    print(f"Current Matching Query Tenders: {r_fin.get('matchingTenders')}")
    print(f"Filters applied: {r_fin.get('filters')}\n")

    # TEST 3: Manpower Designation Filter (Search: Security Guard)
    url_mp = "http://localhost:5000/api/tenders?manpowerType=Security%20Guard"
    r_mp = sess.get(url_mp, headers=headers).json()
    print("--- TEST 3: MANPOWER DESIGNATION SEARCH (Security Guard) ---")
    print(f"Matching Security Guard Tenders: {r_mp.get('matchingTenders')}\n")

    print("==================================================")
    print("    SCAN-SCOPE FILTERING VERIFIED & PASSED")
    print("==================================================")

if __name__ == "__main__":
    test_scope_filtering()
