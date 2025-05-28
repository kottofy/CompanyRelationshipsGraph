from pydantic import BaseModel


class CompanyGraphRequest(BaseModel):
    company: str
    model: str