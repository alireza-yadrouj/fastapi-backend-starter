from fastapi import HTTPException
from repositories.case_repository import delete_case , update_case


def delete_case_service(case_id: int) -> None:
    deleted = delete_case(case_id)
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

def update_case_service(case_id: int, data: dict) -> None:
    updated = update_case(case_id, data)
    """
    Updates a case by its ID.

    :param case_id: ID of the case to update
    :param data: Case data to update (optional fields)
    :return: None
    :raises HTTPException: If the case is not found
    """
    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Case not found or no fields to update"
        )

