from sqlalchemy.orm import Session
from models.case import Case
from schemas.case import CaseCreate

def create_case(db: Session, data:CaseCreate, owner_username: str):
    case = Case(
        title=data["title"],
        description=data["description"],
        owner_username=owner_username
    )
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

def get_all_cases(db: Session):
    return db.query(Case).all()

def get_cases_by_owner(db: Session, owner_username: str):
    return db.query(Case).filter(Case.owner_username == owner_username).all()

def update_case(db: Session, case_id: int, update_data: dict, owner_username: str) -> Case | None:
    case = db.query(Case).filter(
        Case.id == case_id,
        Case.owner_username == owner_username
    ).first()
    if not case:
        return None

    for key, value in update_data.items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)
    return case

def delete_case(db: Session, case_id: int, owner_username: str) -> bool:
    case = db.query(Case).filter(
        Case.id == case_id,
        Case.owner_username == owner_username
    ).first()
    if not case:
        return False

    db.delete(case)
    db.commit()
    return True

def delete_case_admin(db:Session, case_id:int ) -> bool:
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        return False
    
    db.delete(case)
    db.commit()
    return True

def update_case_admin(db:Session, case_id: int, data: dict) -> Case | None:
    case = db.query(Case).filter(Case.id==case_id).first()
    if not case:
        return None
    for key, value in data.items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)
    return case

