import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { ShieldCheck, ShieldAlert, Key, CreditCard, Calendar, Sparkles, CheckCircle2, Clock } from 'lucide-react';

export default function BillingPage() {
  const { user, token, license, isLicenseActive, activateKey, setShowPaymentModal, setSelectedPlanForPayment, showToast } = useAuth();
  const [subscriptionData, setSubscriptionData] = useState(null);
  const [manualKey, setManualKey] = useState('');
  const [activating, setActivating] = useState(false);

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

  useEffect(() => {
    fetchSubscriptionDetails();
  }, [token, license]);

  const handleManualActivate = async (e) => {
    e.preventDefault();
    if (!manualKey.trim()) return;
    setActivating(true);
    try {
      await activateKey(manualKey.trim());
      setManualKey('');
      fetchSubscriptionDetails();
    } catch (err) {
      showToast(err.message, 'error');
    } finally {
      setActivating(false);
    }
  };

  const daysRemaining = subscriptionData?.daysRemaining ?? (license ? Math.max(0, Math.ceil((new Date(license.expiryDate) - new Date()) / (1000 * 60 * 60 * 24))) : 0);

  return (
    <div style={{ padding: '24px', flex: 1, display: 'flex', flexDirection: 'column', gap: '24px', maxWidth: '850px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <CreditCard style={{ width: '28px', height: '28px', color: 'var(--primary-cyan)' }} />
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff' }}>Subscription Dashboard</h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)' }}>Manage your plan, license key, and subscription expiration</p>
        </div>
      </div>

      {/* 31. User Subscription Dashboard Card */}
      <div
        className="glass-panel"
        style={{
          padding: '28px',
          borderRadius: '16px',
          background: 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.8))',
          border: '1px solid var(--border-highlight)'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '24px' }}>
          <div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
              Subscription Details
            </div>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#fff', marginTop: '4px' }}>
              {subscriptionData?.planName || (license ? `${license.plan.toUpperCase()} PASS` : 'No Active Subscription')}
            </h2>
          </div>

          <div style={{ textAlign: 'right' }}>
            <span
              className={`badge ${isLicenseActive() ? 'badge-active' : 'badge-expired'}`}
              style={{ padding: '8px 16px', fontSize: '0.85rem' }}
            >
              {isLicenseActive() ? '🟢 ACTIVE' : '🔴 INACTIVE / EXPIRED'}
            </span>
          </div>
        </div>

        {/* Dynamic Countdown Box */}
        {isLicenseActive() && (
          <div
            style={{
              background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.15))',
              border: '1px solid var(--primary-cyan)',
              borderRadius: '12px',
              padding: '16px 20px',
              marginBottom: '24px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
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
        )}

        {/* License Details Grid */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '16px',
            background: 'rgba(0,0,0,0.3)',
            borderRadius: '12px',
            padding: '20px',
            marginBottom: '24px',
            border: '1px solid var(--border-color)'
          }}
        >
          <div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Activated Date</div>
            <div style={{ fontSize: '0.98rem', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
              {license ? new Date(license.activationDate).toLocaleDateString('en-GB') : '—'}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Expires Date</div>
            <div style={{ fontSize: '0.98rem', fontWeight: 600, color: '#fff', marginTop: '2px' }}>
              {license ? new Date(license.expiryDate).toLocaleDateString('en-GB') : '—'}
            </div>
          </div>

          <div style={{ gridColumn: 'span 2' }}>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Cryptographic License Key</div>
            <div style={{ fontSize: '1.4rem', fontWeight: 900, color: 'var(--primary-cyan)', fontFamily: 'monospace', letterSpacing: '1px', marginTop: '2px' }}>
              {license ? license.key : 'No Key Issued'}
            </div>
          </div>
        </div>

        {/* Action Button */}
        <div style={{ display: 'flex', gap: '14px' }}>
          <button
            onClick={() => {
              setSelectedPlanForPayment(license?.plan || 'monthly');
              setShowPaymentModal(true);
            }}
            className="btn-cyan"
            style={{ padding: '12px 24px', fontSize: '0.95rem' }}
          >
            <Sparkles style={{ width: '18px', height: '18px' }} />
            Renew Subscription
          </button>
        </div>
      </div>

      {/* Manual Key Activation Box */}
      <div className="glass-panel" style={{ padding: '24px', borderRadius: '16px' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Key style={{ width: '18px', color: 'var(--primary-cyan)' }} />
          Activate Admin or Offline License Key
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
          Enter a valid 16-character license key (Format: GEMI-XXXX-XXXX-XXXX) to attach it to your profile.
        </p>

        <form onSubmit={handleManualActivate} style={{ display: 'flex', gap: '12px' }}>
          <input
            type="text"
            placeholder="e.g. GEMI-7F3A-92KD-X81P"
            value={manualKey}
            onChange={(e) => setManualKey(e.target.value)}
            className="input-control"
            style={{ fontFamily: 'monospace', textTransform: 'uppercase', letterSpacing: '1px' }}
          />
          <button type="submit" disabled={activating} className="btn-secondary" style={{ flexShrink: 0 }}>
            {activating ? 'Activating...' : 'Activate Key'}
          </button>
        </form>
      </div>
    </div>
  );
}
