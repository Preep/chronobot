import re
from datetime import datetime
from typing import Optional, Match


def match_by_template(text: str, template: str) -> Optional[Match[str]]:
    template = re.compile(template)
    match = template.match(text)
    return match

def parse_message(text: str) -> dict:

    # Match [start_hour:start_minute] - [end_hour:end_minute] text
    if (match := match_by_template(text, r'^(\d{1,2}).?(\d{2})\s?\D?\s?(\d{1,2}).?(\d{2})\s(.+)$')) is not None:
        parsed_dict = {
            'start_hour': int(match.group(1)),
            'start_minute': int(match.group(2)),
            'end_hour': int(match.group(3)),
            'end_minute': int(match.group(4)),
            'text': match.group(5)
        }
    # Match [end_hour:end_minute] text
    elif (match := match_by_template(text, r'^(\d{1,2}).?(\d{2})\s(.+)$')) is not None:
        parsed_dict = {
            'start_hour': None,
            'start_minute': None,
            'end_hour': int(match.group(1)),
            'end_minute': int(match.group(2)),
            'text': match.group(3)
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
    if parsed_dict['start_hour'] is not None and parsed_dict['end_hour'] is not None:
        if parsed_dict['start_hour'] < 0 or parsed_dict['start_hour'] > 23 or parsed_dict['end_hour'] < 0 or parsed_dict['end_hour'] > 23:
            error = '‼️Неверное значение часов.'

        if parsed_dict['start_minute'] < 0 or parsed_dict['start_minute'] > 59 or parsed_dict['end_minute'] < 0 or parsed_dict['end_minute'] > 59:
            error = '‼️Неверное значение минут.'

        if parsed_dict['start_hour'] > parsed_dict['end_hour']:
            error = '‼️Час начала больше часа окончания.'

        if parsed_dict['start_hour'] == parsed_dict['end_hour'] and parsed_dict['start_minute'] > parsed_dict['end_minute']:
            error = '‼️Минута начала больше минуты окончания.'
    elif parsed_dict['end_hour'] is not None:
        if parsed_dict['end_hour'] < 0 or parsed_dict['end_hour'] > 23:
            error = '‼️Неверное значение часов.'

        if parsed_dict['end_minute'] < 0 or parsed_dict['end_minute'] > 59:
            error = '‼️Неверное значение минут.'
    else:
        parsed_dict['end_hour'] = now.hour
        parsed_dict['end_minute'] = now.minute

    if len(parsed_dict['text']) <= 3:
        error = '‼️Слишком короткий текст.'
    if len(parsed_dict['text']) > 2500:
        error = '‼️Слишком длинный текст.'

    if parsed_dict['start_hour'] is not None and parsed_dict['end_hour'] is not None:
        start_time = datetime(now.year, now.month, now.day, parsed_dict['start_hour'], parsed_dict['start_minute'])
        end_time = datetime(now.year, now.month, now.day, parsed_dict['end_hour'], parsed_dict['end_minute'])
    elif parsed_dict['end_hour'] is not None:
        start_time = None
        end_time = datetime(now.year, now.month, now.day, parsed_dict['end_hour'], parsed_dict['end_minute'])
    else:
        start_time = None
        end_time = None

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

