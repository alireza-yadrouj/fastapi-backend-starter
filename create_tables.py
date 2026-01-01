from database import engine
from models.user import User
from models.case import Case


User.metadata.create_all(bind=engine)
Case.metadata.create_all(bind=engine)


