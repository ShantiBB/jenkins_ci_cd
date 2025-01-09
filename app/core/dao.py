from sqlalchemy import delete, select, update

from .database.db_helper import AsyncSessionDep


class BaseModelDAO:
    model = None

    @classmethod
    async def create(
        cls,
        session: AsyncSessionDep,
        **kwargs,
    ):
        obj = cls.model(**kwargs)
        session.add(obj)
        await session.commit()
        return obj

    @classmethod
    async def update(
        cls,
        obj_id: int,
        session: AsyncSessionDep,
        **kwargs,
    ) -> bool:
        stmt = update(cls.model).filter_by(id=obj_id).values(**kwargs)
        res = await session.execute(stmt)
        await session.commit()
        return res.rowcount > 0

    @classmethod
    async def delete(cls, obj_id: int, session: AsyncSessionDep) -> bool:
        stmt = delete(cls.model).filter_by(id=id)
        res = await session.execute(stmt)
        await session.commit()
        return res.rowcount > 0

    @classmethod
    async def get_by_id(
        cls,
        obj_id: int,
        session: AsyncSessionDep,
    ):
        obj = await session.get(cls.model, obj_id)
        return obj

    @classmethod
    async def get_all(cls, session: AsyncSessionDep):
        objs = select(cls.model)
        res = await session.execute(objs)
        return res.scalars().all()
