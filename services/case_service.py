from fastapi import HTTPException
from repositories.case_repository import delete_case , update_case , get_cases_by_owner


def delete_case_service(case_id: int , owner_username : str) -> None:
    deleted = delete_case(case_id , owner_username)
    """
    Deletes a case by its ID.

    :param case_id: ID of the case to delete
    :return: None
    :raises HTTPException: If case is not found
    """
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

def update_case_service(case_id: int,owner_username : str, data: dict ) -> None:
    updated = update_case(case_id, data , owner_username)
    """
    Updates a case by its ID.

    :param case_id: ID of the case to update
    :param data: Case data to update (optional fields)
    :return: None
    :raises HTTPException: If the case is not found
    """
    if not updated:
        raise HTTPException(
            status_code=403,
            detail="Not allowed or case not found / no fields to update"
        )

def filter_cases(
        owner_username : str ,
        title:str|None = None , 
        description : str |None = None,
):
    """
    Filter cases based on optional criteria.

    :parm title:filter cases containing this title
    :param description: filter cases containing this description
    :return: list of filtered cases
    """

    cases = get_cases_by_owner(owner_username)
    
    if title:
        cases = _filter_by_title(cases, title)

    if description:
        cases = _filter_by_description(cases, description)

    return cases


def _filter_by_title(cases: list, title: str) -> list:
    """
    Filter cases by title.
    """
    return [
        case for case in cases
        if title.lower() in case["title"].lower()
    ]


def _filter_by_description(cases: list, description: str) -> list:
    """
    Filter cases by description.
    """
    return [
        case for case in cases
        if description.lower() in case["description"].lower()
    ]
