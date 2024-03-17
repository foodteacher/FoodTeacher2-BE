from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.user_info import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_kakao_id(self, db: Session, *, kakao_id: str) -> Optional[User]:
        return db.query(User).filter(User.kakao_id == kakao_id).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(**obj_in.model_dump(exclude_unset=True))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def remove_field(self, db: Session, *, db_obj: User, field: str) -> Optional[User]:
        if db_obj:
            if hasattr(db_obj, field):
                setattr(db_obj, field, "")
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            return db_obj
        return None

crud_user = CRUDUser(User)
