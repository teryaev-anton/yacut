from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Кастомный класс исключения"""
    status_code = 400

    def __init__(self, message, status_code=None):
        """Конструктор класса"""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Метод для сериализации переданного сообщения об ошибке"""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обработчик кастомного исключения для API"""
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(404)
def page_not_found(error):
    """Обработчик кастомного исключения для ошибки 404"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработчик кастомного исключения для ошибки 500"""
    db.session.rollback()
    return render_template('500.html'), 500
