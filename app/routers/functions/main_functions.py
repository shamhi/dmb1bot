from datetime import datetime


def remaining_time(target_date):
    target_datetime = datetime.strptime(target_date, "%d.%m.%Y %H:%M:%S")
    current_datetime = datetime.now()

    remaining_time = target_datetime - current_datetime

    years = abs(remaining_time.days // 365)
    months = (remaining_time.days % 365) // 30
    days = (remaining_time.days % 365) % 30
    hours = remaining_time.seconds // 3600
    minutes = (remaining_time.seconds % 3600) // 60
    seconds = (remaining_time.seconds % 3600) % 60

    return years, months, days, hours, minutes, seconds


def remaining_total_time(target_date):
    target_datetime = datetime.strptime(target_date, "%d.%m.%Y %H:%M:%S")
    current_datetime = datetime.now()

    remaining_time = target_datetime - current_datetime

    total_weeks = abs(remaining_time.days // 7)
    total_days = abs(remaining_time.days)
    total_hours = abs(round(remaining_time.total_seconds() // 3600))
    total_minutes = abs(round(remaining_time.total_seconds() // 60))
    total_seconds = abs(round(remaining_time.total_seconds()))

    return total_weeks, total_days, total_hours, total_minutes, total_seconds


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def get_now():
    return datetime.now().strftime('%d.%m.%Y')


def plus_year(date: str):
    return date.replace(date[-4:], str(int(date[-4:]) + 1))


async def edit_main_text(bot, inline_msg_id, date, kb):
    try:
        years, months, days, hours, minutes, seconds = remaining_time(f'{date} 0:00:00')
        return await bot.edit_message_text(inline_message_id=inline_msg_id,
                                           text=f'{"ㅤ" * 2}С `{get_now()}` даты до Дембеля `{date}` осталось{"ㅤ" * 2}\n'
                                                f'{"ㅤ" * 13}*_{years}_* {"год" if 0 < years <= 4 else "лет"}\n'
                                                f'{"ㅤ" * 12}*_{months}_* месяцев\n'
                                                f'{"ㅤ" * 13}*_{days}_* дней\n'
                                                f'{"ㅤ" * 13}*_{hours}_* часов\n'
                                                f'{"ㅤ" * 13}*_{minutes}_* минут\n'
                                                f'{"ㅤ" * 13}*_{seconds}_* секунд\n\n'
                                                f'{"ㅤ" * 5}Это составляет `61%` времени с призыва',
                                           reply_markup=kb, parse_mode='markdownv2')
    except:
        ...


async def edit_total_text(bot, inline_msg_id, date, kb):
    try:
        total_weeks, total_days, total_hours, total_minutes, total_seconds = remaining_total_time(f'{date} 0:00:00')
        return await bot.edit_message_text(inline_message_id=inline_msg_id,
                                           text=f'{"ㅤ" * 2}С `{get_now()}` даты до Дембеля `{date}` осталось{"ㅤ" * 2}\n'
                                                f'{"ㅤ" * 14}ВСЕГО\n'
                                                f'{"ㅤ" * 13}*_{total_weeks}_* недель\n'
                                                f'{"ㅤ" * 13}*_{total_days}_* дней\n'
                                                f'{"ㅤ" * 12}*_{total_hours}_* часов\n'
                                                f'{"ㅤ" * 12}*_{total_minutes}_* минут\n'
                                                f'{"ㅤ" * 12}*_{total_seconds}_* секунд\n\n'
                                                f'{"ㅤ" * 5}Это составляет `61%` времени с призыва',
                                           reply_markup=kb, parse_mode='markdownv2')
    except:
        ...
