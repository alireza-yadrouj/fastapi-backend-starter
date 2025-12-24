from fastapi import FastAPI , status , Query , HTTPException , Depends
from repositories.case_repository import create_case 
from schemas.user import  UserCreate , UserResponse , UserLogin
from schemas.case import CaseCreate , CaseResponse , CaseUpdate
from services.case_service import delete_case_service , update_case_service , filter_cases
from repositories.user_repository import get_user_by_username, create_user
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from core.security import pwd_context,  create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.get("/cases", response_model=list[CaseResponse])
def get_cases_endpoint(
    title : str | None = Query(default=None),
    description: str | None = Query(default=None)
):
    
    """
    Get cases with optional filtering.
    """
    return filter_cases(
        title=title,
        description=description
    )


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



@app.post("/register", response_model=UserResponse)
def register(user: UserCreate):
    existing_user = get_user_by_username(user.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        return create_user(user.username, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # بررسی وجود کاربر
    user = get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # بررسی پسورد
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # ساخت توکن
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}