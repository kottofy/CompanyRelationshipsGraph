import json
import os


def parse_companies_result(result):
    """
    Parse a result string into a list of dicts with 'name', 'type', and 'logo'.
    Handles only valid JSON format. Returns an error dict if parsing fails.
    Also strips whitespace from the result string.
    """
    result = result.strip() if isinstance(result, str) else result
    try:
        companies = json.loads(result)
        # Validate: ensure each item is an object with 'name', 'type', and 'logo'
        if not (isinstance(companies, list) and all(isinstance(c, dict) and 'name' in c and 'type' in c and 'logo' in c for c in companies)):
            raise ValueError('LLM did not return expected format')
        return companies
    except Exception as e:
        return {"error": f"Could not parse companies result: {str(e)}"}

def validate_company_model_request(req=None, company=None, model=None):
    # If called with a request object (legacy), extract company/model from it
    if req is not None:
        company = getattr(req, 'company', None)
        model = getattr(req, 'model', None)
    if company is not None:
        if not isinstance(company, str) or not company.strip():
            return {"error": "Company must be a non-empty string."}
    if model is not None:
        if not isinstance(model, str) or not model.strip():
            return {"error": "Model must be a non-empty string."}
    return None

def get_azure_openai_env():
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    if not endpoint or not api_key:
        return None, None, {"error": "Azure OpenAI endpoint or key not set in environment variables."}
    return endpoint, api_key, None