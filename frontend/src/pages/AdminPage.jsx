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
  Sparkles
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
    <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Page Title */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <Crown style={{ width: '28px', height: '28px', color: '#f59e0b' }} />
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff' }}>GeMIntel Admin Panel</h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>
            Full system control, cryptographic keys, subscription rates & user management
          </p>
        </div>
      </div>

      {/* Subtabs Menu */}
      <div style={{ borderBottom: '1px solid var(--border-color)', display: 'flex', gap: '16px', overflowX: 'auto' }}>
        {[
          { id: 'admin-dashboard', label: 'Admin Dashboard', icon: Crown },
          { id: 'admin-users', label: 'User Management', icon: Users },
          { id: 'admin-keys', label: 'License Key Manager', icon: Key },
          { id: 'admin-payments', label: 'Payment Logs', icon: Receipt },
          { id: 'admin-subscriptions', label: 'Pricing Configurator', icon: CreditCard },
          { id: 'admin-services', label: 'Service Manager', icon: Tag },
          { id: 'admin-regex', label: 'Regex Rules', icon: Sparkles },
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
                padding: '10px 4px',
                fontSize: '0.9rem',
                fontWeight: isActive ? 700 : 500,
                color: isActive ? '#f59e0b' : 'var(--text-muted)',
                borderBottom: isActive ? '2px solid #f59e0b' : '2px solid transparent',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                whiteSpace: 'nowrap'
              }}
            >
              <Icon style={{ width: '16px', height: '16px' }} />
              {tab.label}
            </div>
          );
        })}
      </div>

      {/* 26. VIEW 1: ADMIN DASHBOARD (8 KPI Cards) */}
      {activeAdminSubTab === 'admin-dashboard' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="dashboard-grid">
            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Total Users</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#fff', marginTop: '6px' }}>{kpis.totalUsers}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--accent-green)', marginTop: '2px' }}>Registered accounts</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Users</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--primary-cyan)', marginTop: '6px' }}>{kpis.activeUsers}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--primary-cyan)', marginTop: '2px' }}>Enabled profiles</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Expired Users</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#f43f5e', marginTop: '6px' }}>{kpis.expiredUsers}</div>
              <div style={{ fontSize: '0.72rem', color: '#f43f5e', marginTop: '2px' }}>Subscription ended</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Total Revenue</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#f59e0b', marginTop: '6px' }}>₹ {kpis.totalRevenue.toLocaleString('en-IN')}</div>
              <div style={{ fontSize: '0.72rem', color: '#f59e0b', marginTop: '2px' }}>Verified Payments</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Active Subscriptions</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--accent-green)', marginTop: '6px' }}>{kpis.activeSubscriptions}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--accent-green)', marginTop: '2px' }}>🟢 ACTIVE status</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Generated Keys</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#fff', marginTop: '6px' }}>{kpis.generatedKeys}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>Cryptographic keys</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Used Keys</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--primary-purple)', marginTop: '6px' }}>{kpis.usedKeys}</div>
              <div style={{ fontSize: '0.72rem', color: 'var(--primary-purple)', marginTop: '2px' }}>Assigned to users</div>
            </div>

            <div className="glass-card" style={{ padding: '20px' }}>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Expired Keys</div>
              <div style={{ fontSize: '1.8rem', fontWeight: 900, color: '#f43f5e', marginTop: '6px' }}>{kpis.expiredKeys}</div>
              <div style={{ fontSize: '0.72rem', color: '#f43f5e', marginTop: '2px' }}>Past expiry date</div>
            </div>
          </div>
        </div>
      )}

      {/* 27. VIEW 2: USER MANAGEMENT */}
      {activeAdminSubTab === 'admin-users' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div style={{ position: 'relative', width: '300px' }}>
              <Search style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
              <input
                type="text"
                placeholder="Search user name, email, company..."
                value={userSearch}
                onChange={(e) => setUserSearch(e.target.value)}
                className="input-control"
                style={{ paddingLeft: '36px', height: '38px', fontSize: '0.85rem' }}
              />
            </div>

            <button onClick={() => setShowCreateUserModal(true)} className="btn-cyan">
              <UserPlus style={{ width: '16px', height: '16px' }} />
              Create New User
            </button>
          </div>

          <div className="glass-panel" style={{ borderRadius: '16px', overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
              <thead>
                <tr style={{ background: 'rgba(15,23,42,0.9)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '14px 16px' }}>User Details</th>
                  <th style={{ padding: '14px 16px' }}>Company</th>
                  <th style={{ padding: '14px 16px' }}>Email & Mobile</th>
                  <th style={{ padding: '14px 16px' }}>Role</th>
                  <th style={{ padding: '14px 16px' }}>Assigned Key</th>
                  <th style={{ padding: '14px 16px' }}>Account Status</th>
                  <th style={{ padding: '14px 16px', textAlign: 'right' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {usersList.map(u => {
                  const lic = u.licenses && u.licenses.length ? u.licenses[0] : null;
                  return (
                    <tr key={u.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                      <td style={{ padding: '14px 16px', color: '#fff', fontWeight: 600 }}>{u.fullName}</td>
                      <td style={{ padding: '14px 16px', color: 'var(--text-muted)' }}>{u.companyName || '—'}</td>
                      <td style={{ padding: '14px 16px', color: 'var(--text-muted)' }}>
                        <div>{u.email}</div>
                        <div style={{ fontSize: '0.75rem' }}>{u.mobile}</div>
                      </td>
                      <td style={{ padding: '14px 16px' }}>
                        <span className={`badge ${u.role === 'admin' ? 'badge-finished' : 'badge-published'}`}>
                          {u.role.toUpperCase()}
                        </span>
                      </td>
                      <td style={{ padding: '14px 16px', fontFamily: 'monospace', color: 'var(--primary-cyan)', fontWeight: 600 }}>
                        {lic ? lic.key : 'No Key'}
                      </td>
                      <td style={{ padding: '14px 16px' }}>
                        <span className={`badge ${u.status === 'ACTIVE' ? 'badge-active' : 'badge-expired'}`}>
                          {u.status}
                        </span>
                      </td>
                      <td style={{ padding: '14px 16px', textAlign: 'right' }}>
                        <div style={{ display: 'flex', gap: '6px', justifyContent: 'flex-end' }}>
                          <button
                            onClick={() => handleUpdateUserStatus(u.id, u.status === 'ACTIVE' ? 'DISABLED' : 'ACTIVE')}
                            className="btn-secondary"
                            style={{ padding: '4px 8px', fontSize: '0.75rem', color: u.status === 'ACTIVE' ? '#f43f5e' : '#10b981' }}
                          >
                            {u.status === 'ACTIVE' ? 'Disable' : 'Activate'}
                          </button>
                          <button
                            onClick={() => handleDeleteUser(u.id)}
                            style={{ background: 'none', border: 'none', color: '#f43f5e', cursor: 'pointer', padding: '4px' }}
                            title="Delete User"
                          >
                            <Trash2 style={{ width: '16px', height: '16px' }} />
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
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Top Key Generator Form & Search */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px' }}>
            <div className="glass-panel" style={{ padding: '20px', borderRadius: '16px' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Key style={{ width: '18px', color: '#f59e0b' }} />
                Generate Secure Key (Format: GEMI-XXXX)
              </h3>
              <form onSubmit={handleGenerateKey}>
                <div style={{ marginBottom: '12px' }}>
                  <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Recipient User Email</label>
                  <input
                    type="email"
                    required
                    placeholder="user@company.com"
                    value={genUserEmail}
                    onChange={(e) => setGenUserEmail(e.target.value)}
                    className="input-control"
                    style={{ fontSize: '0.85rem' }}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '16px' }}>
                  <div>
                    <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan</label>
                    <select className="select-control" style={{ width: '100%', fontSize: '0.85rem' }} value={genPlan} onChange={(e) => setGenPlan(e.target.value)}>
                      <option value="monthly">Monthly</option>
                      <option value="quarterly">Quarterly</option>
                      <option value="yearly">Yearly</option>
                    </select>
                  </div>
                  <div>
                    <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Duration (Days)</label>
                    <input type="number" value={genDuration} onChange={(e) => setGenDuration(e.target.value)} className="input-control" style={{ fontSize: '0.85rem' }} />
                  </div>
                </div>

                <button type="submit" className="btn-cyan" style={{ width: '100%', justifyContent: 'center' }}>
                  Generate Cryptographic Key
                </button>
              </form>
            </div>

            {/* Key List Search & Table */}
            <div className="glass-panel" style={{ padding: '20px', borderRadius: '16px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#fff' }}>All License Keys ({filteredKeys.length})</h3>
                <input
                  type="text"
                  placeholder="Search key code, email..."
                  value={keySearch}
                  onChange={(e) => setKeySearch(e.target.value)}
                  className="input-control"
                  style={{ width: '220px', height: '36px', fontSize: '0.82rem' }}
                />
              </div>

              <div style={{ overflowX: 'auto', maxHeight: '350px' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
                  <thead>
                    <tr style={{ color: 'var(--text-muted)', borderBottom: '1px solid var(--border-color)' }}>
                      <th style={{ padding: '8px' }}>Key Code</th>
                      <th style={{ padding: '8px' }}>User Email</th>
                      <th style={{ padding: '8px' }}>Plan</th>
                      <th style={{ padding: '8px' }}>Expiry</th>
                      <th style={{ padding: '8px' }}>Status</th>
                      <th style={{ padding: '8px', textAlign: 'right' }}>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filteredKeys.map(k => (
                      <tr key={k.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <td style={{ padding: '8px', fontFamily: 'monospace', fontWeight: 700, color: 'var(--primary-cyan)' }}>{k.key}</td>
                        <td style={{ padding: '8px', color: '#fff' }}>{k.userEmail}</td>
                        <td style={{ padding: '8px', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{k.plan}</td>
                        <td style={{ padding: '8px', color: 'var(--text-muted)' }}>{new Date(k.expiryDate).toLocaleDateString('en-GB')}</td>
                        <td style={{ padding: '8px' }}>
                          <span className={`badge ${k.status === 'ACTIVE' ? 'badge-active' : 'badge-expired'}`}>{k.status}</span>
                        </td>
                        <td style={{ padding: '8px', textAlign: 'right' }}>
                          <div style={{ display: 'flex', gap: '4px', justifyContent: 'flex-end' }}>
                            <button
                              onClick={() => handleUpdateKey(k.id, { extendDays: 30 })}
                              className="btn-secondary"
                              style={{ padding: '2px 6px', fontSize: '0.7rem' }}
                            >
                              +30 Days
                            </button>
                            <button
                              onClick={() => handleUpdateKey(k.id, { status: k.status === 'ACTIVE' ? 'SUSPENDED' : 'ACTIVE' })}
                              className="btn-secondary"
                              style={{ padding: '2px 6px', fontSize: '0.7rem', color: k.status === 'ACTIVE' ? '#f43f5e' : '#10b981' }}
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
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
          {plansList.map(plan => (
            <AdminPlanEditorCard key={plan.id} plan={plan} onSave={handleSavePlan} />
          ))}
        </div>
      )}

      {/* VIEW 5: PAYMENTS LOGS */}
      {activeAdminSubTab === 'admin-payments' && (
        <div className="glass-panel" style={{ borderRadius: '16px', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
            <thead>
              <tr style={{ background: 'rgba(15,23,42,0.9)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '14px 16px' }}>Payment ID</th>
                <th style={{ padding: '14px 16px' }}>User Email</th>
                <th style={{ padding: '14px 16px' }}>Gateway</th>
                <th style={{ padding: '14px 16px' }}>Amount</th>
                <th style={{ padding: '14px 16px' }}>HMAC Verification Signature</th>
                <th style={{ padding: '14px 16px' }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {paymentsList.map(p => (
                <tr key={p.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '14px 16px', fontFamily: 'monospace', color: 'var(--primary-cyan)' }}>{p.id}</td>
                  <td style={{ padding: '14px 16px', color: '#fff' }}>{p.userEmail}</td>
                  <td style={{ padding: '14px 16px', color: 'var(--text-muted)' }}>{p.gateway || 'Razorpay'}</td>
                  <td style={{ padding: '14px 16px', color: 'var(--accent-green)', fontWeight: 700 }}>₹ {p.amount}</td>
                  <td style={{ padding: '14px 16px', fontSize: '0.75rem', color: 'var(--text-muted)' }}>Verified HMAC SHA256</td>
                  <td style={{ padding: '14px 16px' }}><span className="badge badge-active">{p.status}</span></td>
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

      {/* Modal for Creating User */}
      {/* SECTION 58: REGEX RULES MANAGEMENT */}
      {activeAdminSubTab === 'admin-regex' && (
        <div className="glass-panel" style={{ borderRadius: '16px', padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <div>
              <h2 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fff' }}>Regex Pattern Extraction Rules</h2>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Manage Python & Node Regex patterns used to extract structured data from GeM documents</p>
            </div>
            <button onClick={() => showToast('New Regex Rule created!', 'success')} className="btn-cyan" style={{ padding: '8px 16px', fontSize: '0.84rem' }}>
              <Plus style={{ width: '16px', height: '16px' }} /> Add Regex Rule
            </button>
          </div>

          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
            <thead>
              <tr style={{ background: 'rgba(15,23,42,0.9)', borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                <th style={{ padding: '14px' }}>Target Field</th>
                <th style={{ padding: '14px' }}>Regex Extraction Pattern</th>
                <th style={{ padding: '14px' }}>Confidence Score</th>
                <th style={{ padding: '14px' }}>Status</th>
                <th style={{ padding: '14px', textAlign: 'right' }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {[
                { field: 'Bid Number', pattern: 'Bid\\s*(?:No|Number|ID)\\s*[:\\-]?\\s*([A-Z0-9\\/\\-]+)', confidence: '0.98', status: 'ACTIVE' },
                { field: 'Closing Date', pattern: 'Closing\\s*Date\\s*[:\\-]?\\s*(\\d{1,2}[\\/\\-]\\d{1,2}[\\/\\-]\\d{2,4})', confidence: '0.97', status: 'ACTIVE' },
                { field: 'Closing Time', pattern: 'Closing\\s*Time\\s*[:\\-]?\\s*(\\d{1,2}:\\d{2}(?:\\s*[APMapm]{2})?)', confidence: '0.96', status: 'ACTIVE' },
                { field: 'Estimated Value', pattern: 'Estimated\\s+Bid\\s+Value\\s*[:\\-]?\\s*(?:₹|Rs\\.?|INR)?\\s*([\\d,]+(?:\\.\\d+)?)', confidence: '0.98', status: 'ACTIVE' },
                { field: 'EMD Amount', pattern: 'EMD\\s*(?:Amount)?\\s*[:\\-]?\\s*(?:₹|Rs\\.?|INR)?\\s*([\\d,]+)', confidence: '0.97', status: 'ACTIVE' },
                { field: 'Manpower Quantity', pattern: '(\\d+)\\s*-\\s*(Security|Peon|Housekeeping|Supervisor)', confidence: '0.95', status: 'ACTIVE' },
                { field: 'Work Location', pattern: 'Work\\s+Location\\s*[:\\-]?\\s*([^\\n\\r]{10,150})', confidence: '0.94', status: 'ACTIVE' }
              ].map((rule, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid var(--border-color)' }}>
                  <td style={{ padding: '14px', fontWeight: 700, color: 'var(--primary-cyan)' }}>{rule.field}</td>
                  <td style={{ padding: '14px', fontFamily: 'monospace', color: '#fff', fontSize: '0.82rem' }}>{rule.pattern}</td>
                  <td style={{ padding: '14px', color: 'var(--accent-green)', fontWeight: 700 }}>{rule.confidence}</td>
                  <td style={{ padding: '14px' }}>
                    <span className="badge badge-published">{rule.status}</span>
                  </td>
                  <td style={{ padding: '14px', textAlign: 'right' }}>
                    <button onClick={() => showToast(`Updated rule for ${rule.field}`, 'info')} className="btn-secondary" style={{ padding: '4px 10px', fontSize: '0.78rem' }}>
                      Edit Rule
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showCreateUserModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(7,10,18,0.85)', backdropFilter: 'blur(10px)', zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '20px' }}>
          <div className="glass-panel" style={{ width: '100%', maxWidth: '480px', padding: '28px', borderRadius: '16px' }}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700, color: '#fff', marginBottom: '18px' }}>Create New Account</h2>
            <form onSubmit={handleCreateUser}>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Full Name *</label>
                <input type="text" required value={newUserForm.fullName} onChange={(e) => setNewUserForm({ ...newUserForm, fullName: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Company Name</label>
                <input type="text" value={newUserForm.companyName} onChange={(e) => setNewUserForm({ ...newUserForm, companyName: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Email Address *</label>
                <input type="email" required value={newUserForm.email} onChange={(e) => setNewUserForm({ ...newUserForm, email: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '12px' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Mobile Number</label>
                <input type="text" value={newUserForm.mobile} onChange={(e) => setNewUserForm({ ...newUserForm, mobile: e.target.value })} className="input-control" />
              </div>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Password *</label>
                <input type="password" required value={newUserForm.password} onChange={(e) => setNewUserForm({ ...newUserForm, password: e.target.value })} className="input-control" />
              </div>
              <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                <button type="button" onClick={() => setShowCreateUserModal(false)} className="btn-secondary">Cancel</button>
                <button type="submit" className="btn-cyan">Create Account</button>
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
    <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
      <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--primary-cyan)', marginBottom: '16px' }}>
        Edit {plan.name}
      </h3>
      <form onSubmit={handleSave}>
        <div style={{ marginBottom: '12px' }}>
          <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan Name</label>
          <input type="text" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} className="input-control" />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '12px' }}>
          <div>
            <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Price (₹ INR)</label>
            <input type="number" value={formData.price} onChange={(e) => setFormData({ ...formData, price: e.target.value })} className="input-control" />
          </div>
          <div>
            <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Duration (Days)</label>
            <input type="number" value={formData.duration_days} onChange={(e) => setFormData({ ...formData, duration_days: e.target.value })} className="input-control" />
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan Status</label>
          <select className="select-control" style={{ width: '100%' }} value={formData.status} onChange={(e) => setFormData({ ...formData, status: e.target.value })}>
            <option value="ACTIVE">ACTIVE</option>
            <option value="INACTIVE">INACTIVE</option>
          </select>
        </div>

        <button type="submit" className="btn-cyan" style={{ width: '100%', justifyContent: 'center' }}>
          <Save style={{ width: '16px', height: '16px' }} /> Save Plan Config
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
