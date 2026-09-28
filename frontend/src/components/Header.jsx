import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import {
  ShieldCheck,
  ShieldAlert,
  Search,
  User,
  LogOut,
  Sparkles,
  Key,
  Crown,
  ChevronDown,
  Settings,
  Bell
} from 'lucide-react';

export default function Header({ currentTab, setCurrentTab, searchQuery, setSearchQuery }) {
  const { user, license, isLicenseActive, logout, setShowPaymentModal, setSelectedPlanForPayment } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  const calculateDaysLeft = () => {
    if (!license || !license.expiryDate) return 0;
    const diff = new Date(license.expiryDate) - new Date();
    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
  };

  const daysLeft = calculateDaysLeft();

  // Close dropdown on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header
      style={{
        height: '76px',
        background: 'var(--bg-header)',
        backdropFilter: 'blur(24px)',
        WebkitBackdropFilter: 'blur(24px)',
        borderBottom: '1px solid var(--border-color)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 32px',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}
    >
      {/* Brand Logo */}
      <div
        style={{ display: 'flex', alignItems: 'center', gap: '14px', cursor: 'pointer' }}
        onClick={() => setCurrentTab('dashboard')}
      >
        <div
          style={{
            width: '44px',
            height: '44px',
            borderRadius: '12px',
            background: 'linear-gradient(135deg, #0284c7 0%, #2563eb 50%, #7c3aed 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(37, 99, 235, 0.45)',
            border: '1px solid rgba(255, 255, 255, 0.2)'
          }}
        >
          <Sparkles style={{ color: '#fff', width: '24px', height: '24px' }} />
        </div>
        <div>
          <div style={{ fontSize: '1.45rem', fontWeight: 900, color: '#fff', letterSpacing: '-0.03em', lineHeight: 1.1 }} className="brand-font">
            GeM<span style={{ color: 'var(--primary-cyan-bright)', textShadow: '0 0 12px rgba(56, 189, 248, 0.4)' }}>Intel</span>
          </div>
          <span style={{ fontSize: '0.8rem', display: 'block', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.02em', marginTop: '2px' }}>
            Smart Tender Intelligence Platform
          </span>
        </div>
      </div>

      {/* Global Tender Search Bar */}
      <div style={{ position: 'relative', width: '420px', maxWidth: '100%' }}>
        <Search
          style={{
            position: 'absolute',
            left: '16px',
            top: '50%',
            transform: 'translateY(-50%)',
            width: '18px',
            height: '18px',
            color: 'var(--text-muted)'
          }}
        />
        <input
          type="text"
          placeholder="Search GeM Bids, Department, Location, Service..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="input-control"
          style={{
            paddingLeft: '46px',
            paddingRight: '60px',
            height: '46px',
            fontSize: '0.94rem',
            borderRadius: '12px'
          }}
        />
        <div style={{ position: 'absolute', right: '12px', top: '50%', transform: 'translateY(-50%)', background: 'rgba(255,255,255,0.08)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '2px 8px', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700 }}>
          ⌘K
        </div>
      </div>

      {/* Right Navigation & Status Controls */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '18px' }}>
        {/* License Status Badge */}
        {isLicenseActive() ? (
          <div
            className="badge badge-active"
            style={{
              padding: '8px 16px',
              fontSize: '0.86rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              borderRadius: '12px'
            }}
            onClick={() => setCurrentTab('billing')}
          >
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#10b981', boxShadow: '0 0 8px #10b981' }} />
            <span style={{ fontWeight: 700 }}>Active License</span>
            <span style={{ opacity: 0.9, fontSize: '0.78rem', background: 'rgba(16, 185, 129, 0.22)', padding: '3px 8px', borderRadius: '6px', fontWeight: 800 }}>
              {daysLeft}d left
            </span>
          </div>
        ) : (
          <div
            className="badge badge-expired"
            style={{
              padding: '8px 16px',
              fontSize: '0.86rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '10px',
              borderRadius: '12px'
            }}
            onClick={() => {
              setSelectedPlanForPayment('monthly');
              setShowPaymentModal(true);
            }}
          >
            <ShieldAlert style={{ width: '18px', height: '18px' }} />
            <span>Subscription Inactive</span>
            <span style={{ background: 'rgba(244, 63, 94, 0.35)', padding: '3px 8px', borderRadius: '6px', fontWeight: 800, textTransform: 'none' }}>
              Renew Now
            </span>
          </div>
        )}

        {/* User Profile Menu */}
        <div style={{ position: 'relative' }} ref={dropdownRef}>
          <div
            onClick={() => setShowDropdown(!showDropdown)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '12px',
              padding: '8px 14px',
              borderRadius: '12px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid var(--border-color)',
              cursor: 'pointer',
              transition: 'all 0.2s ease'
            }}
          >
            <div
              style={{
                width: '38px',
                height: '38px',
                borderRadius: '10px',
                background: user?.role === 'admin' ? 'linear-gradient(135deg, #f59e0b, #ef4444)' : 'linear-gradient(135deg, #06b6d4, #2563eb)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                color: '#fff',
                fontSize: '1rem',
                boxShadow: '0 2px 8px rgba(0,0,0,0.4)'
              }}
            >
              {user?.fullName ? user.fullName.charAt(0).toUpperCase() : 'U'}
            </div>
            <div style={{ textAlign: 'left', lineHeight: '1.25' }}>
              <div style={{ fontSize: '0.94rem', fontWeight: 700, color: '#fff' }}>{user?.fullName || 'User Profile'}</div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{user?.companyName || user?.email}</div>
            </div>
            <ChevronDown style={{ width: '16px', height: '16px', color: 'var(--text-muted)', transform: showDropdown ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
          </div>

          {/* Dropdown Menu */}
          {showDropdown && (
            <div
              style={{
                position: 'absolute',
                right: 0,
                top: '58px',
                width: '260px',
                background: '#0d1322',
                border: '1px solid var(--border-color)',
                borderRadius: '14px',
                boxShadow: '0 16px 40px rgba(0,0,0,0.75)',
                padding: '10px',
                zIndex: 200
              }}
            >
              <div style={{ padding: '10px 14px', borderBottom: '1px solid var(--border-color)', marginBottom: '8px' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.5px' }}>
                  Account Info
                </div>
                <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#fff', marginTop: '2px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {user?.email}
                </div>
                <div style={{ display: 'inline-block', marginTop: '4px' }}>
                  <span className={`badge ${user?.role === 'admin' ? 'badge-finished' : 'badge-published'}`} style={{ fontSize: '0.72rem', padding: '2px 8px' }}>
                    {user?.role === 'admin' ? 'MASTER ADMIN' : 'AUTHORIZED USER'}
                  </span>
                </div>
              </div>

              <div
                className="btn-secondary"
                style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '10px 14px', fontSize: '0.92rem', borderRadius: '8px' }}
                onClick={() => {
                  setCurrentTab('billing');
                  setShowDropdown(false);
                }}
              >
                <Key style={{ width: '18px', height: '18px', color: 'var(--primary-cyan)' }} />
                License & Subscription
              </div>

              {user?.role === 'admin' && (
                <div
                  className="btn-secondary"
                  style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '10px 14px', fontSize: '0.92rem', color: '#f59e0b', borderRadius: '8px' }}
                  onClick={() => {
                    setCurrentTab('admin-dashboard');
                    setShowDropdown(false);
                  }}
                >
                  <Crown style={{ width: '18px', height: '18px' }} />
                  Admin Control Panel
                </div>
              )}

              {user?.role === 'admin' && (
                <div
                  className="btn-secondary"
                  style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '10px 14px', fontSize: '0.92rem', color: 'var(--primary-cyan-bright)', borderRadius: '8px' }}
                  onClick={() => {
                    setCurrentTab('admin-settings');
                    setShowDropdown(false);
                  }}
                >
                  <Settings style={{ width: '18px', height: '18px' }} />
                  System Settings
                </div>
              )}

              <div style={{ borderTop: '1px solid var(--border-color)', margin: '6px 0' }} />

              <div
                className="btn-secondary"
                style={{ width: '100%', border: 'none', justifyContent: 'flex-start', padding: '10px 14px', fontSize: '0.92rem', color: '#f43f5e', borderRadius: '8px' }}
                onClick={() => {
                  setShowDropdown(false);
                  logout();
                }}
              >
                <LogOut style={{ width: '18px', height: '18px' }} />
                Sign Out
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
