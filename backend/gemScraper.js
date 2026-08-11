const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const DB_FILE = path.join(__dirname, 'database.json');

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
 * Real Official GeM Portal Live Scraper Engine
 * Connects to Python Live Scraper Microservice (Port 8000) using curl_cffi Chrome TLS impersonation
 * Returns ONLY 100% REAL LIVE BIDS directly from official GeM portal. NO MOCK BIDS!
 */
async function scrapeLiveGeMPortal(searchQuery = '', state = 'ALL', limit = 50, status = 'PUBLISHED', targetDate = null) {
  try {
    const pythonRes = await axios.post('http://localhost:8000/api/scan', {
      date: targetDate || new Date().toISOString().split('T')[0],
      type: (status || 'published').toLowerCase(),
      state: state || 'ALL'
    }, { timeout: 15000 });

    if (pythonRes.data && pythonRes.data.bids && Array.isArray(pythonRes.data.bids)) {
      const liveBids = pythonRes.data.bids;
      // Persist real scanned bids to database.json
      const db = readDB();
      db.tenders = liveBids;
      writeDB(db);
      return liveBids;
    }
  } catch (err) {
    console.warn('Real GeM Scraper API notice:', err.message);
  }

  // Strictly return empty array if no live bids are fetched from official GeM portal
  return [];
}

/**
 * Continuous Background Real Scraper
 * Periodically scans official GeM portal and updates database.json with 100% real live data
 */
function startRealGeMBackgroundScraper() {
  console.log('🚀 Real GeM Live API Scraper Engine Running (Port 8000)...');
  scrapeLiveGeMPortal().catch(err => console.error('Background Scraper notice:', err));

  setInterval(() => {
    scrapeLiveGeMPortal().catch(err => console.error('Background Scraper notice:', err));
  }, 120000);
}

module.exports = {
  scrapeLiveGeMPortal,
  startRealGeMBackgroundScraper,
  fetchRealGeMBids: scrapeLiveGeMPortal
};
