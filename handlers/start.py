from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards.keyboard import reply_keyboard

start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет ' + message.from_user.first_name,
                         reply_markup=reply_keyboard)