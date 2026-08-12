import requests

def test_post_scan():
    print("==================================================")
    print("      TESTING POST /api/scan LIVE TRIGGER")
    print("==================================================")

    url = "http://localhost:5000/api/scan"
    payload = {
        "type": "published",
        "state": "Gujarat",
        "date": "2026-08-12"
    }

    res = requests.post(url, json=payload, timeout=120)
    data = res.json()

    print(f"Status Code: {res.status_code}")
    print(f"Response Status: {data.get('status')}")
    print(f"Total Bids Returned: {data.get('total')}")
    print(f"Scan Date: {data.get('scan_date')}")
    print(f"Scan Error: {data.get('scan_error')}")

    if data.get("total", 0) > 0:
        first = data["data"][0]
        print(f"\nFirst Scan Record:")
        print(f"  Bid ID: {first.get('id')}")
        print(f"  Title: {first.get('title')}")
        print(f"  Category Code: {first.get('category')}")
        print(f"  Employees: {first.get('employees')}")
        print(f"  Value: {first.get('value')}")
        print(f"  State: {first.get('state')}")

    assert res.status_code == 200
    print("\n==================================================")
    print("      POST /api/scan TEST PASSED")
    print("==================================================")

if __name__ == "__main__":
    test_post_scan()
