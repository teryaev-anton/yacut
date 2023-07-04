import string

# Разрешенные символы для короткой ссылки
ALLOWED_SYMBOLS = string.ascii_letters + string.digits
# Длина короткой ссылки для автоматической генерации
SHORT_ID_LENGTH = 6
# Максимальная длина короткой ссылки, полученной от пользователя
USER_INPUT_LIMIT = 16