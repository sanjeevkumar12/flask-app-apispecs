from typing import List

from ..extensions import db as base_db


class Model(base_db.Model):
    __abstract__ = True

    created_on = base_db.Column(base_db.DateTime, default=base_db.func.now())
    updated_on = base_db.Column(
        base_db.DateTime, default=base_db.func.now(), onupdate=base_db.func.now()
    )

    @classmethod
    def find_by_id(cls, _id) -> "Model":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["Model"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        base_db.session.add(self)
        base_db.session.commit()

    def delete_from_db(self) -> None:
        base_db.session.delete(self)
        base_db.session.commit()

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
