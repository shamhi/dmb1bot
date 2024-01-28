import math
import calendar
from datetime import datetime


def remaining_time(target_date):
    target_datetime = datetime.strptime(target_date, "%d.%m.%Y %H:%M:%S")
    current_datetime = datetime.now()

    remaining_time = target_datetime - current_datetime
    year_seconds = 31536000 if not calendar.isleap(target_datetime.year-1) else 31622400

    years = abs(remaining_time.days // 365)
    months = (remaining_time.days % 365) // 30
    days = (remaining_time.days % 365) % 30
    hours = remaining_time.seconds // 3600
    minutes = (remaining_time.seconds % 3600) // 60
    seconds = (remaining_time.seconds % 3600) % 60
    percent = abs(math.floor(100 - ((abs(round(remaining_time.total_seconds())) / year_seconds) * 100)))

    return years, months, days, hours, minutes, seconds, percent


def remaining_total_time(target_date):
    target_datetime = datetime.strptime(target_date, "%d.%m.%Y %H:%M:%S")
    current_datetime = datetime.now()

    remaining_time = target_datetime - current_datetime
    year_seconds = 31536000 if not calendar.isleap(target_datetime.year-1) else 31622400

    total_weeks = abs(remaining_time.days // 7)
    total_days = abs(remaining_time.days)
    total_hours = abs(round(remaining_time.total_seconds() // 3600))
    total_minutes = abs(round(remaining_time.total_seconds() // 60))
    total_seconds = abs(round(remaining_time.total_seconds()))
    percent = abs(math.floor(100 - ((total_seconds / year_seconds) * 100)))

    return total_weeks, total_days, total_hours, total_minutes, total_seconds, percent


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
        years, months, days, hours, minutes, seconds, percent = remaining_time(f'{date} 0:00:00')
        return await bot.edit_message_text(inline_message_id=inline_msg_id,
                                           text=f'С `{get_now()}` даты до Дембеля `{date}` осталось\n\n'
                                                f'```json\n'
                                                '{\n'
                                                f'    "{"Год" if 0 < years <= 4 else "Лет"}": {years} \n'
                                                f'    "Месяцев": {months}\n'
                                                f'    "Дней": {days}\n'
                                                f'    "Часов": {hours}\n'
                                                f'    "Минут": {minutes}\n'
                                                f'    "Секунд": {seconds}\n'
                                                '}\n'
                                                f'```\n\n'
                                                f'Это составляет `{percent}%` времени с призыва',
                                           reply_markup=kb, parse_mode='markdownv2')
    except:
        ...


async def edit_total_text(bot, inline_msg_id, date, kb):
    try:
        total_weeks, total_days, total_hours, total_minutes, total_seconds, percent \
            = remaining_total_time(f'{date} 0:00:00')
        return await bot.edit_message_text(inline_message_id=inline_msg_id,
                                           text=f'С `{get_now()}` даты до Дембеля `{date}` осталось\n\n'
                                                f'```json\n'
                                                '{\n'
                                                f'    "Недель": {total_weeks}\n'
                                                f'    "Дней": {total_days}\n'
                                                f'    "Часов": {total_hours}\n'
                                                f'    "Минут": {total_minutes}\n'
                                                f'    "Секунд": {total_seconds}\n'
                                                '}\n'
                                                f'```\n\n'
                                                f'Это составляет `{percent}%` времени с призыва',
                                           reply_markup=kb, parse_mode='markdownv2')
    except:
        ...
