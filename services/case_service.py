from fastapi import HTTPException
from repositories.case_repository import delete_case, update_case, get_cases_by_owner, delete_case_admin, update_case_admin, get_all_cases


def delete_case_service(case_id: int , owner_username : str , role : str) -> None:
    
    if role =="admin":
        deleted = delete_case_admin(case_id)
        if not deleted :
            raise HTTPException (status_code=404, detail="Case not found.")
    else:
        deleted = delete_case(case_id , owner_username)
        if not deleted:
            raise HTTPException(
                status_code=403 ,
                detail="you can delete just your cases."
            )

def update_case_service(case_id: int,owner_username : str, data: dict, role:str ) -> None:
    if role == "admin":
        updated = update_case_admin(case_id, data)
    else:
        updated = update_case(case_id, data , owner_username)
    
    if not updated:
        raise HTTPException(
            status_code=403,
            detail="Not allowed or case not found "
        )

def filter_cases(
        owner_username : str ,
        role : str,
        title:str|None = None , 
        description : str |None = None,
        page:int =1,
        page_size:int = 10,
        sort_by:str = "title",
        sort_order: str = "asc", 
):
    
    if role == "admin":
        cases = get_all_cases()
    else:
        cases = get_cases_by_owner(owner_username)
    
    if title:                                       #filter by title
        cases = _filter_by_title(cases, title)

    if description:                                 #filter by description
        cases = _filter_by_description(cases, description)

    total = len(cases)

    if sort_by in ["title", "description"]:          # sort by valid fiels
        cases.sort(key=lambda x:x.get(sort_by, ""), reverse = (sort_order=="desc"))

    start = (page -1)*page_size                      #Apply pagination
    end = start + page_size
    paginated_cases = cases[start:end]

    return paginated_cases , total

def _filter_by_title(cases: list, title: str) -> list:
   
    return [
        case for case in cases
        if title.lower() in case["title"].lower()
    ]

def _filter_by_description(cases: list, description: str) -> list:
    
    return [
        case for case in cases
        if description.lower() in case["description"].lower()
    ]




