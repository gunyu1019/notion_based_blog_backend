import datetime
from typing import Sequence

from sqlalchemy.sql import select

from repository.base_repository import BaseRepository


class PostRepository(BaseRepository):
    # async def get_meal(
    #         self,
    #         building: list[Building],
    #         date: datetime.date
    # ) -> Sequence[MealInfo]:
    #     query = select(MealInfo).where(MealInfo.date == date).where(MealInfo.building.in_(building))
    #     result = await self._session.execute(query)
    #     return result.scalars().all()
    pass
