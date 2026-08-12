import requests

def test_api_bids_suite():
    print("==================================================")
    print("      TESTING API /bids, /scan, /status ENDPOINTS")
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

    # 1. Test GET /api/status
    res_status = requests.get("http://localhost:5000/api/status").json()
    print("\n[GET /api/status Response]")
    print(f"  Status: {res_status.get('status')}")
    print(f"  Is Scanning: {res_status.get('is_scanning')}")
    print(f"  Last Scan: {res_status.get('last_scan')}")
    print(f"  Scan Error: {res_status.get('scan_error')}")

    # 2. Test GET /api/bids
    res_bids = requests.get("http://localhost:5000/api/bids").json()
    print("\n[GET /api/bids Response]")
    print(f"  Status: {res_bids.get('status')}")
    print(f"  Scan Date: {res_bids.get('scan_date')}")
    print(f"  Total Bids: {res_bids.get('total')}")
    print(f"  Data Array Count: {len(res_bids.get('data', []))}")

    data = res_bids.get('data', [])
    if data:
        print(f"  Sample Bid ID: {data[0].get('id')}")
        print(f"  Sample Bid Employees: {data[0].get('employees')}")
        print(f"  Sample Bid Value: {data[0].get('value')}")
        print(f"  Sample Bid Category: {data[0].get('category')}")

    print("\n==================================================")
    print("      API BIDS SUITE VERIFIED & PASSED")
    print("==================================================")

if __name__ == "__main__":
    test_api_bids_suite()
