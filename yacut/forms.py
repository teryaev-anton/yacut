from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import USER_INPUT_LIMIT


class URLForm(FlaskForm):
    original_link = URLField(
        'Оригинальная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(max=USER_INPUT_LIMIT),
            Regexp(r'^[a-zA-Z\d]{1,6}$', message='Только a-z, A-Z, 0-9'),
            Optional()
        ]
    )
    submit = SubmitField('Создать')
