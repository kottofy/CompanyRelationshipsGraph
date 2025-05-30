# CompanyGraph Backend

This is the FastAPI backend for the CompanyGraph application. It provides API endpoints to retrieve company-brand relationship data using Wikidata SPARQL queries, Wikimedia Commons for logos, and various AI/LLM/agent integrations (including Azure OpenAI, Foundry Local, and Semantic Kernel agents).

## Features
- REST API endpoints for company relationship graph data
- Supports multiple AI/LLM/agent backends for relationship extraction
- Fetches company/brand logos from Wikimedia Commons
- Modular, maintainable code with robust error handling
- Environment-based configuration for API keys and endpoints

## Getting Started

### Prerequisites
- Python 3.9+
- pip

### Installation
1. Navigate to the backend directory:
   ```sh
   cd backend
   ```
2. (Recommended) Create and activate a virtual environment:
   ```sh
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

### Configuration
- Copy `.env.example` to `.env` and fill in the required environment variables for Azure OpenAI, Azure AI Agent, etc.
- Example variables:
  - `AZURE_OPENAI_ENDPOINT`
  - `AZURE_OPENAI_KEY`
  - `AZURE_AI_AGENT_ENDPOINT`
  - `AZURE_AI_AGENT_AGENT_ID`

### Running the Server
Start the FastAPI server (default port: 8081):
```sh
uvicorn main:app --reload --port 8081
```

## API Endpoints
- `/api/wikidata/{company}` — Get company graph from Wikidata only
- `/api/foundry-local/{model}/{company}` — Use Foundry Local LLM
- `/api/azure-open-ai/{model}/{company}` — Use Azure OpenAI LLM
- `/api/azure-foundry-agent/{model}/{company}` — Use Azure AI Agent
- `/api/chat-completion-agent/{model}/{company}` — Use Semantic Kernel ChatCompletionAgent
- `/api/semantic-kernel-agent/{model}/{company}` — Use Semantic Kernel Agent

All endpoints return JSON with a list of companies/brands, their types (company, parent, subsidiary), and logo URLs (if available).

## Project Structure
- `main.py` — Main FastAPI app and API endpoints
- `wikidata_utils.py` — Wikidata SPARQL and entity helpers
- `prompts.py` — Prompt templates for LLMs/agents
- `utils.py` — Validation and parsing utilities
- `requirements.txt` — Python dependencies
- `.env.example` — Example environment variables

## Customization
- Add new AI/LLM/agent integrations by extending `main.py` and related modules
- Adjust Wikidata queries in `wikidata_utils.py` for different relationship types
- Update prompt logic in `prompts.py` for custom LLM instructions

## Troubleshooting
- Ensure all required environment variables are set in `.env`
- For CORS issues, verify FastAPI CORS middleware settings
- For Azure/OpenAI errors, check API keys and endpoint URLs
- For Wikidata issues, ensure network access to Wikidata SPARQL endpoint
