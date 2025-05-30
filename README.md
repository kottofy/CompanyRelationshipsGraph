# Company Relationships Graph <!-- omit from toc -->

Company Relationships Graph is a full-stack web application designed to help users explore and visualize the relationships between companies and their brands. It leverages data from Wikidata and advanced language models (LLMs), including Azure OpenAI and local Foundry models, to provide rich, interactive graph-based insights. The project demonstrates the integration of modern AI agents, robust backend APIs, and a user-friendly React frontend for business intelligence and research use cases.

## Table of Contents <!-- omit from toc -->

- [Project Structure](#project-structure)
- [Quick Start (VS Code)](#quick-start-vs-code)
- [Impact](#impact)
- [Key Features](#key-features)
- [Observations \& Findings](#observations--findings)


## Project Structure

- **frontend/** — React app for the user interface and graph visualization ([see frontend/README.md](./frontend/README.md))
- **backend/** — FastAPI server for data aggregation, AI/LLM integration, and API endpoints ([see backend/README.md](./backend/README.md))
- **docs/AI_Options_Reference.md** — AI/LLM/Agent options and usage guidance ([see AI Options Reference](./docs/AI_Options_Reference.md))

## Quick Start (VS Code)

1. Open this folder in [Visual Studio Code](https://code.visualstudio.com/).
2. Make sure you have the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) extensions installed.
3. See the [frontend/README.md](./frontend/README.md) and [backend/README.md](./backend/README.md) READMEs for required environment variable setup using .env files.
4. Press <kbd>F5</kbd> or go to the Run & Debug panel and select **Full Stack: Frontend + Backend** to launch both the FastAPI backend and React frontend together.
5. The frontend will open at [http://localhost:3000](http://localhost:3000) and the backend at [http://localhost:8081](http://localhost:8081) by default.
6. Search for a company to explore its ecosystem!

## Impact

- **Accelerates Research:** Enables rapid exploration of company ecosystems for analysts, strategists, and researchers.
- **Demonstrates AI Integration:** Showcases how modern LLMs and agent frameworks can be combined with open data for business intelligence.
- **Foundation for Expansion:** Provides a robust base for future features, such as deeper analytics, export options, or integration with internal datasets.

## Key Features

- **Graph Visualization:** Interactive network graph of company-brand relationships, rendered with vis-network.
- **Multi-Source Data:** Combines Wikidata SPARQL queries and LLM/agentic reasoning for comprehensive results.
- **Flexible Model Selection:** Supports Azure OpenAI, Foundry Local, and agent-based endpoints, with user-selectable models.
- **Company Logo Integration:** Fetches and displays company logos from Wikimedia Commons for visual context.
- **Robust Error Handling:** Handles slow/unreachable backends, parse errors, and invalid user input gracefully.
- **Modular, Maintainable Code:** Backend and frontend are cleanly separated, with reusable components and utilities.

## Observations & Findings

- **Data Quality:** Wikidata provides a strong foundation, but LLMs can supplement gaps or infer relationships not explicitly present in structured data.
- **Agentic Capabilities:** Azure AI Agents and Foundry Local agents enable more dynamic, context-aware responses, improving the depth of insights.
- **User Experience:** The React frontend, with model selection and error feedback, makes the tool accessible to both technical and non-technical users.
- **Extensibility:** The architecture supports easy addition of new data sources, models, or visualization features.
