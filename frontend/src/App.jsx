import React, { useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import PaymentModal from './components/PaymentModal';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import ScanBidsPage from './pages/ScanBidsPage';
import AnalyticsPage from './pages/AnalyticsPage';
import BillingPage from './pages/BillingPage';
import AdminPage from './pages/AdminPage';

function MainAppContent() {
  const { user, loading } = useAuth();

  // Page state: landing | login | register | app
  const [page, setPage] = useState('landing');
  // App internal tab: dashboard | scanner | admin-dashboard | admin-users | admin-keys | admin-payments | admin-subscriptions | admin-services | admin-tenders | admin-settings
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');

  if (loading) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#070a12', color: '#38bdf8', fontWeight: 600 }}>
        Loading GeMIntel System...
      </div>
    );
  }

  // Handle page transitions
  const handleNavigate = (targetPage) => {
    if (targetPage === 'dashboard' || targetPage === 'app') {
      if (!user) {
        setPage('login');
        return;
      }
    }
    setPage(targetPage);
  };

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
      <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />

      <div className="main-content">
        <Header
          currentTab={currentTab}
          setCurrentTab={setCurrentTab}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
        />

        <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflowY: 'auto' }}>
          {isAdminTab ? (
            <AdminPage currentTab={currentTab} />
          ) : currentTab === 'scanner' ? (
            <ScanBidsPage searchQuery={searchQuery} />
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
