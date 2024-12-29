from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import InputMediaPhoto
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.orm_query import (
    orm_get_banner,
    orm_get_image,
    orm_get_user,
    orm_get_slides,
    orm_save_user,
    orm_get_slide
)

from kbds.inline import (
    MenuCallBack,
    get_btns
)

from random import randint


class Game(StatesGroup):
    minigame_0 = State()
    minigame_1 = State()
    minigame_2 = State()


async def menu(session, menu_name):
    banner = await orm_get_banner(session=session, name=menu_name)
    banner_image = await orm_get_image(session=session, id=banner.image_id)
    image = InputMediaPhoto(media=banner_image.data, caption=banner.text)

    kbds = get_btns(callback=MenuCallBack(menu_name=menu_name))

    return image, kbds

async def prehistory_0(session, telegram_id):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    slides = await orm_get_slides(session=session, name="prehistory_0")
    
    if (user.game_state != 1):
        user.last_index = 0
        user.game_state = 1
    index = user.last_index
    if len(slides) == user.last_index:
        user.last_index = 0
        user.game_state = 2
        return await menu(session, "ask_for_difficult")
        
    user.last_index += 1
    await orm_save_user(session=session, user=user)
    
    slide = slides[index]
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)

    kbds = get_btns(callback=MenuCallBack(menu_name="prehistory_0"))

    return image, kbds

async def prehistory_1(session, telegram_id, state):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    slides = await orm_get_slides(session=session, name="prehistory_1")
    
    if user.loc1:
        return await fork(session, telegram_id)
    
    if (user.game_state != 4):
        user.last_index = 0
        user.game_state = 4
    index = user.last_index
    if len(slides) == user.last_index:
        user.last_index = 0
        user.game_state = 5
        return await minigame_0(session, telegram_id, state) # minigame 1
        
    user.last_index += 1
    await orm_save_user(session=session, user=user)
    
    slide = slides[index]
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)

    kbds = get_btns(callback=MenuCallBack(menu_name="prehistory_1"))

    return image, kbds

async def prehistory_2(session, telegram_id, state):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    slides = await orm_get_slides(session=session, name="prehistory_2")
    
    #if user.loc2: # возврат на вилку если игрок уже поиграл в снежки
    #    return await fork(session, telegram_id)
    
    if (user.game_state != 6):
        user.last_index = 0
        user.game_state = 6
    index = user.last_index
    if len(slides) == user.last_index:
        user.last_index = 0
        user.game_state = 7
        return await minigame_1(session, telegram_id, state) # minigame 2
        
    user.last_index += 1
    await orm_save_user(session=session, user=user)
    
    slide = slides[index]
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)

    kbds = get_btns(callback=MenuCallBack(menu_name="prehistory_2"))

    return image, kbds

async def prehistory_3(session, telegram_id, state):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    slides = await orm_get_slides(session=session, name="prehistory_3")
    
    if user.loc3:
        return await fork(session, telegram_id)
    
    if (user.game_state != 8):
        user.last_index = 0
        user.game_state = 8
    index = user.last_index
    if len(slides) == user.last_index:
        user.last_index = 0
        user.game_state = 9
        return await minigame_2(session, telegram_id, state) # minigame 3
        
    user.last_index += 1
    await orm_save_user(session=session, user=user)
    
    slide = slides[index]
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)

    kbds = get_btns(callback=MenuCallBack(menu_name="prehistory_3"))

    return image, kbds

async def fork(session, telegram_id):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    if user.last_index != 0:
        user.last_index = 0
    user.game_state = 3
    await orm_save_user(session=session, user=user)
    
    slide = await orm_get_slide(session=session, name="fork")
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)
    
    kbds = get_btns(callback=MenuCallBack(menu_name="fork"))
    
    return image, kbds

async def minigame_0(session, telegram_id, state):
    await state.set_state(Game.minigame_0)
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    if user.difficult_id == 1:
        return await menu(session, "minigame_0_easy")
    
    # print(await state.get_data())
    return await menu(session, "minigame_0_hard")

async def minigame_0_check(session, telegram_id, state):
    data = await state.get_data()
    if not data.get("minigame_0_word"):
        return await minigame_0(session, telegram_id, state)
    word = data.get("minigame_0_word")
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    
    if user.difficult_id == 1:
        banner = await orm_get_banner(session=session, name="minigame_0_easy")
    else:
        banner = await orm_get_banner(session=session, name="minigame_0_hard")
    if word == banner.description:
        await state.clear()
        user.game_state = 3
        user.score += 1
        user.loc1 = True
        await orm_save_user(session=session, user=user)
        return await menu(session, "minigame_0_finish")
    return await minigame_0(session, telegram_id, state)

async def minigame_1(session, telegram_id, state):
    await state.set_state(Game.minigame_1)
    await state.update_data(minigame_1_plays=0, minigame_1_wins=0)
    
    return await menu(session, "minigame_1")

async def minigame_1_play(session, telegram_id, state):
    data = await state.get_data()
    if not data.get("minigame_1_plays") or not data.get("minigame_1_wins"):
        await state.update_data(minigame_1_plays=0, minigame_1_wins=0)
        data = await state.get_data()
    plays = data.get("minigame_1_plays")
    wins = data.get("minigame_1_wins")
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    if plays > 2:
        if wins == 3:
            user.game_state = 3
            user.score += 1
            user.loc2 = True
            await orm_save_user(session=session, user=user)
            return await menu(session, "minigame_1_win")
        return await menu(session, "minigame_1_lose")
    
    await state.update_data(minigame_1_plays=plays+1)
    
    if user.difficult_id == 1:
        chance = 60
    else:
        chance = 35
    if randint(0,100) < chance:
        ans = await menu(session, "minigame_1_hit")
        if wins+1 > 1:
            ans[0].caption = ans[0].caption + f" x{wins+1}"
        await state.update_data(minigame_1_wins=wins+1)
        return ans
    
    ans = await menu(session, "minigame_1_miss")
    if plays+1-wins > 1:
        ans[0].caption = ans[0].caption + f" x{plays+1-wins}"
    return ans

async def minigame_2(session, telegram_id, state):
    await state.set_state(Game.minigame_2)
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    if user.difficult_id == 1:
        return await menu(session, "minigame_2_easy")
    return await menu(session, "minigame_2_hard")

async def minigame_2_check(session, telegram_id, state):
    data = await state.get_data()
    if not data.get("minigame_2_word"):
        return await minigame_2(session, telegram_id, state)
    word = data.get("minigame_2_word")
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    if user.difficult_id == 1:
        banner = await orm_get_banner(session=session, name="minigame_2_easy")
    else:
        banner = await orm_get_banner(session=session, name="minigame_2_hard")
    if word == banner.description:
        await state.clear()
        user.game_state = 3
        user.score += 1
        user.loc3 = True
        await orm_save_user(session=session, user=user)
        return await menu(session, "minigame_2_finish")
    return await minigame_2(session, telegram_id, state)

async def game_finish(session, telegram_id, state):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    slides = await orm_get_slides(session=session, name="game_finish")
    
    if not user.loc1 or not user.loc2 or not user.loc3:
        return await fork(session, telegram_id)
    
    if (user.game_state != 10):
        user.last_index = 0
        user.game_state = 10
    index = user.last_index
    if len(slides) == user.last_index:
        user.score = 0
        user.last_index = 0 
        user.game_state = 0
        user.difficult_id = None
        user.loc1 = None
        user.loc2 = None
        user.loc3 = None
        await orm_save_user(session=session, user=user)
        return await menu(session, "main")
        
    user.last_index += 1
    await orm_save_user(session=session, user=user)
    
    slide = slides[index]
    slide_image = await orm_get_image(session=session, id=slide.image_id)
    image = InputMediaPhoto(media=slide_image.data, caption=slide.text)

    kbds = get_btns(callback=MenuCallBack(menu_name="game_finish"))

    return image, kbds

async def continue_game(session, telegram_id, state):
    user = await orm_get_user(session=session, telegram_id=telegram_id)
    
    match user.game_state:
        case 1:
            return await prehistory_0(session, telegram_id)
        case 2:
            return await menu(session, "ask_for_difficult")
        case 3:
            return await fork(session, telegram_id)
        case 4:
            return await prehistory_1(session, telegram_id, state)
        case 5:
            return await minigame_0(session, telegram_id, state) # minigame 1
        case 6:
            return await prehistory_2(session, telegram_id, state)
        case 7:
            return await minigame_1(session, telegram_id, state) # minigame 2
        case 8:
            return await prehistory_3(session, telegram_id, state)
        case 9:
            return await minigame_2(session, telegram_id, state) # minigame 3
        case 10:
            return await game_finish(session, telegram_id, state)
        case _:
            return await menu(session, "main")

"""
async def choose(session, level, menu_name):

    banner = await orm_get_banner(session, menu_name)
    image = InputMediaPhoto(media=banner.image, caption=banner.description)

    difficulties = await orm_get_difficulties(session)
    kbds = get_user_difficult_btns(level=level, difficulties=difficulties)

    return image, kbds


def pages(paginator: Paginator):
    btns = dict()
    if paginator.has_previous():
        btns["назад"] = "previous"

    if paginator.has_next():
        btns["вперёд"] = "next"

    return btns


async def slides(session, level, page):
    slides = await orm_get_slides(session)

    paginator = Paginator(slides, page=page)
    slide = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=slide.image,
        caption=f"\
                {slide.desription}\n\
                {paginator.page} из {paginator.pages}",
    )

    pagination_btns = pages(paginator)

    kbds = get_slides_btns(
        level=level,
        page=page,
        pagination_btns=pagination_btns,
    )

    return image, kbds
"""

async def get_menu_content(
        session: AsyncSession,
        callback: types.CallbackQuery | types.Message,
        callback_menu: MenuCallBack,
        state: FSMContext | None = None
):
    #print(session, callback, callback_menu, state, sep="\n")
    print("\n"*5,callback_menu,"\n"*5)
    user = await orm_get_user(session=session, telegram_id=callback.from_user.id)
    match callback_menu.menu_name:
        case "main":
            return await menu(session, callback_menu.menu_name)
        case "about_us":
            return await menu(session, callback_menu.menu_name)
        case "continue_game":
            return await continue_game(session, callback.from_user.id, state)
        
        case "ask_for_newgame":
            return await menu(session, callback_menu.menu_name)
        
        case "prehistory_0": # gamestate 1
            user.difficult_id = None
            user.score = 0
            user.loc1 = None
            user.loc2 = None
            user.loc3 = None
            await orm_save_user(session=session, user=user)
            return await prehistory_0(session, callback.from_user.id)
        
        case "ask_for_difficult": # gamestate 2
            return await menu(session, callback_menu.menu_name)
        
        case "easy_difficult": # gamestate 3
            user.difficult_id = 1
            await orm_save_user(session=session, user=user)
            return await fork(session, callback.from_user.id)
        case "hard_difficult": # gamestate 3
            user.difficult_id = 2
            await orm_save_user(session=session, user=user)
            return await fork(session, callback.from_user.id)

        case "fork":
            return await fork(session, callback.from_user.id)

        case "prehistory_1": # gamestate 4
            return await prehistory_1(session, callback.from_user.id, state)
        case "prehistory_2": # gamestate 6
            return await prehistory_2(session, callback.from_user.id, state)
        case "prehistory_3": # gamestate 8
            return await prehistory_3(session, callback.from_user.id, state)

        case "minigame_0": # gamestate 5
            return await minigame_0(session, callback.from_user.id, state)
        case "minigame_0_check":
            return await minigame_0_check(session, callback.from_user.id, state)

        case "minigame_1":
            return await minigame_1(session, callback.from_user.id, state)
        case "minigame_1_play":
            return await minigame_1_play(session, callback.from_user.id, state)
        
        case "minigame_2":
            return await minigame_2(session, callback.from_user.id, state)
        case "minigame_2_check":
            return await minigame_2_check(session, callback.from_user.id, state)

        case "game_finish":
            return await game_finish(session, callback.from_user.id, state)