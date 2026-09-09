import React from 'react';
import { useAuth } from '../context/AuthContext';
import {
  Sparkles,
  Search,
  Radar,
  Calendar,
  SlidersHorizontal,
  FileCheck2,
  Bell,
  Bookmark,
  Download,
  BarChart3,
  ShieldCheck,
  ArrowRight,
  CheckCircle2,
  Zap,
  Check,
  Building2,
  Eye,
  Layers,
  Lock,
  ChevronRight
} from 'lucide-react';

export default function LandingPage({ onNavigate }) {
  const { user, pricing } = useAuth();

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-dark)', color: 'var(--text-main)', overflowX: 'hidden' }}>

      {/* Top Navbar */}
      <nav
        style={{
          height: '76px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 5%',
          background: 'rgba(7, 10, 18, 0.8)',
          backdropFilter: 'blur(16px)',
          position: 'sticky',
          top: 0,
          zIndex: 100
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', cursor: 'pointer' }} onClick={() => onNavigate('landing')}>
          <div
            style={{
              width: '42px',
              height: '42px',
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
            <span style={{ fontSize: '1.5rem', fontWeight: 800, color: '#fff' }} className="brand-font">
              GeM<span style={{ color: 'var(--primary-cyan)' }}>Intel</span>
            </span>
          </div>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '28px', fontSize: '0.92rem', fontWeight: 500 }}>
          <a href="#about" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>About</a>
          <a href="#features" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Features</a>
          <a href="#how-it-works" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>How It Works</a>
          <a href="#pricing" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Pricing</a>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {user ? (
            <button onClick={() => onNavigate('dashboard')} className="btn-cyan" style={{ padding: '8px 20px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Sparkles style={{ width: '15px', height: '15px' }} /> Open Dashboard
            </button>
          ) : (
            <>
              <button onClick={() => onNavigate('login')} className="btn-secondary" style={{ padding: '8px 18px' }}>
                Login
              </button>
              <button onClick={() => onNavigate('register')} className="btn-cyan" style={{ padding: '8px 20px' }}>
                Register
              </button>
            </>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section style={{ padding: '80px 5% 60px 5%', textAlign: 'center', position: 'relative' }}>
        {/* Glow backdrop */}
        <div
          style={{
            position: 'absolute',
            top: '20%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '600px',
            height: '350px',
            background: 'radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, rgba(139, 92, 246, 0.15) 50%, rgba(0,0,0,0) 80%)',
            filter: 'blur(60px)',
            pointerEvents: 'none',
            zIndex: 0
          }}
        />

        <div style={{ position: 'relative', zIndex: 1, maxWidth: '900px', margin: '0 auto' }}>
          <div
            className="badge badge-published"
            style={{ marginBottom: '20px', padding: '8px 16px', fontSize: '0.82rem', textTransform: 'none' }}
          >
            <Zap style={{ width: '14px', height: '14px', color: 'var(--primary-cyan)' }} />
            Next-Gen AI & Service Filter GeM Tender Scanner
          </div>

          <h1
            style={{
              fontSize: '3.6rem',
              fontWeight: 900,
              lineHeight: 1.15,
              color: '#fff',
              letterSpacing: '-1px',
              marginBottom: '20px'
            }}
            className="brand-font"
          >
            GeM Tender Intelligence Platform
          </h1>

          <p style={{ fontSize: '1.2rem', color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: '36px', maxWidth: '750px', margin: '0 auto 36px auto' }}>
            Discover, filter and monitor GeM tenders that match your business services — all from one intelligent dashboard.
          </p>

          <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginBottom: '50px' }}>
            {user ? (
              <button onClick={() => onNavigate('dashboard')} className="btn-primary" style={{ padding: '14px 32px', fontSize: '1.1rem' }}>
                Open Tender Dashboard <ArrowRight style={{ width: '20px', height: '20px' }} />
              </button>
            ) : (
              <>
                <button onClick={() => onNavigate('register')} className="btn-primary" style={{ padding: '14px 32px', fontSize: '1.1rem' }}>
                  Get Started <ArrowRight style={{ width: '20px', height: '20px' }} />
                </button>
                <button onClick={() => onNavigate('login')} className="btn-secondary" style={{ padding: '14px 28px', fontSize: '1.1rem' }}>
                  Login to Dashboard
                </button>
              </>
            )}
          </div>

          {/* Visual Preview / Dashboard Mockup Card */}
          <div
            className="glass-panel"
            style={{
              borderRadius: '20px',
              padding: '12px',
              boxShadow: '0 25px 80px rgba(0,0,0,0.9), 0 0 30px rgba(59, 130, 246, 0.2)',
              border: '1px solid var(--border-highlight)',
              background: '#090d16'
            }}
          >
            <div style={{ background: '#0f172a', borderRadius: '14px', overflow: 'hidden', padding: '16px', textAlign: 'left' }}>
              {/* Mock top bar */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', pb: '12px', paddingBottom: '12px' }}>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#ef4444' }} />
                  <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#f59e0b' }} />
                  <div style={{ width: '12px', height: '12px', borderRadius: '50%', background: '#10b981' }} />
                </div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                  GeMIntel Dashboard Live Preview — Active Subscription Gated
                </div>
                <span className="badge badge-active">ACTIVE LICENSE</span>
              </div>

              {/* Mock Dashboard Grid */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px', marginTop: '16px' }}>
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Published Bids</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--primary-cyan)', marginTop: '4px' }}>142 Live</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Matching Services</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--primary-purple)', marginTop: '4px' }}>48 Bids</div>
                </div>
                <div style={{ background: 'rgba(255,255,255,0.03)', padding: '14px', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Total Value Scanned</div>
                  <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-green)', marginTop: '4px' }}>₹ 14.8 Cr</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* About Us Section */}
      <section id="about" style={{ padding: '80px 5%', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1000px', margin: '0 auto', textAlign: 'center' }}>
          <div className="badge badge-published" style={{ marginBottom: '16px' }}>ABOUT US</div>
          <h2 style={{ fontSize: '2.4rem', fontWeight: 800, color: '#fff', marginBottom: '16px' }} className="brand-font">
            Smart Government e-Marketplace Intelligence
          </h2>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', lineHeight: 1.7, maxWidth: '850px', margin: '0 auto' }}>
            GeMIntel helps businesses discover relevant Government e-Marketplace tenders by scanning and filtering bids according to services, dates, departments, states and other tender parameters. Our automated subscription engine ensures you never miss a lucrative government contract.
          </p>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" style={{ padding: '80px 5%', background: 'rgba(15, 23, 42, 0.4)', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '50px' }}>
            <div className="badge badge-finished" style={{ marginBottom: '16px' }}>PLATFORM FEATURES</div>
            <h2 style={{ fontSize: '2.4rem', fontWeight: 800, color: '#fff' }} className="brand-font">
              Everything You Need To Win GeM Tenders
            </h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
            {[
              { icon: Radar, title: '🔎 Smart Tender Scanner', desc: 'Real-time tender portal scanner matching exact categories & keywords.' },
              { icon: Calendar, title: '📅 Date-Based Tender Search', desc: 'Filter published and upcoming tenders by today, 7 days, or 30 days.' },
              { icon: SlidersHorizontal, title: '🏢 Service-Based Filtering', desc: 'Categorize bids by IT, Manpower, Security, Solar, Catering & custom tags.' },
              { icon: FileCheck2, title: '📊 Published & Finished Bids', desc: 'Track active open tenders alongside closed evaluation benchmarks.' },
              { icon: Bell, title: '🔔 Tender Status Monitoring', desc: 'Live status badges and countdown clocks on submission deadlines.' },
              { icon: Bookmark, title: '💾 Save Important Tenders', desc: 'Bookmark priority bids into your personal saved library for team review.' },
              { icon: Download, title: '📥 Export Tender Data', desc: 'Export formatted tender listings directly into CSV, Excel or PDF specs.' },
              { icon: BarChart3, title: '📈 Tender Analytics', desc: 'Visual distribution charts of estimated bid values and top ministries.' },
              { icon: ShieldCheck, title: '🔐 Secure User Accounts', desc: 'Encrypted passwords with cryptographic license key verification.' }
            ].map((feat, idx) => {
              const Icon = feat.icon;
              return (
                <div key={idx} className="glass-card" style={{ padding: '24px' }}>
                  <div
                    style={{
                      width: '48px',
                      height: '48px',
                      borderRadius: '12px',
                      background: 'rgba(6, 182, 212, 0.12)',
                      border: '1px solid rgba(6, 182, 212, 0.3)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      marginBottom: '16px'
                    }}
                  >
                    <Icon style={{ width: '24px', height: '24px', color: 'var(--primary-cyan)' }} />
                  </div>
                  <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fff', marginBottom: '8px' }}>{feat.title}</h3>
                  <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>{feat.desc}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" style={{ padding: '80px 5%', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '50px' }}>
            <div className="badge badge-active" style={{ marginBottom: '16px' }}>STEP-BY-STEP PROCESS</div>
            <h2 style={{ fontSize: '2.4rem', fontWeight: 800, color: '#fff' }} className="brand-font">How It Works</h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))', gap: '16px', textOverflow: 'ellipsis' }}>
            {[
              '1. Create Account',
              '2. Select Subscription',
              '3. Make Payment',
              '4. Get License Key',
              '5. Select Services',
              '6. Scan GeM Tenders',
              '7. View Matching Bids'
            ].map((step, idx) => (
              <div
                key={idx}
                className="glass-panel"
                style={{
                  padding: '20px 12px',
                  textAlign: 'center',
                  background: 'linear-gradient(135deg, rgba(30,41,59,0.5), rgba(15,23,42,0.7))'
                }}
              >
                <div style={{ fontSize: '1.8rem', fontWeight: 900, color: 'var(--primary-cyan)', marginBottom: '6px' }}>
                  0{idx + 1}
                </div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, color: '#fff' }}>{step.replace(/^\d+\.\s*/, '')}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" style={{ padding: '80px 5%', background: 'rgba(15, 23, 42, 0.5)', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '50px' }}>
            <div className="badge badge-published" style={{ marginBottom: '16px' }}>SUBSCRIPTION PLANS</div>
            <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: '#fff' }} className="brand-font">
              Flexible & Transparent Pricing
            </h2>
            <p style={{ color: 'var(--text-muted)', marginTop: '8px' }}>
              Choose a plan that fits your business needs. Fully configurable from the Admin Panel.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '28px' }}>
            {/* Monthly Plan */}
            <div className="glass-card" style={{ padding: '32px', borderRadius: '16px' }}>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-muted)' }}>Monthly Plan</div>
              <div style={{ fontSize: '2.5rem', fontWeight: 900, color: '#fff', margin: '12px 0' }}>
                {pricing.symbol}{pricing.monthly} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ month</span>
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: '24px 0', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.92rem' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Tender scanning engine</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Service & category filtering</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Date-based filtering</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Full Dashboard access</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Save tenders library</li>
              </ul>
              <button onClick={() => onNavigate('register')} className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                Choose Monthly
              </button>
            </div>

            {/* Quarterly Plan */}
            <div
              className="glass-card"
              style={{
                padding: '32px',
                borderRadius: '16px',
                border: '2px solid var(--primary-cyan)',
                position: 'relative',
                boxShadow: 'var(--glow-cyan)'
              }}
            >
              <span
                style={{
                  position: 'absolute',
                  top: '-12px',
                  right: '24px',
                  background: 'linear-gradient(135deg, var(--primary-cyan), var(--primary-blue))',
                  color: '#fff',
                  fontSize: '0.75rem',
                  fontWeight: 800,
                  padding: '4px 12px',
                  borderRadius: '12px'
                }}
              >
                POPULAR
              </span>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--primary-cyan)' }}>Quarterly Plan</div>
              <div style={{ fontSize: '2.5rem', fontWeight: 900, color: '#fff', margin: '12px 0' }}>
                {pricing.symbol}{pricing.quarterly} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ 3 months</span>
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: '24px 0', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.92rem' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> All Monthly Plan features</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> PDF & Excel Spec exports</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Priority tender updates</li>
              </ul>
              <button onClick={() => onNavigate('register')} className="btn-cyan" style={{ width: '100%', justifyContent: 'center' }}>
                Choose Quarterly
              </button>
            </div>

            {/* Yearly Plan */}
            <div className="glass-card" style={{ padding: '32px', borderRadius: '16px' }}>
              <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--primary-purple)' }}>Yearly Plan</div>
              <div style={{ fontSize: '2.5rem', fontWeight: 900, color: '#fff', margin: '12px 0' }}>
                {pricing.symbol}{pricing.yearly} <span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontWeight: 400 }}>/ year</span>
              </div>
              <ul style={{ listStyle: 'none', padding: 0, margin: '24px 0', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '0.92rem' }}>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Everything included</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Unlimited tender scans</li>
                <li style={{ display: 'flex', alignItems: 'center', gap: '10px' }}><Check style={{ width: '18px', color: 'var(--accent-green)' }} /> Dedicated support & license key</li>
              </ul>
              <button onClick={() => onNavigate('register')} className="btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                Choose Yearly
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ padding: '40px 5%', borderTop: '1px solid var(--border-color)', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
        <p>© 2026 GeMIntel – Smart GeM Tender Intelligence Platform. All rights reserved.</p>
      </footer>

    </div>
  );
}
