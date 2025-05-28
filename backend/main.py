from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.kernel import Kernel
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
from foundry_local import FoundryLocalManager
import json
from wikidata_utils import get_wikidata_qid, get_company_graph
from prompts import build_user_prompt
from utils import parse_companies_result, validate_company_model_request, get_azure_openai_env
from CompanyGraphRequest import CompanyGraphRequest
from dotenv import load_dotenv

# Load environment variables from .env if present
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


# Endpoint: Wikidata Only mode
@app.post("/api/wikidata")
async def wikidata_graph(req: CompanyGraphRequest):
    qid = await get_wikidata_qid(req.company)
    if not qid:
        return JSONResponse({"error": "Company not found on Wikidata"}, status_code=404)
    data = await get_company_graph(qid)
    # Build a flat list of entities with name, type, logo
    companies = [{
        "name": req.company,
        "type": "company",
        "logo": None
    }]
    seen = set([req.company])
    for row in data["results"]["bindings"]:
        rel = row["relation"]["value"]
        related_qid = row["relatedQid"]["value"].split("/")[-1]
        label = row.get("relatedLabel", {}).get("value") if "relatedLabel" in row else related_qid
        logo = row.get("logo", {}).get("value") if "logo" in row else None
        if not label:
            label = related_qid
        if label not in seen:
            companies.append({
                "name": label,
                "type": rel,
                "logo": logo if logo else None
            })
            seen.add(label)
    # Validate and format using shared util
    validated = parse_companies_result(json.dumps(companies))
    return {"result": validated}



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
    result = response.content.content
    # Ensure response is a valid JSON
    companies = parse_companies_result(result)
    # Return the response content
    return {"result": companies}

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
    result = response.content.content
    # Ensure response is a valid JSON
    companies = parse_companies_result(result)
    # Return the response content
    return {"result": companies}

@app.post("/api/azure-open-ai")
async def azure_open_ai(req: CompanyGraphRequest):
    try:
        validation_error = validate_company_model_request(req)
        if validation_error:
            return validation_error
        user_prompt = build_user_prompt(req.company)
        deployment_name = req.model

        # Use Azure OpenAI
        azure_endpoint, azure_key, env_error = get_azure_openai_env()
        azure_deployment = deployment_name
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

        companies = parse_companies_result(result)
        return {"result": companies}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/foundry-local")
async def foundry_local(req: CompanyGraphRequest):
    try:
        validation_error = validate_company_model_request(req)
        if validation_error:
            return validation_error
        user_prompt = build_user_prompt(req.company)
        deployment_name = req.model
        # Use Foundry Local Manager
        manager = FoundryLocalManager(deployment_name)
        client = openai.OpenAI(
            base_url=manager.endpoint,
            api_key=manager.api_key  # API key is not required for local usage
        )
        completion = client.chat.completions.create(
            model=manager.get_model_info(deployment_name).id,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4096
        )
        result = completion.choices[0].message.content

        companies = parse_companies_result(result)
        return {"result": companies}
    except Exception as e:
        return {"error": str(e)}
