# --- Move all imports to the top and ensure FastAPI app is defined first ---

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import urllib.parse
import aiohttp
import openai
from foundry_local import FoundryLocalManager
import json
import os
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
    # Helper: Resolve company name to Wikidata QID
async def get_wikidata_qid(company_name: str) -> str:
    url = (
        "https://www.wikidata.org/w/api.php"
        "?action=wbsearchentities"
        f"&search={urllib.parse.quote(company_name)}"
        "&language=en"
        "&format=json"
        "&type=item"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get("search"):
                return data["search"][0]["id"]
    return None

    # Helper: Query Wikidata for brands, subsidiaries, and parent companies
async def get_company_graph(qid: str):
    # SPARQL: brands (P127, P452, P749), subsidiaries (P355), parent (P749)
    sparql = f"""
    SELECT ?relation ?relatedQid ?relatedLabel ?logo WHERE {{
      VALUES ?company {{ wd:{qid} }}
      {{
        ?company wdt:P355 ?relatedQid. BIND("subsidiary" AS ?relation)
      }} UNION {{
        ?company wdt:P127 ?relatedQid. BIND("owned_brand" AS ?relation)
      }} UNION {{
        ?company wdt:P749 ?relatedQid. BIND("parent" AS ?relation)
      }} UNION {{
        ?relatedQid wdt:P355 ?company. BIND("parent_of" AS ?relation)
      }}
      OPTIONAL {{ ?relatedQid wdt:P154 ?logo. }}
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    url = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}
    params = {"query": sparql}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data


# Request model for Wikidata search
class WikidataGraphRequest(BaseModel):
    company: str

    # Endpoint: Wikidata Only mode
@app.post("/api/wikidata-graph")
async def wikidata_graph(req: WikidataGraphRequest):
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

# Brand filter (LLM) endpoint
class BrandFilterRequest(BaseModel):
    company: str
    brands: list
    model: str
    prompt: str = "Select the most relevant brands for this company. Return a JSON list of brand names."

@app.post("/api/select-brands")
async def select_brands(req: BrandFilterRequest):
    # Use Foundry Local SDK instead of HTTP
    user_prompt = (
        f"You are an expert in company relationships. "
        f"IMPORTANT: Do not include any <think> sections, reasoning, explanations, notes, or any text before or after the JSON. "
        f"Given the company '{req.company}', return ONLY a JSON array of objects, each with 'name', 'type', and 'logo'. Do not include any notes, explanations, or text outside the JSON array. "
        f"Restrict the number of companies to 10. "
        f"The central company node must have type 'company'. Parent companies must have type 'parent', subsidiaries must have type 'subsidiary'. "
        f"List the parent company (if any), and all direct subsidiaries of {req.company}, each as a separate object. For subsidiaries, use real-world companies that are or have been subsidiaries of {req.company}, such as Pratt & Whitney, Collins Aerospace, Raytheon, and others. Do not repeat the same entity for different types unless it is correct in real life. "
        f"For each entity, search Wikimedia Commons for the official logo. Use the direct file URL (ending in .svg or .png) from https://upload.wikimedia.org/wikipedia/commons/. Do not use any URL containing '/thumb/'. If no logo is available, set 'logo' to null. Do not use Wikipedia or any other source. "
        f"Example: [{{\"name\": \"RTX Corporation\", \"type\": \"company\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/7/7e/RTX_Corporation_logo.svg\"}}, {{\"name\": \"Pratt & Whitney\", \"type\": \"subsidiary\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/2/2d/Pratt_%26_Whitney_logo.svg\"}}, {{\"name\": \"Collins Aerospace\", \"type\": \"subsidiary\", \"logo\": \"https://upload.wikimedia.org/wikipedia/commons/6/6d/Collins_Aerospace_logo.svg\"}}] "
        f"Do not repeat the same name for different types unless it is correct in real life. "
        f"Do not include products such as \"Windows Phone\" or \"Azure\". "
        f"Return ONLY a JSON array of objects as your entire response. Do not include any <think> sections, explanations, or any text before or after the JSON. Your response must be a valid JSON array and nothing else."
        f"Do not include any characters or text outside the JSON array. "
    )
    try:
        if req.model == "model-router":
            # Use Azure OpenAI
            azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
            azure_key = os.environ.get("AZURE_OPENAI_KEY")
            azure_deployment = req.model
            if not azure_endpoint or not azure_key:
                return {"error": "Azure OpenAI endpoint or key not set in environment variables."}
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
