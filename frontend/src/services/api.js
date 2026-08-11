const API_BASE = '/api';

export async function fetchPricingConfig() {
  const res = await fetch(`${API_BASE}/config/pricing`);
  return res.json();
}

export async function loginUser(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Login failed');
  return data;
}

export async function registerUser(userData) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Registration failed');
  return data;
}

export async function fetchCurrentUser(token) {
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to fetch user profile');
  return data;
}

export async function createPaymentOrder(token, plan) {
  const res = await fetch(`${API_BASE}/payment/create-order`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ plan })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to create payment order');
  return data;
}

export async function verifyPaymentAndGenerateKey(token, paymentDetails) {
  const res = await fetch(`${API_BASE}/payment/verify`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(paymentDetails)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Payment verification failed');
  return data;
}

export async function activateLicenseKey(token, key) {
  const res = await fetch(`${API_BASE}/license/activate-key`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ key })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Key activation failed');
  return data;
}

export async function fetchTenders(token, filters = {}) {
  const query = new URLSearchParams(filters).toString();
  const res = await fetch(`${API_BASE}/tenders?${query}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  if (!res.ok) {
    const errorObj = new Error(data.error || 'Failed to fetch tenders');
    errorObj.code = data.code;
    throw errorObj;
  }
  return data;
}

export async function triggerGeMScan(token, scanParams) {
  const res = await fetch(`${API_BASE}/tenders/scan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(scanParams)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'GeM Scan failed');
  return data;
}

// Admin APIs
export async function fetchAdminUsers(token) {
  const res = await fetch(`${API_BASE}/admin/users`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Admin fetch failed');
  return data;
}

export async function adminGenerateKey(token, params) {
  const res = await fetch(`${API_BASE}/admin/generate-key`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(params)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Admin key generation failed');
  return data;
}

export async function fetchServices() {
  const res = await fetch(`${API_BASE}/services`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to fetch services');
  return data;
}

export async function addAdminService(token, name) {
  const res = await fetch(`${API_BASE}/admin/services`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ name })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to add service');
  return data;
}

export async function deleteAdminService(token, name) {
  const res = await fetch(`${API_BASE}/admin/services/${encodeURIComponent(name)}`, {
    method: 'DELETE',
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to delete service');
  return data;
}

export async function updateAdminPricing(token, prices) {
  const res = await fetch(`${API_BASE}/admin/pricing`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(prices)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to update pricing');
  return data;
}

export async function updateLicenseStatus(token, licenseId, payload) {
  const res = await fetch(`${API_BASE}/admin/license/${licenseId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify(payload)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to update license');
  return data;
}

export async function parseTenderDocument(token, tenderId) {
  const res = await fetch(`${API_BASE}/documents/parse`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ tender_id: tenderId })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to parse tender document');
  return data;
}

export async function fetchRegexRules(token) {
  const res = await fetch(`${API_BASE}/admin/regex-rules`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to fetch regex rules');
  return data;
}
