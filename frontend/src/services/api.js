// api.js - Centralized API calls for CompanyGraph frontend
// This file provides functions to interact with the backend endpoints for company graph data.


const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:8000';

/**
 * Fetch company graph data from the backend.
 * @param {Object} params - The search parameters (mode, model, company, etc.)
 * @returns {Promise<Object>} - The API response
 */

export async function fetchCompanyGraph(params) {
  let endpoint;
  switch (params.mode) {
    case 'wikidata':
      endpoint = `/api/wikidata/${encodeURIComponent(params.company)}`;
      break;
    case 'foundry-local':
      endpoint = `/api/foundry-local/${encodeURIComponent(params.model)}/${encodeURIComponent(params.company)}`;
      break;
    case 'azure-open-ai':
      endpoint = `/api/azure-open-ai/${encodeURIComponent(params.model)}/${encodeURIComponent(params.company)}`;
      break;
    case 'chat-completion-agent':
      endpoint = `/api/chat-completion-agent/${encodeURIComponent(params.model)}/${encodeURIComponent(params.company)}`;
      break;
    case 'semantic-kernel-agent':
      endpoint = `/api/semantic-kernel-agent/${encodeURIComponent(params.model)}/${encodeURIComponent(params.company)}`;
      break;
    default:
      throw new Error(`Unknown mode: ${params.mode}`);
  }
  // 60 seconds timeout (60000 ms)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 60000);
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      signal: controller.signal,
    });
    clearTimeout(timeoutId);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return response.json();
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Request timed out after 60 seconds.');
    }
    throw err;
  }
}

/**
 * (Optional) Fetch available models for a given mode from the backend.
 * @param {string} mode
 * @returns {Promise<string[]>}
 */
export async function fetchModelsForMode(mode) {
  const response = await fetch(`${API_BASE}/api/models?mode=${encodeURIComponent(mode)}`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
