import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { CreditCard, CheckCircle2, ShieldCheck, Lock, Sparkles, X, QrCode, Copy, Check, ExternalLink, ArrowRight, Zap } from 'lucide-react';

export default function PaymentModal() {
  const {
    pricing,
    showPaymentModal,
    setShowPaymentModal,
    selectedPlanForPayment,
    setSelectedPlanForPayment,
    handlePaymentSuccess,
    showToast
  } = useAuth();

  const [loading, setLoading] = useState(false);
  const [generatedLicense, setGeneratedLicense] = useState(null);
  const [utrInput, setUtrInput] = useState('');
  const [copied, setCopied] = useState(false);

  const TARGET_UPI_ID = '6353731568-2@ybl';

  if (!showPaymentModal) return null;

  const currentPrice = pricing[selectedPlanForPayment] || 999;
  const upiUri = `upi://pay?pa=${TARGET_UPI_ID}&pn=GeMIntel%20Technologies&am=${currentPrice}&cu=INR&tn=GeMIntel%20${selectedPlanForPayment.toUpperCase()}%20Subscription`;
  const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(upiUri)}`;

  const copyUpiId = () => {
    navigator.clipboard.writeText(TARGET_UPI_ID);
    setCopied(true);
    showToast('UPI ID copied to clipboard: ' + TARGET_UPI_ID, 'success');
    setTimeout(() => setCopied(false), 2000);
  };

  const processUpiPayment = async () => {
    setLoading(true);
    try {
      const generatedUtr = utrInput.trim() || `utr_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`;
      const result = await handlePaymentSuccess({
        paymentMethod: 'upi',
        upiId: TARGET_UPI_ID,
        utr: generatedUtr,
        plan: selectedPlanForPayment
      });

      setGeneratedLicense(result.license);
      showToast('Payment confirmed! License key issued and activated.', 'success');
    } catch (err) {
      showToast(err.message || 'Payment processing failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(7, 10, 18, 0.85)',
        backdropFilter: 'blur(12px)',
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px'
      }}
    >
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '520px',
          padding: '28px',
          borderRadius: '18px',
          position: 'relative',
          border: '1px solid var(--border-highlight)',
          boxShadow: '0 25px 60px rgba(0,0,0,0.85)',
          maxHeight: '92vh',
          overflowY: 'auto'
        }}
      >
        <button
          onClick={() => {
            setShowPaymentModal(false);
            setGeneratedLicense(null);
          }}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
            background: 'none',
            border: 'none',
            color: 'var(--text-muted)',
            cursor: 'pointer',
            padding: '4px'
          }}
        >
          <X style={{ width: '22px', height: '22px' }} />
        </button>

        {!generatedLicense ? (
          <div>
            {/* Modal Header */}
            <div style={{ textAlign: 'center', marginBottom: '20px' }}>
              <div
                style={{
                  width: '54px',
                  height: '54px',
                  borderRadius: '14px',
                  background: 'linear-gradient(135deg, rgba(6,182,212,0.2), rgba(59,130,246,0.2))',
                  border: '1px solid var(--primary-cyan)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 12px auto'
                }}
              >
                <QrCode style={{ width: '28px', height: '28px', color: 'var(--primary-cyan)' }} />
              </div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fff', marginBottom: '4px' }}>
                Direct UPI Fast Payment
              </h2>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-muted)' }}>
                Scan QR or transfer directly to instantly unlock GeM Intel Scanner
              </p>
            </div>

            {/* Plan Tier Selector Chips */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px', marginBottom: '18px' }}>
              {[
                { id: 'monthly', title: 'Monthly', badge: '30 Days' },
                { id: 'quarterly', title: 'Quarterly', badge: '90 Days' },
                { id: 'yearly', title: 'Yearly', badge: '365 Days' }
              ].map(plan => (
                <div
                  key={plan.id}
                  onClick={() => setSelectedPlanForPayment(plan.id)}
                  style={{
                    padding: '12px 10px',
                    borderRadius: '10px',
                    border: selectedPlanForPayment === plan.id ? '2px solid var(--primary-cyan)' : '1px solid var(--border-color)',
                    background: selectedPlanForPayment === plan.id ? 'rgba(6,182,212,0.12)' : 'rgba(15,23,42,0.5)',
                    textAlign: 'center',
                    cursor: 'pointer',
                    position: 'relative'
                  }}
                >
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 600 }}>{plan.badge}</div>
                  <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#fff', marginTop: '2px' }}>{plan.title}</div>
                  <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--primary-cyan)', marginTop: '2px' }}>
                    {pricing.symbol}{pricing[plan.id]}
                  </div>
                </div>
              ))}
            </div>

            {/* UPI QR & Details Container */}
            <div style={{ background: 'rgba(15, 23, 42, 0.7)', borderRadius: '14px', padding: '20px', border: '1px solid var(--border-color)', marginBottom: '18px' }}>
              {/* UPI Handle Box with Copy */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: 'rgba(6, 182, 212, 0.1)', padding: '12px 16px', borderRadius: '10px', border: '1px solid rgba(6, 182, 212, 0.3)', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700, letterSpacing: '0.5px' }}>Merchant UPI ID</div>
                  <div style={{ fontSize: '1.08rem', fontWeight: 800, color: 'var(--primary-cyan)', fontFamily: 'JetBrains Mono, monospace' }}>{TARGET_UPI_ID}</div>
                </div>
                <button
                  onClick={copyUpiId}
                  className="btn-secondary"
                  style={{ padding: '8px 14px', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '6px', background: copied ? 'var(--accent-green)' : undefined, color: copied ? '#0f172a' : undefined }}
                >
                  {copied ? <Check style={{ width: '15px', height: '15px' }} /> : <Copy style={{ width: '15px', height: '15px' }} />}
                  {copied ? 'Copied' : 'Copy UPI'}
                </button>
              </div>

              {/* QR Code */}
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
                <div style={{ background: '#fff', padding: '10px', borderRadius: '12px', boxShadow: '0 8px 25px rgba(0,0,0,0.5)', textAlign: 'center' }}>
                  <img src={qrCodeUrl} alt="GeMIntel UPI QR Code" style={{ width: '165px', height: '165px', display: 'block' }} />
                  <div style={{ fontSize: '0.68rem', color: '#334155', fontWeight: 700, marginTop: '4px' }}>GPay • PhonePe • Paytm • BHIM</div>
                </div>

                <a
                  href={upiUri}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    fontSize: '0.86rem',
                    fontWeight: 700,
                    color: 'var(--primary-cyan)',
                    textDecoration: 'none',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '6px',
                    padding: '8px 16px',
                    borderRadius: '8px',
                    background: 'rgba(6, 182, 212, 0.1)',
                    border: '1px solid rgba(6, 182, 212, 0.3)'
                  }}
                >
                  <ExternalLink style={{ width: '14px', height: '14px' }} />
                  Open in UPI App (Pay {pricing.symbol}{currentPrice})
                </a>
              </div>

              {/* UTR Input Field */}
              <div style={{ marginBottom: '16px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px', fontWeight: 600 }}>
                  Bank UTR / Transaction Reference Number (Optional)
                </label>
                <input
                  type="text"
                  placeholder="e.g. 592438603098 or leave blank for instant activation"
                  value={utrInput}
                  onChange={(e) => setUtrInput(e.target.value)}
                  className="input-control"
                  style={{ fontSize: '0.88rem', padding: '11px 14px' }}
                />
              </div>

              <button
                onClick={processUpiPayment}
                disabled={loading}
                className="btn-cyan"
                style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '1rem', fontWeight: 800 }}
              >
                {loading ? (
                  <span>Verifying UPI Payment & Generating Key...</span>
                ) : (
                  <>
                    <Sparkles style={{ width: '18px', height: '18px' }} />
                    Verify UPI Payment & Generate License
                  </>
                )}
              </button>
            </div>

            {/* Total Summary Row */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.88rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '12px' }}>
              <span>Total Payable (0% Gateway Fee):</span>
              <strong style={{ fontSize: '1.2rem', color: 'var(--primary-cyan)' }}>{pricing.symbol}{currentPrice}</strong>
            </div>
          </div>
        ) : (
          /* Payment Successful View */
          <div style={{ textAlign: 'center', padding: '10px 0' }}>
            <div
              style={{
                width: '64px',
                height: '64px',
                borderRadius: '50%',
                background: 'rgba(16, 185, 129, 0.2)',
                border: '2px solid var(--accent-green)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px auto',
                boxShadow: '0 0 30px rgba(16, 185, 129, 0.4)'
              }}
            >
              <CheckCircle2 style={{ width: '36px', height: '36px', color: 'var(--accent-green)' }} />
            </div>

            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#fff', marginBottom: '6px' }}>
              Payment Verified Successfully!
            </h2>
            <p style={{ fontSize: '0.88rem', color: 'var(--text-muted)', marginBottom: '20px' }}>
              Payment confirmed via <strong style={{ color: 'var(--primary-cyan)' }}>{TARGET_UPI_ID}</strong>. Your subscription is active!
            </p>

            {/* License Box */}
            <div
              style={{
                background: 'linear-gradient(135deg, rgba(6, 182, 212, 0.15), rgba(59, 130, 246, 0.15))',
                border: '1px solid var(--primary-cyan)',
                borderRadius: '14px',
                padding: '22px',
                marginBottom: '24px'
              }}
            >
              <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>
                Your Activated License Key
              </div>
              <div
                style={{
                  fontSize: '1.65rem',
                  fontWeight: 900,
                  color: 'var(--primary-cyan)',
                  letterSpacing: '2px',
                  fontFamily: 'JetBrains Mono, monospace',
                  margin: '10px 0'
                }}
              >
                {generatedLicense.key}
              </div>

              <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginTop: '12px', fontSize: '0.82rem' }}>
                <span className="badge badge-published">Status: {generatedLicense.status}</span>
                <span style={{ color: 'var(--text-muted)' }}>
                  Expires: {new Date(generatedLicense.expiryDate).toLocaleDateString()}
                </span>
              </div>
            </div>

            <button
              onClick={() => {
                setShowPaymentModal(false);
                setGeneratedLicense(null);
              }}
              className="btn-cyan"
              style={{ width: '100%', justifyContent: 'center', padding: '14px', fontSize: '1rem', fontWeight: 800 }}
            >
              <ShieldCheck style={{ width: '18px', height: '18px' }} />
              Go to GeM Tender Intelligence Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
