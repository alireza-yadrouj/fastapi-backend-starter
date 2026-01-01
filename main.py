from fastapi import FastAPI , status , Query , HTTPException , Depends
from schemas.user import  UserCreate , UserResponse, CurrentUser
from schemas.case import CaseCreate, CaseUpdate, PaginatedCaseResponse, CaseSortFields, SortOrder
from services.case_service import delete_case_service , update_case_service , filter_cases
from repositories.user_repository import get_user_by_username, create_user
from fastapi.security import OAuth2PasswordRequestForm 
from core.security import pwd_context,  create_access_token , get_current_user
from sqlalchemy.orm import Session
from database import get_db
from repositories.case_repository import create_case


app = FastAPI()

@app.get("/cases", response_model=PaginatedCaseResponse)
def get_cases_endpoint(
    title : str | None = Query(default=None),
    description: str | None = Query(default=None),
    page:int = Query(default=1, ge=1, description="page number"),
    page_size: int = Query(default=10, ge=1, le=100, description="Number of items per page"),
    sort_by:CaseSortFields = Query(default=CaseSortFields.title),
    sort_order:SortOrder = Query(default=SortOrder.asc),
    current_user: CurrentUser = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    items, total = filter_cases(
        db=db,
        owner_username=current_user.username,
        role=current_user.role,
        title=title,
        description=description,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order
        )
    
    return {
        "items" : items,
        "page": page,
        "page_size": page_size,
        "total": total
    }
     
@app.post("/cases" , status_code=201)
def create_case_endpoint(
    case:CaseCreate ,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_case(db, case.model_dump(), current_user.username)

@app.delete("/cases/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case_endpoint(
    case_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    delete_case_service(db, case_id , current_user.username , current_user.role )

@app.patch("/cases/{case_id}", status_code=status.HTTP_200_OK)
def update_case_endpoint(
    case_id: int,
    case: CaseUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db:Session = Depends(get_db)
):
    data = case.dict(exclude_none=True)
    return update_case_service(db, case_id, current_user.username, data, current_user.role )

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db:Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    try:
        return create_user(db, user.username, user.password , role = user.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):

    user = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if not pwd_context.verify(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username , "role":user.role})
    return {"access_token": access_token, "token_type": "bearer"}

