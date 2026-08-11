const axios = require('axios');
const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, 'database.json');

let lastScanAudit = {
  scan_id: `SCAN-${Date.now()}`,
  source: "GeM Public Listing",
  source_url: "https://bidplus.gem.gov.in/bidlists",
  status: "CONNECTED",
  last_retrieval_at: new Date().toISOString(),
  records_received: 0,
  last_error: null
};

function readDB() {
  try {
    const data = fs.readFileSync(DB_FILE, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    return { tenders: [], users: [] };
  }
}

function writeDB(data) {
  try {
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
  } catch (err) {
    console.error('Error writing to database.json:', err);
  }
}

function getSourceHealthStatus() {
  const db = readDB();
  const tendersCount = (db.tenders || []).length;
  if (tendersCount > 0) {
    lastScanAudit.status = "CONNECTED";
    lastScanAudit.records_received = tendersCount;
  }
  return lastScanAudit;
}

/**
 * GeM Authorized Public Data Connector
 */
async function scrapeLiveGeMPortal(opts = {}) {
  let searchQuery = '';
  let state = 'ALL';
  let limit = 500;
  let status = 'PUBLISHED';
  let targetDate = null;

  if (typeof opts === 'object' && opts !== null && !Array.isArray(opts)) {
    searchQuery = opts.searchQuery || '';
    state = opts.state || 'ALL';
    limit = opts.limit || 500;
    status = opts.status || opts.type || 'PUBLISHED';
    targetDate = opts.targetDate || opts.date || null;
  } else {
    searchQuery = arguments[0] || '';
    state = arguments[1] || 'ALL';
    limit = arguments[2] || 500;
    status = arguments[3] || 'PUBLISHED';
    targetDate = arguments[4] || null;
  }

  const scanId = `SCAN-${Date.now()}`;
  lastScanAudit.scan_id = scanId;
  lastScanAudit.requested_date = targetDate || new Date().toISOString().split('T')[0];

  try {
    const pythonRes = await axios.post('http://localhost:8000/api/scan', {
      date: targetDate,
      type: (status || 'published').toLowerCase(),
      state: state || 'ALL'
    }, { timeout: 30000 });

    if (pythonRes.data && pythonRes.data.bids && Array.isArray(pythonRes.data.bids) && pythonRes.data.bids.length > 0) {
      const liveBids = pythonRes.data.bids;
      
      lastScanAudit.status = "CONNECTED";
      lastScanAudit.last_retrieval_at = new Date().toISOString();
      lastScanAudit.records_received = liveBids.length;
      lastScanAudit.last_error = null;

      const db = readDB();
      db.tenders = liveBids;
      writeDB(db);
      return liveBids;
    }
  } catch (err) {
    lastScanAudit.status = "NOT_AVAILABLE";
    lastScanAudit.last_error = err.message;
    console.warn('Real GeM Scraper API notice:', err.message);
  }

  return [];
}

/**
 * Continuous Background Real Scraper
 */
function startRealGeMBackgroundScraper() {
  console.log('🚀 Real GeM Authorized Public Connector Engine Running (Port 8000)...');
  scrapeLiveGeMPortal().catch(err => console.error('Background Scraper notice:', err));

  setInterval(() => {
    scrapeLiveGeMPortal().catch(err => console.error('Background Scraper notice:', err));
  }, 120000);
}

module.exports = {
  scrapeLiveGeMPortal,
  startRealGeMBackgroundScraper,
  fetchRealGeMBids: scrapeLiveGeMPortal,
  getSourceHealthStatus
};
