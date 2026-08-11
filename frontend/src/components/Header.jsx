import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  ShieldCheck,
  ShieldAlert,
  Search,
  User,
  LogOut,
  SlidersHorizontal,
  Sparkles,
  Key,
  Crown
} from 'lucide-react';

export default function Header({ currentTab, setCurrentTab, searchQuery, setSearchQuery }) {
  const { user, license, isLicenseActive, logout, setShowPaymentModal, setSelectedPlanForPayment } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  const calculateDaysLeft = () => {
    if (!license || !license.expiryDate) return 0;
    const diff = new Date(license.expiryDate) - new Date();
    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
  };

  const daysLeft = calculateDaysLeft();

  return (
    <header
      style={{
        height: '70px',
        background: 'var(--bg-header)',
        backdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 24px',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}
    >
      {/* Brand Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={() => setCurrentTab('dashboard')}>
        <div
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '10px',
            background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 15px rgba(59, 130, 246, 0.5)'
          }}
        >
          <Sparkles style={{ color: '#fff', width: '22px', height: '22px' }} />
        </div>
        <div>
          <span style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fff', letterSpacing: '-0.5px' }} className="brand-font">
            GeM<span style={{ color: 'var(--primary-cyan)' }}>Intel</span>
          </span>
          <span style={{ fontSize: '0.68rem', display: 'block', color: 'var(--text-muted)', marginTop: '-4px', fontWeight: 500 }}>
            Smart GeM Tender Intelligence
          </span>
        </div>
      </div>

      {/* Global Tender Search */}
      <div style={{ position: 'relative', width: '380px' }}>
        <Search
          style={{
            position: 'absolute',
            left: '14px',
            top: '50%',
            transform: 'translateY(-50%)',
            width: '18px',
            height: '18px',
            color: 'var(--text-muted)'
          }}
        />
        <input
          type="text"
          placeholder="Search GeM Bid ID, Department, State, Services..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="input-control"
          style={{ paddingLeft: '42px', height: '40px', fontSize: '0.88rem' }}
        />
      </div>

      {/* Right Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        {/* License Status Badge */}
        {isLicenseActive() ? (
          <div
            className="badge badge-active"
            style={{ padding: '6px 14px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
            onClick={() => setCurrentTab('billing')}
          >
            <ShieldCheck style={{ width: '16px', height: '16px' }} />
            <span>Active License: {license?.key}</span>
            <span style={{ opacity: 0.8, fontSize: '0.72rem', background: 'rgba(0,0,0,0.2)', padding: '2px 6px', borderRadius: '4px' }}>
              {daysLeft} Days Left
            </span>
          </div>
        ) : (
          <div
            className="badge badge-expired"
            style={{ padding: '6px 14px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px' }}
            onClick={() => {
              setSelectedPlanForPayment('monthly');
              setShowPaymentModal(true);
            }}
          >
            <ShieldAlert style={{ width: '16px', height: '16px' }} />
            <span>Subscription Expired</span>
            <span style={{ background: 'rgba(244,63,94,0.3)', padding: '2px 6px', borderRadius: '4px', textTransform: 'none' }}>
              Renew Now
            </span>
          </div>
        )}

        {/* User Profile Menu */}
        <div style={{ position: 'relative' }}>
          <div
            onClick={() => setShowDropdown(!showDropdown)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              padding: '6px 12px',
              borderRadius: '8px',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-color)',
              cursor: 'pointer'
            }}
          >
            <div
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                background: user?.role === 'admin' ? 'linear-gradient(135deg, #f59e0b, #ef4444)' : 'linear-gradient(135deg, #06b6d4, #3b82f6)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 'bold',
                color: '#fff',
                fontSize: '0.9rem'
              }}
            >
              {user?.fullName ? user.fullName.charAt(0).toUpperCase() : 'U'}
            </div>
            <div style={{ textAlign: 'left', lineHeight: '1.2' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fff' }}>{user?.fullName || 'User'}</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{user?.companyName || user?.email}</div>
            </div>
          </div>

          {/* Dropdown items */}
          {showDropdown && (
            <div
              style={{
                position: 'absolute',
                right: 0,
                top: '50px',
                width: '220px',
                background: '#0f172a',
                border: '1px solid var(--border-color)',
                borderRadius: '10px',
                boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
                padding: '8px',
                zIndex: 200
              }}
            >
              <div style={{ padding: '8px 12px', borderBottom: '1px solid var(--border-color)', marginBottom: '6px' }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Signed in as</div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fff', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user?.email}
                </div>
              </div>

              <div
                className="btn-secondary"
                style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '8px 12px', fontSize: '0.85rem' }}
                onClick={() => {
                  setCurrentTab('billing');
                  setShowDropdown(false);
                }}
              >
                <Key style={{ width: '16px', height: '16px', color: 'var(--primary-cyan)' }} />
                License & Billing
              </div>

              {user?.role === 'admin' && (
                <div
                  className="btn-secondary"
                  style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '8px 12px', fontSize: '0.85rem', color: '#f59e0b' }}
                  onClick={() => {
                    setCurrentTab('admin');
                    setShowDropdown(false);
                  }}
                >
                  <Crown style={{ width: '16px', height: '16px' }} />
                  Admin Panel
                </div>
              )}

              <div
                className="btn-secondary"
                style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '8px 12px', fontSize: '0.85rem', color: '#f43f5e', marginTop: '4px' }}
                onClick={() => {
                  setShowDropdown(false);
                  logout();
                }}
              >
                <LogOut style={{ width: '16px', height: '16px' }} />
                Sign Out
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
