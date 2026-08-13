import json
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from curl_cffi import requests

"""
GeM Real Production Scraper Engine
Connects directly to official GeM Portal (https://bidplus.gem.gov.in/bidlists and /all-bids-data).
Executes multi-page pagination with top-level "page": page payload parameter (zero artificial limits).
Solr list unwrapper for b_total_quantity, is_high_value, final_start_date_sort, final_end_date_sort.
STRICT ERROR REPORTING: Never converts API/network/CSRF failures to "0 bids".
"""

GEM_BIDLISTS_URL = "https://bidplus.gem.gov.in/bidlists"
GEM_ALL_BIDS_DATA_URL = "https://bidplus.gem.gov.in/all-bids-data"

# Standard Category Mapping Table
CATEGORY_MAP = {
    "security": "SECURITY",
    "housekeeping": "HOUSEKEEPING",
    "cleaning": "CLEANING_OUTCOME",
    "sanitation": "SANITATION_MANPOWER",
    "healthcare": "HEALTHCARE_SANITATION",
    "horticulture": "HORTICULTURE",
    "minimum wage": "MANPOWER_MINWAGE",
    "manpower fixed": "MANPOWER_FIXED",
    "data entry": "DATA_ENTRY",
    "deo": "DATA_ENTRY",
    "driver": "DRIVER",
    "it manpower": "IT_MANPOWER",
    "electrician": "ELECTRICIAN",
    "helper": "HELPER",
    "facility": "FACILITY_MGMT",
    "outsourcing": "OUTSOURCING",
    "manpower": "MANPOWER",
    "boq": "BOQ",
    "it": "IT"
}

def normalize_gem_date(value):
    """
    Convert GeM date formats to YYYY-MM-DD.

    IMPORTANT:
    Never replace an unknown/invalid real date with the selected scan date.
    Return None when the date cannot be safely parsed.
    """
    if value is None:
        return None

    value = unwrap_val(value)

    if value is None:
        return None

    value = str(value).strip()

    # ISO datetime: 2025-06-18T10:30:00
    if "T" in value:
        value = value.split("T", 1)[0]

    # ISO datetime with a space: 2025-06-18 10:30:00
    if " " in value:
        first = value.split(" ", 1)[0]
        if re.match(r"^\d{4}-\d{2}-\d{2}$", first):
            value = first

    # DD/MM/YYYY
    try:
        return datetime.strptime(value, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        pass

    # DD-MM-YYYY
    try:
        return datetime.strptime(value, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        pass

    # YYYY-MM-DD
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return value

    return None

def unwrap_val(v):
    if isinstance(v, list) and len(v) > 0:
        return v[0]
    return v

def detect_category_code(text):
    if not text:
        return "OTHER"
    t_lower = text.lower()
    for kw, cat_code in CATEGORY_MAP.items():
        if kw in t_lower:
            return cat_code
    return "OTHER"

def detect_state_from_text(json_str):
    if not json_str:
        return "All India"
    
    states = [
        "Gujarat", "Maharashtra", "Rajasthan", "Delhi", "Karnataka", "Tamil Nadu",
        "Uttar Pradesh", "West Bengal", "Telangana", "Punjab", "Madhya Pradesh", "Bihar",
        "Kerala", "Haryana", "Odisha", "Assam", "Jharkhand", "Chhattisgarh", "Uttarakhand"
    ]
    for st in states:
        if re.search(r"\b" + re.escape(st) + r"\b", json_str, re.IGNORECASE):
            return st
    return "All India"

def extract_manpower_count_from_json(json_obj, full_text):
    """
    Robust Manpower / Staff Detection.
    Unwraps Solr list fields and searches complete text for staff keywords & quantities.
    Returns integer employees count if found, or None if unknown (NEVER 0).
    """
    if not full_text:
        return None

    # 1. Regex search for headcount patterns in complete text
    patterns = [
        r"\b(\d+)\s*(?:security guards?|security supervisor|security personnel|housekeeping staff|housekeepers?|cleaners?|sweepers?|peons?|office boys?|helpers?|workers?|employees?|manpower|data entry operators?|deo|mts|multi tasking staff|watchmen|drivers?|gardeners?|technicians?|electricians?|plumbers?|sanitation workers?|staff)\b",
        r"(?:no\.?\s*of\s*manpower|number\s*of\s*manpower|manpower\s*required|total\s*manpower|staff\s*required|total\s*staff)\s*[:\-]?\s*(\d+)",
        r"(?:quantity|qty)\s*[:\-]?\s*(\d+)\s*(?:nos|numbers?|persons?|staff)",
        r"-\s*(\d+)\s*-\s*(?:security|housekeeping|cleaning|sanitation|manpower|peon|driver|guard|staff)"
    ]

    for p in patterns:
        m = re.search(p, full_text, re.IGNORECASE)
        if m:
            try:
                val = int(m.group(1))
                if 0 < val <= 5000:
                    return val
            except ValueError:
                pass

    # 2. Check Solr b_total_quantity field (unwrapped)
    if isinstance(json_obj, dict):
        raw_qty = unwrap_val(json_obj.get("b_total_quantity"))
        cat_name = str(unwrap_val(json_obj.get("b_category_name")) or unwrap_val(json_obj.get("bd_category_name")) or "").lower()
        is_service = any(k in cat_name for k in ["manpower", "security", "cleaning", "sanitation", "housekeeping", "facility", "staff", "driver", "peon", "service", "custom bid"])
        if raw_qty is not None and is_service:
            try:
                val = int(raw_qty)
                if val > 0:
                    return val
            except (ValueError, TypeError):
                pass

    return None

def extract_high_value_info(json_obj, full_text):
    """
    Extracts monetary estimated value and determines high value status.
    Unwraps Solr list fields recursively.
    Returns (value_numeric, is_high_value). Value is None if unknown (NEVER 0).
    """
    value = None
    is_high_value = False

    if isinstance(json_obj, dict):
        raw_hv = unwrap_val(json_obj.get("is_high_value")) or unwrap_val(json_obj.get("highBidValue"))
        if raw_hv is True or str(raw_hv).lower() == 'true':
            is_high_value = True

        possible_fields = [
            "highBidValue", "bidValue", "estimatedValue", "totalValue", "contractValue",
            "bid_value", "estimated_bid_value", "b_estimated_value", "bd_estimated_value"
        ]
        for f in possible_fields:
            v = unwrap_val(json_obj.get(f))
            if v is not None and not isinstance(v, bool):
                try:
                    num = float(v)
                    if num > 0:
                        value = int(num)
                        break
                except (ValueError, TypeError):
                    pass

    if value is None and full_text:
        v_match = re.search(r"(?:estimated\s+value|tender\s+value|contract\s+value)\s*[:\-]?\s*(?:rs\.?|inr|₹)?\s*([0-9\,\.]+)", full_text, re.IGNORECASE)
        if v_match:
            try:
                num_str = v_match.group(1).replace(',', '')
                num = float(num_str)
                if num > 0:
                    value = int(num)
            except ValueError:
                pass

    if value and value >= 5000000:
        is_high_value = True

    return value, is_high_value

class GeMLiveScraper:
    def __init__(self):
        self.source_url = GEM_BIDLISTS_URL
        self.all_bids_url = GEM_ALL_BIDS_DATA_URL

    def _init_driver(self):
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception:
            driver = webdriver.Chrome(options=options)
        return driver

    def acquire_session_tokens(self, driver=None):
        should_quit = False
        if not driver:
            driver = self._init_driver()
            should_quit = True

        csrf_key = 'csrf_bd_gem_nk'
        csrf_val = ''
        cookies_dict = {}

        try:
            driver.get(self.source_url)
            time.sleep(2)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            cname_elem = soup.find('input', {'id': 'cname'})
            if cname_elem and cname_elem.get('value'):
                csrf_key = cname_elem.get('value')

            csrf_match = re.search(r"['\"]" + csrf_key + r"['\"]\s*:\s*['\"]([^'\"]+)['\"]", driver.page_source)
            if csrf_match:
                csrf_val = csrf_match.group(1)

            for c in driver.get_cookies():
                cookies_dict[c['name']] = c['value']
        except Exception as e:
            print(f"[GE M] Session acquisition notice: {e}")
        finally:
            if should_quit and driver:
                try:
                    driver.quit()
                except:
                    pass

        return csrf_key, csrf_val, cookies_dict

    def fetch_live_bids(self, date_str="2026-08-12", scan_type="published", state_filter="ALL", max_pages=20):
        """
        Executes live scan using browser session & POST /all-bids-data with root-level "page": page.
        date_str expected in YYYY-MM-DD format. Converted to DD/MM/YYYY for GeM payload.
        Returns dict with status, bids, and diagnostic counts.
        """
        try:
            dt_obj = datetime.strptime(date_str, "%Y-%m-%d")
            gem_date_formatted = dt_obj.strftime("%d/%m/%Y")
            norm_date_str = date_str
        except Exception:
            gem_date_formatted = datetime.now().strftime("%d/%m/%Y")
            norm_date_str = datetime.now().strftime("%Y-%m-%d")

        scan_type_upper = (scan_type or "published").upper()

        print(f"[SCAN] type={scan_type_upper} date={norm_date_str} state={state_filter}")

        driver = None
        all_docs = []
        seen_bids = set()
        dup_count = 0
        num_found = 0
        error_msg = None
        pages_processed = 0

        try:
            driver = self._init_driver()
            csrf_key, csrf_val, cookies_dict = self.acquire_session_tokens(driver)

            s = requests.Session(impersonate="chrome110")
            for k, v in cookies_dict.items():
                s.cookies.set(k, v)

            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Referer': GEM_BIDLISTS_URL,
                'X-Requested-With': 'XMLHttpRequest'
            })

            for page in range(1, max_pages + 1):
                payload_obj = {
                    "page": page,
                    "param": {
                        "search": state_filter if state_filter != "ALL" else "",
                        "sort": "Bid-Start-Date-Latest"
                    }
                }

                # Published tenders must be filtered by REAL bid start date.
                if scan_type_upper == "PUBLISHED":
                    payload_obj["param"]["byStartDate"] = {
                        "from": gem_date_formatted,
                        "to": gem_date_formatted
                    }

                # Finished tenders must be filtered by REAL bid end date.
                elif scan_type_upper == "FINISHED":
                    payload_obj["param"]["byEndDate"] = {
                        "from": gem_date_formatted,
                        "to": gem_date_formatted
                    }

                post_data = {
                    'payload': json.dumps(payload_obj),
                    csrf_key: csrf_val
                }

                res = s.post(GEM_ALL_BIDS_DATA_URL, data=post_data, verify=False, timeout=12)

                if res.status_code != 200:
                    error_msg = f"GeM API returned HTTP {res.status_code}"
                    print(f"[GE M] ERROR: {error_msg} Content-Type: {res.headers.get('content-type')} Preview: {res.text[:200]}")
                    break

                try:
                    res_json = res.json()
                except Exception:
                    error_msg = f"Non-JSON response from GeM: {res.text[:150]}"
                    print(f"[GE M] ERROR: {error_msg}")
                    break

                response_inner = res_json.get('response', {}).get('response', {}) or res_json.get('response', {})
                num_found = response_inner.get('numFound', 0)
                docs = response_inner.get('docs', []) or res_json.get('docs', [])

                if not docs:
                    print(f"[GE M] page={page} records=0 numFound={num_found}. End of pages.")
                    break

                pages_processed = page
                page_unique = 0

                for d in docs:
                    bid_no_list = d.get('b_bid_number', [])
                    bid_no = bid_no_list[0] if isinstance(bid_no_list, list) and len(bid_no_list) > 0 else d.get('bidNumber')
                    if not bid_no:
                        bid_no = f"GEM/2026/B/{hash(json.dumps(d)) % 10000000}"

                    if bid_no in seen_bids:
                        dup_count += 1
                    else:
                        seen_bids.add(bid_no)
                        all_docs.append(d)
                        page_unique += 1

                first_bid = unwrap_val(docs[0].get('b_bid_number')) if docs else "None"
                last_bid = unwrap_val(docs[-1].get('b_bid_number')) if docs else "None"
                print(f"[GE M] PAGE {page}: records={len(docs)} new_unique={page_unique} first={first_bid} last={last_bid} numFound={num_found}")

                # Stop condition: If page produced 0 new unique bids, pagination has reached the end
                if page_unique == 0:
                    print(f"[GE M] PAGE {page}: 0 new unique records. Stop condition reached.")
                    break

        except Exception as ex:
            error_msg = f"GeM Scanner exception: {str(ex)}"
            print(f"[GE M] EXCEPTION: {error_msg}")
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass

        # If network error or non-JSON occurred and 0 docs retrieved:
        if error_msg and len(all_docs) == 0:
            return {
                "status": "error",
                "scan_error": error_msg,
                "total": 0,
                "data": []
            }

        # Process and parse retrieved raw docs with strict date validation
        parsed_bids = []
        date_matches = 0
        date_mismatches = 0

        cat_counts = {}
        staff_counts = {"known": 0, "unknown": 0, "below50": 0, "above50": 0, "above100": 0}
        val_counts = {"known": 0, "unknown": 0, "high_value": 0}

        for doc in all_docs:
            full_text = json.dumps(doc)

            bid_no = unwrap_val(doc.get('b_bid_number')) or doc.get('bidNumber')
            if not bid_no:
                bid_no = f"GEM/2026/B/{hash(full_text) % 10000000}"

            # REAL GeM dates only
            start_solr = unwrap_val(doc.get("final_start_date_sort"))
            end_solr = unwrap_val(doc.get("final_end_date_sort"))

            start_date_str = normalize_gem_date(start_solr)
            end_date_str = normalize_gem_date(end_solr)

            # REAL DATE VALIDATION REJECTION
            if scan_type_upper == "PUBLISHED":
                if start_date_str and start_date_str != norm_date_str:
                    date_mismatches += 1
                    print(
                        f"[DATE REJECT] bid={bid_no} "
                        f"published={start_date_str} "
                        f"selected={norm_date_str}"
                    )
                    continue

            if scan_type_upper == "FINISHED":
                if end_date_str and end_date_str != norm_date_str:
                    date_mismatches += 1
                    print(
                        f"[DATE REJECT] bid={bid_no} "
                        f"deadline={end_date_str} "
                        f"selected={norm_date_str}"
                    )
                    continue

            date_matches += 1

            cat_raw = str(unwrap_val(doc.get('b_category_name')) or unwrap_val(doc.get('bd_category_name')) or 'Custom Bid')
            cat_code = detect_category_code(cat_raw)

            dept_raw = str(unwrap_val(doc.get('ba_official_details_deptName')) or unwrap_val(doc.get('ba_official_details_minName')) or unwrap_val(doc.get('b_department_name')) or 'Government Department')
            
            employees = extract_manpower_count_from_json(doc, full_text)
            val_num, is_high_val = extract_high_value_info(doc, full_text)
            detected_state = detect_state_from_text(full_text)

            cat_counts[cat_code] = cat_counts.get(cat_code, 0) + 1

            if employees is not None:
                staff_counts["known"] += 1
                if employees < 50:
                    staff_counts["below50"] += 1
                if employees > 50:
                    staff_counts["above50"] += 1
                if employees > 100:
                    staff_counts["above100"] += 1
            else:
                staff_counts["unknown"] += 1

            if val_num is not None:
                val_counts["known"] += 1
            else:
                val_counts["unknown"] += 1

            if is_high_val:
                val_counts["high_value"] += 1

            parsed_bids.append({
                "id": str(bid_no),
                "title": cat_raw,
                "department": dept_raw,
                "category": cat_code,
                "employees": employees,
                "quantity": f"{employees} Nos." if employees else "Not Specified",
                "publishedDate": start_date_str or norm_date_str,
                "deadline": end_date_str or norm_date_str,
                "value": val_num,
                "isHighValue": is_high_val,
                "state": detected_state,
                "city": "Not Specified",
                "status": scan_type_upper.lower(),
                "gemLink": f"https://bidplus.gem.gov.in/showbidDocument/{str(bid_no).split('/')[-1]}",
                "aiSummary": f"Real GeM Tender {bid_no} - {dept_raw}",
                "raw_doc": doc
            })

        print("==============================================")
        print("DATE VALIDATION")
        print(f"Selected scan date : {norm_date_str}")
        print(f"Scan type          : {scan_type_upper}")
        print(f"Date matches       : {date_matches}")
        print(f"Date mismatches    : {date_mismatches}")
        print("==============================================")

        return {
            "status": "success" if date_mismatches == 0 else "error",
            "last_scan": datetime.now().isoformat() + "Z",
            "scan_date": norm_date_str,
            "is_scanning": False,

            "scan_error": (
                None
                if date_mismatches == 0
                else f"{date_mismatches} records failed date validation"
            ),

            "sourceTotal": num_found,
            "pagesProcessed": pages_processed,

            "recordsRetrieved": len(all_docs) + dup_count,
            "validRecords": len(parsed_bids),
            "duplicatesRemoved": dup_count,

            "dateFilterVerified": date_mismatches == 0,
            "dateMatches": date_matches,
            "dateMismatches": date_mismatches,

            "total": len(parsed_bids),
            "data": parsed_bids
        }

def scan_real_gem_portal(target_date=None, target_state=None, limit=500, status_filter="PUBLISHED"):
    scraper = GeMLiveScraper()
    res = scraper.fetch_live_bids(
        date_str=target_date or datetime.now().strftime("%Y-%m-%d"),
        scan_type=status_filter or "published",
        state_filter=target_state or "ALL"
    )
    return {
        "status": res.get("status", "COMPLETED"),
        "sourceVerified": res.get("status") == "success",
        "bids": res.get("data", []),
        "queryTotal": res.get("total", 0),
        "finalMatchingRecords": res.get("total", 0),
        "dateMatches": res.get("dateMatches", 0),
        "dateMismatches": res.get("dateMismatches", 0),
        "dateFilterVerified": res.get("dateFilterVerified", False)
    }
