const API_BASE = '/api';

async function safeJsonFetch(url, options = {}) {
  try {
    const res = await fetch(url, options);
    const text = await res.text();
    let data;
    try {
      data = text ? JSON.parse(text) : {};
    } catch (e) {
      throw new Error(`Server returned non-JSON response (${res.status}). Please verify backend server.`);
    }
    return { ok: res.ok, status: res.status, data };
  } catch (err) {
    if (err.message.includes('Server returned') || err.message.includes('failed')) throw err;
    throw new Error('Backend Server Unavailable (Port 5000). Please ensure Node server is running.');
  }
}

export async function fetchPricingConfig() {
  const { data } = await safeJsonFetch(`${API_BASE}/config/pricing`);
  return data;
}

export async function fetchSourceHealth() {
  const { data } = await safeJsonFetch(`${API_BASE}/source-health`);
  return data;
}

export async function loginUser(email, password) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!ok) throw new Error(data.error || 'Login failed');
  return data;
}

export async function registerUser(userData) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  if (!ok) throw new Error(data.error || 'Registration failed');
  return data;
}

export async function fetchCurrentUser(token) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!ok) throw new Error(data.error || 'Failed to fetch user profile');
  return data;
}

export async function createPaymentOrder(token, plan) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/payment/create-order`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ plan })
  });
  if (!ok) throw new Error(data.error || 'Failed to create payment order');
  return data;
}

export async function verifyPaymentAndGenerateKey(token, paymentDetails) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/payment/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(paymentDetails)
  });
  if (!ok) throw new Error(data.error || 'Payment verification failed');
  return data;
}

export async function activateLicenseKey(token, key) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/license/activate-key`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ key })
  });
  if (!ok) throw new Error(data.error || 'Key activation failed');
  return data;
}

export async function fetchTenders(token, filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const { ok, data } = await safeJsonFetch(`${API_BASE}/tenders?${query}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!ok) {
    const errorObj = new Error(data.error || 'Failed to fetch tenders');
    errorObj.code = data.code;
    throw errorObj;
  }
  return data;
}

export async function triggerGeMScan(token, scanParams) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/tenders/scan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(scanParams)
  });
  if (!ok) throw new Error(data.error || 'Failed to execute GeM Portal Scan');
  return data;
}

export async function parseTenderDocument(token, tenderId) {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/tenders/${encodeURIComponent(tenderId)}/parse-document`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` }
  });
  if (!ok) throw new Error(data.error || 'Failed to parse tender document');
  return data;
}

export async function fetchServices() {
  const { ok, data } = await safeJsonFetch(`${API_BASE}/services`);
  if (!ok) throw new Error(data.error || 'Failed to fetch services');
  return data;
}
