from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_kb(query):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Всего', callback_data='edit_total')],
        [InlineKeyboardButton(text='Обновить', callback_data='update_date')],
        [InlineKeyboardButton(text='Fork', switch_inline_query_current_chat=query)]
    ])
    return kb

def get_edited_kb(query):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Классический', callback_data='edit_main')],
        [InlineKeyboardButton(text='Обновить', callback_data='update_date')],
        [InlineKeyboardButton(text='Fork', switch_inline_query_current_chat=query)]
    ])
    return kb
