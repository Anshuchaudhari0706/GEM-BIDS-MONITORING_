import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import PaymentModal from './components/PaymentModal';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import AnalyticsPage from './pages/AnalyticsPage';
import BillingPage from './pages/BillingPage';
import AdminPage from './pages/AdminPage';

const VALID_TABS = [
  'dashboard', 'scanner', 'analytics', 'billing',
  'admin-dashboard', 'admin-users', 'admin-keys', 'admin-payments',
  'admin-subscriptions', 'admin-services', 'admin-tenders', 'admin-settings', 'admin'
];

function MainAppContent() {
  const { user, token, loading } = useAuth();

  // Determine initial tab from URL hash or localStorage
  const getInitialTab = () => {
    const rawHash = (window.location.hash || '').replace('#/', '').replace('#', '').trim();
    if (VALID_TABS.includes(rawHash)) {
      return rawHash;
    }
    const saved = localStorage.getItem('gemintel_current_tab');
    if (saved && VALID_TABS.includes(saved)) {
      return saved;
    }
    return 'dashboard';
  };

  // Determine initial page from URL hash, auth token, or localStorage
  const getInitialPage = () => {
    const rawHash = (window.location.hash || '').replace('#/', '').replace('#', '').trim();
    const savedToken = localStorage.getItem('gemintel_token');

    if (rawHash === 'login') return 'login';
    if (rawHash === 'register') return 'register';
    if (rawHash === 'landing') return 'landing';

    if (VALID_TABS.includes(rawHash)) {
      return savedToken ? 'dashboard' : 'login';
    }

    if (savedToken) {
      const savedPage = localStorage.getItem('gemintel_current_page');
      return (savedPage === 'login' || savedPage === 'register') ? 'dashboard' : (savedPage || 'dashboard');
    }

    return 'landing';
  };

  const [page, setPage] = useState(getInitialPage);
  const [currentTab, setCurrentTab] = useState(getInitialTab);
  const [searchQuery, setSearchQuery] = useState('');

  // Synchronize hash and localStorage when currentTab changes in dashboard view
  const handleSelectTab = (tabId) => {
    setCurrentTab(tabId);
    localStorage.setItem('gemintel_current_tab', tabId);
    if (page === 'dashboard' || page === 'app') {
      window.location.hash = '#' + tabId;
    }
  };

  // Handle page transitions
  const handleNavigate = (targetPage, tabName) => {
    const savedToken = localStorage.getItem('gemintel_token');

    if (targetPage === 'dashboard' || targetPage === 'app') {
      setPage('dashboard');
      localStorage.setItem('gemintel_current_page', 'dashboard');
      const targetTab = tabName || currentTab || 'dashboard';
      setCurrentTab(targetTab);
      localStorage.setItem('gemintel_current_tab', targetTab);
      window.location.hash = '#' + targetTab;
      return;
    }

    if (targetPage === 'login') {
      setPage('login');
      localStorage.setItem('gemintel_current_page', 'login');
      window.location.hash = '#login';
      return;
    }

    if (targetPage === 'register') {
      setPage('register');
      localStorage.setItem('gemintel_current_page', 'register');
      window.location.hash = '#register';
      return;
    }

    if (targetPage === 'landing') {
      setPage('landing');
      localStorage.setItem('gemintel_current_page', 'landing');
      window.location.hash = '#landing';
      return;
    }

    setPage(targetPage);
    localStorage.setItem('gemintel_current_page', targetPage);
  };

  // Listen to browser hash changes (Back/Forward buttons & manual URL changes)
  useEffect(() => {
    const handleHashChange = () => {
      const rawHash = (window.location.hash || '').replace('#/', '').replace('#', '').trim();
      const savedToken = localStorage.getItem('gemintel_token');

      if (rawHash === 'login') {
        setPage('login');
      } else if (rawHash === 'register') {
        setPage('register');
      } else if (rawHash === 'landing' || rawHash === '') {
        setPage('landing');
      } else if (VALID_TABS.includes(rawHash)) {
        if (savedToken || user || token) {
          setPage('dashboard');
          setCurrentTab(rawHash);
          localStorage.setItem('gemintel_current_tab', rawHash);
        } else {
          setPage('landing');
          window.location.hash = '#landing';
        }
      } else {
        setPage('landing');
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [user, token]);

  // When user logs out (no token & no user), immediately redirect to landing page
  useEffect(() => {
    const savedToken = localStorage.getItem('gemintel_token');
    if (!token && !user && !savedToken) {
      if (page === 'dashboard' || page === 'app') {
        setPage('landing');
        localStorage.setItem('gemintel_current_page', 'landing');
        window.location.hash = '#landing';
      }
    }
  }, [token, user, page]);

  // When user logs in, if they are on login/register/landing, auto-open dashboard
  useEffect(() => {
    if (user && (page === 'login' || page === 'register')) {
      setPage('dashboard');
      localStorage.setItem('gemintel_current_page', 'dashboard');
      window.location.hash = '#' + currentTab;
    }
  }, [user]);

  // Synchronize URL hash when on dashboard
  useEffect(() => {
    if (page === 'dashboard' || page === 'app') {
      const rawHash = (window.location.hash || '').replace('#/', '').replace('#', '').trim();
      if (!VALID_TABS.includes(rawHash)) {
        window.location.hash = '#' + currentTab;
      }
      localStorage.setItem('gemintel_current_page', 'dashboard');
      localStorage.setItem('gemintel_current_tab', currentTab);
    }
  }, [page, currentTab]);

  if (loading) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#070a12', color: '#38bdf8', fontWeight: 600 }}>
        Loading GeMIntel System...
      </div>
    );
  }

  if (page === 'landing') {
    return <LandingPage onNavigate={handleNavigate} />;
  }

  if (page === 'login') {
    return <LoginPage onNavigate={handleNavigate} />;
  }

  if (page === 'register') {
    return <RegisterPage onNavigate={handleNavigate} />;
  }

  const isAdminTab = currentTab.startsWith('admin-') || currentTab === 'admin';

  return (
    <div className="app-container">
      <Sidebar currentTab={currentTab} setCurrentTab={handleSelectTab} />

      <div className="main-content">
        <Header
          currentTab={currentTab}
          setCurrentTab={handleSelectTab}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />

        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
          {isAdminTab ? (
            <AdminPage currentTab={currentTab} />
          ) : currentTab === 'analytics' ? (
            <AnalyticsPage />
          ) : currentTab === 'billing' ? (
            <BillingPage />
          ) : (
            <DashboardPage
              currentTab={currentTab}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
            />
          )}
        </main>
      </div>

      <PaymentModal />
    </div>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <MainAppContent />
    </AuthProvider>
  );
}
