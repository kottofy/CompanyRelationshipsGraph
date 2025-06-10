# Data Quality & Validation Learnings

## Wikidata Challenges
- Wikidata is a rich, open resource, but data can be incomplete, inconsistent, or ambiguous (e.g., multiple entities with similar names).
- Some companies lack structured relationships or logo data, requiring fallback logic or user feedback.

## Logo Retrieval
- Fetching company logos from Wikimedia Commons is powerful, but not all entities have logos, and some links may be outdated or missing.
- Filtering out thumbnail URLs and ensuring only direct image links are used improves reliability and display quality.

## Robust Result Validation
- LLM and API responses can be unpredictable; always validate and sanitize results before displaying or using them.
- Parsing and cleaning LLM output (e.g., ensuring valid JSON, removing extra text) is essential for a smooth user experience.

## Takeaways
- Open data sources require defensive programming and clear user messaging about data limitations.
- Automated validation and post-processing of results help prevent UI errors and user confusion.
- Building in fallback logic (e.g., default images, error messages) improves resilience and trust in the tool.
