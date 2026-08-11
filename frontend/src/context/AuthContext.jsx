import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  fetchCurrentUser,
  loginUser as apiLogin,
  registerUser as apiRegister,
  verifyPaymentAndGenerateKey,
  activateLicenseKey as apiActivateKey,
  fetchPricingConfig
} from '../services/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('gemintel_token') || null);
  const [user, setUser] = useState(null);
  const [license, setLicense] = useState(null);
  const [pricing, setPricing] = useState({ monthly: 1499, quarterly: 3999, yearly: 11999, symbol: '₹' });
  const [loading, setLoading] = useState(true);

  // Saved tenders state persisted in localStorage
  const [savedTenders, setSavedTenders] = useState(() => {
    const saved = localStorage.getItem('gemintel_saved_tenders');
    return saved ? JSON.parse(saved) : [];
  });

  const [toast, setToast] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [selectedPlanForPayment, setSelectedPlanForPayment] = useState('monthly');

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  useEffect(() => {
    localStorage.setItem('gemintel_saved_tenders', JSON.stringify(savedTenders));
  }, [savedTenders]);

  const toggleSaveTender = (tender) => {
    setSavedTenders(prev => {
      const exists = prev.some(t => t.id === tender.id);
      if (exists) {
        showToast(`Tender ${tender.id} removed from saved list`, 'info');
        return prev.filter(t => t.id !== tender.id);
      } else {
        showToast(`Tender ${tender.id} saved successfully!`, 'success');
        return [...prev, tender];
      }
    });
  };

  const loadPricing = async () => {
    try {
      const data = await fetchPricingConfig();
      if (data.pricing) setPricing(data.pricing);
    } catch (e) {
      console.error('Failed to load pricing:', e);
    }
  };

  const loadUser = async (authToken) => {
    if (!authToken) {
      setUser(null);
      setLicense(null);
      setLoading(false);
      return;
    }
    try {
      const data = await fetchCurrentUser(authToken);
      setUser(data.user);
      setLicense(data.license);
    } catch (err) {
      console.error('Auth load error:', err);
      logout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPricing();
    if (token) {
      loadUser(token);
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (email, password) => {
    setLoading(true);
    try {
      const data = await apiLogin(email, password);
      localStorage.setItem('gemintel_token', data.token);
      setToken(data.token);
      setUser(data.user);
      setLicense(data.license);
      showToast(`Welcome back, ${data.user.fullName}!`, 'success');
      return data;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const register = async (formData, plan) => {
    setLoading(true);
    try {
      const data = await apiRegister(formData);
      localStorage.setItem('gemintel_token', data.token);
      setToken(data.token);
      setUser(data.user);
      setSelectedPlanForPayment(plan || 'monthly');
      setShowPaymentModal(true);
      showToast('Registration successful! Complete payment to activate your license.', 'success');
      return data;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSuccess = async (paymentDetails) => {
    try {
      const data = await verifyPaymentAndGenerateKey(token, paymentDetails);
      setLicense(data.license);
      setShowPaymentModal(false);
      showToast(`Payment Successful! License Key ${data.license.key} Activated!`, 'success');
      return data;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    }
  };

  const activateKey = async (keyString) => {
    try {
      const data = await apiActivateKey(token, keyString);
      setLicense(data.license);
      showToast('License Key successfully activated!', 'success');
      return data;
    } catch (err) {
      showToast(err.message, 'error');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('gemintel_token');
    setToken(null);
    setUser(null);
    setLicense(null);
    showToast('Logged out safely', 'info');
  };

  const isLicenseActive = () => {
    if (!license) return false;
    if (license.status !== 'ACTIVE') return false;
    const exp = new Date(license.expiryDate);
    return exp > new Date();
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        license,
        pricing,
        loading,
        savedTenders,
        toggleSaveTender,
        showPaymentModal,
        setShowPaymentModal,
        selectedPlanForPayment,
        setSelectedPlanForPayment,
        login,
        register,
        logout,
        handlePaymentSuccess,
        activateKey,
        isLicenseActive,
        showToast,
        refreshUser: () => loadUser(token),
        refreshPricing: loadPricing
      }}
    >
      {children}
      {toast && (
        <div
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            zIndex: 9999,
            padding: '12px 20px',
            borderRadius: '8px',
            background: toast.type === 'error' ? '#ef4444' : toast.type === 'success' ? '#10b981' : '#3b82f6',
            color: '#fff',
            fontWeight: 600,
            boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            animation: 'fadeIn 0.3s ease-in-out'
          }}
        >
          {toast.message}
        </div>
      )}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
