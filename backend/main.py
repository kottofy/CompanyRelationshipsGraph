
import json
import openai
import time

from azure.identity.aio import DefaultAzureCredential
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from foundry_local import FoundryLocalManager
from prompts import build_user_prompt
from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread, ChatCompletionAgent
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.kernel import Kernel
from utils import get_azure_openai_env, parse_companies_result, validate_company_model_request
from wikidata_utils import get_company_graph, get_wikidata_qid

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
@app.get("/api/wikidata/{company}")
async def wikidata_graph(company: str):
    qid = await get_wikidata_qid(company)
    if not qid:
        return JSONResponse({"error": "Company not found on Wikidata"}, status_code=404)
    data = await get_company_graph(qid)
    companies = [{
        "name": company,
        "type": "company",
        "logo": None
    }]
    seen = set([company])
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
    validated = parse_companies_result(json.dumps(companies))
    if isinstance(validated, dict) and "error" in validated:
        return JSONResponse({"error": validated["error"]}, status_code=422)
    return {"result": validated}

# Endpoint: Foundry Local
@app.get("/api/foundry-local/{model}/{company}")
async def foundry_local(model: str, company: str):
    try:
        validation_error = validate_company_model_request(company=company, model=model)
        if validation_error:
            return validation_error
        user_prompt = build_user_prompt(company)
        deployment_name = model
        manager = FoundryLocalManager(deployment_name)
        client = openai.OpenAI(
            base_url=manager.endpoint,
            api_key=manager.api_key  # API key is not required for local usage
        )
        start_time = time.time()
        completion = client.chat.completions.create(
            model=manager.get_model_info(deployment_name).id,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=4096
        )
        elapsed = time.time() - start_time
        print(f"[FoundryLocal] Inference time for model '{model}' and company '{company}': {elapsed:.2f} seconds")
        result = completion.choices[0].message.content
        companies = parse_companies_result(result)
        if isinstance(companies, dict) and "error" in companies:
            return JSONResponse({"error": companies["error"]}, status_code=422)
        print(companies)
        return {"result": companies}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Azure OpenAI
@app.get("/api/azure-open-ai/{model}/{company}")
async def azure_open_ai(model: str, company: str):
    try:
        validation_error = validate_company_model_request(company=company, model=model)
        if validation_error:
            return validation_error
        user_prompt = build_user_prompt(company)
        deployment_name = model
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
        if isinstance(companies, dict) and "error" in companies:
            return JSONResponse({"error": companies["error"]}, status_code=422)
        return {"result": companies}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Chat Completion Agent (using AzureChatCompletion)
@app.get("/api/chat-completion-agent/{model}/{company}")
async def chat_completion_agent_endpoint(model: str, company: str):
    validation_error = validate_company_model_request(company=company, model=model)
    if validation_error:
        return validation_error
    deployment_name = model
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
    companies = parse_companies_result(result)
    if isinstance(companies, dict) and "error" in companies:
        return JSONResponse({"error": companies["error"]}, status_code=422)
    return {"result": companies}

# Endpoint: Semantic Kernel Agent (using AzureChatCompletion from Semantic Kernel)
@app.get("/api/semantic-kernel-agent/{model}/{company}")
async def semantic_kernel_agent_endpoint(model: str, company: str):
    validation_error = validate_company_model_request(company=company, model=model)
    if validation_error:
        return validation_error
    deployment_name = model
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
    companies = parse_companies_result(result)
    if isinstance(companies, dict) and "error" in companies:
        return JSONResponse({"error": companies["error"]}, status_code=422)
    return {"result": companies}


# Endpoint: Foundry Agent (using AzureAIAgent from Semantic Kernel)
@app.get("/api/azure-foundry-agent/{model}/{company}")
async def azure_foundry_agent_endpoint(model: str, company: str):
    try:
        validation_error = validate_company_model_request(company=company, model=model)
        if validation_error:
            return validation_error

        user_prompt = build_user_prompt(company)
        ai_agent_settings = AzureAIAgentSettings(model_deployment_name=model)  # Reads from .env or environment

        async with (
            DefaultAzureCredential() as creds,
            AzureAIAgent.create_client(
                credential=creds,
                endpoint=ai_agent_settings.endpoint
                ) as client,
        ):
            # OPTION 1 - Create an agent on the Azure AI agent service
            # agent_definition = await client.agents.create_agent(
            #     model=model,
            #     name="CompanyGraphFoundryAgent",
            #     instructions="You are a helpful assistant for company graph queries. Use your tools to answer questions about company relationships.",
            # )

            # agent = AzureAIAgent(
            #     client=client,
            #     definition=agent_definition,
            # )
            # OPTION 2 - Use an existing agent if available
            agent_definition = await client.agents.get_agent(
                agent_id=ai_agent_settings.agent_id,
            )
            agent = AzureAIAgent(
                client=client,
                definition=agent_definition,
            )
            # Create a thread for the agent
            thread: AzureAIAgentThread = None
            try:
                # 4. Invoke the agent with the specified message for response
                response = await agent.get_response(messages=user_prompt, thread=thread)
                thread = response.thread
            finally:
                # 6. Cleanup: Delete the thread and agent
                await thread.delete() if thread else None
                # await client.agents.delete_agent(agent.id)
            if not response or not response.content.content:
                return {"error": "No response from the agent."}
            result = response.content.content
            companies = parse_companies_result(result)
            if isinstance(companies, dict) and "error" in companies:
                return JSONResponse({"error": companies["error"]}, status_code=422)
            return {"result": companies}
    except Exception as e:
        return {"error": str(e)}