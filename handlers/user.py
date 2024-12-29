from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.orm_query import (
    orm_get_user,
    orm_get_all_users,
    orm_save_user
)
from handlers.menu_processing import get_menu_content, Game
from kbds.inline import MenuCallBack

user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    if not await orm_get_user(session=session, telegram_id=message.from_user.id):
        user = User(id=len(await orm_get_all_users(session=session)),telegram_id=message.from_user.id)
        await orm_save_user(session=session, user=user)
    
    media, reply_markup = await get_menu_content(session,callback=message,callback_menu=MenuCallBack(menu_name="main"))

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


@user_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession, state=FSMContext):
    user = await orm_get_user(session=session, telegram_id=callback.from_user.id)
    match callback_data.menu_name:
        case "prehistory_1":
            if user.loc1:
                return await callback.answer("Вы уже побывали там", show_alert=True)
        case "prehistory_3":
            if user.loc3:
                return await callback.answer("Вы уже побывали там", show_alert=True)
        case "game_finish":
            if not user.loc1 or not user.loc2 or not user.loc3:
                return await callback.answer("Вы еще не везде побывали", show_alert=True)
        case "continue_game":
            if user.game_state == 0:
                return await callback.answer("Вы еще не начали игру", show_alert=True)
    
    media, reply_markup = await get_menu_content(session,callback=callback,callback_menu=callback_data,state=state)
    
    await callback.message.edit_media(media=media, reply_markup=reply_markup)
    await callback.answer()


@user_router.message(Game.minigame_0)
async def minigame_0(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(minigame_0_word=message.text.lower())
    await message.delete()

@user_router.message(Game.minigame_2)
async def minigame_2(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(minigame_2_word=message.text.lower())
    await message.delete()