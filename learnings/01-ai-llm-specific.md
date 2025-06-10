# AI/LLM-Specific Learnings

## Model Selection Trade-Offs
- Choosing between local, cloud, and agent-based models involves balancing speed, accuracy, privacy, and cost.
- Local models (e.g., Foundry Local) offer privacy and low latency, while cloud models (e.g., Azure OpenAI) provide access to larger, more capable models.
- Hybrid and agentic approaches can combine the strengths of both, but add complexity.

## Grounding LLMs with Structured Data
- Using structured data (e.g., Wikidata) to ground LLM responses helps reduce hallucinations and improves factual accuracy.
- Hybrid search modes that combine LLMs with knowledge bases provide more reliable and explainable results.

## API Usage Limits and Monitoring
- Many commercial LLM APIs (e.g., Claude Sonnet) have strict usage limits; tracking and managing these is essential to avoid service interruptions.
- For example, Claude Sonnet has a limit of 1,000 calls per month for many users. See the [Anthropic API documentation](https://docs.anthropic.com/claude/docs/rate-limits) for details and the latest limits.
- Implementing usage monitoring and fallback strategies (e.g., switching to local models) helps maintain availability.

## Latency and Performance
- Local models (e.g., Foundry Local) typically offer lower latency compared to cloud-based APIs, as data does not need to travel over the internet.
- Cloud models may provide higher accuracy or larger context windows, but can introduce network delays and rate limiting.
- Monitoring and comparing response times for different models and deployment types helps inform model selection and user experience improvements.
- Optimizing prompt length and batching requests can further reduce latency and improve throughput.

## Takeaways
- There is no one-size-fits-all model: evaluate your needs for privacy, speed, and accuracy before choosing a solution.
- Grounding LLMs with external data sources is a practical way to improve reliability for business and research use cases.
- Always monitor API usage and have a plan for handling rate limits or outages.
