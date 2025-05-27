
import React, { useState, useRef, useEffect } from 'react';
import { Network } from 'vis-network/standalone';
import './App.css';



function App() {
  const [query, setQuery] = useState('Microsoft');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [model, setModel] = useState('phi-3-mini-4k'); // Default model
  const [searchMode, setSearchMode] = useState('llm'); // 'llm', 'wikidata', 'hybrid'
  const networkRef = useRef(null);
  const visNetwork = useRef(null);

  const modelOptions = [
    { value: 'phi-3-mini-4k', label: 'Foundry Local Phi 3 Mini 4k' },
    { value: 'deepseek-r1-7b', label: 'Foundry Local Deepseek R1 7b' },
    { value: 'model-router', label: 'Azure OpenAI Model Router' },
    { value: 'gpt-4.1', label: 'Azure OpenAI GPT-4.1' },
    // Add more as needed
  ];

  // Shared fetch function for all endpoints
  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8081';

  const fetchBrandsFromEndpoint = async (endpoint, company, model, extraBody = {}, resultField = 'selectedBrands') => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${backendUrl}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company, model, ...extraBody }),
      });
      if (!response.ok) {
        setError(`Backend error: ${response.status} ${response.statusText}`);
        return null;
      }
      const data = await response.json();
      if (data.error) {
        setError('Backend error: ' + data.error);
        return null;
      }
      let brands = data[resultField] || data.result;
      // Defensive: if it's a string, try to parse as JSON
      if (typeof brands === 'string') {
        try {
          brands = JSON.parse(brands);
        } catch {
          // fallback: comma-separated string
          brands = brands.split(',').map(b => ({ name: b.trim(), type: 'brand' }));
        }
      }
      // If it's an array of strings, convert to array of objects
      if (Array.isArray(brands) && typeof brands[0] === 'string') {
        brands = brands.map(b => ({ name: b, type: 'brand' }));
      }
      // If it's not an array, fallback to empty
      if (!Array.isArray(brands)) brands = [];
      return brands;
    } catch (err) {
      setError('Could not reach backend. Is the backend server running?\n' + err.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Build vis-network data for LLM-only mode
  const buildLlmGraph = (companyLabel, brands) => {
    if (!brands || brands.length === 0) return { nodes: [], edges: [] };

    // Find the main company node (type: 'company'), fallback to matching label, then first element
    let companyNode = brands.find(b => b.type && b.type.toLowerCase() === 'company')
      || brands.find(b => b.name.toLowerCase() === companyLabel.toLowerCase())
      || brands[0];
    const companyId = 'company';

    // Assign unique IDs to all nodes
    const nodeMap = new Map();
    let nodeIdx = 0;
    brands.forEach((b) => {
      if (b === companyNode) {
        nodeMap.set(b, companyId);
      } else {
        nodeMap.set(b, `node-${nodeIdx++}`);
      }
    });

    // Build nodes, using logo if available
    const nodes = brands.map((b) => ({
      id: nodeMap.get(b),
      label: b.name,
      shape: b.logo ? 'circularImage' : 'ellipse',
      image: b.logo || undefined,
      size: 60,
      font: { size: 18, vadjust: 50 },
    }));

    // Build edges: subsidiaries/brands from company to node, parent from node to company
    const edges = brands
      .filter(b => b !== companyNode)
      .map((b) => {
        if (b.type && b.type.toLowerCase() === 'parent') {
          // Parent: edge from parent to company
          return {
            from: nodeMap.get(b),
            to: companyId,
            label: 'parent',
          };
        } else {
          // Subsidiary/brand: edge from company to node
          return {
            from: companyId,
            to: nodeMap.get(b),
            label: b.type || '',
          };
        }
      });

    return { nodes, edges };
  };

  // Render the graph
  const renderGraph = (graphData) => {
    if (!networkRef.current) return;
    if (visNetwork.current) {
      visNetwork.current.destroy();
    }
    // Defensive: vis-network may not be loaded if not installed
    if (typeof Network !== 'function') {
      setError('vis-network is not available. Please run: npm install vis-network');
      return;
    }
    visNetwork.current = new Network(networkRef.current, graphData, {
      nodes: {
        shape: 'circularImage',
        size: 60,
        font: { size: 18, vadjust: 50 },
        borderWidth: 2,
        shapeProperties: { useImageSize: false, interpolation: true, borderDashes: false },
      },
      edges: {
        arrows: 'to',
        font: { align: 'middle' },
        smooth: false, // Disable edge curving
      },
      layout: {
        improvedLayout: true,
      },
      physics: {
        stabilization: true,
        barnesHut: {
          centralGravity: 0.05,
          springLength: 350,
          springConstant: 0.01,
          avoidOverlap: 2,
        },
        minVelocity: 0.75,
      },
    });
    // Disable physics after stabilization so the graph becomes static
    visNetwork.current.once('stabilizationIterationsDone', function () {
      visNetwork.current.setOptions({ physics: false });
    });
  };

  // Handle search
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    console.log('[SEARCH] Search button clicked. Query:', query, 'Mode:', searchMode);
    let brands = null;
    if (searchMode === 'llm') {
      brands = await fetchBrandsFromEndpoint('/api/llm-only', query.trim(), model, { brands: [] }, 'selectedBrands');
    } else if (searchMode === 'chat-completion-agent') {
      brands = await fetchBrandsFromEndpoint('/api/chat-completion-agent', query.trim(), model, {}, 'result');
    } else if (searchMode === 'semantic-kernel-agent') {
      brands = await fetchBrandsFromEndpoint('/api/semantic-kernel-agent', query.trim(), model, {}, 'result');
    } else {
      alert('Only LLM and Agent modes are implemented in this version.');
      return;
    }
    if (brands) {
      const graphData = buildLlmGraph(query.trim(), brands);
      renderGraph(graphData);
    }
  };

  // Initial render for default company (LLM only)
  useEffect(() => {
    (async () => {
      if (searchMode === 'llm') {
        const brands = await fetchBrandsFromEndpoint('/api/llm-only', query.trim(), model, { brands: [] }, 'selectedBrands');
        const graphData = buildLlmGraph(query.trim(), brands);
        renderGraph(graphData);
      }
    })();
    // eslint-disable-next-line
  }, []);

  return (
    <div className="App" style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <h2>Company Graph Visualizer</h2>
      <form onSubmit={handleSearch} style={{ marginBottom: 20, display: 'flex', alignItems: 'center' }}>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Enter company name (e.g. Microsoft)"
          style={{ width: 300, fontSize: 16 }}
        />
        <select
          value={searchMode}
          onChange={e => setSearchMode(e.target.value)}
          style={{ marginLeft: 10, fontSize: 16 }}
        >
          <option value="llm">LLM Only</option>
          <option value="chat-completion-agent">ChatCompletionAgent</option>
          <option value="semantic-kernel-agent">Semantic Kernel Agent</option>
          <option value="wikidata" disabled>Wikidata Only (not implemented)</option>
          <option value="hybrid" disabled>Hybrid (not implemented)</option>
        </select>
        <select
          value={model}
          onChange={e => setModel(e.target.value)}
          style={{ marginLeft: 10, fontSize: 16 }}
        >
          {modelOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
        <button type="submit" style={{ marginLeft: 10, fontSize: 16 }}>Search</button>
      </form>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <div
        ref={networkRef}
        style={{
          flex: 1,
          minHeight: 0,
          border: '1px solid #ccc',
          background: '#fff',
        }}
      />
    </div>
  );
}

export default App;
