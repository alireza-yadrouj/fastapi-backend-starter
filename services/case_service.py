from fastapi import HTTPException
from repositories.case_repository import delete_case , update_case


def delete_case_service(case_id: int) -> None:
    deleted = delete_case(case_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

def update_case_service(case_id: int, data: dict) -> None:
    updated = update_case(case_id, data)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Case not found or no fields to update"
        )