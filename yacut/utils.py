from random import choices

from .constants import ALLOWED_SYMBOLS, SHORT_ID_LENGTH, USER_INPUT_LIMIT
from .models import URLMap


def get_unique_short_id():
    """Генерация короткой ссылки и проверка ее на уникальность"""
    short_id = ''.join(choices(ALLOWED_SYMBOLS, k=SHORT_ID_LENGTH))
    while URLMap.query.filter_by(short=short_id).first():
        short_id = ''.join(choices(ALLOWED_SYMBOLS, k=SHORT_ID_LENGTH))
    return short_id


def check_short_id(short_id):
    """Проверка длины короткой ссылки и разрешенных символов в ней"""
    if len(short_id) > USER_INPUT_LIMIT:
        return False
    for symbol in short_id:
        if symbol not in ALLOWED_SYMBOLS:
            return False
    return True
