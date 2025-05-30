# AI Options

## Search Modes
Below are all the search modes a user can select in the CompanyGraph frontend, along with guidance on when and why to use each option.

![Search Form](frontend/screenshots/search_form.png)

### 1. **Foundry Local LLM**
- **Description:** Uses a locally hosted Foundry LLM to infer company-brand relationships.
- **When to use:**
  - When you want fast, private inference without relying on cloud APIs.
  - For experimenting with open-source or custom local models.
- **Model Options:**
  - Phi 3 Mini 4k
  - Deepseek R1 7b

### 2. **Azure OpenAI LLM**
- **Description:** Uses Azure-hosted OpenAI models for company-brand relationship extraction.
- **When to use:**
  - When you need high-quality, cloud-based LLM inference.
  - For leveraging Microsoft’s managed OpenAI service.
- **Model Options:**
  - Model Router
  - GPT-4.1

### 3. **Azure Foundry Agent**
- **Description:** Uses an Azure AI Agent (Semantic Kernel) to answer queries, potentially with agentic reasoning and tool use.
- **When to use:**
  - When you want advanced, context-aware responses that may use plugins or external tools.
  - For leveraging the latest Azure AI Agent capabilities.
- **Model Options:**
  - GPT-4.1
  - GPT-4.o

### 4. **ChatCompletionAgent**
- **Description:** Uses a Semantic Kernel agent with OpenAI/Foundry models for more structured, agentic responses.
- **When to use:**
  - When you want the LLM to use skills/plugins for richer answers.
  - For scenarios where agent workflows are beneficial.
- **Model Options:**
  - Model Router
  - GPT-4.1

### 5. **Semantic Kernel Agent**
- **Description:** Uses a Semantic Kernel agent with skills/plugins, typically with Azure OpenAI models.
- **When to use:**
  - When you want to combine LLM reasoning with custom skills (e.g., Wikidata lookups).
  - For advanced, extensible agentic workflows.
- **Model Options:**
  - Model Router
  - GPT-4.1

### 6. **Wikidata Only**
- **Description:** Uses only Wikidata SPARQL queries to retrieve company-brand relationships (no LLMs involved).
- **When to use:**
  - When you want strictly factual, structured data from Wikidata.
  - For maximum transparency and reproducibility.
- **Model Options:**
  - None (model selection is hidden)

What else should we try??

---

## Model Options (Summary Table)

![Graph Example](frontend/screenshots/graph_example.png)

| Model Value      | Label           | Available In Modes                        |
|------------------|-----------------|-------------------------------------------|
| phi-3-mini-4k    | Phi 3 Mini 4k   | Foundry Local LLM                         |
| deepseek-r1-7b   | Deepseek R1 7b  | Foundry Local LLM                         |
| model-router     | Model Router    | ChatCompletionAgent, Azure OpenAI LLM, Semantic Kernel Agent |
| gpt-4.1          | GPT-4.1         | ChatCompletionAgent, Semantic Kernel Agent, Azure OpenAI LLM, Azure Foundry Agent |
| gpt-4.o          | GPT-4.o         | Azure Foundry Agent                       |

---

*Choose the mode and model that best fit your data needs, privacy requirements, and desired depth of analysis.*
