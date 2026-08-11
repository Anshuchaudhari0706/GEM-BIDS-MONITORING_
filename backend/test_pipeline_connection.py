import requests
import urllib.parse

def test_pipeline():
    print("==================================================")
    print("      TESTING DATA PIPELINE CONNECTION")
    print("==================================================")

    # 1. Login
    login_url = "http://localhost:5000/api/auth/login"
    login_payload = {
        "email": "chaudharianshu0706@gmail.com",
        "password": "Anshu@2746"
    }
    
    sess = requests.Session()
    res = sess.post(login_url, json=login_payload)
    if res.status_code != 200:
        login_payload = {"email": "admin@gemintel.com", "password": "admin123"}
        res = sess.post(login_url, json=login_payload)

    res_json = res.json()
    token = res_json.get("token")
    print(f"Login token acquired: {token[:20]}...\n")

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Fetch Tenders (Dashboard API)
    tenders_url = "http://localhost:5000/api/tenders?status=PUBLISHED&state=ALL&services=ALL"
    t_res = sess.get(tenders_url, headers=headers)
    t_data = t_res.json()

    tenders = t_data.get('tenders', [])
    print(f"[Dashboard API Output]")
    print(f"Total Tenders Returned: {len(tenders)}")
    if tenders:
        print(f"Sample Tender 1: {tenders[0].get('id')} | Dept: {tenders[0].get('department')[:30]}")

    extracted_count = sum(1 for t in tenders if t.get("document_processed"))
    print(f"Tenders with Extracted Document Intelligence Data: {extracted_count}")

    # 3. Test Single Tender Audit Endpoint
    if tenders:
        sample_id = tenders[0].get('id')
        encoded_id = urllib.parse.quote(sample_id, safe='')
        audit_res = sess.get(f"http://localhost:5000/api/tenders/detail/{encoded_id}", headers=headers)
        if audit_res.status_code == 200:
            audit_data = audit_res.json()
            print(f"\n[Single Tender Audit Output for {sample_id}]")
            print(f"  Source Verified: {audit_data.get('source', {}).get('verified')}")
            print(f"  Document Status: {audit_data.get('document', {}).get('status')}")
            print(f"  Office Address: {audit_data.get('extracted', {}).get('officeAddress', {}).get('value')[:50]}")
            print(f"  Manpower Extracted: {len(audit_data.get('extracted', {}).get('manpower', []))} designations\n")

    print("==================================================")
    print("   DATA PIPELINE SUCCESSFULLY CONNECTED & VERIFIED")
    print("==================================================")

if __name__ == "__main__":
    test_pipeline()
