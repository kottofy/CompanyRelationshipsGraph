// constants.js - Centralized constants for the CompanyGraph frontend

export const allModelOptions = [
  { value: 'phi-3-mini-4k', label: 'Foundry Local Phi 3 Mini 4k', modes: ['llm'] },
  { value: 'deepseek-r1-7b', label: 'Foundry Local Deepseek R1 7b', modes: ['llm'] },
  { value: 'model-router', label: 'Azure OpenAI Model Router', modes: ['llm', 'semantic-kernel-agent'] },
  { value: 'gpt-4.1', label: 'Azure OpenAI GPT-4.1', modes: ['chat-completion-agent', 'semantic-kernel-agent'] },
  // Add more as needed
];
