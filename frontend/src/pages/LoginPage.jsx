import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Sparkles, Mail, Lock, ArrowRight, ShieldAlert, Key } from 'lucide-react';

export default function LoginPage({ onNavigate }) {
  const { login, isLicenseActive, license, setShowPaymentModal, setSelectedPlanForPayment } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [loggedInState, setLoggedInState] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    try {
      const res = await login(email, password);
      setLoggedInState(res);
      // Check subscription
      if (res.license && res.license.status === 'ACTIVE' && new Date(res.license.expiryDate) > new Date()) {
        onNavigate('dashboard');
      }
    } catch (err) {
      setErrorMsg(err.message || 'Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'radial-gradient(circle at 50% 30%, rgba(15, 23, 42, 0.9) 0%, rgba(7, 10, 18, 1) 90%)',
        padding: '20px'
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '440px',
          padding: '36px',
          borderRadius: '20px',
          boxShadow: '0 20px 50px rgba(0,0,0,0.8)',
          border: '1px solid var(--border-highlight)'
        }}
      >
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <div
            style={{
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 12px auto',
              boxShadow: '0 0 20px rgba(59, 130, 246, 0.5)'
            }}
          >
            <Sparkles style={{ color: '#fff', width: '28px', height: '28px' }} />
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fff' }} className="brand-font">
            GeM<span style={{ color: 'var(--primary-cyan)' }}>Intel</span> Login
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Sign in to access your tender scanner dashboard
          </p>
        </div>

        {errorMsg && (
          <div
            style={{
              background: 'rgba(239, 68, 68, 0.15)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              borderRadius: '8px',
              padding: '10px 14px',
              color: '#f87171',
              fontSize: '0.88rem',
              marginBottom: '20px'
            }}
          >
            {errorMsg}
          </div>
        )}

        {/* If logged in but subscription issues exist */}
        {loggedInState && !isLicenseActive() ? (
          <div style={{ textAlign: 'center', padding: '10px 0' }}>
            <div
              style={{
                width: '50px',
                height: '50px',
                borderRadius: '50%',
                background: 'rgba(245, 158, 11, 0.15)',
                border: '1px solid #f59e0b',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 14px auto'
              }}
            >
              <ShieldAlert style={{ width: '28px', height: '28px', color: '#f59e0b' }} />
            </div>

            {loggedInState.license ? (
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '8px' }}>
                  Subscription Expired
                </h3>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '20px', lineHeight: 1.5 }}>
                  Your subscription has expired. Please renew your subscription to continue using GeMIntel.
                </p>
                <button
                  onClick={() => {
                    setSelectedPlanForPayment('monthly');
                    setShowPaymentModal(true);
                  }}
                  className="btn-cyan"
                  style={{ width: '100%', justifyContent: 'center' }}
                >
                  Renew Subscription
                </button>
              </div>
            ) : (
              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: '8px' }}>
                  Subscription Required
                </h3>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '20px', lineHeight: 1.5 }}>
                  An active subscription is required to access the dashboard.
                </p>
                <button
                  onClick={() => {
                    setSelectedPlanForPayment('monthly');
                    setShowPaymentModal(true);
                  }}
                  className="btn-primary"
                  style={{ width: '100%', justifyContent: 'center' }}
                >
                  Subscribe Now & Get License Key
                </button>
              </div>
            )}
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '18px' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '6px' }}>
                Email Address
              </label>
              <div style={{ position: 'relative' }}>
                <Mail style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', width: '18px', color: 'var(--text-muted)' }} />
                <input
                  type="email"
                  required
                  placeholder="name@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="input-control"
                  style={{ paddingLeft: '42px' }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '24px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                <label style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Password</label>
                <a href="#forgot" onClick={(e) => { e.preventDefault(); alert('Password reset link sent to email'); }} style={{ fontSize: '0.8rem', color: 'var(--primary-cyan)', textDecoration: 'none' }}>
                  Forgot Password?
                </a>
              </div>
              <div style={{ position: 'relative' }}>
                <Lock style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', width: '18px', color: 'var(--text-muted)' }} />
                <input
                  type="password"
                  required
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="input-control"
                  style={{ paddingLeft: '42px' }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '1rem' }}
            >
              {loading ? 'Authenticating...' : 'Login to Dashboard'}
            </button>
          </form>
        )}

        <div style={{ borderTop: '1px solid var(--border-color)', margin: '24px 0 18px 0' }} />

        <div style={{ textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Don't have an account?{' '}
          <span
            onClick={() => onNavigate('register')}
            style={{ color: 'var(--primary-cyan)', fontWeight: 600, cursor: 'pointer' }}
          >
            Create Account
          </span>
        </div>
      </div>
    </div>
  );
}
