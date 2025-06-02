
import React from 'react';
import TextField from '@mui/material/TextField';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Box from '@mui/material/Box';

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
    <Box component="form" onSubmit={onSubmit} sx={{ mb: 2, display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
      <TextField
        label="Company name"
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="Enter company name (e.g. Microsoft)"
        sx={{ width: 300 }}
        size="small"
        disabled={loading}
      />
      <FormControl sx={{ minWidth: 180 }} size="small" disabled={loading}>
        <InputLabel id="search-mode-label">Search mode</InputLabel>
        <Select
          labelId="search-mode-label"
          value={searchMode}
          label="Search mode"
          onChange={e => setSearchMode(e.target.value)}
        >
          <MenuItem value="wikidata">Wikidata Only</MenuItem>
          <MenuItem value="foundry-local">Foundry Local LLM</MenuItem>
          <MenuItem value="azure-open-ai">Azure OpenAI LLM</MenuItem>
          <MenuItem value="chat-completion-agent">ChatCompletionAgent</MenuItem>
          <MenuItem value="semantic-kernel-agent">Semantic Kernel Agent</MenuItem>
          <MenuItem value="azure-foundry-agent">Azure Foundry Agent</MenuItem>
        </Select>
      </FormControl>
      {searchMode !== 'wikidata' && filteredModelOptions.length > 0 && (
        <FormControl sx={{ minWidth: 180 }} size="small" disabled={loading}>
          <InputLabel id="model-selector-label">Model</InputLabel>
          <Select
            labelId="model-selector-label"
            value={model}
            label="Model"
            onChange={e => setModel(e.target.value)}
          >
            {filteredModelOptions.map(opt => (
              <MenuItem key={opt.value} value={opt.value}>{opt.label}</MenuItem>
            ))}
          </Select>
        </FormControl>
      )}
      <Button type="submit" variant="contained" color="primary" sx={{ minWidth: 100 }} disabled={loading}>
        Search
      </Button>
    </Box>
  );
}
