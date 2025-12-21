from fastapi import FastAPI , status
from repositories.case_repository import get_all_cases, create_case
from schemas.case import CaseCreate , CaseResponse , CaseUpdate
from services.case_service import delete_case_service , update_case_service


app = FastAPI()

@app.get("/cases", response_model=list[CaseResponse])
def read_cases():
    return get_all_cases()

@app.post("/cases" , status_code=201)
def create_case_endpoint(case:CaseCreate):
    create_case(case)
    return {"message" : "case created"}

@app.delete("/cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case_endpoint(case_id: int):
    delete_case_service(case_id)

@app.patch("/cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_case_endpoint(case_id: int, case: CaseUpdate):
    data = case.dict(exclude_none=True)
    update_case_service(case_id, data)