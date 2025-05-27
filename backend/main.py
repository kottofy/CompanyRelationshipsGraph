from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.kernel import Kernel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from foundry_local import FoundryLocalManager
import json
import os
from wikidata_utils import get_wikidata_qid, get_company_graph
from prompts import build_user_prompt


# Load environment variables from .env if present
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model for Wikidata search
class CompanyGraphRequest(BaseModel):
    company: str
    model: str

    # Endpoint: Wikidata Only mode
@app.post("/api/wikidata-graph")
async def wikidata_graph(req: CompanyGraphRequest):
    qid = await get_wikidata_qid(req.company)
    if not qid:
        return JSONResponse({"error": "Company not found on Wikidata"}, status_code=404)
    data = await get_company_graph(qid)
    # Parse results into nodes/edges for frontend
    nodes = [{"id": qid, "label": req.company, "type": "company"}]
    edges = []
    qid_to_node = {qid: nodes[0]}
    for row in data["results"]["bindings"]:
        rel = row["relation"]["value"]
        related_qid = row["relatedQid"]["value"].split("/")[-1]
        label = row["relatedLabel"]["value"]
        logo = row.get("logo", {}).get("value")
        if related_qid not in qid_to_node:
            qid_to_node[related_qid] = {
                "id": related_qid,
                "label": label,
                "type": rel,
                "logo": logo,
            }
        # Edge direction: from company to related (except parent_of)
        if rel == "parent_of":
            edges.append({"from": related_qid, "to": qid, "label": rel})
        else:
            edges.append({"from": qid, "to": related_qid, "label": rel})
    # Add all unique nodes
    nodes.extend([n for k, n in qid_to_node.items() if k != qid])
    return {"nodes": nodes, "edges": edges}


def validate_company_model_request(req):
    if not hasattr(req, 'company') or not req.company or not isinstance(req.company, str) or not req.company.strip():
        return {"error": "Company must be a non-empty string."}
    if not hasattr(req, 'model') or not req.model or not isinstance(req.model, str) or not req.model.strip():
        return {"error": "Model must be a non-empty string."}
    return None

def get_azure_openai_env():
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    if not endpoint or not api_key:
        return None, None, {"error": "Azure OpenAI endpoint or key not set in environment variables."}
    return endpoint, api_key, None

@app.post("/api/chat-completion-agent")
async def chat_completion_agent_endpoint(req: CompanyGraphRequest):
    validation_error = validate_company_model_request(req)
    if validation_error:
        return validation_error
    deployment_name = req.model
    company = req.company
    user_prompt = build_user_prompt(company)
    endpoint, api_key, env_error = get_azure_openai_env()
    if env_error:
        return env_error
    service = AzureChatCompletion(
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key
    )
    agent = ChatCompletionAgent(
        service=service,
        name="CompanyGraphAgent",
        instructions="You are a helpful assistant for company graph queries.",
    )
    response = await agent.get_response(messages=user_prompt)

    if not response or not response.content.content:
        return {"error": "No response from the agent."}
    content = response.content.content.strip()
    # Ensure response is a valid JSON
    try:
        json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Agent response is not valid JSON."}
    # Return the response content
    return {"result": content}

@app.post("/api/semantic-kernel-agent")
async def semantic_kernel_agent_endpoint(req: CompanyGraphRequest):
    validation_error = validate_company_model_request(req)
    if validation_error:
        return validation_error
    deployment_name = req.model
    company = req.company
    user_prompt = build_user_prompt(company)
    endpoint, api_key, env_error = get_azure_openai_env()
    if env_error:
        return env_error

    # Create Semantic Kernel and register skill
    kernel = Kernel()
    kernel.add_service(
        AzureChatCompletion(
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key
        )
    )
    kernel.add_plugin("company_graph", "CompanyGraphPlugin")

    # Create agent with kernel
    agent = ChatCompletionAgent(
        kernel=kernel,
        name="CompanyGraphAgent",
        instructions="You are a helpful assistant for company graph queries. Use your tools to answer questions about company relationships.",
    )
    response = await agent.get_response(messages=user_prompt)

    if not response or not response.content.content:
        return {"error": "No response from the agent."}
    content = response.content.content.strip()
    # Ensure response is a valid JSON
    try:
        json.loads(content)
    except json.JSONDecodeError:
        return {"error": "Agent response is not valid JSON."}
    # Return the response content
    return {"result": content}


@app.post("/api/llm-only")
async def llm_only(req: CompanyGraphRequest):
    try:
        validation_error = validate_company_model_request(req)
        if validation_error:
            return validation_error
        user_prompt = build_user_prompt(req.company)
        if req.model == "model-router":
            # Use Azure OpenAI
            azure_endpoint, azure_key, env_error = get_azure_openai_env()
            azure_deployment = req.model
            if env_error:
                return env_error
            client = openai.AzureOpenAI(
                api_key=azure_key,
                api_version="2023-05-15",
                azure_endpoint=azure_endpoint
            )
            completion = client.chat.completions.create(
                model=azure_deployment,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=4096
            )
            result = completion.choices[0].message.content
            print(result)
        else:
            manager = FoundryLocalManager(req.model)
            client = openai.OpenAI(
                base_url=manager.endpoint,
                api_key=manager.api_key  # API key is not required for local usage
            )
            completion = client.chat.completions.create(
                model=manager.get_model_info(req.model).id,
                messages=[{"role": "user", "content": user_prompt}],
                max_tokens=4096
            )
            result = completion.choices[0].message.content
            print(result)

        try:
            brands = json.loads(result)
            # Validate: ensure each item is an object with 'name', 'type', and 'logo'
            if not (isinstance(brands, list) and all(isinstance(b, dict) and 'name' in b and 'type' in b and 'logo' in b for b in brands)):
                raise ValueError('LLM did not return expected format')
        except Exception:
            # fallback: treat as comma-separated list of names, type 'brand', logo null
            brands = [b.strip() for b in result.split(',') if b.strip()]
            brands = [{"name": b, "type": "brand", "logo": None} for b in brands]

        return {"selectedBrands": brands}
    except Exception as e:
        return {"error": str(e)}
