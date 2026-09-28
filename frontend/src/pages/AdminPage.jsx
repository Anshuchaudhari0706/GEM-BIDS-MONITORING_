import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Crown,
  Users,
  Key,
  CreditCard,
  Receipt,
  Plus,
  ShieldCheck,
  ShieldAlert,
  Save,
  Tag,
  Database,
  Settings,
  Search,
  CheckCircle2,
  Trash2,
  Edit,
  Clock,
  UserPlus,
  UserCheck,
  UserX,
  Sparkles,
  Server,
  Sliders,
  Download,
  UploadCloud,
  Bell,
  Lock,
  Globe,
  Activity,
  FileCode,
  Check,
  AlertCircle,
  Cpu,
  Zap,
  RotateCcw,
  FileText,
  Eye,
  EyeOff,
  Send,
  AlertTriangle,
  RefreshCw,
  ExternalLink
} from 'lucide-react';

export default function AdminPage({ currentTab }) {
  const { token, showToast } = useAuth();

  const [kpis, setKpis] = useState({
    totalUsers: 0,
    activeUsers: 0,
    expiredUsers: 0,
    totalRevenue: 0,
    activeSubscriptions: 0,
    generatedKeys: 0,
    usedKeys: 0,
    expiredKeys: 0
  });

  const [usersList, setUsersList] = useState([]);
  const [licensesList, setLicensesList] = useState([]);
  const [plansList, setPlansList] = useState([]);
  const [paymentsList, setPaymentsList] = useState([]);
  const [adminLogs, setAdminLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // Tab State
  const [activeAdminSubTab, setActiveAdminSubTab] = useState(currentTab || 'admin-dashboard');

  // Search States
  const [userSearch, setUserSearch] = useState('');
  const [keySearch, setKeySearch] = useState('');

  // Modals & Form States
  const [showCreateUserModal, setShowCreateUserModal] = useState(false);
  const [newUserForm, setNewUserForm] = useState({ fullName: '', companyName: '', email: '', mobile: '', password: '', role: 'user' });

  // Key Generator State
  const [genUserEmail, setGenUserEmail] = useState('');
  const [genPlan, setGenPlan] = useState('yearly');
  const [genDuration, setGenDuration] = useState('365');

  // Load All Admin Data
  const loadAdminData = async () => {
    if (!token) return;
    setLoading(true);
    try {
      // 1. Fetch KPIs (Section 26)
      const kpiRes = await fetch('/api/admin/kpis', { headers: { Authorization: `Bearer ${token}` } });
      const kpiData = await kpiRes.json();
      setKpis(kpiData);

      // 2. Fetch Users
      const uRes = await fetch(`/api/admin/users?search=${encodeURIComponent(userSearch)}`, { headers: { Authorization: `Bearer ${token}` } });
      const uData = await uRes.json();
      setUsersList(uData.users || []);

      // 3. Fetch Licenses (Section 28)
      const lRes = await fetch('/api/admin/licenses', { headers: { Authorization: `Bearer ${token}` } });
      const lData = await lRes.json();
      setLicensesList(lData.licenses || []);

      // 4. Fetch Pricing Plans (Section 29)
      const pRes = await fetch('/api/admin/subscriptions', { headers: { Authorization: `Bearer ${token}` } });
      const pData = await pRes.json();
      setPlansList(pData.plans || []);

      // 5. Fetch Payments
      const payRes = await fetch('/api/admin/payments', { headers: { Authorization: `Bearer ${token}` } });
      const payData = await payRes.json();
      setPaymentsList(payData.payments || []);

      // 6. Fetch Logs
      const logRes = await fetch('/api/admin/logs', { headers: { Authorization: `Bearer ${token}` } });
      const logData = await logRes.json();
      setAdminLogs(logData.logs || []);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAdminData();
  }, [token, userSearch, activeAdminSubTab]);

  useEffect(() => {
    if (currentTab && currentTab.startsWith('admin-')) {
      setActiveAdminSubTab(currentTab);
    }
  }, [currentTab]);

  // Admin User Actions (Section 27)
  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/admin/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(newUserForm)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`User ${newUserForm.email} created!`, 'success');
      setShowCreateUserModal(false);
      setNewUserForm({ fullName: '', companyName: '', email: '', mobile: '', password: '', role: 'user' });
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleUpdateUserStatus = async (userId, newStatus) => {
    try {
      const res = await fetch(`/api/admin/users/${userId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ status: newStatus })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`User status set to ${newStatus}`, 'info');
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDeleteUser = async (userId) => {
    if (!window.confirm('Are you sure you want to delete this user?')) return;
    try {
      const res = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast('User deleted', 'info');
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Admin Key Actions (Section 28)
  const handleGenerateKey = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/admin/licenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ userEmail: genUserEmail, plan: genPlan, durationDays: genDuration })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`Cryptographic Key Generated: ${data.license.key}`, 'success');
      setGenUserEmail('');
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleUpdateKey = async (licenseId, payload) => {
    try {
      const res = await fetch(`/api/admin/licenses/${licenseId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(data.message, 'info');
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  // Admin Pricing Action (Section 29)
  const handleSavePlan = async (planId, planData) => {
    try {
      const res = await fetch(`/api/admin/subscriptions/${planId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(planData)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`Subscription plan ${planData.name} updated!`, 'success');
      loadAdminData();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const filteredKeys = licensesList.filter(k =>
    (k.key || '').toLowerCase().includes(keySearch.toLowerCase()) ||
    (k.userEmail || '').toLowerCase().includes(keySearch.toLowerCase()) ||
    (k.plan || '').toLowerCase().includes(keySearch.toLowerCase())
  );

  return (
    <div style={{ padding: '32px', flex: 1, display: 'flex', flexDirection: 'column', gap: '28px', maxWidth: '1600px', margin: '0 auto', width: '100%' }}>
      
      {/* Page Title & Breadcrumb */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div
            style={{
              width: '48px',
              height: '48px',
              borderRadius: '14px',
              background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(239, 68, 68, 0.15))',
              border: '1px solid rgba(245, 158, 11, 0.4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 20px rgba(245, 158, 11, 0.25)'
            }}
          >
            <Crown style={{ width: '28px', height: '28px', color: '#f59e0b' }} />
          </div>
          <div>
            <h1 style={{ fontSize: '1.9rem', fontWeight: 900, color: '#fff', letterSpacing: '-0.03em', lineHeight: 1.2 }}>
              GeMIntel Admin Console
            </h1>
            <p style={{ fontSize: '0.94rem', color: 'var(--text-muted)', fontWeight: 500, marginTop: '2px' }}>
              Master system control, license key generation, pricing models, crawler engine & audit telemetry
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <span className="badge badge-published" style={{ fontSize: '0.82rem', padding: '6px 14px' }}>
            MASTER ADMIN ACCESS
          </span>
        </div>
      </div>

      {/* Subtabs Menu */}
      <div
        style={{
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          gap: '8px',
          overflowX: 'auto',
          paddingBottom: '2px'
        }}
      >
        {[
          { id: 'admin-dashboard', label: 'Admin Dashboard', icon: Crown },
          { id: 'admin-users', label: 'User Management', icon: Users },
          { id: 'admin-keys', label: 'License Key Manager', icon: Key },
          { id: 'admin-payments', label: 'Payment Logs', icon: Receipt },
          { id: 'admin-subscriptions', label: 'Pricing Configurator', icon: CreditCard },
          { id: 'admin-services', label: 'Service Manager', icon: Tag },
          { id: 'admin-tenders', label: 'Tender Data', icon: Database },
          { id: 'admin-settings', label: 'System Settings', icon: Settings }
        ].map(tab => {
          const Icon = tab.icon;
          const isActive = activeAdminSubTab === tab.id;
          return (
            <div
              key={tab.id}
              onClick={() => setActiveAdminSubTab(tab.id)}
              style={{
                padding: '12px 18px',
                fontSize: '0.96rem',
                fontWeight: isActive ? 800 : 600,
                color: isActive ? '#f59e0b' : 'var(--text-muted)',
                borderBottom: isActive ? '3px solid #f59e0b' : '3px solid transparent',
                background: isActive ? 'rgba(245, 158, 11, 0.08)' : 'transparent',
                borderRadius: '8px 8px 0 0',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s ease'
              }}
            >
              <Icon style={{ width: '18px', height: '18px' }} />
              {tab.label}
            </div>
          );
        })}
      </div>

      {/* 26. VIEW 1: ADMIN DASHBOARD (8 KPI Cards) */}
      {activeAdminSubTab === 'admin-dashboard' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '28px' }}>
          <div className="dashboard-grid">
            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Users</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#fff', marginTop: '8px' }}>{kpis.totalUsers}</div>
              <div style={{ fontSize: '0.84rem', color: 'var(--accent-green-bright)', marginTop: '4px', fontWeight: 600 }}>Registered platform accounts</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Active Users</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: 'var(--primary-cyan-bright)', marginTop: '8px' }}>{kpis.activeUsers}</div>
              <div style={{ fontSize: '0.84rem', color: 'var(--primary-cyan-bright)', marginTop: '4px', fontWeight: 600 }}>Enabled active accounts</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Expired Users</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#f43f5e', marginTop: '8px' }}>{kpis.expiredUsers}</div>
              <div style={{ fontSize: '0.84rem', color: '#f43f5e', marginTop: '4px', fontWeight: 600 }}>Subscription ended</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Total Revenue</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#f59e0b', marginTop: '8px' }}>₹ {kpis.totalRevenue.toLocaleString('en-IN')}</div>
              <div style={{ fontSize: '0.84rem', color: '#f59e0b', marginTop: '4px', fontWeight: 600 }}>Verified payments collected</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Active Subscriptions</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: 'var(--accent-green)', marginTop: '8px' }}>{kpis.activeSubscriptions}</div>
              <div style={{ fontSize: '0.84rem', color: 'var(--accent-green)', marginTop: '4px', fontWeight: 600 }}>🟢 ACTIVE licensed users</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Generated Keys</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#fff', marginTop: '8px' }}>{kpis.generatedKeys}</div>
              <div style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginTop: '4px', fontWeight: 600 }}>Cryptographic keys created</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Used Keys</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: 'var(--primary-purple)', marginTop: '8px' }}>{kpis.usedKeys}</div>
              <div style={{ fontSize: '0.84rem', color: 'var(--primary-purple)', marginTop: '4px', fontWeight: 600 }}>Assigned to active profiles</div>
            </div>

            <div className="glass-card" style={{ padding: '24px' }}>
              <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px' }}>Expired Keys</div>
              <div style={{ fontSize: '2.2rem', fontWeight: 900, color: '#f43f5e', marginTop: '8px' }}>{kpis.expiredKeys}</div>
              <div style={{ fontSize: '0.84rem', color: '#f43f5e', marginTop: '4px', fontWeight: 600 }}>Past license expiration</div>
            </div>
          </div>
        </div>
      )}

      {/* 27. VIEW 2: USER MANAGEMENT */}
      {activeAdminSubTab === 'admin-users' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px' }}>
            <div style={{ position: 'relative', width: '380px', maxWidth: '100%' }}>
              <Search style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', width: '18px', color: 'var(--text-muted)' }} />
              <input
                type="text"
                placeholder="Search user name, email, company..."
                value={userSearch}
                onChange={(e) => setUserSearch(e.target.value)}
                className="input-control"
                style={{ paddingLeft: '44px', height: '44px', fontSize: '0.94rem' }}
              />
            </div>

            <button onClick={() => setShowCreateUserModal(true)} className="btn-cyan" style={{ padding: '12px 22px', fontSize: '0.94rem' }}>
              <UserPlus style={{ width: '18px', height: '18px' }} />
              Create New User Account
            </button>
          </div>

          <div className="glass-panel" style={{ borderRadius: '16px', overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.94rem' }}>
              <thead>
                <tr style={{ background: 'rgba(15,23,42,0.95)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>User Name</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>Company</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>Email & Contact</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>Role</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>Assigned License Key</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800 }}>Account Status</th>
                  <th style={{ padding: '16px 20px', fontWeight: 800, textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {usersList.map(u => {
                  const lic = u.licenses && u.licenses.length ? u.licenses[0] : null;
                  return (
                    <tr key={u.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '16px 20px', color: '#fff', fontWeight: 700, fontSize: '0.96rem' }}>{u.fullName}</td>
                      <td style={{ padding: '16px 20px', color: 'var(--text-muted)' }}>{u.companyName || '—'}</td>
                      <td style={{ padding: '16px 20px', color: 'var(--text-muted)' }}>
                        <div style={{ color: '#fff', fontWeight: 600 }}>{u.email}</div>
                        <div style={{ fontSize: '0.84rem', marginTop: '2px' }}>{u.mobile || '—'}</div>
                      </td>
                      <td style={{ padding: '16px 20px' }}>
                        <span className={`badge ${u.role === 'admin' ? 'badge-finished' : 'badge-published'}`}>
                          {u.role.toUpperCase()}
                        </span>
                      </td>
                      <td style={{ padding: '16px 20px', fontFamily: 'JetBrains Mono, monospace', color: 'var(--primary-cyan-bright)', fontWeight: 700, fontSize: '0.92rem' }}>
                        {lic ? lic.key : 'No Key Assigned'}
                      </td>
                      <td style={{ padding: '16px 20px' }}>
                        <span className={`badge ${u.status === 'ACTIVE' ? 'badge-active' : 'badge-expired'}`}>
                          {u.status}
                        </span>
                      </td>
                      <td style={{ padding: '16px 20px', textAlign: 'right' }}>
                        <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
                          <button
                            onClick={() => handleUpdateUserStatus(u.id, u.status === 'ACTIVE' ? 'DISABLED' : 'ACTIVE')}
                            className="btn-secondary"
                            style={{ padding: '6px 12px', fontSize: '0.84rem', color: u.status === 'ACTIVE' ? '#f43f5e' : '#10b981' }}
                          >
                            {u.status === 'ACTIVE' ? 'Disable' : 'Activate'}
                          </button>
                          <button
                            onClick={() => handleDeleteUser(u.id)}
                            style={{ background: 'none', border: 'none', color: '#f43f5e', cursor: 'pointer', padding: '6px' }}
                            title="Delete User"
                          >
                            <Trash2 style={{ width: '18px', height: '18px' }} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* 28. VIEW 3: LICENSE KEY MANAGER */}
      {activeAdminSubTab === 'admin-keys' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Top Key Generator Form & Search */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
            <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#fff', marginBottom: '18px', display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Key style={{ width: '20px', color: '#f59e0b' }} />
                Generate Secure Key (GEMI-XXXX)
              </h3>
              <form onSubmit={handleGenerateKey}>
                <div style={{ marginBottom: '16px' }}>
                  <label style={{ fontSize: '0.86rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Recipient User Email</label>
                  <input
                    type="email"
                    required
                    placeholder="user@company.com"
                    value={genUserEmail}
                    onChange={(e) => setGenUserEmail(e.target.value)}
                    className="input-control"
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '20px' }}>
                  <div>
                    <label style={{ fontSize: '0.86rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Plan Duration</label>
                    <select className="select-control" style={{ width: '100%' }} value={genPlan} onChange={(e) => setGenPlan(e.target.value)}>
                      <option value="monthly">Monthly Pass (30 Days)</option>
                      <option value="quarterly">Quarterly Pass (90 Days)</option>
                      <option value="yearly">Professional Yearly (365 Days)</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ fontSize: '0.86rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Days</label>
                    <input type="number" value={genDuration} onChange={(e) => setGenDuration(e.target.value)} className="input-control" />
                  </div>
                </div>

                <button type="submit" className="btn-cyan" style={{ width: '100%', justifyContent: 'center', padding: '12px' }}>
                  Generate Cryptographic Key
                </button>
              </form>
            </div>

            {/* Key List Search & Table */}
            <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#fff' }}>All License Keys ({filteredKeys.length})</h3>
                <input
                  type="text"
                  placeholder="Search key code, email..."
                  value={keySearch}
                  onChange={(e) => setKeySearch(e.target.value)}
                  className="input-control"
                  style={{ width: '260px', height: '40px', fontSize: '0.88rem' }}
                />
              </div>

              <div style={{ overflowX: 'auto', maxHeight: '400px' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.92rem' }}>
                  <thead>
                    <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
                      <th style={{ padding: '12px 14px', fontWeight: 800 }}>Key Code</th>
                      <th style={{ padding: '12px 14px', fontWeight: 800 }}>User Email</th>
                      <th style={{ padding: '12px 14px', fontWeight: 800 }}>Plan</th>
                      <th style={{ padding: '12px 14px', fontWeight: 800 }}>Expiry</th>
                      <th style={{ padding: '12px 14px', fontWeight: 800 }}>Status</th>
                      <th style={{ padding: '12px 14px', fontWeight: 800, textAlign: 'right' }}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredKeys.map(k => (
                      <tr key={k.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <td style={{ padding: '12px 14px', fontFamily: 'JetBrains Mono, monospace', fontWeight: 800, color: 'var(--primary-cyan-bright)' }}>{k.key}</td>
                        <td style={{ padding: '12px 14px', color: '#fff', fontWeight: 600 }}>{k.userEmail}</td>
                        <td style={{ padding: '12px 14px', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{k.plan}</td>
                        <td style={{ padding: '12px 14px', color: 'var(--text-muted)' }}>{new Date(k.expiryDate).toLocaleDateString('en-GB')}</td>
                        <td style={{ padding: '12px 14px' }}>
                          <span className={`badge ${k.status === 'ACTIVE' ? 'badge-active' : 'badge-expired'}`}>{k.status}</span>
                        </td>
                        <td style={{ padding: '12px 14px', textAlign: 'right' }}>
                          <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                            <button
                              onClick={() => handleUpdateKey(k.id, { extendDays: 30 })}
                              className="btn-secondary"
                              style={{ padding: '4px 10px', fontSize: '0.8rem' }}
                            >
                              +30 Days
                            </button>
                            <button
                              onClick={() => handleUpdateKey(k.id, { status: k.status === 'ACTIVE' ? 'SUSPENDED' : 'ACTIVE' })}
                              className="btn-secondary"
                              style={{ padding: '4px 10px', fontSize: '0.8rem', color: k.status === 'ACTIVE' ? '#f43f5e' : '#10b981' }}
                            >
                              {k.status === 'ACTIVE' ? 'Suspend' : 'Activate'}
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 29. VIEW 4: PRICING MANAGEMENT */}
      {activeAdminSubTab === 'admin-subscriptions' && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: '24px' }}>
          {plansList.map(plan => (
            <AdminPlanEditorCard key={plan.id} plan={plan} onSave={handleSavePlan} />
          ))}
        </div>
      )}

      {/* VIEW 5: PAYMENTS LOGS */}
      {activeAdminSubTab === 'admin-payments' && (
        <div className="glass-panel" style={{ borderRadius: '16px', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.94rem' }}>
            <thead>
              <tr style={{ background: 'rgba(15,23,42,0.95)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>Payment ID</th>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>User Email</th>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>Gateway</th>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>Amount</th>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>Verification Signature</th>
                <th style={{ padding: '16px 20px', fontWeight: 800 }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {paymentsList.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '16px 20px', fontFamily: 'JetBrains Mono, monospace', color: 'var(--primary-cyan-bright)', fontWeight: 700 }}>{p.id}</td>
                  <td style={{ padding: '16px 20px', color: '#fff', fontWeight: 600 }}>{p.userEmail}</td>
                  <td style={{ padding: '16px 20px', color: 'var(--text-muted)' }}>{p.gateway || 'Razorpay'}</td>
                  <td style={{ padding: '16px 20px', color: 'var(--accent-green-bright)', fontWeight: 800, fontSize: '1.05rem' }}>₹ {p.amount}</td>
                  <td style={{ padding: '16px 20px', fontSize: '0.84rem', color: 'var(--text-muted)', fontFamily: 'JetBrains Mono, monospace' }}>Verified HMAC SHA256</td>
                  <td style={{ padding: '16px 20px' }}><span className="badge badge-active">{p.status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* VIEW 6: SERVICES */}
      {activeAdminSubTab === 'admin-services' && (
        <AdminServicesManager token={token} showToast={showToast} />
      )}

      {/* VIEW 7: TENDER DATA MANAGER */}
      {activeAdminSubTab === 'admin-tenders' && (
        <AdminTenderDataManager token={token} showToast={showToast} />
      )}

      {/* VIEW 9: SYSTEM SETTINGS CONSOLE */}
      {activeAdminSubTab === 'admin-settings' && (
        <AdminSystemSettings token={token} showToast={showToast} />
      )}

      {showCreateUserModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(5,8,16,0.88)', backdropFilter: 'blur(12px)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '24px' }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '540px', padding: '32px', borderRadius: '20px' }}>
            <h2 style={{ fontSize: '1.45rem', fontWeight: 900, color: '#fff', marginBottom: '22px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <UserPlus style={{ width: '22px', color: 'var(--primary-cyan)' }} />
              Create New Account
            </h2>
            <form onSubmit={handleCreateUser}>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Full Name *</label>
                <input type="text" required value={newUserForm.fullName} onChange={(e) => setNewUserForm({ ...newUserForm, fullName: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Company Name</label>
                <input type="text" value={newUserForm.companyName} onChange={(e) => setNewUserForm({ ...newUserForm, companyName: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Email Address *</label>
                <input type="email" required value={newUserForm.email} onChange={(e) => setNewUserForm({ ...newUserForm, email: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Mobile Number</label>
                <input type="text" value={newUserForm.mobile} onChange={(e) => setNewUserForm({ ...newUserForm, mobile: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '22px' }}>
                <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Password *</label>
                <input type="password" required value={newUserForm.password} onChange={(e) => setNewUserForm({ ...newUserForm, password: e.target.value })} className="input-control" />
              </div>
              <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
                <button type="button" onClick={() => setShowCreateUserModal(false)} className="btn-secondary" style={{ padding: '10px 20px', fontSize: '0.92rem' }}>Cancel</button>
                <button type="submit" className="btn-cyan" style={{ padding: '10px 24px', fontSize: '0.92rem' }}>Create Account</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

// Plan Editor Card for Section 29
function AdminPlanEditorCard({ plan, onSave }) {
  const [formData, setFormData] = useState({
    name: plan.name,
    price: plan.price,
    duration_days: plan.duration_days,
    status: plan.status || 'ACTIVE'
  });

  const handleSave = (e) => {
    e.preventDefault();
    onSave(plan.id, formData);
  };

  return (
    <div className="glass-panel" style={{ padding: '28px', borderRadius: '18px' }}>
      <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--primary-cyan-bright)', marginBottom: '20px' }}>
        Configure {plan.name}
      </h3>
      <form onSubmit={handleSave}>
        <div style={{ marginBottom: '16px' }}>
          <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Plan Name</label>
          <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="input-control" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '16px' }}>
          <div>
            <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Price (₹ INR)</label>
            <input type="number" value={formData.price} onChange={(e) => setFormData({ ...formData, price: e.target.value })} className="input-control" />
          </div>
          <div>
            <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Duration (Days)</label>
            <input type="number" value={formData.duration_days} onChange={(e) => setFormData({ ...formData, duration_days: e.target.value })} className="input-control" />
          </div>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ fontSize: '0.88rem', color: 'var(--text-muted)', fontWeight: 700, display: 'block', marginBottom: '6px' }}>Plan Status</label>
          <select className="select-control" style={{ width: '100%' }} value={formData.status} onChange={(e) => setFormData({ ...formData, status: e.target.value })}>
            <option value="ACTIVE">ACTIVE</option>
            <option value="INACTIVE">INACTIVE</option>
          </select>
        </div>

        <button type="submit" className="btn-cyan" style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '0.94rem' }}>
          <Save style={{ width: '18px', height: '18px' }} /> Save Plan Config
        </button>
      </form>
    </div>
  );
}

function AdminServicesManager({ token, showToast }) {
  const [services, setServices] = useState([]);
  const [newServiceName, setNewServiceName] = useState('');

  const loadServices = async () => {
    try {
      const res = await fetch('/api/services');
      const data = await res.json();
      setServices(data.services || []);
    } catch (e) {
      showToast('Failed to load services', 'error');
    }
  };

  useEffect(() => {
    loadServices();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newServiceName.trim()) return;
    try {
      const res = await fetch('/api/admin/services', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ name: newServiceName.trim() })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`Service "${newServiceName}" added!`, 'success');
      setNewServiceName('');
      setServices(data.services);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  const handleDelete = async (name) => {
    try {
      const res = await fetch(`/api/admin/services/${encodeURIComponent(name)}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`Service "${name}" removed`, 'info');
      setServices(data.services);
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '800px' }}>
      <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '12px' }}>
          Add Custom GeM Service Category
        </h3>
        <form onSubmit={handleAdd} style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            placeholder="e.g. Solar Operations & Maintenance"
            value={newServiceName}
            onChange={(e) => setNewServiceName(e.target.value)}
            className="input-control"
          />
          <button type="submit" className="btn-cyan" style={{ flexShrink: 0 }}>
            + Add Service
          </button>
        </form>
      </div>

      <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '16px' }}>
          Configured Services ({services.length})
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: '12px' }}>
          {services.map((srv, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.03)', padding: '12px 14px', borderRadius: '8px', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <span style={{ color: '#fff', fontWeight: 600, fontSize: '0.88rem' }}>{srv}</span>
              <button onClick={() => handleDelete(srv)} style={{ background: 'none', border: 'none', color: '#f43f5e', cursor: 'pointer' }}>✕</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// SECTION: ADMIN SYSTEM SETTINGS CONSOLE (Section 25 / 30)
// -------------------------------------------------------------
function AdminSystemSettings({ token, showToast }) {
  const [settingsSubTab, setSettingsSubTab] = useState('scraper');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [testingWebhook, setTestingWebhook] = useState(false);
  const [triggeringScan, setTriggeringScan] = useState(false);
  const [clearingCache, setClearingCache] = useState(false);
  const [showSecret, setShowSecret] = useState(false);

  const defaultSettings = {
    scraper: {
      engine: 'node_axios',
      gemEndpointUrl: 'https://bidplus.gem.gov.in/all-bids-data',
      autoScanIntervalMinutes: 30,
      maxPagesPerScan: 25,
      rateLimitDelayMs: 400,
      autoFilterServicesOnly: true,
      rotateUserAgents: true,
      proxyEnabled: false,
      proxyUrl: ''
    },
    payment: {
      adminUpiId: '6353731568-2@ybl',
      adminUpiPayeeName: 'GeMIntel Technologies',
      autoVerifyUtr: true,
      gstPercentage: 18,
      currency: 'INR'
    },
    security: {
      maintenanceMode: false,
      maintenanceMessage: 'System is currently undergoing scheduled maintenance. Please check back shortly.',
      enforceLicenseOnSignup: false,
      freeTrialDays: 7,
      jwtExpiryDays: 7,
      licenseKeyPrefix: 'GEMI-',
      maxConcurrentSessions: 2
    },
    alerts: {
      highValueTenderThreshold: 5000000,
      alertEmail: 'admin@gemintel.com',
      enableHighValueEmailAlerts: true,
      webhookUrl: '',
      enableWebhookAlerts: false,
      dailySummaryEmail: true
    }
  };

  const [settings, setSettings] = useState(defaultSettings);

  const loadSettings = async () => {
    try {
      setLoading(true);
      const res = await fetch('/api/admin/settings', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.settings) {
        setSettings(data.settings);
      }
    } catch (err) {
      showToast('Failed to load system settings', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSettings();
  }, [token]);

  const updateSectionField = (section, field, value) => {
    setSettings(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const handleSave = async (e) => {
    if (e) e.preventDefault();
    try {
      setSaving(true);
      const res = await fetch('/api/admin/settings', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ settings })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to save settings');
      showToast('System configuration saved and active!', 'success');
      if (data.settings) setSettings(data.settings);
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleTriggerLiveScan = async () => {
    try {
      setTriggeringScan(true);
      const res = await fetch('/api/admin/system/trigger-scan', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(data.message || 'Live GeM scan triggered!', 'success');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setTriggeringScan(false);
    }
  };

  const handleClearCache = async () => {
    if (!window.confirm('Clear crawler cache and purge duplicate tenders?')) return;
    try {
      setClearingCache(true);
      const res = await fetch('/api/admin/system/clear-cache', {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(data.message || 'Cache cleared successfully', 'info');
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setClearingCache(false);
    }
  };

  const handleDownloadBackup = () => {
    const downloadUrl = `/api/admin/system/backup`;
    fetch(downloadUrl, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.blob())
      .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `gemintel_backup_${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast('Database backup downloaded successfully', 'success');
      })
      .catch(() => showToast('Failed to download backup', 'error'));
  };

  const handleTestWebhook = async () => {
    const url = settings.alerts?.webhookUrl;
    if (!url) {
      showToast('Please enter a Webhook URL first', 'error');
      return;
    }
    try {
      setTestingWebhook(true);
      const res = await fetch('/api/admin/system/test-webhook', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ webhookUrl: url })
      });
      const data = await res.json();
      if (data.success) {
        showToast(data.message || 'Webhook ping delivered!', 'success');
      } else {
        showToast(data.message || 'Webhook test failed', 'error');
      }
    } catch (err) {
      showToast('Webhook dispatch failed', 'error');
    } finally {
      setTestingWebhook(false);
    }
  };

  const handleResetDefaults = () => {
    if (window.confirm('Reset all settings to default values? Unsaved changes will be applied.')) {
      setSettings(defaultSettings);
      showToast('Reset to defaults. Click "Save Settings" to persist.', 'info');
    }
  };

  if (loading) {
    return (
      <div className="glass-panel" style={{ padding: '40px', textAlign: 'center', color: 'var(--primary-cyan)' }}>
        Loading System Settings Configuration...
      </div>
    );
  }

  const subTabs = [
    { id: 'scraper', label: 'Scraper & Crawler Engine', icon: Server, desc: 'Crawler delays, page limits & endpoints' },
    { id: 'payment', label: 'UPI Payment & Billing', icon: CreditCard, desc: 'Direct UPI QR & merchant handle settings' },
    { id: 'security', label: 'Security & Access Control', icon: Lock, desc: 'Maintenance mode, trial days & sessions' },
    { id: 'alerts', label: 'Alerts & Webhooks', icon: Bell, desc: 'High-value tender threshold & notification bots' },
    { id: 'maintenance', label: 'System Operations & Backups', icon: Activity, desc: 'Live scan trigger, cache flush & database export' }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* Settings Navigation Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
        {subTabs.map(tab => {
          const Icon = tab.icon;
          const isActive = settingsSubTab === tab.id;
          return (
            <div
              key={tab.id}
              onClick={() => setSettingsSubTab(tab.id)}
              className="glass-card"
              style={{
                padding: '16px',
                cursor: 'pointer',
                borderColor: isActive ? '#f59e0b' : 'var(--border-color)',
                background: isActive ? 'rgba(245, 158, 11, 0.08)' : 'rgba(15, 23, 42, 0.5)'
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                <Icon style={{ width: '18px', height: '18px', color: isActive ? '#f59e0b' : 'var(--primary-cyan)' }} />
                <span style={{ fontSize: '0.9rem', fontWeight: 700, color: isActive ? '#fff' : 'var(--text-muted)' }}>
                  {tab.label}
                </span>
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>
                {tab.desc}
              </p>
            </div>
          );
        })}
      </div>

      {/* Main Settings Panel */}
      <div className="glass-panel" style={{ padding: '28px', borderRadius: '16px' }}>
        <form onSubmit={handleSave}>
          
          {/* TAB 1: SCRAPER & CRAWLER */}
          {settingsSubTab === 'scraper' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Server style={{ width: '22px', color: 'var(--primary-cyan)' }} />
                  GeM Public Portal Scraper Engine Configuration
                </h2>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Configure background crawler parameters, target public APIs, pagination limits, and rate-limiting safeguards.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Scraper Execution Engine
                  </label>
                  <select
                    className="select-control"
                    style={{ width: '100%' }}
                    value={settings.scraper?.engine || 'node_axios'}
                    onChange={(e) => updateSectionField('scraper', 'engine', e.target.value)}
                  >
                    <option value="node_axios">High-Throughput Node.js Axios Connector (Recommended)</option>
                    <option value="python_requests">Python 3.11 Requests Microservice (Port 8000)</option>
                    <option value="playwright_headless">Playwright Chromium Headless Parser</option>
                  </select>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
                    Selects the execution runtime for crawling GeM BidPlus endpoints.
                  </span>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    GeM BidPlus Target Endpoint URL
                  </label>
                  <input
                    type="text"
                    className="input-control"
                    value={settings.scraper?.gemEndpointUrl || ''}
                    onChange={(e) => updateSectionField('scraper', 'gemEndpointUrl', e.target.value)}
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
                    Default: https://bidplus.gem.gov.in/all-bids-data
                  </span>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Maximum Pages per Scan: <strong style={{ color: 'var(--primary-cyan)' }}>{settings.scraper?.maxPagesPerScan || 25} pages</strong> (approx {(settings.scraper?.maxPagesPerScan || 25) * 10} bids)
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="100"
                    step="5"
                    value={settings.scraper?.maxPagesPerScan || 25}
                    onChange={(e) => updateSectionField('scraper', 'maxPagesPerScan', Number(e.target.value))}
                    style={{ width: '100%', accentColor: 'var(--primary-cyan)', cursor: 'pointer' }}
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Rate-Limiting Request Delay (ms)
                  </label>
                  <input
                    type="number"
                    min="100"
                    max="3000"
                    step="50"
                    className="input-control"
                    value={settings.scraper?.rateLimitDelayMs || 400}
                    onChange={(e) => updateSectionField('scraper', 'rateLimitDelayMs', Number(e.target.value))}
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
                    Delay between consecutive page fetches to avoid GeM firewall 429 / 403 blocks.
                  </span>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Auto-Scan Interval Frequency
                  </label>
                  <select
                    className="select-control"
                    style={{ width: '100%' }}
                    value={settings.scraper?.autoScanIntervalMinutes ?? 30}
                    onChange={(e) => updateSectionField('scraper', 'autoScanIntervalMinutes', Number(e.target.value))}
                  >
                    <option value={15}>Every 15 Minutes</option>
                    <option value={30}>Every 30 Minutes (Recommended)</option>
                    <option value={60}>Every 1 Hour</option>
                    <option value={360}>Every 6 Hours</option>
                    <option value={0}>Disabled (Manual Admin Scan Only)</option>
                  </select>
                </div>
              </div>

              {/* Toggles */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px', marginTop: '10px' }}>
                <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontWeight: 600, color: '#fff', fontSize: '0.88rem' }}>Auto-Filter Services Only</div>
                    <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Excludes product/goods bids (b_type=0)</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => updateSectionField('scraper', 'autoFilterServicesOnly', !settings.scraper?.autoFilterServicesOnly)}
                    style={{
                      width: '44px',
                      height: '24px',
                      borderRadius: '12px',
                      background: settings.scraper?.autoFilterServicesOnly ? 'var(--primary-cyan)' : 'rgba(255,255,255,0.15)',
                      border: 'none',
                      cursor: 'pointer',
                      position: 'relative',
                      transition: 'background 0.2s',
                      padding: '2px',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: '#fff', transform: settings.scraper?.autoFilterServicesOnly ? 'translateX(20px)' : 'translateX(0px)', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} />
                  </button>
                </div>

                <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <div>
                    <div style={{ fontWeight: 600, color: '#fff', fontSize: '0.88rem' }}>Rotate Request User-Agents</div>
                    <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Randomizes client fingerprints per batch</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => updateSectionField('scraper', 'rotateUserAgents', !settings.scraper?.rotateUserAgents)}
                    style={{
                      width: '44px',
                      height: '24px',
                      borderRadius: '12px',
                      background: settings.scraper?.rotateUserAgents ? 'var(--primary-cyan)' : 'rgba(255,255,255,0.15)',
                      border: 'none',
                      cursor: 'pointer',
                      position: 'relative',
                      transition: 'background 0.2s',
                      padding: '2px',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: '#fff', transform: settings.scraper?.rotateUserAgents ? 'translateX(20px)' : 'translateX(0px)', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} />
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: PAYMENT & GATEWAY */}
          {settingsSubTab === 'payment' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <CreditCard style={{ width: '22px', color: '#f59e0b' }} />
                  Direct UPI QR & Payment Configuration
                </h2>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Manage UPI payment QR code, admin UPI VPA address, payee name, and instant license key activation rules.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Primary Admin UPI ID (Displayed on QR)
                  </label>
                  <input
                    type="text"
                    className="input-control"
                    value={settings.payment?.adminUpiId || ''}
                    onChange={(e) => updateSectionField('payment', 'adminUpiId', e.target.value)}
                    placeholder="e.g. 6353731568-2@ybl"
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Admin UPI Payee Name
                  </label>
                  <input
                    type="text"
                    className="input-control"
                    value={settings.payment?.adminUpiPayeeName || ''}
                    onChange={(e) => updateSectionField('payment', 'adminUpiPayeeName', e.target.value)}
                    placeholder="e.g. GeMIntel Technologies"
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Payment Currency
                  </label>
                  <input
                    type="text"
                    className="input-control"
                    value={settings.payment?.currency || 'INR'}
                    onChange={(e) => updateSectionField('payment', 'currency', e.target.value)}
                    placeholder="INR"
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    GST Tax Percentage (%)
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="28"
                    className="input-control"
                    value={settings.payment?.gstPercentage ?? 18}
                    onChange={(e) => updateSectionField('payment', 'gstPercentage', Number(e.target.value))}
                  />
                </div>
              </div>

              <div style={{ background: 'rgba(255,255,255,0.02)', padding: '16px', borderRadius: '12px', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '10px' }}>
                <div>
                  <div style={{ fontWeight: 600, color: '#fff', fontSize: '0.88rem' }}>Auto-Activate Key on UPI UTR Submission</div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Automatically issues cryptographic license key when user submits bank UTR reference number</div>
                </div>
                <button
                  type="button"
                  onClick={() => updateSectionField('payment', 'autoVerifyUtr', !settings.payment?.autoVerifyUtr)}
                  style={{
                    width: '44px',
                    height: '24px',
                    borderRadius: '12px',
                    background: settings.payment?.autoVerifyUtr ? 'var(--primary-cyan)' : 'rgba(255,255,255,0.15)',
                    border: 'none',
                    cursor: 'pointer',
                    position: 'relative',
                    transition: 'background 0.2s',
                    padding: '2px',
                    display: 'flex',
                    alignItems: 'center'
                  }}
                >
                  <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: '#fff', transform: settings.payment?.autoVerifyUtr ? 'translateX(20px)' : 'translateX(0px)', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} />
                </button>
              </div>
            </div>
          )}

          {/* TAB 3: SECURITY & ACCESS */}
          {settingsSubTab === 'security' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Lock style={{ width: '22px', color: '#10b981' }} />
                  Security, Licensing & User Access Policies
                </h2>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Manage system maintenance mode, registration paywalls, free trial duration, and token lifecycle.
                </p>
              </div>

              {/* Maintenance Mode Alert Box */}
              <div style={{
                background: settings.security?.maintenanceMode ? 'rgba(244, 63, 94, 0.15)' : 'rgba(255,255,255,0.02)',
                border: `1px solid ${settings.security?.maintenanceMode ? '#f43f5e' : 'var(--border-color)'}`,
                borderRadius: '12px',
                padding: '16px'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <AlertTriangle style={{ width: '20px', color: settings.security?.maintenanceMode ? '#f43f5e' : 'var(--text-muted)' }} />
                    <div>
                      <div style={{ fontWeight: 700, color: settings.security?.maintenanceMode ? '#f43f5e' : '#fff', fontSize: '0.92rem' }}>
                        System Maintenance Mode
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        When enabled, non-admin users will see a maintenance screen.
                      </div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => updateSectionField('security', 'maintenanceMode', !settings.security?.maintenanceMode)}
                    style={{
                      width: '48px',
                      height: '26px',
                      borderRadius: '13px',
                      background: settings.security?.maintenanceMode ? '#f43f5e' : 'rgba(255,255,255,0.15)',
                      border: 'none',
                      cursor: 'pointer',
                      position: 'relative',
                      transition: 'background 0.2s',
                      padding: '2px',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <div style={{ width: '22px', height: '22px', borderRadius: '50%', background: '#fff', transform: settings.security?.maintenanceMode ? 'translateX(22px)' : 'translateX(0px)', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} />
                  </button>
                </div>

                {settings.security?.maintenanceMode && (
                  <div>
                    <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>
                      Maintenance Banner Message:
                    </label>
                    <input
                      type="text"
                      className="input-control"
                      value={settings.security?.maintenanceMessage || ''}
                      onChange={(e) => updateSectionField('security', 'maintenanceMessage', e.target.value)}
                    />
                  </div>
                )}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Free Trial Period (Days)
                  </label>
                  <select
                    className="select-control"
                    style={{ width: '100%' }}
                    value={settings.security?.freeTrialDays ?? 7}
                    onChange={(e) => updateSectionField('security', 'freeTrialDays', Number(e.target.value))}
                  >
                    <option value={0}>0 Days (Instant Paywall - Key Required)</option>
                    <option value={3}>3 Days Trial</option>
                    <option value={7}>7 Days Free Trial (Recommended)</option>
                    <option value={14}>14 Days Free Trial</option>
                    <option value={30}>30 Days Free Trial</option>
                  </select>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Cryptographic License Key Prefix
                  </label>
                  <input
                    type="text"
                    className="input-control"
                    value={settings.security?.licenseKeyPrefix || 'GEMI-'}
                    onChange={(e) => updateSectionField('security', 'licenseKeyPrefix', e.target.value.toUpperCase())}
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px', display: 'block' }}>
                    Format: {settings.security?.licenseKeyPrefix || 'GEMI-'}XXXX-XXXX-XXXX
                  </span>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    JWT Session Lifetime (Days)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="90"
                    className="input-control"
                    value={settings.security?.jwtExpiryDays || 7}
                    onChange={(e) => updateSectionField('security', 'jwtExpiryDays', Number(e.target.value))}
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Max Concurrent Logins Per User
                  </label>
                  <select
                    className="select-control"
                    style={{ width: '100%' }}
                    value={settings.security?.maxConcurrentSessions || 2}
                    onChange={(e) => updateSectionField('security', 'maxConcurrentSessions', Number(e.target.value))}
                  >
                    <option value={1}>1 Active Device Only</option>
                    <option value={2}>2 Devices (Desktop + Mobile)</option>
                    <option value={5}>5 Devices (Team Sharing)</option>
                    <option value={999}>Unlimited</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: ALERTS & WEBHOOKS */}
          {settingsSubTab === 'alerts' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Bell style={{ width: '22px', color: '#38bdf8' }} />
                  Automated Alerts & Webhook Integrations
                </h2>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Set up high-value tender thresholds, notification webhooks for Telegram/WhatsApp bots, and daily digest emails.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    High-Value Tender Alert Threshold (₹ INR)
                  </label>
                  <input
                    type="number"
                    step="100000"
                    className="input-control"
                    value={settings.alerts?.highValueTenderThreshold || 5000000}
                    onChange={(e) => updateSectionField('alerts', 'highValueTenderThreshold', Number(e.target.value))}
                  />
                  <span style={{ fontSize: '0.72rem', color: 'var(--accent-green)', marginTop: '4px', display: 'block', fontWeight: 600 }}>
                    ₹ {(settings.alerts?.highValueTenderThreshold || 5000000).toLocaleString('en-IN')} INR
                  </span>
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: 'var(--text-muted)', fontWeight: 600, display: 'block', marginBottom: '6px' }}>
                    Admin Notification Email
                  </label>
                  <input
                    type="email"
                    className="input-control"
                    value={settings.alerts?.alertEmail || ''}
                    onChange={(e) => updateSectionField('alerts', 'alertEmail', e.target.value)}
                  />
                </div>
              </div>

              {/* Webhook Configuration */}
              <div style={{ background: 'rgba(255,255,255,0.02)', padding: '20px', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
                  <div>
                    <div style={{ fontWeight: 700, color: '#fff', fontSize: '0.92rem' }}>Notification Webhook Dispatcher (Telegram / Slack / WhatsApp / Custom API)</div>
                    <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Sends real-time JSON payload whenever high-value tenders are scanned</div>
                  </div>
                  <button
                    type="button"
                    onClick={() => updateSectionField('alerts', 'enableWebhookAlerts', !settings.alerts?.enableWebhookAlerts)}
                    style={{
                      width: '44px',
                      height: '24px',
                      borderRadius: '12px',
                      background: settings.alerts?.enableWebhookAlerts ? 'var(--primary-cyan)' : 'rgba(255,255,255,0.15)',
                      border: 'none',
                      cursor: 'pointer',
                      position: 'relative',
                      transition: 'background 0.2s',
                      padding: '2px',
                      display: 'flex',
                      alignItems: 'center'
                    }}
                  >
                    <div style={{ width: '20px', height: '20px', borderRadius: '50%', background: '#fff', transform: settings.alerts?.enableWebhookAlerts ? 'translateX(20px)' : 'translateX(0px)', transition: 'transform 0.2s', boxShadow: '0 2px 4px rgba(0,0,0,0.3)' }} />
                  </button>
                </div>

                <div style={{ display: 'flex', gap: '10px' }}>
                  <input
                    type="url"
                    placeholder="https://api.telegram.org/bot<TOKEN>/sendMessage or https://hooks.slack.com/services/..."
                    className="input-control"
                    value={settings.alerts?.webhookUrl || ''}
                    onChange={(e) => updateSectionField('alerts', 'webhookUrl', e.target.value)}
                  />
                  <button
                    type="button"
                    onClick={handleTestWebhook}
                    disabled={testingWebhook || !settings.alerts?.webhookUrl}
                    className="btn-secondary"
                    style={{ flexShrink: 0, padding: '8px 16px', fontSize: '0.84rem', color: 'var(--primary-cyan)' }}
                  >
                    <Send style={{ width: '15px', height: '15px' }} />
                    {testingWebhook ? 'Testing...' : 'Test Webhook'}
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* TAB 5: SYSTEM OPERATIONS & BACKUPS */}
          {settingsSubTab === 'maintenance' && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '12px' }}>
                <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Activity style={{ width: '22px', color: '#8b5cf6' }} />
                  System Diagnostics, Cache Management & Database Backups
                </h2>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                  Trigger immediate background crawler cycles, purge corrupt duplicate cache, and export full JSON database backups.
                </p>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
                {/* Action Card 1 */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <Zap style={{ width: '20px', color: '#f59e0b' }} />
                    <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#fff' }}>Force Live GeM Scan</h3>
                  </div>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '16px', minHeight: '36px' }}>
                    Trigger immediate background scraping pass of today's published tenders across GeM portal.
                  </p>
                  <button
                    type="button"
                    onClick={handleTriggerLiveScan}
                    disabled={triggeringScan}
                    className="btn-cyan"
                    style={{ width: '100%', justifyContent: 'center', fontSize: '0.84rem' }}
                  >
                    <RefreshCw style={{ width: '15px', height: '15px', animation: triggeringScan ? 'spin 1s linear infinite' : 'none' }} />
                    {triggeringScan ? 'Triggering...' : 'Run Live Scan Now'}
                  </button>
                </div>

                {/* Action Card 2 */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <RotateCcw style={{ width: '20px', color: '#06b6d4' }} />
                    <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#fff' }}>Flush Duplicate Cache</h3>
                  </div>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '16px', minHeight: '36px' }}>
                    Clean dataset by removing redundant bid numbers and flushing in-memory crawl maps.
                  </p>
                  <button
                    type="button"
                    onClick={handleClearCache}
                    disabled={clearingCache}
                    className="btn-secondary"
                    style={{ width: '100%', justifyContent: 'center', fontSize: '0.84rem', color: 'var(--primary-cyan)' }}
                  >
                    <Trash2 style={{ width: '15px', height: '15px' }} />
                    {clearingCache ? 'Cleaning...' : 'Flush Cache & Duplicates'}
                  </button>
                </div>

                {/* Action Card 3 */}
                <div className="glass-card" style={{ padding: '20px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <Download style={{ width: '20px', color: '#10b981' }} />
                    <h3 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#fff' }}>Export Database Backup</h3>
                  </div>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '16px', minHeight: '36px' }}>
                    Download complete snapshot of users, licenses, subscriptions, payments, and scanned tenders in JSON.
                  </p>
                  <button
                    type="button"
                    onClick={handleDownloadBackup}
                    className="btn-secondary"
                    style={{ width: '100%', justifyContent: 'center', fontSize: '0.84rem', color: 'var(--accent-green)' }}
                  >
                    <Download style={{ width: '15px', height: '15px' }} />
                    Download JSON Backup
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Bottom Action Footer */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--border-color)', paddingTop: '20px', marginTop: '24px' }}>
            <button
              type="button"
              onClick={handleResetDefaults}
              className="btn-secondary"
              style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}
            >
              Reset to Factory Defaults
            </button>

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                onClick={loadSettings}
                className="btn-secondary"
                style={{ fontSize: '0.84rem' }}
              >
                Cancel / Reload
              </button>
              <button
                type="submit"
                disabled={saving}
                className="btn-primary"
                style={{ padding: '10px 24px', fontSize: '0.9rem' }}
              >
                <Save style={{ width: '16px', height: '16px' }} />
                {saving ? 'Saving...' : 'Save System Settings'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}

// -------------------------------------------------------------
// SECTION: ADMIN TENDER DATA MANAGER
// -------------------------------------------------------------
function AdminTenderDataManager({ token, showToast }) {
  const [tenders, setTenders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [totalCount, setTotalCount] = useState(0);
  const [page, setPage] = useState(1);
  const [selectedRawDoc, setSelectedRawDoc] = useState(null);

  const loadTenders = async () => {
    try {
      setLoading(true);
      const res = await fetch(`/api/admin/tenders?search=${encodeURIComponent(search)}&page=${page}&limit=25`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      setTenders(data.tenders || []);
      setTotalCount(data.total || 0);
    } catch (err) {
      showToast('Failed to load tenders database', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTenders();
  }, [search, page]);

  const handleDeleteTender = async (id, bidNum) => {
    if (!window.confirm(`Delete tender ${bidNum || id} from database?`)) return;
    try {
      const res = await fetch(`/api/admin/tenders/${encodeURIComponent(id || bidNum)}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error);
      showToast(`Tender ${bidNum} deleted from database`, 'info');
      loadTenders();
    } catch (err) {
      showToast(err.message, 'error');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ position: 'relative', width: '360px' }}>
          <Search style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search bid number, department, service..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            className="input-control"
            style={{ paddingLeft: '36px', height: '38px', fontSize: '0.85rem' }}
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span className="badge badge-published" style={{ fontSize: '0.84rem' }}>
            {totalCount} Total Stored Tenders
          </span>
          <button onClick={loadTenders} className="btn-secondary" style={{ padding: '8px 14px', fontSize: '0.82rem' }}>
            <RefreshCw style={{ width: '14px', height: '14px' }} /> Refresh Data
          </button>
        </div>
      </div>

      <div className="glass-panel" style={{ borderRadius: '16px', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.86rem' }}>
          <thead>
            <tr style={{ background: 'rgba(15,23,42,0.9)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
              <th style={{ padding: '12px 16px' }}>Bid Number</th>
              <th style={{ padding: '12px 16px' }}>Title & Description</th>
              <th style={{ padding: '12px 16px' }}>Department</th>
              <th style={{ padding: '12px 16px' }}>Category / Service</th>
              <th style={{ padding: '12px 16px' }}>Estimated Value</th>
              <th style={{ padding: '12px 16px' }}>End Date</th>
              <th style={{ padding: '12px 16px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="7" style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading tender dataset...</td>
              </tr>
            ) : tenders.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>No tenders match current search.</td>
              </tr>
            ) : (
              tenders.map((t, idx) => (
                <tr key={t.id || t.bid_number || idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '12px 16px', fontFamily: 'monospace', fontWeight: 700, color: 'var(--primary-cyan)' }}>
                    {t.bid_number || t.bidNo || '—'}
                  </td>
                  <td style={{ padding: '12px 16px', color: '#fff', maxWidth: '280px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {t.title || 'Untitled Tender'}
                  </td>
                  <td style={{ padding: '12px 16px', color: 'var(--text-muted)', maxWidth: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    {t.department || '—'}
                  </td>
                  <td style={{ padding: '12px 16px' }}>
                    <span className="badge badge-active" style={{ fontSize: '0.72rem' }}>
                      {t.service_type || t.category || 'Service'}
                    </span>
                  </td>
                  <td style={{ padding: '12px 16px', color: 'var(--accent-green)', fontWeight: 700 }}>
                    {t.estimated_value_original || (t.estimated_value ? `₹ ${Number(t.estimated_value).toLocaleString('en-IN')}` : '—')}
                  </td>
                  <td style={{ padding: '12px 16px', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                    {t.deadlineDate || t.deadline || t.endDate || '—'}
                  </td>
                  <td style={{ padding: '12px 16px', textAlign: 'right' }}>
                    <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                      <button
                        onClick={() => setSelectedRawDoc(t)}
                        className="btn-secondary"
                        style={{ padding: '4px 8px', fontSize: '0.74rem' }}
                        title="View Raw JSON"
                      >
                        <FileCode style={{ width: '14px', height: '14px' }} />
                        JSON
                      </button>
                      <button
                        onClick={() => handleDeleteTender(t.id || t.bid_number, t.bid_number)}
                        style={{ background: 'none', border: 'none', color: '#f43f5e', cursor: 'pointer', padding: '4px' }}
                        title="Delete Tender"
                      >
                        <Trash2 style={{ width: '16px', height: '16px' }} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 4px' }}>
        <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          Showing page {page} of {Math.max(1, Math.ceil(totalCount / 25))}
        </span>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button
            disabled={page <= 1}
            onClick={() => setPage(p => p - 1)}
            className="btn-secondary"
            style={{ padding: '6px 12px', fontSize: '0.8rem', opacity: page <= 1 ? 0.5 : 1 }}
          >
            Previous
          </button>
          <button
            disabled={page * 25 >= totalCount}
            onClick={() => setPage(p => p + 1)}
            className="btn-secondary"
            style={{ padding: '6px 12px', fontSize: '0.8rem', opacity: page * 25 >= totalCount ? 0.5 : 1 }}
          >
            Next
          </button>
        </div>
      </div>

      {/* RAW JSON INSPECTOR MODAL */}
      {selectedRawDoc && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(7,10,18,0.85)', backdropFilter: 'blur(10px)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '750px', maxHeight: '85vh', display: 'flex', flexDirection: 'column', borderRadius: '16px', padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', borderBottom: '1px solid var(--border-color)', paddingBottom: '10px' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FileCode style={{ width: '18px', color: 'var(--primary-cyan)' }} />
                Raw Tender Payload: {selectedRawDoc.bid_number || selectedRawDoc.id}
              </h3>
              <button onClick={() => setSelectedRawDoc(null)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1.2rem' }}>
                ✕
              </button>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', background: '#090d16', padding: '16px', borderRadius: '8px', border: '1px solid var(--border-color)', fontFamily: 'monospace', fontSize: '0.8rem', color: '#a5f3fc' }}>
              <pre style={{ margin: 0, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                {JSON.stringify(selectedRawDoc, null, 2)}
              </pre>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '16px', gap: '10px' }}>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(JSON.stringify(selectedRawDoc, null, 2));
                  showToast('JSON copied to clipboard', 'info');
                }}
                className="btn-cyan"
                style={{ fontSize: '0.84rem' }}
              >
                Copy JSON
              </button>
              <button onClick={() => setSelectedRawDoc(null)} className="btn-secondary" style={{ fontSize: '0.84rem' }}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
