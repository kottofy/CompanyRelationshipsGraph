# API & Integration Learnings

## Flexible Backend API Design
- Designing API endpoints to support multiple search modes (Wikidata, LLM, hybrid) and model options made the backend adaptable to new requirements.
- Using path and query parameters for mode/model selection keeps the API clean and easy to extend.

## Multi-Endpoint AI Integration
- Integrating with Azure OpenAI, Foundry Local, and agent-based endpoints required careful abstraction to handle different authentication methods and response formats.
- Wrapping each AI provider in a dedicated backend function simplified error handling and future maintenance.

## Environment Variable & Secret Management
- Storing API keys and configuration in `.env` files (and documenting them in `.env.example`) made local and cloud development safer and more consistent.
- Using libraries like `python-dotenv` to load environment variables at runtime streamlined setup and reduced onboarding friction.

## Takeaways
- Plan for extensibility: a modular API makes it easier to add new data sources or AI providers.
- Consistent error handling and response validation are critical when aggregating results from multiple backends.
- Secure, documented environment variable management is essential for both developer productivity and security.
