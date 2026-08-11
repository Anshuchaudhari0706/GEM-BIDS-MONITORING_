import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Sparkles, User, Building, Mail, Phone, Lock, CheckCircle2, ShieldCheck, ArrowRight } from 'lucide-react';

export default function RegisterPage({ onNavigate }) {
  const { register, pricing } = useAuth();

  const [formData, setFormData] = useState({
    fullName: '',
    companyName: '',
    email: '',
    mobile: '',
    password: '',
    confirmPassword: ''
  });

  const [selectedPlan, setSelectedPlan] = useState('monthly');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    if (formData.password !== formData.confirmPassword) {
      setErrorMsg('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      await register(formData, selectedPlan);
      onNavigate('dashboard');
    } catch (err) {
      setErrorMsg(err.message || 'Registration failed');
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
        background: 'radial-gradient(circle at 50% 20%, rgba(15, 23, 42, 0.95) 0%, rgba(7, 10, 18, 1) 90%)',
        padding: '40px 20px'
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '560px',
          padding: '36px',
          borderRadius: '20px',
          boxShadow: '0 20px 50px rgba(0,0,0,0.8)',
          border: '1px solid var(--border-highlight)'
        }}
      >
        {/* Header */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <div
            style={{
              width: '50px',
              height: '50px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #06b6d4, #3b82f6)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              margin: '0 auto 12px auto',
              boxShadow: '0 0 20px rgba(6, 182, 212, 0.5)'
            }}
          >
            <Sparkles style={{ color: '#fff', width: '28px', height: '28px' }} />
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: '#fff' }} className="brand-font">
            Create GeM<span style={{ color: 'var(--primary-cyan)' }}>Intel</span> Account
          </h1>
          <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginTop: '4px' }}>
            Register your business & choose your tender scanning subscription
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

        <form onSubmit={handleSubmit}>
          {/* User & Company Info */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Full Name *
              </label>
              <div style={{ position: 'relative' }}>
                <User style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="text"
                  name="fullName"
                  required
                  placeholder="Rahul Verma"
                  value={formData.fullName}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Company Name
              </label>
              <div style={{ position: 'relative' }}>
                <Building style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="text"
                  name="companyName"
                  placeholder="Apex Infra Solutions"
                  value={formData.companyName}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '14px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Email Address *
              </label>
              <div style={{ position: 'relative' }}>
                <Mail style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="email"
                  name="email"
                  required
                  placeholder="rahul@apexinfra.com"
                  value={formData.email}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Mobile Number
              </label>
              <div style={{ position: 'relative' }}>
                <Phone style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="text"
                  name="mobile"
                  placeholder="9876543210"
                  value={formData.mobile}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px', marginBottom: '24px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Password *
              </label>
              <div style={{ position: 'relative' }}>
                <Lock style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="password"
                  name="password"
                  required
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                Confirm Password *
              </label>
              <div style={{ position: 'relative' }}>
                <Lock style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', width: '16px', color: 'var(--text-muted)' }} />
                <input
                  type="password"
                  name="confirmPassword"
                  required
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="input-control"
                  style={{ paddingLeft: '38px', fontSize: '0.88rem' }}
                />
              </div>
            </div>
          </div>

          {/* Subscription Selection Box */}
          <div style={{ marginBottom: '24px' }}>
            <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 600, color: '#fff', marginBottom: '10px' }}>
              Choose Your Subscription Plan
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
              {[
                { id: 'monthly', title: 'Monthly', price: pricing.monthly },
                { id: 'quarterly', title: 'Quarterly', price: pricing.quarterly },
                { id: 'yearly', title: 'Yearly', price: pricing.yearly }
              ].map(plan => (
                <div
                  key={plan.id}
                  onClick={() => setSelectedPlan(plan.id)}
                  style={{
                    padding: '12px',
                    borderRadius: '10px',
                    border: selectedPlan === plan.id ? '2px solid var(--primary-cyan)' : '1px solid var(--border-color)',
                    background: selectedPlan === plan.id ? 'rgba(6, 182, 212, 0.15)' : 'rgba(15, 23, 42, 0.6)',
                    cursor: 'pointer',
                    textAlign: 'center'
                  }}
                >
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fff' }}>{plan.title}</div>
                  <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--primary-cyan)', marginTop: '4px' }}>
                    {pricing.symbol}{plan.price}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-cyan"
            style={{ width: '100%', justifyContent: 'center', padding: '12px', fontSize: '1rem' }}
          >
            {loading ? 'Creating Account...' : 'Proceed to Payment & Activate Key'}
          </button>
        </form>

        <div style={{ borderTop: '1px solid var(--border-color)', margin: '24px 0 16px 0' }} />

        <div style={{ textAlign: 'center', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Already have an account?{' '}
          <span
            onClick={() => onNavigate('login')}
            style={{ color: 'var(--primary-cyan)', fontWeight: 600, cursor: 'pointer' }}
          >
            Login Here
          </span>
        </div>
      </div>
    </div>
  );
}
