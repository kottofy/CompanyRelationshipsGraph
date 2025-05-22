# Company Graph SPA

This project is a single-page React application that lets users search for a company and visualizes its brands, subsidiaries, and parent relationships as a graph. Data and logos are fetched live from Wikidata/Wikipedia and Wikimedia Commons.

## Features
- Search for a company by name
- Visualize company relationships (brands, subsidiaries, parent companies)
- Display company/brand logos from Wikimedia Commons
- Interactive graph using vis-network

## How it works
1. User searches for a company
2. The app queries Wikipedia/Wikidata for the company entity
3. Fetches relationships and logo images from Wikidata
4. Renders an interactive graph

## Getting Started

1. `cd frontend`
2. `npm start`

## Tech Stack
- React
- vis-network
- Wikidata SPARQL API
- Wikimedia Commons (for logos)

---

Feel free to contribute or suggest improvements!
