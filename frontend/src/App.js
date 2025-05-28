import React, { useState, useEffect } from 'react';
import './App.css';
import SearchForm from './components/SearchForm';
import CompanyGraph from './components/CompanyGraph';
import { fetchCompanyGraph } from './services/api';
import { allModelOptions } from './constants';

function App() {
  const [query, setQuery] = useState('Microsoft');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [model, setModel] = useState('phi-3-mini-4k');
  // Default to foundry-local for backward compatibility
  const [searchMode, setSearchMode] = useState('foundry-local');
  const [graphData, setGraphData] = useState(null);



  // Filter model options based on selected search mode
  const filteredModelOptions = allModelOptions.filter(opt =>
    opt.modes.includes(searchMode)
  );

  // Utility: Build vis-network data for LLM/agent/wikidata results
  const buildGraph = (companyLabel, companies) => {
    if (!companies || companies.length === 0) return { nodes: [], edges: [] };
    let companyNode = companies.find(b => b.type && b.type.toLowerCase() === 'company')
      || companies.find(b => b.name.toLowerCase() === companyLabel.toLowerCase())
      || companies[0];
    const companyId = 'company';
    const nodeMap = new Map();
    let nodeIdx = 0;
    companies.forEach((b) => {
      if (b === companyNode) {
        nodeMap.set(b, companyId);
      } else {
        nodeMap.set(b, `node-${nodeIdx++}`);
      }
    });
    const nodes = companies.map((b) => ({
      id: nodeMap.get(b),
      label: b.name,
      shape: b.logo ? 'circularImage' : 'ellipse',
      image: b.logo || undefined,
      size: 60,
      font: { size: 18, vadjust: 50 },
    }));
    const edges = companies
      .filter(b => b !== companyNode)
      .map((b) => {
        if (b.type && b.type.toLowerCase() === 'parent') {
          return { from: nodeMap.get(b), to: companyId, label: 'parent' };
        } else {
          return { from: companyId, to: nodeMap.get(b), label: b.type || '' };
        }
      });
    return { nodes, edges };
  };

  // Build vis-network data for LLM-only mode


  // Render the graph


  // Handle search using centralized API service
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const params = {
        mode: searchMode,
        model,
        company: query.trim(),
      };
      const data = await fetchCompanyGraph(params);
      let companies = data.result || data.selectedBrands || [];
      // Defensive: if it's a string, try to parse as JSON
      if (typeof companies === 'string') {
        try {
          companies = JSON.parse(companies);
        } catch {
          companies = companies.split(',').map(b => ({ name: b.trim(), type: 'company' }));
        }
      }
      if (Array.isArray(companies) && typeof companies[0] === 'string') {
        companies = companies.map(b => ({ name: b, type: 'company' }));
      }
      if (!Array.isArray(companies)) companies = [];
      setGraphData(buildGraph(query.trim(), companies));
    } catch (err) {
      setError('Could not reach backend. ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Initial render for default company
  useEffect(() => {
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const params = {
          mode: searchMode,
          model,
          company: query.trim(),
        };
        const data = await fetchCompanyGraph(params);
        let companies = data.result || data.selectedBrands || [];
        if (typeof companies === 'string') {
          try {
            companies = JSON.parse(companies);
          } catch {
            companies = companies.split(',').map(b => ({ name: b.trim(), type: 'company' }));
          }
        }
        if (Array.isArray(companies) && typeof companies[0] === 'string') {
          companies = companies.map(b => ({ name: b, type: 'company' }));
        }
        if (!Array.isArray(companies)) companies = [];
        setGraphData(buildGraph(query.trim(), companies));
      } catch (err) {
        setError('Could not reach backend. ' + err.message);
      } finally {
        setLoading(false);
      }
    })();
    // eslint-disable-next-line
  }, []);

    // Automatically update model when searchMode changes to ensure a valid model is selected
  useEffect(() => {
    if (
      filteredModelOptions.length > 0 &&
      !filteredModelOptions.some(opt => opt.value === model)
    ) {
      setModel(filteredModelOptions[0].value);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchMode, filteredModelOptions]);

  return (
    <div className="App" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <h2>Company Relationships Graph</h2>
      <SearchForm
        query={query}
        setQuery={setQuery}
        searchMode={searchMode}
        setSearchMode={setSearchMode}
        model={model}
        setModel={setModel}
        filteredModelOptions={filteredModelOptions}
        onSubmit={handleSearch}
        loading={loading}
      />
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <CompanyGraph graphData={graphData} setError={setError} />
    </div>
  );
}

export default App;
