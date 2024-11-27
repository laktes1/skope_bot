from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
import re
import logging
from keyboards.keyboard import reply_keyboard, keyboard_manager

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Словарь для хранения состояний пользователей
user_states = {}  # {user_id: "waiting_for_phone_number"}


class UserHandler:
    def __init__(self, router: Router):
        self.router = router
        self.setup_routes()

    def setup_routes(self):
        self.router.message(F.text == "Привет")(self.greet_user)
        self.router.message(F.text == "Manager")(self.show_manager)
        self.router.callback_query(F.data == "find_user")(self.find_user)
        self.router.message()(self.handle_message)

    async def greet_user(self, message: Message):
        logger.info(f"User {message.from_user.id} sent a greeting message.")
        await message.answer(
            f"Привет, {message.from_user.first_name}!\nВыберите раздел:",
            reply_markup=reply_keyboard
        )

    async def show_manager(self, message: Message):
        logger.info(f"User {message.from_user.id} entered the 'Manager' section.")
        await message.answer(
            "Вы вошли в раздел Manager.\nВыберите действие:",
            reply_markup=keyboard_manager
        )

    async def find_user(self, callback: CallbackQuery):
        user_id = callback.from_user.id
        logger.info(f"User {user_id} clicked 'Find user'.")

        # Устанавливаем состояние для пользователя
        user_states[user_id] = "waiting_for_phone_number"
        logger.info(f"State set for user {user_id}: waiting_for_phone_number")

        await callback.message.answer("Введите номер телефона пользователя в формате +79998887766:")
        await callback.answer()

    async def handle_message(self, message: Message):
        user_id = message.from_user.id

        # Проверяем текущее состояние пользователя
        user_state = user_states.get(user_id)
        logger.info(f"User {user_id} current state: {user_state}")

        if user_state == "waiting_for_phone_number":
            await self.handle_phone_number(message)
        else:
            await message.answer(
                "Я не понимаю этого запроса. Пожалуйста, выберите действие из меню.",
                reply_markup=reply_keyboard
            )

    async def handle_phone_number(self, message: Message):
        user_id = message.from_user.id
        phone_number = message.text
        logger.info(f"User {user_id} provided phone number: {phone_number}")

        # Регулярное выражение для проверки номера телефона
        phone_regex = r"^\+7\d{10}$"
        if re.match(phone_regex, phone_number):
            logger.info(f"Phone number {phone_number} accepted from user {user_id}.")
            await message.answer(f"Номер телефона принят: {phone_number}")

            # Сбрасываем состояние пользователя
            user_states.pop(user_id, None)
            logger.info(f"State cleared for user {user_id}")

            # Отображаем основное меню
            await message.answer("Теперь вы можете выбрать раздел:", reply_markup=reply_keyboard)
        else:
            logger.warning(f"Invalid phone number format received from user {user_id}: {phone_number}")
            await message.answer(
                "Неверный формат номера телефона. Попробуйте снова. Пример: +79998887766"
            )
