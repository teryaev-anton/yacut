from http import HTTPStatus

from flask import jsonify, request, url_for

from . import app, db

from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import check_short_id, get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id):
    """Получение оригинальной ссылки по короткому идентификатору"""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url_map.original}), HTTPStatus.OK


@app.route('/api/id/', methods=['POST'])
def create_id():
    """Создание короткого идентификатора"""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(
            f'Имя "{data["custom_id"]}" уже занято.')
    if not check_short_id(data['custom_id']):
        raise InvalidAPIUsage(
            'Указано недопустимое имя для короткой ссылки')
    url_map = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.original,
        'short_link': url_for('index_view', _external=True) + url_map.short
    }), HTTPStatus.CREATED
