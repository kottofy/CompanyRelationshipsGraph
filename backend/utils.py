import json
import os


def parse_companies_result(result):
    """
    Parse a result string into a list of dicts with 'name', 'type', and 'logo'.
    Handles both JSON and comma-separated string formats.
    """
    try:
        companies = json.loads(result)
        # Validate: ensure each item is an object with 'name', 'type', and 'logo'
        if not (isinstance(companies, list) and all(isinstance(c, dict) and 'name' in c and 'type' in c and 'logo' in c for c in companies)):
            raise ValueError('LLM did not return expected format')
    except Exception:
        # fallback: treat as comma-separated list of names, type 'company', logo null
        companies = [c.strip() for c in result.split(',') if c.strip()]
        companies = [{"name": c, "type": "company", "logo": None} for c in companies]
    return companies


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