# GeMIntel - Smart GeM Tender Intelligence Platform

A professional SaaS platform for real-time scanning, monitoring, and intelligent analysis of Government e-Marketplace (GeM) tenders.

---

## Table of Contents

1. [Features](#features)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Installation and Setup](#installation-and-setup)
5. [Running the Application](#running-the-application)
6. [Login Credentials](#login-credentials)
7. [How to Use](#how-to-use)
8. [Admin Panel](#admin-panel)
9. [GeM Tender Scanner Logic](#gem-tender-scanner-logic)
10. [Python Document Reader](#python-document-reader)
11. [Subscription and Licensing](#subscription-and-licensing)
12. [API Endpoints](#api-endpoints)
13. [Environment Variables](#environment-variables)

---

## Features

### Real-Time GeM Tender Scanning
- Scans 200-500 pages of GeM Portal (bidplus.gem.gov.in)
- Extracts Bid Number, Items/Services, Quantity, Department Name & Address
- Reads exact Start Date & Time (e.g. 24-07-2026 9:14 AM) and End Date & Time (e.g. 12-08-2026 5:00 PM)
- Accurately evaluates PUBLISHED vs FINISHED status based on real end-time comparison

### Dashboard
- 196+ live tenders displayed matching exact GeM Portal layout
- GeM Stepper Progress Bar (TECHNICAL BID -> OFFER PRICE -> UPLOAD DOCUMENTS -> EMD/EPBG -> VERIFY & ESIGN)
- Participate button on every bid card
- Status badges: OPEN FOR SUBMISSION / CLOSED ENDED
- Start Date shown in green, End Date in amber/red

### Service-Based Filtering
- Multi-select services: Security Guards, Cleaning Services, Manpower Fixed, Custom Bid, Facility Management, Housekeeping, Healthcare, Horticulture, BOP, IT Services, Data Entry
- Admin can add/edit/delete services dynamically
- Click service cards to instantly filter matching tenders

### Date-Based Filtering
- Select any date using the Custom Calendar Date Picker
- PUBLISHED filter: shows bids where selected date falls within Start-End window
- FINISHED filter: shows bids where End Date <= selected date
- ALL BIDS filter: returns all bids regardless of date

### Python Tender Document Intelligence
- PDF Download & Text Extraction
- Regex pattern extraction for 47+ fields:
  - Estimated Value, EMD, Tender Fee, Performance Security
  - Work Location (Office Name, City, District, State, PIN)
  - Manpower Breakdown (1 - Security Guard, 3 - Peon, etc.)
  - Dates & Times, Bid Number
- Converts Indian Lakh/Crore values to numeric: 25 Lakhs -> Rs.25,00,000

### Tender Details Modal (5 Tabs)
1. Overview - Bid summary, status, dates
2. Manpower Table - Designation-wise breakdown
3. Financial Details - Est. Value, EMD, Tender Fee, Performance Security
4. Work Location - Address + Google Maps link
5. Document Intelligence - Regex Reader with live progress indicator

### Subscription & Licensing System
- Plans: Monthly (Rs.999), Quarterly (Rs.2499), Yearly (Rs.7999)
- Razorpay payment gateway integration
- Auto-generated 16-character License Keys (GEMI-XXXX-XXXX-XXXX)
- Key management: Activate, Suspend, Revoke, Extend Expiry

### Admin Panel
- Separate protected admin login
- User management (View, Create, Edit, Disable, Delete)
- License Key management (Generate, Activate, Suspend, Revoke)
- Pricing management (change plans without code changes)
- Regex Rules management
- Revenue & subscription analytics

### Export Options
- Export to Excel/CSV with all tender fields
- PDF Report download
- Read PDF Addresses from GeM tender documents

---

## Technology Stack

| Layer            | Technology                                      |
|------------------|-------------------------------------------------|
| Frontend         | React 18, Vite, Vanilla CSS, Lucide Icons, XLSX.js |
| Backend API      | Node.js, Express.js, JWT Auth, bcryptjs         |
| Database         | JSON flat-file database (database.json)         |
| Python Service   | FastAPI, PyMuPDF, pdfplumber, Regex Engine      |
| Payment          | Razorpay Integration                            |
| Fonts            | Google Fonts (Inter)                            |
| Containerization | Docker Compose (optional)                       |

---

## Project Structure

```
GEM BIDS/
|
+-- backend/                        # Express.js API Server (Port 5000)
|   +-- server.js                   # Main API server
|   +-- tenderGenerator.js          # GeM-format tender data generator
|   +-- gem_scraper.py              # GeM Portal live scraper (Python)
|   +-- database.json               # Flat-file database
|   +-- .env                        # Environment variables
|   +-- package.json
|   |
|   +-- document-reader/            # Python Microservice (Port 8000)
|       +-- main.py                 # FastAPI server entry point
|       +-- pdf_reader.py           # PDF text extraction
|       +-- text_cleaner.py         # Text cleaning pipeline
|       +-- regex_extractor.py      # 47-field regex extraction engine
|       +-- tender_parser.py        # Multi-stage document parser
|       +-- requirements.txt        # Python dependencies
|
+-- frontend/                       # React + Vite Frontend (Port 3000)
|   +-- src/
|       +-- App.jsx                 # Root component & routing
|       +-- index.css               # Global CSS design system
|       |
|       +-- context/
|       |   +-- AuthContext.jsx     # Authentication & global state
|       |
|       +-- services/
|       |   +-- api.js              # API service layer
|       |
|       +-- components/
|       |   +-- TenderDetailsModal.jsx      # 5-tab tender details modal
|       |   +-- CustomDatePicker.jsx        # GeM-style calendar picker
|       |   +-- CustomStatusDropdown.jsx    # Status filter dropdown
|       |
|       +-- pages/
|           +-- LandingPage.jsx     # Marketing landing page
|           +-- LoginPage.jsx       # User login
|           +-- RegisterPage.jsx    # User registration
|           +-- DashboardPage.jsx   # Main tender monitoring dashboard
|           +-- ScanBidsPage.jsx    # Advanced scanner with services
|           +-- AdminPage.jsx       # Admin panel (protected)
|           +-- PlansPage.jsx       # Subscription plans & pricing
|           +-- KeyActivationPage.jsx  # License key activation
|           +-- ProfilePage.jsx     # User profile & subscription
|
+-- .env.example                    # Environment variables template
+-- docker-compose.yml              # Docker configuration
+-- README.md                       # This file
```

---

## Installation and Setup

### Prerequisites
- Node.js v18+ (https://nodejs.org)
- Python 3.10+ (https://python.org)
- npm (comes with Node.js)

### Step 1: Open Project Directory
```powershell
cd "C:\Users\ASUS\OneDrive\Desktop\GEM BIDS"
```

### Step 2: Install Backend Dependencies
```powershell
cd backend
npm install
```

### Step 3: Install Frontend Dependencies
```powershell
cd ..\frontend
npm install
```

### Step 4: Install Python Document Reader Dependencies
```powershell
cd ..\backend\document-reader
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables
Edit `backend/.env` with your values:
```env
PORT=5000
JWT_SECRET=your_jwt_secret_key_here
ADMIN_EMAIL=admin@gemintel.com
ADMIN_PASSWORD=admin123
RAZORPAY_KEY_ID=rzp_test_your_key
RAZORPAY_KEY_SECRET=your_secret
```

---

## Running the Application

Open 3 separate terminal windows:

### Terminal 1 - Backend API Server
```powershell
cd "C:\Users\ASUS\OneDrive\Desktop\GEM BIDS\backend"
node server.js
# Output: GeMIntel Production API running at http://localhost:5000
```

### Terminal 2 - Frontend Dev Server
```powershell
cd "C:\Users\ASUS\OneDrive\Desktop\GEM BIDS\frontend"
npm run dev
# Output: Frontend running at http://localhost:3000
```

### Terminal 3 - Python Document Reader (Optional)
```powershell
cd "C:\Users\ASUS\OneDrive\Desktop\GEM BIDS\backend\document-reader"
python main.py
# Output: Python Document Reader running at http://localhost:8000
```

### Open in Browser
```
http://localhost:3000
```

---

## Login Credentials

### Demo User (Active Yearly Subscription)
| Field       | Value                    |
|-------------|--------------------------|
| Email       | demo@techsolutions.com   |
| Password    | admin123                 |
| License Key | GEMI-7F3A-92KD-X81P      |
| Plan        | Yearly                   |

### Admin Account (Full Control)
| Field       | Value                    |
|-------------|--------------------------|
| Email       | admin@gemintel.com       |
| Password    | admin123                 |
| License Key | GEMI-ADMIN-8888-KEYS     |
| Access      | Unlimited                |

---

## How to Use

### 1. Scan GeM Tenders
1. Log in with demo credentials
2. Go to Dashboard or Scan Bids page
3. Select Tender Status (Published / Finished / All)
4. Pick a Scan Date from the calendar
5. Click Scan GeM Tenders Now
6. Watch live scan progress indicators
7. Tenders appear with exact GeM Portal formatting

### 2. Filter by Services
- Click any Service Card (Security Guards, Cleaning Services, Custom Bid, etc.)
- Counts update live for each service category
- Use Select All / Deselect All for bulk selection

### 3. Published vs Finished Logic
| Status    | Date Filter Logic                                |
|-----------|--------------------------------------------------|
| PUBLISHED | Selected date falls within Start Date-End Date   |
| FINISHED  | End Date <= Selected Date (tender has closed)    |
| ALL       | No date restriction                              |

### 4. View Tender Details
- Click Participate button on any card
- Opens 5-tab modal with full tender spec, manpower table, financial details, work location

### 5. Export Data
- Click Export CSV to download Excel report
- Click Download Report PDF for PDF format

---

## Admin Panel

Access: http://localhost:3000/admin -> Login with admin credentials

| Tab              | Features                                          |
|------------------|---------------------------------------------------|
| Overview         | Total Users, Revenue, Active Subscriptions        |
| User Management  | View, Search, Create, Edit, Disable, Delete users |
| License Keys     | Generate, Activate, Suspend, Revoke, Extend keys  |
| Pricing          | Change plan prices & durations without code       |
| Services         | Add/Edit/Delete tender service categories         |
| Regex Rules      | Manage PDF extraction patterns                    |
| Settings         | System configuration                              |

---

## GeM Tender Scanner Logic

```
GeM Portal (bidplus.gem.gov.in)
    |
    v
Scan 200-500 Pages
    |
    v
Extract via Regex:
  * BID NO (GEM/2026/B/7821915)
  * Items (Manpower Outsourcing Services...)
  * Quantity (217 Units)
  * Department Name And Address
  * Start Date: 24-07-2026 9:14 AM  [Shown in GREEN]
  * End Date:   12-08-2026 5:00 PM  [Shown in AMBER/RED]
    |
    v
Evaluate Status:
  * End Time < Current Time  -> FINISHED (Red badge)
  * End Time > Current Time  -> PUBLISHED (Green badge)
    |
    v
Display in Dashboard with GeM Stepper Bar:
  [TECHNICAL BID] -> [OFFER PRICE] -> [UPLOAD DOCUMENTS] -> [EMD/EPBG] -> [VERIFY & ESIGN]
                                                                         [Participate Button]
```

---

## Python Document Reader

The Python microservice at http://localhost:8000 processes GeM tender PDFs and extracts 47 structured fields.

### Sample Extracted Fields
```json
{
  "bid_number": "GEM/2026/B/7821915",
  "estimated_value": 2500000,
  "estimated_value_original": "Rs.25,00,000",
  "emd_amount": 50000,
  "tender_fee": 5000,
  "performance_security": 125000,
  "work_location": {
    "office_name": "Ministry of Petroleum and Natural Gas",
    "city": "New Delhi",
    "state": "Delhi",
    "pincode": "110001"
  },
  "manpower": [
    { "designation": "Security Guard", "quantity": 10 },
    { "designation": "Peon", "quantity": 3 },
    { "designation": "Supervisor", "quantity": 2 }
  ],
  "total_manpower": 15
}
```

### Parse API Call
```
POST http://localhost:8000/parse
Content-Type: application/json

{
  "pdf_url": "https://bidplus.gem.gov.in/...",
  "bid_number": "GEM/2026/B/7821915"
}
```

---

## Subscription and Licensing

| Plan      | Price    | Duration |
|-----------|----------|----------|
| Monthly   | Rs.999   | 30 days  |
| Quarterly | Rs.2,499 | 90 days  |
| Yearly    | Rs.7,999 | 365 days |

### License Key Format
```
GEMI-XXXX-XXXX-XXXX
Example: GEMI-7F3A-92KD-X81P
```

Key States: ACTIVE -> USED -> EXPIRED / SUSPENDED / REVOKED

---

## API Endpoints

| Method | Endpoint                    | Description                | Auth  |
|--------|-----------------------------|----------------------------|-------|
| POST   | /api/auth/login             | User login                 | No    |
| POST   | /api/auth/register          | User registration          | No    |
| GET    | /api/tenders                | Get tenders with filters   | JWT   |
| POST   | /api/tenders/scan           | Trigger GeM scan           | JWT   |
| GET    | /api/services               | Get service categories     | JWT   |
| POST   | /api/documents/parse        | Parse PDF document         | JWT   |
| GET    | /api/subscription/status    | Get subscription status    | JWT   |
| POST   | /api/license/activate       | Activate license key       | JWT   |
| GET    | /api/admin/users            | List all users             | Admin |
| GET    | /api/admin/keys             | List license keys          | Admin |
| POST   | /api/admin/keys/generate    | Generate new keys          | Admin |
| GET    | /api/admin/pricing          | Get pricing plans          | Admin |
| PUT    | /api/admin/pricing          | Update pricing             | Admin |
| GET    | /api/admin/regex-rules      | Get regex rules            | Admin |
| POST   | /api/admin/regex-rules      | Update regex rules         | Admin |

---

## Environment Variables

| Variable                | Description                        | Default            |
|-------------------------|------------------------------------|--------------------|
| PORT                    | Backend server port                | 5000               |
| JWT_SECRET              | JWT signing secret                 | Required           |
| ADMIN_EMAIL             | Admin login email                  | admin@gemintel.com |
| ADMIN_PASSWORD          | Admin login password               | admin123           |
| RAZORPAY_KEY_ID         | Razorpay API key                   | Required           |
| RAZORPAY_KEY_SECRET     | Razorpay secret                    | Required           |
| SUBSCRIPTION_MONTHLY    | Monthly plan price (paise)         | 99900              |
| SUBSCRIPTION_QUARTERLY  | Quarterly plan price (paise)       | 249900             |
| SUBSCRIPTION_YEARLY     | Yearly plan price (paise)          | 799900             |

---

## Docker (Optional)

```bash
docker-compose up --build
```

This starts all 3 services simultaneously:
- Frontend:      http://localhost:3000
- Backend API:   http://localhost:5000
- Python Reader: http://localhost:8000

---

Built with care for GeM Procurement Professionals
(c) 2026 GeMIntel - All Rights Reserved
