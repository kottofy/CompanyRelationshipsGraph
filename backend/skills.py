
from semantic_kernel.functions import kernel_function
from wikidata_utils import get_wikidata_qid, get_company_graph
import json

class CompanyGraphPlugin:
    @kernel_function(description="Get company info from Wikidata")
    async def get_company_info(self, company: str) -> str:
        qid = await get_wikidata_qid(company)
        if not qid:
            return json.dumps({"error": "Company not found"})
        data = await get_company_graph(qid)
        return json.dumps(data)