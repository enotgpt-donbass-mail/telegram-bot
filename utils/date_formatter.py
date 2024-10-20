import datetime
import re


def format_custom_date(date):
    suffix = 'T00:00:00.000Z'
    today = datetime.date.today()

    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }

    print(date)

    match date:
        case 'Сегодня':
            return f'{today.strftime("%Y-%m-%d")}{suffix}'
        case 'Завтра':
            next_day = today + datetime.timedelta(days=1)
            return f'{next_day.strftime("%Y-%m-%d")}{suffix}'
        case 'Послезавтра':
            next_day = today + datetime.timedelta(days=2)
            return f'{next_day.strftime("%Y-%m-%d")}{suffix}'

    reverse_months = {v: k for k, v in months.items()}

    match = re.match(r"(\d+) (.+)", date)

    day = int(match.group(1))
    month_name = match.group(2)
    month = reverse_months[month_name]

    current_year = datetime.date.today().year
    date_object = datetime.date(current_year, month, day)

    formatted_date = date_object.strftime("%Y-%m-%d")
    return f'{formatted_date}{suffix}'
