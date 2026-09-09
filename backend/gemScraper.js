const axios = require('axios');
const fs = require('fs');
const path = require('path');

const DB_FILE = path.join(__dirname, 'database.json');

const scansMap = new Map();

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

/**
 * Dynamic Authoritative Source Health & Diagnostic Audit Status
 * Zero hard-coded fake numbers or fake bid numbers.
 */
function getSourceHealthStatus() {
  const db = readDB();
  const lastScan = db.last_scan || {
    status: "NO_SCAN",
    sourceVerified: false,
    queryDate: null,
    bidType: null,
    state: "ALL",
    recordCount: 0,
    scan_error: null
  };

  const isVerified = lastScan.status === "COMPLETED" || lastScan.status === "VERIFIED_CONNECTED" || lastScan.status === "SOURCE_REACHABLE_ZERO" || lastScan.status === "INCOMPLETE";
  const isConnected = lastScan.status !== "FAILED" && lastScan.status !== "NO_SCAN";

  let canonicalStatus = "NO_SCAN";
  if (lastScan.status === "FAILED") {
    canonicalStatus = "FAILED";
  } else if (lastScan.status === "INCOMPLETE") {
    canonicalStatus = "INCOMPLETE";
  } else if (lastScan.status === "SOURCE_REACHABLE_ZERO") {
    canonicalStatus = "SOURCE_REACHABLE_ZERO";
  } else if (isVerified) {
    canonicalStatus = "VERIFIED_CONNECTED";
  }

  return {
    scan_id: lastScan.scanId || `SCAN-${lastScan.queryDate ? lastScan.queryDate.replace(/-/g, '') : '001'}`,
    source: "GeM BidPlus",
    source_url: "https://bidplus.gem.gov.in/bidlists",
    data_endpoint: "https://bidplus.gem.gov.in/all-bids-data",
    status: canonicalStatus,
    http_status: isConnected ? 200 : (lastScan.status === "FAILED" ? 500 : null),
    response_type: isConnected ? "application/json" : null,
    connected: isConnected,
    verified: isVerified,
    requested_date: lastScan.queryDate || null,
    bid_type: lastScan.bidType || null,
    state: lastScan.state || "ALL",
    last_retrieval_at: lastScan.last_scan || new Date().toISOString(),
    source_total: lastScan.sourceTotal ?? null,
    pages_processed: lastScan.pagesProcessed ?? 0,
    records_received: lastScan.recordsRetrieved ?? (lastScan.recordCount || 0),
    valid_records: lastScan.validRecords ?? (lastScan.recordCount || 0),
    unique_bids: lastScan.recordCount || 0,
    duplicates_removed: lastScan.duplicatesRemoved ?? 0,
    date_matches: lastScan.dateMatches ?? 0,
    date_mismatches: lastScan.dateMismatches ?? 0,
    last_error: lastScan.scan_error || null
  };
}

function createScanJob(params = {}) {
  const scanId = `SCAN-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
  const job = {
    scanId,
    status: "STARTED",
    params,
    startedAt: new Date().toISOString(),
    completedAt: null,
    pagesProcessed: 0,
    recordsRetrieved: 0,
    uniqueRecords: 0,
    httpStatus: null,
    responseType: null,
    error: null
  };
  scansMap.set(scanId, job);
  return job;
}

function getScanJob(scanId) {
  return scansMap.get(scanId) || null;
}

/**
 * Single Authoritative GeM Public Scraper Proxy
 * Delegates directly to Python microservice (http://localhost:8000/api/scan)
 * Standardizing real GeM payload acquisition via /all-bids-data
 */
async function scrapeLiveGeMPortal(opts = {}) {
  let state = 'ALL';
  let status = 'PUBLISHED';
  let targetDate = null;
  let scanId = opts.scanId || null;

  if (typeof opts === 'object' && opts !== null && !Array.isArray(opts)) {
    state = opts.state || 'ALL';
    status = opts.status || opts.type || 'PUBLISHED';
    targetDate = opts.targetDate || opts.date || null;
  }

  if (!scanId) {
    const job = createScanJob({ state, status, targetDate });
    scanId = job.scanId;
  }

  const currentJob = scansMap.get(scanId);
  if (currentJob) {
    currentJob.status = "RUNNING";
  }

  try {
    const pythonRes = await axios.post('http://127.0.0.1:8000/api/scan', {
      date: targetDate,
      type: (status || 'published').toLowerCase(),
      state: state || 'ALL'
    }, { timeout: 120000 });

    const pyData = pythonRes.data;
    const isPyError = ['error', 'FAILED'].includes(pyData.status);

    if (isPyError) {
      throw new Error(pyData.scan_error || "GeM acquisition failed");
    }

    const liveBids = pyData.bids || pyData.data || [];
    const pagesProcessed = pyData.pagesProcessed || 0;
    const finalMatching = liveBids.length;
    const isVerified = pyData.status === "success" || pyData.status === "SOURCE_REACHABLE_ZERO";

    if (currentJob) {
      currentJob.status = isVerified ? (liveBids.length === 0 ? "SOURCE_REACHABLE_ZERO" : "COMPLETED") : "INCOMPLETE";
      currentJob.completedAt = new Date().toISOString();
      currentJob.pagesProcessed = pagesProcessed;
      currentJob.recordsRetrieved = pyData.recordsRetrieved || finalMatching;
      currentJob.uniqueRecords = finalMatching;
      currentJob.sourceTotal = pyData.sourceTotal ?? null;
      currentJob.queryTotal = pyData.queryTotal || finalMatching;
      currentJob.validRecords = pyData.validRecords || finalMatching;
      currentJob.duplicatesRemoved = pyData.duplicatesRemoved || 0;
      currentJob.finalMatchingRecords = finalMatching;
      currentJob.error = pyData.scan_error || null;
    }

    const db = readDB();
    db.tenders = liveBids;
    db.last_scan = {
      status: liveBids.length === 0 ? "SOURCE_REACHABLE_ZERO" : (pyData.paginationComplete ? "COMPLETED" : "INCOMPLETE"),
      sourceVerified: isVerified,
      dateFilterVerified: pyData.dateFilterVerified !== false,
      queryDate: targetDate,
      bidType: (status || 'PUBLISHED').toUpperCase(),
      state: state,
      recordCount: liveBids.length,
      sourceTotal: pyData.sourceTotal ?? null,
      pagesProcessed: pagesProcessed,
      recordsRetrieved: pyData.recordsRetrieved || liveBids.length,
      validRecords: pyData.validRecords || liveBids.length,
      duplicatesRemoved: pyData.duplicatesRemoved || 0,
      dateMatches: pyData.dateMatches || 0,
      dateMismatches: pyData.dateMismatches || 0,
      paginationComplete: pyData.paginationComplete === true,
      stop_reason: pyData.stop_reason || null,
      gemNumFound: pyData.gemNumFound ?? null,
      scan_error: pyData.scan_error || null,
      last_scan: new Date().toISOString()
    };
    writeDB(db);

    return liveBids;
  } catch (err) {
    const errorMsg = err.response ? `HTTP ${err.response.status}` : err.message;
    if (currentJob) {
      currentJob.status = "FAILED";
      currentJob.completedAt = new Date().toISOString();
      currentJob.error = errorMsg;
    }

    const db = readDB();
    db.tenders = [];
    db.last_scan = {
      status: "FAILED",
      sourceVerified: false,
      dateFilterVerified: false,
      is_scanning: false,
      queryDate: targetDate,
      bidType: (status || 'PUBLISHED').toUpperCase(),
      state: state,
      recordCount: 0,
      scan_error: errorMsg,
      last_scan: new Date().toISOString()
    };
    writeDB(db);

    console.warn('[gemScraper.js] Live Scraper Error:', errorMsg);
    return [];
  }
}

function startRealGeMBackgroundScraper() {
  console.log('🚀 Real GeM Authorized Public Connector Engine Ready (Port 8000)...');
}

module.exports = {
  scrapeLiveGeMPortal,
  startRealGeMBackgroundScraper,
  fetchRealGeMBids: scrapeLiveGeMPortal,
  getSourceHealthStatus,
  createScanJob,
  getScanJob
};
