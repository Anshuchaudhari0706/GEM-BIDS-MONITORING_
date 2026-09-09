import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, ShieldAlert, Key, CreditCard, Calendar, Sparkles, CheckCircle2, Clock, Copy, Check, RefreshCw, Zap, QrCode, ArrowRight } from 'lucide-react';
import { fetchMyLicenses } from '../services/api';

export default function BillingPage() {
  const { user, token, license, pricing, isLicenseActive, activateKey, generateKey, setShowPaymentModal, setSelectedPlanForPayment, showToast } = useAuth();
  const [subscriptionData, setSubscriptionData] = useState(null);
  const [manualKey, setManualKey] = useState('');
  const [activating, setActivating] = useState(false);
  
  // Admin Generator State
  const [genPlan, setGenPlan] = useState('monthly');
  const [genDuration, setGenDuration] = useState('30');
  const [genEmail, setGenEmail] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [lastGeneratedKey, setLastGeneratedKey] = useState(null);
  const [copiedKey, setCopiedKey] = useState(null);

  // My Keys List
  const [myKeys, setMyKeys] = useState([]);
  const [loadingKeys, setLoadingKeys] = useState(false);

  const fetchSubscriptionDetails = async () => {
    if (!token) return;
    try {
      const res = await fetch('/api/subscription', {
        headers: { Authorization: `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.subscription) {
        setSubscriptionData(data.subscription);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadMyKeys = async () => {
    if (!token) return;
    setLoadingKeys(true);
    try {
      const data = await fetchMyLicenses(token);
      setMyKeys(data.keys || []);
    } catch (err) {
      console.error('Failed to load user keys:', err);
    } finally {
      setLoadingKeys(false);
    }
  };

  useEffect(() => {
    fetchSubscriptionDetails();
    loadMyKeys();
  }, [token, license]);

  const handleManualActivate = async (e) => {
    if (e) e.preventDefault();
    if (!manualKey.trim()) return;
    setActivating(true);
    try {
      await activateKey(manualKey.trim());
      setManualKey('');
      fetchSubscriptionDetails();
      loadMyKeys();
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setActivating(false);
    }
  };

  const handleAdminGenerateKey = async (e) => {
    if (e) e.preventDefault();
    setIsGenerating(true);
    try {
      const res = await generateKey({
        plan: genPlan,
        durationDays: Number(genDuration) || 30,
        recipientEmail: genEmail.trim() || user?.email
      });
      setLastGeneratedKey(res.key);
      showToast(`🎉 Admin Generated Key: ${res.key}`, 'success');
      fetchSubscriptionDetails();
      loadMyKeys();
    } catch (err) {
      showToast(err.message || 'Failed to generate key', 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = (keyText) => {
    if (!keyText) return;
    navigator.clipboard.writeText(keyText);
    setCopiedKey(keyText);
    showToast(`Key copied: ${keyText}`, 'success');
    setTimeout(() => setCopiedKey(null), 3000);
  };

  const openPaymentForPlan = (planId) => {
    setSelectedPlanForPayment(planId);
    setShowPaymentModal(true);
  };

  const daysRemaining = subscriptionData?.daysRemaining ?? (license ? Math.max(0, Math.ceil((new Date(license.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))) : 0);

  return (
    <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '960px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <CreditCard style={{ width: '28px', height: '28px', color: 'var(--primary-cyan)' }} />
          <div>
            <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff' }}>Subscription & License Center</h1>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>Choose a subscription plan, make payment to generate your license key, or activate an offline key</p>
          </div>
        </div>

        <button
          onClick={() => {
            fetchSubscriptionDetails();
            loadMyKeys();
          }}
          className="btn-secondary"
          style={{ padding: '8px 14px', fontSize: '0.82rem', gap: '6px' }}
        >
          <RefreshCw style={{ width: '14px', height: '14px' }} /> Refresh
        </button>
      </div>

      {/* 1. CURRENT SUBSCRIPTION STATUS CARD */}
      <div
        className="glass-panel"
        style={{
          padding: '24px',
          borderRadius: '16px',
          background: isLicenseActive()
            ? 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85))'
            : 'linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(15, 23, 42, 0.95))',
          border: isLicenseActive() ? '1px solid var(--border-highlight)' : '1px solid rgba(239, 68, 68, 0.4)'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
              Your Account Status
            </div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff', marginTop: '4px' }}>
              {isLicenseActive()
                ? (subscriptionData?.planName || `${(license?.plan || 'monthly').toUpperCase()} PASS`)
                : 'No Active Subscription'}
            </h2>
          </div>

          <div style={{ textAlign: 'right' }}>
            <span
              className={`badge ${isLicenseActive() ? 'badge-active' : 'badge-expired'}`}
              style={{ padding: '8px 16px', fontSize: '0.85rem' }}
            >
              {isLicenseActive() ? '🟢 ACTIVE LICENSE' : '🔴 UNPAID / INACTIVE'}
            </span>
          </div>
        </div>

        {/* Dynamic Countdown Box */}
        {isLicenseActive() ? (
          <div
            style={{
              background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.15))',
              border: '1px solid var(--primary-cyan)',
              borderRadius: '12px',
              padding: '16px 20px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '12px'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <Clock style={{ width: '24px', height: '24px', color: 'var(--primary-cyan)' }} />
              <div>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Subscription Expiry Countdown</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#fff' }}>
                  Subscription expires in {daysRemaining} days
                </div>
              </div>
            </div>
            <span className="badge badge-published">{daysRemaining} Days Left</span>
          </div>
        ) : (
          <div
            style={{
              background: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              borderRadius: '12px',
              padding: '16px 20px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '12px'
            }}
          >
            <ShieldAlert style={{ width: '24px', height: '24px', color: '#f87171', flexShrink: 0 }} />
            <div>
              <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#fff' }}>
                Payment Required to Access GeM Tender Intelligence
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                Select a subscription plan below to pay via UPI QR or Card and instantly generate your active license key.
              </div>
            </div>
          </div>
        )}

        {/* Active Key Display */}
        {license?.key && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '16px',
              background: 'rgba(0,0,0,0.3)',
              borderRadius: '12px',
              padding: '16px 20px',
              marginBottom: '20px',
              border: '1px solid var(--border-color)'
            }}
          >
            <div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Activated Date</div>
              <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
                {license ? new Date(license.activationDate).toLocaleDateString('en-GB') : '—'}
              </div>
            </div>

            <div>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Expires Date</div>
              <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
                {license ? new Date(license.expiryDate).toLocaleDateString('en-GB') : '—'}
              </div>
            </div>

            <div style={{ gridColumn: 'span 2' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Active Cryptographic Key</div>
                <button
                  onClick={() => copyToClipboard(license.key)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: copiedKey === license.key ? 'var(--accent-green)' : 'var(--primary-cyan)',
                    cursor: 'pointer',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px'
                  }}
                >
                  {copiedKey === license.key ? <Check style={{ width: '14px', height: '14px' }} /> : <Copy style={{ width: '14px', height: '14px' }} />}
                  {copiedKey === license.key ? 'Copied' : 'Copy'}
                </button>
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: 900, color: 'var(--primary-cyan)', fontFamily: 'monospace', letterSpacing: '1px', marginTop: '2px' }}>
                {license.key}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 2. SUBSCRIPTION PRICING & PAYMENT PLANS (Required Payment First) */}
      <div>
        <div style={{ marginBottom: '16px' }}>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Sparkles style={{ width: '20px', color: 'var(--primary-cyan)' }} />
            Choose a Plan & Make Payment to Generate Key
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
            Complete payment via UPI QR code or Razorpay to instantly receive and activate your cryptographic license key.
          </p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '16px' }}>
          {/* Monthly Pass */}
          <div
            className="glass-panel"
            style={{
              padding: '24px',
              borderRadius: '16px',
              border: '1px solid var(--border-color)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              background: 'rgba(15, 23, 42, 0.7)'
            }}
          >
            <div>
              <span className="badge badge-published" style={{ fontSize: '0.72rem', textTransform: 'uppercase' }}>Starter</span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', marginTop: '8px' }}>Monthly Pass</h3>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '14px 0' }}>
                <span style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--primary-cyan)' }}>
                  {pricing.symbol}{pricing.monthly || 1499}
                </span>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>/ 30 days</span>
              </div>

              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 20px 0', fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Full GeM Live Tender Scanning
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> 11+ Service & Category Filters
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Date & State-based Matching
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Saved Bids Library
                </li>
              </ul>
            </div>

            <button
              onClick={() => openPaymentForPlan('monthly')}
              className="btn-cyan"
              style={{ width: '100%', justifyContent: 'center', padding: '10px', fontSize: '0.92rem', gap: '8px' }}
            >
              <CreditCard style={{ width: '16px', height: '16px' }} />
              Pay & Generate Key
            </button>
          </div>

          {/* Quarterly Pass */}
          <div
            className="glass-panel"
            style={{
              padding: '24px',
              borderRadius: '16px',
              border: '2px solid var(--primary-cyan)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(15, 23, 42, 0.8))',
              position: 'relative'
            }}
          >
            <div style={{ position: 'absolute', top: '-10px', right: '20px' }}>
              <span className="badge badge-active" style={{ fontSize: '0.7rem', padding: '3px 8px' }}>POPULAR</span>
            </div>

            <div>
              <span className="badge badge-published" style={{ fontSize: '0.72rem', textTransform: 'uppercase' }}>Quarterly</span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', marginTop: '8px' }}>Quarterly Pass</h3>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '14px 0' }}>
                <span style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--primary-cyan)' }}>
                  {pricing.symbol}{pricing.quarterly || 3999}
                </span>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>/ 90 days</span>
              </div>

              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 20px 0', fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Everything in Monthly
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> PDF Spec Sheet Exports
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Excel / CSV Downloads
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Priority Scanner Speed
                </li>
              </ul>
            </div>

            <button
              onClick={() => openPaymentForPlan('quarterly')}
              className="btn-cyan"
              style={{ width: '100%', justifyContent: 'center', padding: '10px', fontSize: '0.92rem', gap: '8px' }}
            >
              <CreditCard style={{ width: '16px', height: '16px' }} />
              Pay & Generate Key
            </button>
          </div>

          {/* Yearly Pass */}
          <div
            className="glass-panel"
            style={{
              padding: '24px',
              borderRadius: '16px',
              border: '1px solid var(--border-color)',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              background: 'rgba(15, 23, 42, 0.7)'
            }}
          >
            <div>
              <span className="badge badge-published" style={{ fontSize: '0.72rem', textTransform: 'uppercase' }}>Best Value</span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#fff', marginTop: '8px' }}>Professional Yearly</h3>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: '4px', margin: '14px 0' }}>
                <span style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--primary-cyan)' }}>
                  {pricing.symbol}{pricing.yearly || 11999}
                </span>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>/ 365 days</span>
              </div>

              <ul style={{ listStyle: 'none', padding: 0, margin: '0 0 20px 0', fontSize: '0.85rem', color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Everything in Quarterly
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Unlimited Live GeM Scans
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> Dedicated Cryptographic Key
                </li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <CheckCircle2 style={{ width: '16px', color: 'var(--accent-green)', flexShrink: 0 }} /> 24/7 Priority Support
                </li>
              </ul>
            </div>

            <button
              onClick={() => openPaymentForPlan('yearly')}
              className="btn-cyan"
              style={{ width: '100%', justifyContent: 'center', padding: '10px', fontSize: '0.92rem', gap: '8px' }}
            >
              <CreditCard style={{ width: '16px', height: '16px' }} />
              Pay & Generate Key
            </button>
          </div>
        </div>
      </div>

      {/* 3. ACTIVATE OFFLINE / ADMIN LICENSE KEY */}
      <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Key style={{ width: '18px', color: 'var(--primary-cyan)' }} />
          Activate Offline or Admin License Key
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
          Have you received a license key from the administrator or offline bank payment? Enter your 16-character key below to activate access immediately.
        </p>

        <form onSubmit={handleManualActivate} style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder="e.g. GEMI-XXXX-XXXX-XXXX"
            value={manualKey}
            onChange={(e) => setManualKey(e.target.value)}
            className="input-control"
            style={{ fontFamily: 'monospace', textTransform: 'uppercase', letterSpacing: '1px', flex: 1, minWidth: '220px' }}
          />
          <button type="submit" disabled={activating || !manualKey.trim()} className="btn-secondary" style={{ flexShrink: 0 }}>
            {activating ? 'Activating...' : 'Activate Key'}
          </button>
        </form>
      </div>

      {/* 4. ADMIN ONLY GENERATOR (Visible only to Admin accounts) */}
      {user?.role === 'admin' && (
        <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px', border: '1px solid rgba(245, 158, 11, 0.4)', background: 'rgba(245, 158, 11, 0.05)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '6px', borderRadius: '8px', background: 'rgba(245, 158, 11, 0.2)' }}>
              <Key style={{ width: '20px', height: '20px', color: '#f59e0b' }} />
            </div>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#fff' }}>Admin Master Key Generator</h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>Directly issue manual cryptographic keys for users (Admin Privilege)</p>
            </div>
          </div>

          <form onSubmit={handleAdminGenerateKey} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '12px' }}>
              <div>
                <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Target User Email</label>
                <input
                  type="email"
                  placeholder="user@domain.com"
                  value={genEmail}
                  onChange={(e) => setGenEmail(e.target.value)}
                  className="input-control"
                  style={{ fontSize: '0.85rem', marginTop: '4px' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Plan Tier</label>
                <select
                  value={genPlan}
                  onChange={(e) => setGenPlan(e.target.value)}
                  className="select-control"
                  style={{ width: '100%', fontSize: '0.85rem', marginTop: '4px' }}
                >
                  <option value="monthly">Monthly Pass (30 Days)</option>
                  <option value="quarterly">Quarterly Pass (90 Days)</option>
                  <option value="yearly">Professional Yearly (365 Days)</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Duration (Days)</label>
                <input
                  type="number"
                  min="1"
                  max="1825"
                  value={genDuration}
                  onChange={(e) => setGenDuration(e.target.value)}
                  className="input-control"
                  style={{ fontSize: '0.85rem', marginTop: '4px' }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isGenerating}
              className="btn-cyan"
              style={{ width: 'fit-content', padding: '10px 20px', fontSize: '0.9rem', gap: '8px' }}
            >
              <Zap style={{ width: '16px', height: '16px' }} />
              {isGenerating ? 'Generating...' : 'Issue Master License Key'}
            </button>
          </form>

          {lastGeneratedKey && (
            <div
              style={{
                marginTop: '16px',
                padding: '14px 18px',
                background: 'rgba(0,0,0,0.4)',
                borderRadius: '10px',
                border: '1px solid #f59e0b',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                flexWrap: 'wrap',
                gap: '10px'
              }}
            >
              <div>
                <div style={{ fontSize: '0.72rem', color: '#f59e0b', fontWeight: 700 }}>ISSUED KEY CODE</div>
                <div style={{ fontSize: '1.2rem', fontWeight: 900, color: '#fff', fontFamily: 'monospace', letterSpacing: '1px' }}>
                  {lastGeneratedKey}
                </div>
              </div>
              <button
                type="button"
                onClick={() => copyToClipboard(lastGeneratedKey)}
                className="btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.8rem', gap: '4px' }}
              >
                {copiedKey === lastGeneratedKey ? <Check style={{ width: '14px', color: 'var(--accent-green)' }} /> : <Copy style={{ width: '14px' }} />}
                {copiedKey === lastGeneratedKey ? 'Copied' : 'Copy Key'}
              </button>
            </div>
          )}
        </div>
      )}

      {/* 5. MY LICENSE KEYS TABLE */}
      {myKeys.length > 0 && (
        <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck style={{ width: '18px', color: 'var(--accent-green)' }} />
              My License Keys ({myKeys.length})
            </h3>
          </div>

          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                  <th style={{ padding: '10px' }}>LICENSE KEY</th>
                  <th style={{ padding: '10px' }}>PLAN</th>
                  <th style={{ padding: '10px' }}>STATUS</th>
                  <th style={{ padding: '10px' }}>EXPIRY DATE</th>
                  <th style={{ padding: '10px', textAlign: 'right' }}>ACTIONS</th>
                </tr>
              </thead>
              <tbody>
                {myKeys.map((k) => (
                  <tr key={k.id || k.key} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                    <td style={{ padding: '12px 10px', fontFamily: 'monospace', fontWeight: 700, color: 'var(--primary-cyan)' }}>
                      {k.key}
                    </td>
                    <td style={{ padding: '12px 10px', textTransform: 'capitalize' }}>
                      {k.plan || 'Monthly'}
                    </td>
                    <td style={{ padding: '12px 10px' }}>
                      <span className={`badge ${k.status === 'ACTIVE' ? 'badge-active' : 'badge-expired'}`}>
                        {k.status || 'ACTIVE'}
                      </span>
                    </td>
                    <td style={{ padding: '12px 10px', color: 'var(--text-muted)' }}>
                      {k.expiryDate ? new Date(k.expiryDate).toLocaleDateString('en-GB') : '—'}
                    </td>
                    <td style={{ padding: '12px 10px', textAlign: 'right' }}>
                      <div style={{ display: 'inline-flex', gap: '6px' }}>
                        <button
                          type="button"
                          onClick={() => copyToClipboard(k.key)}
                          className="btn-secondary"
                          style={{ padding: '4px 8px', fontSize: '0.75rem', gap: '4px' }}
                        >
                          {copiedKey === k.key ? <Check style={{ width: '12px', color: 'var(--accent-green)' }} /> : <Copy style={{ width: '12px' }} />}
                          {copiedKey === k.key ? 'Copied' : 'Copy'}
                        </button>

                        {license?.key !== k.key && (
                          <button
                            type="button"
                            onClick={() => {
                              activateKey(k.key).then(() => {
                                fetchSubscriptionDetails();
                                loadMyKeys();
                              });
                            }}
                            className="btn-cyan"
                            style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                          >
                            Apply
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
