from fastapi import FastAPI
from repositories.case_repository import get_all_cases

app = FastAPI()

@app.get("/cases")
def read_cases():
    return get_all_cases()
