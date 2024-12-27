import sys
from typing import List, TypeVar
from sqlalchemy import select
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from .schemas.schemas import InputModel
from fastapi.encoders import jsonable_encoder
from .exceptions import NotFoundException

T = TypeVar('T')

def get_by_id(db: Session, model: DeclarativeMeta, id: int, **kwargs) -> T:
    """ Get element by id with filters"""
    data = db.get(model, id)
    # data = query.get(id)
    if hasattr(model, "enable") and "active" not in kwargs:
        if data.enable == False:
            data = None
    elif hasattr(model, "enable") and "active" in kwargs:
        # TODO hacer cuando viene l parametro enable = True, False, Any
        if kwargs["active"] == True:
            data = None
    if data == None:
        raise NotFoundException(f"{model.__tablename__} not found").with_traceback(sys.exc_info()[2])
    return data

def get_by_date_range(db: Session, model: DeclarativeMeta, start_date: str, end_date: str) -> List[T]:
    query = db.query(model).filter(model.date.between(start_date, end_date))
    return query.all()

async def create(db: Session, model: DeclarativeMeta, data: InputModel) -> T:
    new_data = [model(**item.__dict__) for item in data]
    inserted_data = db.add_all(new_data)
    await db.commit()
    return new_data

def flush(db: Session, model: DeclarativeMeta, data: InputModel) -> T:
    new_data = model(**data.__dict__)
    db.add(new_data)
    db.flush()
    return new_data

def patch(db: Session, model: DeclarativeMeta, id: int, data: InputModel) -> T:
    existing_data = db.query(model).get(id)
    schema = jsonable_encoder(existing_data)
    update = data.model_dump(exclude_unset=True)
    for field in schema:
        if field in update:
            setattr(existing_data, field, update[field])
    db.add(existing_data)
    db.commit()
    db.refresh(existing_data)
    return existing_data

def delete(db: Session, model: DeclarativeMeta, id: int) -> T:
    data = db.query(model).get(id)

    # if data.enable is True or data.enable is None:
    #     data.enable = False
    # db.add(data)
    # db.commit()
    # db.refresh(data)
    # return data

    if data:
        db.delete(data)
        db.commit()
    return data

def delete_relations(db: Session, model: DeclarativeMeta, **kwargs) -> T:
    data = db.query(model).filter_by(**kwargs).first()

    if data:
        db.delete(data)
        db.commit()

    return data

async def bulk_qry(db: AsyncSession, model: DeclarativeMeta, data1: list, ask_column: str, data2: list = None, ask_column_2: str = None):
    if ask_column_2:
        qry = select(model).where(getattr(model, ask_column).in_(data1), getattr(model, ask_column_2).in_(data2))
        return await db.execute(qry)
    else:
        qry = select(model).where(getattr(model, ask_column).in_(data1))
        return await db.execute(qry)

async def get_all(db: AsyncSession, model: DeclarativeMeta):
    result = await db.execute(select(model))
    return result.unique().scalars().all()

def model_to_dict(model_instance):
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}