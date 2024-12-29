

import math
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import (
    Banner,
    Image,
    User,
    Slide
)

# Простой пагинатор
class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError('Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError('Previous page does not exist. Use has_previous() to check before.')



# orm get // получение данных из БД

async def orm_get_banner(session: AsyncSession, name: str):
    query = select(Banner).where(Banner.name == name)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_slide(session: AsyncSession, name: str):
    query = select(Slide).where(Slide.name == name)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_slides(session: AsyncSession, name: str):
    query = select(Slide).where(Slide.name == name)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_image(session: AsyncSession, id: int):
    query = select(Image).where(Image.id == id)
    result = await session.execute(query)
    return result.scalar()

async def orm_get_all_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_user(session: AsyncSession, telegram_id: int):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    return result.scalar()

# orm save // сохранение данных в БД

async def orm_save_user(session: AsyncSession, user: User):
    session.add(user)
    await session.commit()