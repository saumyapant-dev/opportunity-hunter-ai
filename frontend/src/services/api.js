/**
 * API client service for Opportunity Hunter backend.
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(url, config);
    if (!res.ok) {
      let errorDetail = `HTTP Error ${res.status}`;
      try {
        const errJson = await res.json();
        errorDetail = errJson.detail || errJson.message || errorDetail;
      } catch (e) {
        // Fallback to text
        errorDetail = await res.text();
      }
      throw new Error(errorDetail);
    }
    if (res.status === 204) return null;
    return await res.json();
  } catch (err) {
    console.error(`API request failed [${url}]:`, err);
    throw err;
  }
}

export const api = {
  // Health & System Status
  getHealth: () => request('/health'),
  getWorkflowStatus: () => request('/api/workflows/status'),
  getDashboardStats: () => request('/api/dashboard/stats'),

  // Research Runner
  triggerResearch: (payload, useN8n = null) => {
    let url = '/api/research';
    if (useN8n !== null) {
      url += `?use_n8n=${useN8n}`;
    }
    return request(url, {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  getResearchRun: (runId) => request(`/api/research/${runId}`),

  // Opportunities Catalog
  getOpportunities: (params = {}) => {
    const query = new URLSearchParams();
    if (params.type) query.append('type', params.type);
    if (params.status) query.append('status', params.status);
    if (params.search) query.append('search', params.search);
    if (params.remote_only !== undefined && params.remote_only !== null) {
      query.append('remote_only', params.remote_only);
    }
    if (params.limit) query.append('limit', params.limit);
    if (params.offset) query.append('offset', params.offset);

    const queryString = query.toString();
    return request(`/api/opportunities${queryString ? `?${queryString}` : ''}`);
  },
  getOpportunity: (id) => request(`/api/opportunities/${id}`),
  updateOpportunity: (id, updates) =>
    request(`/api/opportunities/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(updates),
    }),
  deleteOpportunity: (id) =>
    request(`/api/opportunities/${id}`, {
      method: 'DELETE',
    }),

  // User Preferences
  getPreferences: () => request('/api/preferences'),
  updatePreferences: (preferences) =>
    request('/api/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences),
    }),
};
