import React, { useState, useEffect } from 'react';
import Container from '@mui/material/Container';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Alert from '@mui/material/Alert';
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import './App.css';
import SearchForm from './components/SearchForm';
import CompanyGraph from './components/CompanyGraph';
import { fetchCompanyGraph } from './services/api';
import { ALL_MODEL_OPTIONS, SEARCH_MODE_DESCRIPTIONS, MODEL_DESCRIPTIONS } from './constants';

function App() {
  const [query, setQuery] = useState('Microsoft');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [model, setModel] = useState('phi-3-mini-4k');
  const [searchMode, setSearchMode] = useState('foundry-local');
  const [graphData, setGraphData] = useState(null);

  // Filter model options based on selected search mode
  const filteredModelOptions = ALL_MODEL_OPTIONS.filter(opt =>
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

  // Show a short description for the selected search mode
  const selectedModeDescription = SEARCH_MODE_DESCRIPTIONS[searchMode] || '';

  // Show a short description for the selected model
  const selectedModelDescription = MODEL_DESCRIPTIONS[model] || '';

  return (
    <Container maxWidth="xl" disableGutters sx={{ minHeight: '100vh', height: '100vh', display: 'flex', flexDirection: 'column', py: 2 }}>
      <Paper elevation={3} sx={{ p: 3, mb: 3, maxWidth: 900, mx: 'auto', width: '100%' }}>
        <Typography variant="h4" component="h1" gutterBottom align="center">
          Company Relationships Graph
        </Typography>
        <Typography variant="body1" align="center" sx={{ mb: 2, color: '#333' }}>
          Enter a company name to visualize its brands, subsidiaries, and parent relationships as an interactive graph.
        </Typography>
      </Paper>
      <Paper elevation={3} sx={{ p: 3, mb: 3, maxWidth: 900, mx: 'auto', width: '100%' }}>
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
        <Typography variant="body2" sx={{ mb: 1, minHeight: 24, color: '#444', fontStyle: 'italic' }}>
          {selectedModeDescription}
          {filteredModelOptions.some(opt => opt.value === model) && selectedModelDescription && (
            <><br />{selectedModelDescription}</>
          )}
        </Typography>
        {loading && (
          <div style={{ display: 'flex', justifyContent: 'center', margin: '16px 0' }}>
            <CircularProgress />
          </div>
        )}
        {error && <Alert severity="error" sx={{ my: 2 }}>{error}</Alert>}
      </Paper>
      <Box sx={{ flex: 1, minHeight: 0, display: 'flex', flexDirection: 'column', pb: 2, height: '100%' }}>
        <Paper elevation={1} sx={{ p: 2, flex: 1, minHeight: 0, height: '100%', display: 'flex', flexDirection: 'column' }}>
          <CompanyGraph graphData={graphData} setError={setError} />
        </Paper>
      </Box>
    </Container>
  );
}

export default App;
