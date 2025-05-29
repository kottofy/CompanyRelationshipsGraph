// constants.js - Centralized constants for the CompanyGraph frontend

export const allModelOptions = [
  { value: 'phi-3-mini-4k', label: 'Phi 3 Mini 4k', modes: ['foundry-local'] },
  { value: 'deepseek-r1-7b', label: 'Deepseek R1 7b', modes: ['foundry-local'] },
  { value: 'model-router', label: 'Model Router', modes: ['chat-completion-agent', 'azure-open-ai', 'semantic-kernel-agent'] },
  { value: 'gpt-4.1', label: 'GPT-4.1', modes: ['chat-completion-agent', 'semantic-kernel-agent', 'azure-open-ai', 'azure-foundry-agent'] },
  { value: 'gpt-4.o', label: 'GPT-4.o', modes: ['azure-foundry-agent'] },
  // Add more as needed
];
