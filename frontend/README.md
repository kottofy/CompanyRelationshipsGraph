# CompanyGraph Frontend

This is the React frontend for the CompanyGraph application, which visualizes company-brand relationships as an interactive graph using data from Wikidata, Wikimedia Commons, and AI/LLM-powered agents.

## Features
- Search for a company and visualize its brands, subsidiaries, and parent relationships
- Interactive graph rendered with [vis-network](https://visjs.github.io/vis-network/)
- Company and brand logos fetched from Wikimedia Commons
- Multiple AI/LLM/agent options for richer relationship extraction
- Responsive, modern UI built with [Material-UI (MUI)](https://mui.com/)
- Robust error handling and user guidance

## Getting Started

### Prerequisites
- Node.js (v18+ recommended)
- npm (v9+ recommended)

### Installation
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```

### Configuration
- Copy `.env.example` to `.env` and set the `REACT_APP_API_BASE` variable to point to your backend API (default: `http://localhost:8001`).

### Running the App
Start the development server:
```sh
npm start
```
The app will be available at [http://localhost:3000](http://localhost:3000).

## Project Structure
- `src/` — Main React source code
  - `components/` — UI components (search form, graph, etc.)
  - `services/` — API service functions
  - `constants.js` — Centralized constants for modes/models
  - `App.js` — Main application component
- `.env.example` — Example environment variables
- `public/` — Static assets

## Usage
1. Enter a company name in the search bar.
2. Select the desired search mode and model (if applicable).
3. Click "Search" to visualize the company ecosystem as a graph.
4. Hover over nodes to see company/brand names and view logos.

## Customization
- To add or modify AI models or search modes, edit `src/constants.js`.
- To change the API base URL, update `.env`.
- For UI tweaks, edit components in `src/components/` and styles in `src/App.css`.

## Tech Stack
- React
- Material-UI (MUI)
- vis-network
- Wikidata/Wikimedia Commons APIs

## Troubleshooting
- If the graph does not render, ensure the backend is running and accessible at the API base URL.
- For vis-network issues, ensure it is installed (`npm install vis-network`).
- For CORS errors, check backend CORS settings.
