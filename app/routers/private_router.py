from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.filters import ChatTypeFilter
from app.routers.functions import fn
from app.keyboards import ikb

private_router = Router()


private_router.message.register(ChatTypeFilter('private'))


@private_router.message(CommandStart())
async def main_handler(message: Message):
    kb = ikb.get_switch_inline_kb(fn.get_now())
    await message.answer(text=r'Бот работает *только* в инлайн режиме\!\!\!', reply_markup=kb, parse_mode='markdownv2')
