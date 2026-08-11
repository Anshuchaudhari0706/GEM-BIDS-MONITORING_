import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Radar,
  Crown,
  Users,
  Key,
  Receipt,
  CreditCard,
  Tag,
  Database,
  Settings,
  ShieldCheck,
  Menu,
  X
} from 'lucide-react';

export default function Sidebar({ currentTab, setCurrentTab }) {
  const { user } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const mainItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'scanner', label: 'Scan Bids', icon: Radar, highlight: true }
  ];

  const adminItems = [
    { id: 'admin-dashboard', label: 'Admin Dashboard', icon: Crown },
    { id: 'admin-users', label: 'Users', icon: Users },
    { id: 'admin-keys', label: 'License Keys', icon: Key },
    { id: 'admin-payments', label: 'Payments', icon: Receipt },
    { id: 'admin-subscriptions', label: 'Subscriptions', icon: CreditCard },
    { id: 'admin-services', label: 'Services', icon: Tag },
    { id: 'admin-tenders', label: 'Tender Data', icon: Database },
    { id: 'admin-settings', label: 'System Settings', icon: Settings }
  ];

  const handleSelectTab = (tabId) => {
    setCurrentTab(tabId);
    setMobileOpen(false);
  };

  return (
    <>
      {/* Mobile Hamburger Toggle Bar (Section 37) */}
      <div
        style={{
          display: 'none',
          padding: '12px 16px',
          background: 'var(--bg-sidebar)',
          borderBottom: '1px solid var(--border-color)',
          alignItems: 'center',
          justifyContent: 'space-between',
          zIndex: 110
        }}
        className="mobile-header-toggle"
      >
        <button
          onClick={() => setMobileOpen(!mobileOpen)}
          style={{ background: 'none', border: 'none', color: '#fff', display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '1rem', fontWeight: 600 }}
        >
          {mobileOpen ? <X style={{ width: '22px', height: '22px' }} /> : <Menu style={{ width: '22px', height: '22px' }} />}
          <span>☰ Menu</span>
        </button>
      </div>

      {/* Sidebar Navigation Panel */}
      <aside
        style={{
          width: '260px',
          background: 'var(--bg-sidebar)',
          borderRight: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '20px 16px',
          flexShrink: 0
        }}
        className={`sidebar-panel ${mobileOpen ? 'mobile-show' : ''}`}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Main Section */}
          <div>
            <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px', padding: '0 12px 8px 12px' }}>
              Main
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {mainItems.map((item) => {
                const Icon = item.icon;
                const isActive = currentTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => handleSelectTab(item.id)}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      padding: '11px 14px',
                      borderRadius: '10px',
                      border: isActive
                        ? '1px solid rgba(59, 130, 246, 0.4)'
                        : item.highlight
                        ? '1px solid rgba(6, 182, 212, 0.3)'
                        : '1px solid transparent',
                      background: isActive
                        ? 'linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(139, 92, 246, 0.15))'
                        : item.highlight
                        ? 'rgba(6, 182, 212, 0.08)'
                        : 'transparent',
                      color: isActive ? '#fff' : 'var(--text-muted)',
                      fontWeight: isActive ? 600 : 500,
                      fontSize: '0.9rem',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <Icon style={{ width: '18px', height: '18px', color: isActive ? 'var(--primary-cyan)' : 'var(--text-muted)' }} />
                      <span>{item.label}</span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Administration Section */}
          {user?.role === 'admin' && (
            <div>
              <div style={{ fontSize: '0.72rem', fontWeight: 700, color: '#f59e0b', textTransform: 'uppercase', letterSpacing: '1px', padding: '0 12px 8px 12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Crown style={{ width: '12px', height: '12px' }} />
                Administration
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {adminItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = currentTab === item.id;
                  return (
                    <button
                      key={item.id}
                      onClick={() => handleSelectTab(item.id)}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        padding: '10px 14px',
                        borderRadius: '10px',
                        border: isActive ? '1px solid rgba(245, 158, 11, 0.4)' : '1px solid transparent',
                        background: isActive ? 'rgba(245, 158, 11, 0.15)' : 'transparent',
                        color: isActive ? '#fff' : 'var(--text-muted)',
                        fontWeight: isActive ? 600 : 500,
                        fontSize: '0.86rem',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Icon style={{ width: '17px', height: '17px', color: isActive ? '#f59e0b' : 'var(--text-muted)' }} />
                        <span>{item.label}</span>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>

        {/* Footer Banner */}
        <div
          className="glass-panel"
          style={{
            padding: '14px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%)',
            textAlign: 'center'
          }}
        >
          <ShieldCheck style={{ width: '26px', height: '26px', color: 'var(--primary-cyan)', margin: '0 auto 6px auto' }} />
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#fff' }}>GeMIntel SaaS Engine</div>
          <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>v2.4 Production REST</div>
        </div>
      </aside>
    </>
  );
}
