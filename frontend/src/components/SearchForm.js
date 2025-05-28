import React from 'react';

export default function SearchForm({
  query,
  setQuery,
  searchMode,
  setSearchMode,
  model,
  setModel,
  filteredModelOptions,
  onSubmit,
  loading
}) {
  return (
    <form onSubmit={onSubmit} style={{ marginBottom: 20, display: 'flex', alignItems: 'center' }}>
      <input
        type="text"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter company name (e.g. Microsoft)"
        style={{ width: 300, fontSize: 16 }}
        aria-label="Company name"
        disabled={loading}
      />
      <select
        value={searchMode}
        onChange={e => setSearchMode(e.target.value)}
        style={{ marginLeft: 10, fontSize: 16 }}
        aria-label="Search mode"
        disabled={loading}
      >
        <option value="foundry-local">Foundry Local LLM</option>
        <option value="azure-open-ai">Azure OpenAI LLM</option>
        <option value="chat-completion-agent">ChatCompletionAgent</option>
        <option value="semantic-kernel-agent">Semantic Kernel Agent</option>
        <option value="wikidata">Wikidata Only</option>
      </select>
      {searchMode !== 'wikidata' && filteredModelOptions.length > 0 && (
        <select
          value={model}
          onChange={e => setModel(e.target.value)}
          style={{ marginLeft: 10, fontSize: 16 }}
          aria-label="Model selector"
          disabled={loading}
        >
          {filteredModelOptions.map(opt => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      )}
      <button type="submit" style={{ marginLeft: 10, fontSize: 16 }} disabled={loading}>Search</button>
    </form>
  );
}
