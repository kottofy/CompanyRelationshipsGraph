// constants.js - Centralized constants for the CompanyGraph frontend

export const ALL_MODEL_OPTIONS = [
  { value: 'phi-3-mini-4k', label: 'Phi 3 Mini 4k', modes: ['foundry-local'] },
  { value: 'deepseek-r1-7b', label: 'Deepseek R1 7b', modes: ['foundry-local'] },
  { value: 'model-router', label: 'Model Router', modes: ['chat-completion-agent', 'azure-open-ai', 'semantic-kernel-agent'] },
  { value: 'gpt-4.1', label: 'GPT-4.1', modes: ['chat-completion-agent', 'semantic-kernel-agent', 'azure-open-ai', 'azure-foundry-agent'] },
  { value: 'gpt-4.o', label: 'GPT-4.o', modes: ['azure-foundry-agent'] },
  // Add more as needed
];

// Short descriptions for each AI method
export const SEARCH_MODE_DESCRIPTIONS = {
  'foundry-local': 'Foundry Local LLM: Uses a local language model for fast, private inference. Good for experimentation and when cloud access is not desired.',
  'azure-open-ai': 'Azure OpenAI LLM: Uses Microsoft-hosted OpenAI models for high-quality, cloud-based results. Best for production-grade accuracy and reliability. Uses API keys for authentication.',
  'azure-foundry-agent': 'Azure Foundry Agent: Uses an Azure AI Agent for advanced, context-aware answers. Supports agentic reasoning and tool use for deeper insights. Uses Microsoft Entra ID for authentication.',
  'chat-completion-agent': 'Semantic Kernel ChatCompletionAgent: Uses a Semantic Kernel agent (interface) with LLMs for structured, multi-step reasoning.',
  'semantic-kernel-agent': 'Semantic Kernel Agent: Uses a Semantic Kernel agent (interface) with LLMs with custom skills for extensible, skill-driven answers with grounded data.',
  'wikidata': 'Wikidata Only: Uses only structured data from Wikidata. Most transparent and reproducible, but may miss inferred relationships and requires custom queries to obtain data.'
};

// Short descriptions for each model option
export const MODEL_DESCRIPTIONS = {
  'phi-3-mini-4k': 'Phi 3 Mini 4k: Lightweight, open-source model for fast, local inference. Good for experimentation and privacy.',
  'deepseek-r1-7b': 'Deepseek R1 7b: Larger open-source model for local use, offering more capacity than Phi 3 Mini.',
  'model-router': 'Model Router: Lets the backend choose the best model for your query, balancing speed and accuracy.',
  'gpt-4.1': 'GPT-4.1: Microsoft/Azure-hosted, high-accuracy model. Best for complex queries and production use.',
  'gpt-4.o': 'GPT-4.o: Latest generation Azure model, offering improved reasoning and performance.',
};