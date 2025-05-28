import urllib.parse
import aiohttp

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

async def get_company_graph(qid: str):
    sparql = f"""
    SELECT ?relation ?relatedQid ?relatedLabel ?logo WHERE {{
      VALUES ?company {{ wd:{qid} }}
      {{
        ?company wdt:P355 ?relatedQid. BIND("subsidiary" AS ?relation)
      }} UNION {{
        ?company wdt:P749 ?relatedQid. BIND("parent" AS ?relation)
      }} UNION {{
        ?relatedQid wdt:P355 ?company. BIND("parent_of" AS ?relation)
      }}
      OPTIONAL {{ ?relatedQid wdt:P154 ?logo. }}
      OPTIONAL {{ ?relatedQid rdfs:label ?relatedLabel . FILTER (lang(?relatedLabel) = "en") }}
    }}
    """
    url = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}
    params = {"query": sparql}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as resp:
            data = await resp.json()
            return data
