from aiogram import Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from database import add_user, user_exists, update_user_settings



router = Router()


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать задачу"), KeyboardButton(text="Список задач")],
            [KeyboardButton(text="Отмена")],
        ],
        resize_keyboard=True
    )


def priority_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Низкий", callback_data="priority_low")],
            [InlineKeyboardButton(text="Средний", callback_data="priority_medium")],
            [InlineKeyboardButton(text="Высокий", callback_data="priority_high")],
        ]
    )
    return keyboard


def category_keyboard(categories: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(InlineKeyboardButton(text=category, callback_data=f"category_{category}"))
    keyboard.add(InlineKeyboardButton(text="Добавить новую категорию", callback_data="add_new_category"))
    return keyboard


@router.message(CommandStart())
async def statr(message: Message):
    if user_exists(message.from_user.id):
        await message.answer(
            text=(
                f"Добро пожаловать снова, {message.from_user.first_name}!\n"
                "Ваши данные уже есть в системе.\n\n"
                "Вы можете начать работу с помощью команд или меню."
            ),
            reply_markup=main_keyboard()
        )
    else:
        # Добавляем нового пользователя
        add_user(
            username=message.from_user.username or "Неизвестный",
            telegram_id=message.from_user.id,
        )
        await message.answer(
            text=(
                f"Привет, {message.from_user.first_name}!\n"
                "Вы успешно зарегистрированы в системе.\n\n"
                "Используйте команды или меню для управления своими задачами."
            ),
            reply_markup=main_keyboard()
        )