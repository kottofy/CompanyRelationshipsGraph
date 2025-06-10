# Security & Privacy Learnings

## Local vs. Cloud Inference
- Running models locally (e.g., with Foundry Local) ensures that sensitive data never leaves the user’s device, supporting privacy and regulatory compliance.
- Cloud-based inference (e.g., Azure OpenAI) may offer more powerful models but requires careful handling of data privacy and access controls.

## Environment Variable Management
- Storing secrets and API keys in environment variables (not in code) reduces the risk of accidental exposure.
- `.env` files should never be committed to version control; this project uses `.env.example` for documentation.

## Privacy Implications of Model Hosting
- Understand the privacy guarantees and data retention policies of any third-party model provider or API.
- For highly sensitive or regulated data, prefer on-device or private cloud inference whenever possible.

## Takeaways
- Always consider privacy and security from the start—especially when handling user or business data.
- Use local inference for maximum privacy, and document any data flows to external services.
- Secure environment variable and secret management is a must for any production AI system.
