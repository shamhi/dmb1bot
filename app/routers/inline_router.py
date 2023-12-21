from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from app.routers.functions import fn
from app.keyboards import ikb

inline_router = Router()


@inline_router.inline_query(F.query.regexp(r"^(?:\d{1,2}\.\d{2}\.\d{4}|\d{1,2}\.\d{1,2}\.\d{4})$"))
async def get_date(query: InlineQuery, state: FSMContext):
    date = fn.plus_year(query.query)

    check = fn.is_valid_date(date)
    if not check:
        results = [InlineQueryResultArticle(
            id='0',
            title='Bad query',
            description=f'Ваша дата {date} не действительна, попробуйте еще раз',
            input_message_content=InputTextMessageContent(
                message_text='Bad query'
            )
        )]
        return await query.answer(results=results)

    years, months, days, hours, minutes, seconds = fn.remaining_time(f'{date} 0:00:00')

    results = [InlineQueryResultArticle(
        id='0',
        title='До Дембеля осталось',
        description=f'{years} {"год" if 0 < years <= 4 else "лет"}, {months} месяцев, {days} дней, {hours} часов, {minutes} минут, {seconds} секунд',
        input_message_content=InputTextMessageContent(
            message_text=f'С `{fn.get_now()}` даты до Дембеля `{date}` осталось\n\n'
                         f'*_{years}_* {"год" if 0 < years <= 4 else "лет"}\n'
                         f'*_{months}_* месяцев\n'
                         f'*_{days}_* дней\n'
                         f'*_{hours}_* часов\n'
                         f'*_{minutes}_* минут\n'
                         f'*_{seconds}_* секунд\n\n'
                         f'Это составляет `61%` времени с призыва',
            parse_mode='markdownv2'
        ),
        reply_markup=ikb.get_main_kb(query.query)
    )]
    await query.answer(results=results)

    await state.update_data(date=date, query=query.query, current_kb='main')


@inline_router.callback_query(F.data == 'edit_total')
async def edit_total(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    date = state_data.get('date')
    query = state_data.get('query')
    kb = ikb.get_edited_kb(query)
    await fn.edit_total_text(bot, call.inline_message_id, date, kb)
    await state.update_data(current_kb='total')


@inline_router.callback_query(F.data == 'edit_main')
async def edit_main(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    date = state_data.get('date')
    query = state_data.get('query')
    kb = ikb.get_main_kb(query)
    await fn.edit_main_text(bot, call.inline_message_id, date, kb)
    await state.update_data(current_kb='main')


@inline_router.callback_query(F.data == 'update_date')
async def update_date(call: CallbackQuery, bot: Bot, state: FSMContext):
    state_data = await state.get_data()
    date = state_data.get('date')
    query = state_data.get('query')
    current_kb = state_data.get('current_kb')
    if current_kb == 'main':
        kb = ikb.get_main_kb(query)
        return await fn.edit_main_text(bot, call.inline_message_id, date, kb)
    elif current_kb == 'total':
        kb = ikb.get_edited_kb(query)
        return await fn.edit_total_text(bot, call.inline_message_id, date, kb)


@inline_router.inline_query()
async def no_check(query: InlineQuery):
    date = query.query
    results = [InlineQueryResultArticle(
        id='0',
        title='Usage',
        description='Usage: @dmb1bot [дата призыва (01.01.2021)]',
        input_message_content=InputTextMessageContent(
            message_text=f'`{date}` не является датой',
            parse_mode='markdownv2'
        )
    )]
    await query.answer(results=results)
