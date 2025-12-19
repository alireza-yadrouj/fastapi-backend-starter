from fastapi import FastAPI
from repositories.case_repository import get_all_cases, create_case
from schemas.case import CaseCreate , CaseResponse


app = FastAPI()

@app.get("/cases", response_model=list[CaseResponse])
def read_cases():
    return get_all_cases()

@app.post("/cases" , status_code=201)
def create_case_endpoint(case:CaseCreate):
    create_case(case)
    return {"message" : "case created"}

