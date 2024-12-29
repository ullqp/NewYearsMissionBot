from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from database.orm_query import orm_get_user

class MenuCallBack(CallbackData, prefix="menu"):
    menu_name: str
    page: int = 1


def get_btns(*, callback: MenuCallBack, **kwargs):
    keyboard = InlineKeyboardBuilder()
    match callback.menu_name:
        case "main":
            btns = {
                "Начать игру": "ask_for_newgame",
                "Продолжить игру": "continue_game",
                "О нас": "about_us",
            }
        case "about_us":
            btns = {
                "Назад": "main",
            }
        case "ask_for_newgame":
            btns = {
                "Да": "prehistory_0",
                "Нет": "main",
            }
        case "ask_for_difficult":
            btns = {
                "Легкая": "easy_difficult",
                "Сложная": "hard_difficult",
                "В главное меню": "main"
            }
        case "prehistory_0":
            btns = {
                "—>": "prehistory_0",
                "В главное меню": "main",
            }
        case "prehistory_0_finish":
            btns = {
                "—>": "ask_for_difficult",
                "В главное меню": "main",
            }
        case "continue_game":
            btns = {
                "В главное меню": "main"
            }
        case "fork":
            btns = {
                "К оленям...": "game_finish",
                "В замок": "prehistory_1",
                "В горы": "prehistory_2",
                "В лес": "prehistory_3",
                "В главное меню": "main"
            }
        case "prehistory_1":
            btns = {
                "—>": "prehistory_1",
                "В главное меню": "main",
            }
        case "prehistory_2":
            btns = {
                "—>": "prehistory_2",
                "В главное меню": "main",
            }
        case "prehistory_3":
            btns = {
                "—>": "prehistory_3",
                "В главное меню": "main",
            }
        case "minigame_0_easy":
            btns = {
                "Проверить слово": "minigame_0_check",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        case "minigame_0_hard":
            btns = {
                "Проверить слово": "minigame_0_check",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        case "minigame_0_finish":
            btns = {
                "—>": "fork",
                "В главное меню": "main"
            }
        case "minigame_1":
            btns = {
                "кинуть снежок": "minigame_1_play",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        
        case "minigame_1_hit":
            btns = {
                "кинуть снежок": "minigame_1_play",
                "В главное меню": "main"
            }
        case "minigame_1_miss":
            btns = {
                "кинуть снежок": "minigame_1_play",
                "В главное меню": "main"
            }
        case "minigame_1_win":
            btns = {
                "—>": "fork",
                "В главное меню": "main"
            }
        case "minigame_1_lose":
            btns = {
                "по новой": "minigame_1",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        case "minigame_2_easy":
            btns = {
                "Проверить слово": "minigame_2_check",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        case "minigame_2_hard":
            btns = {
                "Проверить слово": "minigame_2_check",
                "Вернуться к развилке": "fork",
                "В главное меню": "main"
            }
        case "minigame_2_finish":
            btns = {
                "—>": "fork",
                "В главное меню": "main"
            }
        case "game_finish":
            btns = {
                "—>": "game_finish",
                "В главное меню": "main"
            }
    for text, menu_name in btns.items():
        keyboard.add(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    menu_name=menu_name
                ).pack()))
    return keyboard.adjust(1).as_markup()