# Prompt Engineering Learnings

## Iterative Prompt Design
- Effective prompt engineering is an iterative process: start simple, test, and refine based on model output and user feedback.
- Documenting successful prompts and their effects helps maintain consistency and enables others to build on your work.

## Using Copilot and AI Assistants
- Leveraging tools like GitHub Copilot to brainstorm, plan, and review code or prompt strategies can accelerate development and surface new ideas.
- Asking Copilot or similar tools to generate a plan before implementing a feature often leads to better-structured and more maintainable code.

## Leveraging .github/copilot-instructions
- Using a `.github/copilot-instructions.md` file allows you to provide project-specific guidance to GitHub Copilot, improving the relevance and quality of AI-generated code and suggestions.
- This approach helps ensure that Copilot understands your project's context, coding standards, and preferred patterns, leading to more consistent and useful completions.
- Keeping this file up to date as your project evolves can further enhance Copilot's effectiveness for your team.

## Testing and Validation
- Always test prompts with a variety of inputs to ensure robustness and avoid unexpected or biased outputs.
- Validate that the model’s responses match the intended format and content, especially when integrating with downstream systems.

## Model Choice for Code Generation
- When using Claude Sonnet 3.7 to generate frontend code, it often produced TypeScript code with many errors and incompatibilities for this project.
- Switching to GPT-4.1 (due to hitting the API rate limit for Claude) resulted in much cleaner, working code and allowed the site to function as intended.
- This experience highlighted the importance of matching the model and language to the project’s actual requirements, and not assuming all LLMs or code outputs are equally reliable.

## Takeaways
- Treat prompt engineering as a core part of the development process, not an afterthought.
- Use AI assistants to enhance creativity and productivity, but always review and validate their suggestions.
- Maintain a library of effective prompts and lessons learned to accelerate future projects.
