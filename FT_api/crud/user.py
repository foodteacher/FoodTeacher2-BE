from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from FT_api.crud.base import CRUDBase
from FT_api.models.user import User
from FT_api.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_social_id(self, db: Session, *, social_id: str) -> Optional[User]:
        return db.query(User).filter(User.user_social_id == social_id).first()

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
