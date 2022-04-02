import re
from datetime import datetime


def parse_message(text: str) -> dict:
    template = re.compile(r'^(\d{1,2}).?(\d{2})\s?\D?\s?(\d{1,2}).?(\d{2})\s(.+)$')
    match = template.match(text)

    parsed_dict = {
        'start_time': None,
        'start_minute': None,
        'end_hour': None,
        'end_minute': None,
        'text': None
    }

    if match is not None:
        parsed_dict = {
            'start_hour': int(match.group(1)),
            'start_minute': int(match.group(2)),
            'end_hour': int(match.group(3)),
            'end_minute': int(match.group(4)),
            'text': match.group(5)
        }

    else:
        parsed_dict = {
            'start_hour': None,
            'start_minute': None,
            'end_hour': None,
            'end_minute': None,
            'text': text
        }

    return parsed_dict


def sanitize_message(parsed_dict: dict) -> dict:

    error = None
    now = datetime.now()

    if parsed_dict['start_hour'] is not None:
        if parsed_dict['start_hour'] < 0 or parsed_dict['start_hour'] > 23 or parsed_dict['end_hour'] < 0 or parsed_dict['end_hour'] > 23:
            error = 'Неверное значение часов. Ничего не записано'

        if parsed_dict['start_minute'] < 0 or parsed_dict['start_minute'] > 59 or parsed_dict['end_minute'] < 0 or parsed_dict['end_minute'] > 59:
            error = 'Неверное значение минут. Ничего не записано'

        if parsed_dict['start_hour'] > parsed_dict['end_hour']:
            error = 'Час начала больше часа окончания. Ничего не записано'

        if parsed_dict['start_hour'] == parsed_dict['end_hour'] and parsed_dict['start_minute'] > parsed_dict['end_minute']:
            error = 'Минута начала больше минуты окончания. Ничего не записано'
    else:
        parsed_dict['end_hour'] = now.hour
        parsed_dict['end_minute'] = now.minute

    if len(parsed_dict['text']) <= 3:
        error = 'Слишком короткий текст. Ничего не записано'
    if len(parsed_dict['text']) > 2500:
        error = 'Слишком длинный текст. Ничего не записано'

    if parsed_dict['start_hour'] is not None:
        start_time = datetime(now.year, now.month, now.day, parsed_dict['start_hour'], parsed_dict['start_minute'])
    else:
        start_time = None
    end_time = datetime(now.year, now.month, now.day, parsed_dict['end_hour'], parsed_dict['end_minute'])

    sanitized_dict = {
        'error': error,
        'start_time': start_time,
        'end_time': end_time,
        'text': parsed_dict['text']
    }

    return sanitized_dict


def parse_and_sanitize(text: str) -> dict:
    parse_dict = parse_message(text)
    sanitized_dict = sanitize_message(parse_dict)

    return sanitized_dict

