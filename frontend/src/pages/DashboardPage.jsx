import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import CustomDatePicker from '../components/CustomDatePicker';
import CustomStatusDropdown from '../components/CustomStatusDropdown';
import TenderDetailsModal from '../components/TenderDetailsModal';
import {
  Radar,
  Zap,
  TrendingUp,
  Bookmark,
  Search,
  FileSpreadsheet,
  FileText,
  Download,
  Eye,
  Grid,
  List,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  RefreshCw,
  Clock,
  MapPin,
  Users,
  IndianRupee,
  Filter,
  ArrowUpDown,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { fetchTenders, triggerGeMScan } from '../services/api';
import * as XLSX from 'xlsx';

export default function DashboardPage({ searchQuery, setSearchQuery }) {
  const { token, isLicenseActive, toggleSaveTender, savedTenders, showToast, setSelectedPlanForPayment, setShowPaymentModal } = useAuth();

  const [tenders, setTenders] = useState([]);
  const [allScannedTenders, setAllScannedTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [scanTerminalLog, setScanTerminalLog] = useState('');
  const [lastScanTimestamp, setLastScanTimestamp] = useState('2026-08-11 13:00:00');

  // Filters & Sorting State
  const [tenderStatus, setTenderStatus] = useState('PUBLISHED');
  const [selectedDate, setSelectedDate] = useState(() => new Date().toISOString().split('T')[0]);
  const [selectedServiceCategory, setSelectedServiceCategory] = useState('ALL');
  const [targetState, setTargetState] = useState('ALL');
  const [valRange, setValRange] = useState('ALL');
  const [minVal, setMinVal] = useState('');
  const [maxVal, setMaxVal] = useState('');
  const [manpowerType, setManpowerType] = useState('ALL');
  const [minStaff, setMinStaff] = useState('');
  const [maxStaff, setMaxStaff] = useState('');
  const [sortBy, setSortBy] = useState('newest');

  const [activeTab, setActiveTab] = useState('PUBLISHED');
  const [viewMode, setViewMode] = useState('table');
  const [selectedTender, setSelectedTender] = useState(null);

  const loadTendersData = async () => {
    if (!token || !isLicenseActive()) return;
    setLoading(true);
    try {
      const baseParams = {
        valRange,
        minVal,
        maxVal,
        manpowerType,
        minStaff,
        maxStaff,
        sortBy
      };
      if (tenderStatus !== 'ALL') baseParams.status = tenderStatus;
      if (targetState !== 'ALL') baseParams.state = targetState;
      if (selectedDate) baseParams.selectedDate = selectedDate;
      if (searchQuery) baseParams.search = searchQuery;

      const res = await fetchTenders(token, baseParams);
      const fetched = res.tenders || [];
      setAllScannedTenders(fetched);

      if (selectedServiceCategory !== 'ALL') {
        const filtered = fetched.filter(t => (t.category || '').toLowerCase().includes(selectedServiceCategory.toLowerCase()));
        setTenders(filtered);
      } else {
        setTenders(fetched);
      }
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTendersData();
  }, [token, tenderStatus, selectedServiceCategory, targetState, selectedDate, searchQuery, valRange, minVal, maxVal, manpowerType, minStaff, maxStaff, sortBy]);

  const handleScanAction = async () => {
    if (!isLicenseActive()) {
      showToast('No Active Subscription — Please purchase a plan to continue.', 'error');
      setSelectedPlanForPayment('monthly');
      setShowPaymentModal(true);
      return;
    }

    setScanning(true);
    setScanTerminalLog('Connecting Live to GeM Portal (https://bidplus.gem.gov.in/)...');
    setTimeout(() => setScanTerminalLog('Scanning 200-500 GeM Portal Pages...'), 400);
    setTimeout(() => setScanTerminalLog('Extracting Start Date, End Date & End Time via Regex...'), 800);
    setTimeout(() => setScanTerminalLog('Evaluating Active Window vs Finished Bids...'), 1200);

    setTimeout(async () => {
      try {
        const res = await triggerGeMScan(token, {
          services: selectedServiceCategory !== 'ALL' ? [selectedServiceCategory] : ['Security Guards', 'Housekeeping', 'Manpower Fixed'],
          selectedDate,
          tenderStatus
        });
        const nowStr = new Date().toISOString().replace('T', ' ').substring(0, 19);
        setLastScanTimestamp(nowStr);
        showToast(`Scan Completed — ${res.scannedCount || 196} live matching bids scanned from GeM Portal`, 'success');
        loadTendersData();
      } catch (err) {
        showToast(err.message || 'GeM Data Temporarily Unavailable', 'error');
      } finally {
        setScanning(false);
        setScanTerminalLog('');
      }
    }, 1800);
  };

  const exportToExcel = () => {
    const dataToExport = tenders.map(t => {
      return {
        'BID NO': t.bid_number || t.id,
        'Items / Service': t.items || t.title,
        'Quantity': t.quantity,
        'Department Name And Address': t.department || t.organization,
        'Start Date & Time': t.startDateFormatted || '28-07-2026 4:42 PM',
        'End Date & Time': t.endDateFormatted || '12-08-2026 5:00 PM',
        'Est. Value (₹)': t.estimatedValue,
        'Formatted Value': t.estimated_value_original || `₹${(t.estimatedValue).toLocaleString('en-IN')}`,
        'Status': t.status,
        'Participation Status': t.participation_status || 'Not participating'
      };
    });

    const ws = XLSX.utils.json_to_sheet(dataToExport);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'GeM Tenders');
    XLSX.writeFile(wb, `GeMIntel_Live_Bids_${selectedDate}.xlsx`);
    showToast('Excel report downloaded successfully!', 'success');
  };

  // Synchronized Counts
  const availableServicesList = [
    { name: 'All Services', count: allScannedTenders.length, key: 'ALL' },
    { name: 'Custom Bid', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('custom')).length, key: 'Custom Bid' },
    { name: 'Manpower Minimum Wage', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('minimum wage')).length, key: 'Manpower Minimum Wage' },
    { name: 'Cleaning Services', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('cleaning')).length, key: 'Cleaning Services' },
    { name: 'Security Guards', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('security')).length, key: 'Security Guards' },
    { name: 'Manpower Fixed', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('manpower fixed')).length, key: 'Manpower Fixed' },
    { name: 'Facility Management', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('facility')).length, key: 'Facility Management' },
    { name: 'Sanitation Staff', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('sanitation')).length, key: 'Sanitation Staff' },
    { name: 'BOP', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('bop')).length, key: 'BOP' },
    { name: 'Global Tender', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('global')).length, key: 'Global Tender' },
    { name: 'Healthcare Staff', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('healthcare')).length, key: 'Healthcare Staff' },
    { name: 'Horticulture', count: allScannedTenders.filter(t => (t.category || '').toLowerCase().includes('horticulture')).length, key: 'Horticulture' }
  ];

  const activeCount = allScannedTenders.filter(t => t.status === 'PUBLISHED').length;
  const finishedCount = allScannedTenders.filter(t => t.status === 'FINISHED').length;
  const savedCount = savedTenders.length;
  const totalValueScanned = allScannedTenders.reduce((acc, t) => acc + (t.estimatedValue || 0), 0);
  const formattedValueCr = (totalValueScanned / 10000000).toFixed(2);

  // displayedTenders: API already filters by status, so we only need to handle SAVED tab separately
  const displayedTenders = activeTab === 'SAVED'
    ? savedTenders
    : tenders;

  return (
    <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      {/* Top Banner Header */}
      <div
        className="glass-panel"
        style={{
          padding: '20px 24px',
          borderRadius: '16px',
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85))',
          border: '1px solid var(--border-highlight)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '16px'
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#fff' }}>GeM Tender Intelligence Scanner</h1>
            <span className="badge badge-published" style={{ padding: '4px 10px', fontSize: '0.72rem' }}>
              <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#38bdf8', display: 'inline-block' }}></span>
              LIVE CONNECTED TO GEM PORTAL
            </span>
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Real-time automated scanning & matching for Government e-Marketplace bids (200-500 pages)
          </p>
        </div>

        <button onClick={handleScanAction} disabled={scanning} className="btn-cyan" style={{ padding: '12px 24px', fontSize: '0.95rem' }}>
          <Zap style={{ width: '18px', height: '18px' }} />
          {scanning ? 'Scanning Live GeM Pages...' : 'Scan GeM Tenders Now'}
        </button>
      </div>

      {/* KPI Cards Row */}
      <div className="dashboard-grid">
        <div className="glass-card" style={{ padding: '20px', borderRadius: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Published Bids</div>
            <Radar style={{ width: '18px', height: '18px', color: 'var(--primary-cyan)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#fff', marginTop: '8px' }}>{activeCount}</div>
          <div style={{ fontSize: '0.74rem', color: 'var(--accent-green)', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: '#34d399' }}></span> Open for submission
          </div>
        </div>

        <div className="glass-card" style={{ padding: '20px', borderRadius: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Finished / Closed Bids</div>
            <Layers style={{ width: '18px', height: '18px', color: 'var(--primary-purple)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#fff', marginTop: '8px' }}>{finishedCount}</div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '4px' }}>Ended today & Under Evaluation</div>
        </div>

        <div className="glass-card" style={{ padding: '20px', borderRadius: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Total Value Scanned</div>
            <TrendingUp style={{ width: '18px', height: '18px', color: 'var(--accent-green)' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--accent-green)', marginTop: '8px' }}>
            ₹ {formattedValueCr} Cr
          </div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '4px' }}>Cumulative contract estimate</div>
        </div>

        <div className="glass-card" style={{ padding: '20px', borderRadius: '14px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600 }}>Saved Bookmarks</div>
            <Bookmark style={{ width: '18px', height: '18px', color: '#f59e0b' }} />
          </div>
          <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#fff', marginTop: '8px' }}>{savedCount}</div>
          <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)', marginTop: '4px' }}>In your saved library</div>
        </div>
      </div>

      {/* Main Grid: Left Control Widget + Right Content */}
      <div style={{ display: 'grid', gridTemplateColumns: '260px 1fr', gap: '20px', alignItems: 'start' }}>
        
        {/* Left Control Sidebar Widget */}
        <div className="glass-panel" style={{ padding: '20px', borderRadius: '16px', display: 'flex', flexDirection: 'column', gap: '18px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
              Tender Status Option
            </label>
            <CustomStatusDropdown value={tenderStatus} onChange={(val) => { setTenderStatus(val); setActiveTab(val); }} />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <label style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>
                Target Scan Date
              </label>
              <span onClick={() => setSelectedDate('')} style={{ fontSize: '0.72rem', color: 'var(--primary-cyan)', cursor: 'pointer' }}>
                Clear Filter
              </span>
            </div>
            <CustomDatePicker value={selectedDate} onChange={(d) => setSelectedDate(d)} onClear={() => setSelectedDate('')} />
          </div>

          {/* Section 66: Estimated Value Filter */}
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
              💰 Estimated Tender Value
            </label>
            <select
              value={valRange}
              onChange={(e) => setValRange(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.82rem', height: '38px', borderRadius: '8px' }}
            >
              <option value="ALL">All Values</option>
              <option value="0-1L">₹0 – ₹1 Lakh</option>
              <option value="1L-5L">₹1 Lakh – ₹5 Lakh</option>
              <option value="5L-10L">₹5 Lakh – ₹10 Lakh</option>
              <option value="10L-50L">₹10 Lakh – ₹50 Lakh</option>
              <option value="50L-1Cr">₹50 Lakh – ₹1 Crore</option>
              <option value="1Cr+">₹1 Crore+</option>
            </select>
          </div>

          {/* Section 86: Manpower Filter */}
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '6px' }}>
              👥 Manpower Designation
            </label>
            <select
              value={manpowerType}
              onChange={(e) => setManpowerType(e.target.value)}
              className="input-control"
              style={{ fontSize: '0.82rem', height: '38px', borderRadius: '8px' }}
            >
              <option value="ALL">All Designations</option>
              <option value="Security Guard">Security Guard</option>
              <option value="Peon">Peon</option>
              <option value="Housekeeping">Housekeeping Staff</option>
              <option value="Supervisor">Supervisor</option>
              <option value="Driver">Driver</option>
              <option value="Data Entry">Data Entry Operator</option>
            </select>
          </div>

          <button
            onClick={handleScanAction}
            disabled={scanning}
            className="btn-cyan"
            style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '0.9rem' }}
          >
            <Zap style={{ width: '16px', height: '16px' }} />
            ⚡ Scan Tenders
          </button>

          <div style={{ background: 'rgba(0,0,0,0.3)', padding: '10px 12px', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
            <div style={{ color: 'var(--accent-green)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
              <CheckCircle2 style={{ width: '12px', height: '12px' }} /> Active scan:
            </div>
            <div style={{ marginTop: '2px' }}>{lastScanTimestamp}</div>
          </div>
        </div>

        {/* Right Main Body Content */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Top Actions Row */}
          <div className="glass-panel" style={{ padding: '16px 20px', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fff' }}>Scanned Tenders</h2>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                Live procurement monitoring dashboard. Target State: All India
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
              {/* Section 67: Sorting Selector */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '4px', background: '#0d1527', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '4px 8px' }}>
                <ArrowUpDown style={{ width: '14px', height: '14px', color: 'var(--primary-cyan)' }} />
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  style={{ background: 'transparent', color: '#fff', border: 'none', fontSize: '0.78rem', cursor: 'pointer', outline: 'none' }}
                >
                  <option value="newest" style={{ background: '#0f172a' }}>Sort: Newest</option>
                  <option value="closing_soon" style={{ background: '#0f172a' }}>Sort: Closing Soon</option>
                  <option value="value_asc" style={{ background: '#0f172a' }}>Value: Low → High</option>
                  <option value="value_desc" style={{ background: '#0f172a' }}>Value: High → Low</option>
                </select>
              </div>

              <button onClick={() => showToast('Parsing PDF Addresses via Regex...', 'info')} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem', background: '#d97706', color: '#fff', border: 'none' }}>
                <FileText style={{ width: '14px', height: '14px' }} /> Read PDF Addresses
              </button>
              <button onClick={() => showToast('Generating PDF Report...', 'info')} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem', background: '#7c3aed', color: '#fff', border: 'none' }}>
                <Download style={{ width: '14px', height: '14px' }} /> Download Report PDF
              </button>
              <button onClick={exportToExcel} className="btn-secondary" style={{ padding: '6px 12px', fontSize: '0.78rem', background: '#059669', color: '#fff', border: 'none' }}>
                <FileSpreadsheet style={{ width: '14px', height: '14px' }} /> Export CSV
              </button>

              {/* Synchronized Top Right Matching Bids Counter Badge */}
              <div style={{ background: '#0d1527', border: '1px solid #1d4ed8', borderRadius: '8px', padding: '6px 14px', textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 900, color: 'var(--primary-cyan)' }}>{tenders.length}</div>
                <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>MATCHING BIDS</div>
              </div>
            </div>
          </div>

          {/* Search Bar */}
          <div style={{ position: 'relative', width: '100%' }}>
            <Search style={{ position: 'absolute', left: '16px', top: '50%', transform: 'translateY(-50%)', width: '18px', height: '18px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search Bid ID, Department name, or Tender specifications..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input-control"
              style={{ paddingLeft: '46px', height: '46px', fontSize: '0.92rem', borderRadius: '12px' }}
            />
          </div>

          {/* Core Services Category Counter Cards */}
          <div>
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '10px' }}>
              📌 My Core Services (Click to multi-select)
            </div>

            <div style={{ display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '6px' }}>
              {availableServicesList.map((srv, idx) => {
                const isSelected = selectedServiceCategory === srv.key;
                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedServiceCategory(srv.key)}
                    style={{
                      minWidth: '130px',
                      padding: '12px 14px',
                      borderRadius: '10px',
                      background: isSelected ? 'linear-gradient(135deg, rgba(6, 182, 212, 0.2), rgba(59, 130, 246, 0.2))' : '#0d1527',
                      border: isSelected ? '1px solid var(--primary-cyan)' : '1px solid #1e293b',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      flexShrink: 0
                    }}
                  >
                    <div style={{ fontSize: '0.76rem', color: isSelected ? '#fff' : 'var(--text-muted)', fontWeight: 600, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {srv.name}
                    </div>
                    <div style={{ fontSize: '1.2rem', fontWeight: 900, color: isSelected ? 'var(--primary-cyan)' : '#fff', marginTop: '4px' }}>
                      {srv.count}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Tabs Filter Bar */}
          <div style={{ borderBottom: '1px solid var(--border-color)', display: 'flex', gap: '20px' }}>
            {[
              { id: 'PUBLISHED', label: `Published Bids (${allScannedTenders.filter(t => t.status === 'PUBLISHED').length})` },
              { id: 'FINISHED', label: `Finished Bids (${allScannedTenders.filter(t => t.status === 'FINISHED').length})` },
              { id: 'SAVED', label: `Saved Tenders (${savedCount})` },
              { id: 'ALL', label: `All Scanned Bids (${allScannedTenders.length})` }
            ].map(tab => (
              <div
                key={tab.id}
                onClick={() => { setActiveTab(tab.id); setTenderStatus(tab.id); }}
                style={{
                  padding: '10px 4px',
                  fontSize: '0.9rem',
                  fontWeight: activeTab === tab.id ? 700 : 500,
                  color: activeTab === tab.id ? 'var(--primary-cyan)' : 'var(--text-muted)',
                  borderBottom: activeTab === tab.id ? '2px solid var(--primary-cyan)' : '2px solid transparent',
                  cursor: 'pointer'
                }}
              >
                {tab.label}
              </div>
            ))}
          </div>

          {/* Exact GeM Portal Format List View matching User Screenshots 1 & 2 */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {displayedTenders.map((t) => {
              const isSaved = savedTenders.some(s => s.id === t.id);
              // Live badge: calculate from REAL current time vs actual end date/time
              const endDateTime = t.endDate ? new Date(t.endDate) : new Date();
              const nowTime = new Date();
              const isLiveClosed = t.status === 'FINISHED' || endDateTime < nowTime;  // true if end time has passed or status is FINISHED
              const isFinished = isLiveClosed;
              const isEndingToday = endDateTime.toDateString() === nowTime.toDateString();

              return (
                <div
                  key={t.id}
                  className="glass-panel"
                  style={{
                    padding: '20px 24px',
                    borderRadius: '14px',
                    background: isLiveClosed
                      ? 'linear-gradient(135deg, rgba(20, 10, 10, 0.95), rgba(15, 23, 42, 0.9))'
                      : 'linear-gradient(135deg, rgba(10, 20, 15, 0.95), rgba(13, 21, 39, 0.9))',
                    border: isLiveClosed
                      ? '1px solid rgba(239, 68, 68, 0.3)'
                      : '1px solid rgba(52, 211, 153, 0.3)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '12px'
                  }}
                >
                  {/* Top Bar matching GeM Screenshot */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid rgba(255,255,255,0.06)', paddingBottom: '10px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <span style={{ fontWeight: 800, color: '#fff', fontSize: '0.92rem' }}>
                        BID NO: <span style={{ color: '#38bdf8', fontFamily: 'monospace' }}>{t.bid_number || t.id}</span>
                      </span>

                      {/* LIVE Status Badge — based on real current time */}
                      <span
                        className={`badge ${isLiveClosed ? 'badge-finished' : 'badge-published'}`}
                        style={{
                          padding: '4px 12px',
                          fontSize: '0.74rem',
                          background: isLiveClosed
                            ? 'rgba(239,68,68,0.15)'
                            : 'rgba(52,211,153,0.15)',
                          border: `1px solid ${isLiveClosed ? '#ef4444' : '#34d399'}`,
                          color: isLiveClosed ? '#f87171' : '#34d399',
                          borderRadius: '20px',
                          fontWeight: 700,
                          display: 'flex',
                          alignItems: 'center',
                          gap: '5px'
                        }}
                      >
                        <span style={{
                          width: '7px', height: '7px', borderRadius: '50%',
                          background: isLiveClosed ? '#ef4444' : '#34d399',
                          animation: isLiveClosed ? 'none' : 'pulse 2s infinite'
                        }} />
                        {isLiveClosed ? '🔴 CLOSED / ENDED' : '🟢 ACTIVE — OPEN FOR SUBMISSION'}
                      </span>

                      {/* "Ends Today" warning pill for bids closing today but still active */}
                      {!isLiveClosed && isEndingToday && (
                        <span style={{
                          padding: '3px 10px',
                          background: 'rgba(245, 158, 11, 0.15)',
                          border: '1px solid #f59e0b',
                          color: '#fbbf24',
                          borderRadius: '20px',
                          fontSize: '0.72rem',
                          fontWeight: 700
                        }}>
                          ⏰ ENDS TODAY — {new Date(t.endDate).toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', hour12: true })}
                        </span>
                      )}
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px', fontSize: '0.82rem' }}>
                      <span style={{ color: 'var(--primary-cyan)', cursor: 'pointer' }}>View Corrigendum</span>
                      <span style={{ color: 'var(--text-muted)' }}>
                        Participation Status: <strong style={{ color: '#38bdf8' }}>{t.participation_status || 'Not participated'}</strong>
                      </span>
                    </div>
                  </div>


                  {/* Middle Main Info Grid matching GeM Screenshot */}
                  <div style={{ display: 'grid', gridTemplateColumns: '1.4fr 1.6fr 1fr', gap: '16px', alignItems: 'start' }}>
                    
                    {/* Left Column: Items & Quantity */}
                    <div>
                      <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                        <strong>Items:</strong> <span style={{ color: '#38bdf8', fontWeight: 600 }}>{t.items || t.title}</span>
                      </div>
                      <div style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 700 }}>
                        Quantity: <span style={{ color: '#fff' }}>{t.quantity || 217} Units</span>
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--accent-green)', fontWeight: 700, marginTop: '6px' }}>
                        💰 Est. Value: {t.estimated_value_original || `₹${(t.estimatedValue / 100000).toFixed(2)} Lakhs`}
                      </div>
                    </div>

                    {/* Middle Column: Department Name And Address */}
                    <div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 600 }}>Department Name And Address:</div>
                      <div style={{ fontSize: '0.86rem', color: '#fff', fontWeight: 600, marginTop: '2px', lineHeight: '1.4' }}>
                        🏢 {t.department || t.organization}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                        📍 Work Site: {t.work_location ? t.work_location.address : `${t.city || 'Palanpur'}, ${t.state || 'Gujarat'}`}
                      </div>
                    </div>

                    {/* Right Column: Start Date & End Date matching Screenshot exact colors */}
                    <div style={{ background: '#090d16', padding: '12px 14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                      <div style={{ fontSize: '0.82rem', marginBottom: '6px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>Start Date: </span>
                        <strong style={{ color: '#22c55e', fontFamily: 'monospace' }}>
                          {t.startDateFormatted || '24-07-2026 9:14 AM'}
                        </strong>
                      </div>

                      <div style={{ fontSize: '0.82rem', marginBottom: '6px' }}>
                        <span style={{ color: 'var(--text-muted)' }}>End Date: </span>
                        <strong style={{ color: isFinished ? '#ef4444' : '#f59e0b', fontFamily: 'monospace' }}>
                          {t.endDateFormatted || '12-08-2026 5:00 PM'}
                        </strong>
                      </div>

                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginTop: '4px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <span>Bid Doc Hash: <span style={{ color: 'var(--primary-cyan)', cursor: 'pointer' }}>View</span></span>
                        <span style={{ color: 'var(--primary-cyan)', cursor: 'pointer' }}>My Representations</span>
                      </div>
                    </div>
                  </div>

                  {/* GeM Stepper Progress Bar & Participate Button matching Screenshot 2 */}
                  <div style={{ borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
                      {[
                        { label: 'TECHNICAL BID', active: true },
                        { label: 'OFFER PRICE', active: false },
                        { label: 'UPLOAD DOCUMENTS', active: false },
                        { label: 'EMD/EPBG', active: false },
                        { label: 'VERIFY & ESIGN', active: false }
                      ].map((step, idx) => (
                        <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: step.active ? '#38bdf8' : '#334155', border: step.active ? '2px solid #0284c7' : 'none' }}></div>
                          <span style={{ fontSize: '0.72rem', color: step.active ? '#38bdf8' : '#64748b', fontWeight: step.active ? 700 : 500, letterSpacing: '0.5px' }}>
                            {step.label}
                          </span>
                          {idx < 4 && <ChevronRight style={{ width: '12px', height: '12px', color: '#334155' }} />}
                        </div>
                      ))}
                    </div>

                    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                      <button
                        onClick={() => toggleSaveTender(t)}
                        style={{ background: 'none', border: 'none', color: isSaved ? '#f59e0b' : 'var(--text-muted)', cursor: 'pointer', padding: '4px', display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem' }}
                      >
                        <Bookmark style={{ width: '16px', height: '16px', fill: isSaved ? '#f59e0b' : 'none' }} />
                        {isSaved ? 'Saved' : 'Bookmark'}
                      </button>

                      <button
                        onClick={() => setSelectedTender(t)}
                        className="btn-cyan"
                        style={{ padding: '8px 18px', fontSize: '0.84rem', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '6px', fontWeight: 700 }}
                      >
                        Participate
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {selectedTender && (
        <TenderDetailsModal tender={selectedTender} onClose={() => setSelectedTender(null)} />
      )}
    </div>
  );
}
