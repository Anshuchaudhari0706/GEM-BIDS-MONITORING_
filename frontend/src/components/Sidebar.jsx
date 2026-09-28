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
  X,
  Sparkles,
  ChevronRight
} from 'lucide-react';

export default function Sidebar({ currentTab, setCurrentTab }) {
  const { user } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  const mainItems = [
    { id: 'dashboard', label: 'Tender Intelligence', icon: LayoutDashboard },
    { id: 'billing', label: 'License & Subscription', icon: CreditCard }
  ];

  const adminItems = [
    { id: 'admin-dashboard', label: 'Admin Dashboard', icon: Crown },
    { id: 'admin-users', label: 'User Accounts', icon: Users },
    { id: 'admin-keys', label: 'License Keys', icon: Key },
    { id: 'admin-payments', label: 'Payment Logs', icon: Receipt },
    { id: 'admin-subscriptions', label: 'Pricing Plans', icon: CreditCard },
    { id: 'admin-services', label: 'Service Categories', icon: Tag },
    { id: 'admin-tenders', label: 'Tender Database', icon: Database },
    { id: 'admin-settings', label: 'System Settings', icon: Settings }
  ];

  const handleSelectTab = (tabId) => {
    setCurrentTab(tabId);
    setMobileOpen(false);
  };

  return (
    <>
      {/* Mobile Hamburger Toggle Bar */}
      <div
        style={{
          display: 'none',
          padding: '14px 20px',
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
          style={{ background: 'none', border: 'none', color: '#fff', display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer', fontSize: '1.05rem', fontWeight: 700 }}
        >
          {mobileOpen ? <X style={{ width: '24px', height: '24px' }} /> : <Menu style={{ width: '24px', height: '24px' }} />}
          <span>Navigation Menu</span>
        </button>
      </div>

      {/* Sidebar Navigation Panel */}
      <aside
        style={{
          width: '270px',
          background: 'var(--bg-sidebar)',
          borderRight: '1px solid var(--border-color)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '24px 18px',
          flexShrink: 0
        }}
        className={`sidebar-panel ${mobileOpen ? 'mobile-show' : ''}`}
      >
        <div style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
          {/* Main Navigation */}
          <div>
            <div style={{ fontSize: '0.76rem', fontWeight: 800, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1.2px', padding: '0 12px 10px 12px' }}>
              Workspace
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
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
                      padding: '12px 16px',
                      borderRadius: '12px',
                      border: isActive
                        ? '1px solid rgba(56, 189, 248, 0.4)'
                        : '1px solid transparent',
                      background: isActive
                        ? 'linear-gradient(135deg, rgba(37, 99, 235, 0.22), rgba(6, 182, 212, 0.15))'
                        : 'transparent',
                      color: isActive ? '#fff' : 'var(--text-muted)',
                      fontWeight: isActive ? 700 : 600,
                      fontSize: '0.95rem',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      boxShadow: isActive ? '0 4px 14px rgba(6, 182, 212, 0.15)' : 'none'
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                      <Icon style={{ width: '20px', height: '20px', color: isActive ? 'var(--primary-cyan-bright)' : 'var(--text-muted)' }} />
                      <span>{item.label}</span>
                    </div>
                    {isActive && <ChevronRight style={{ width: '16px', height: '16px', color: 'var(--primary-cyan-bright)' }} />}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Administration Navigation */}
          {user?.role === 'admin' && (
            <div>
              <div style={{ fontSize: '0.76rem', fontWeight: 800, color: '#f59e0b', textTransform: 'uppercase', letterSpacing: '1.2px', padding: '0 12px 10px 12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Crown style={{ width: '14px', height: '14px' }} />
                Admin Console
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
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
                        justifyContent: 'space-between',
                        padding: '11px 16px',
                        borderRadius: '12px',
                        border: isActive ? '1px solid rgba(245, 158, 11, 0.45)' : '1px solid transparent',
                        background: isActive ? 'rgba(245, 158, 11, 0.16)' : 'transparent',
                        color: isActive ? '#fff' : 'var(--text-muted)',
                        fontWeight: isActive ? 700 : 500,
                        fontSize: '0.92rem',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease',
                        boxShadow: isActive ? '0 4px 14px rgba(245, 158, 11, 0.15)' : 'none'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                        <Icon style={{ width: '18px', height: '18px', color: isActive ? '#f59e0b' : 'var(--text-muted)' }} />
                        <span>{item.label}</span>
                      </div>
                      {isActive && <ChevronRight style={{ width: '14px', height: '14px', color: '#f59e0b' }} />}
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
            padding: '16px',
            borderRadius: '14px',
            background: 'linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%)',
            textAlign: 'center',
            border: '1px solid var(--border-color)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '6px' }}>
            <ShieldCheck style={{ width: '22px', height: '22px', color: 'var(--primary-cyan-bright)' }} />
            <span style={{ fontSize: '0.92rem', fontWeight: 800, color: '#fff' }}>GeMIntel Enterprise</span>
          </div>
          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 500 }}>
            v2.5 Live Scanner Active
          </div>
        </div>
      </aside>
    </>
  );
}
