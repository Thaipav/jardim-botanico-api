from sqlalchemy.orm import Session

class Base:
    def __init__(self, db: Session):
        self.db = db