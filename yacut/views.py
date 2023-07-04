from flask import Markup, flash, redirect, render_template, url_for

from . import app, db

from .forms import URLForm
from .models import URLMap
from .utils import check_short_id, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """View-функция главной страницы (создание короткой ссылки)"""
    form = URLForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash(f'Имя {custom_id} уже занято!')
            return render_template('index.html', form=form)
        if custom_id:
            if not check_short_id(custom_id):
                flash('Коротка ссылка не может превышать 16 символов' +
                      'Разрешены только латинские буквы' +
                      'и цифры в диапазоне 0-9')
                return render_template('index.html', form=form)
        else:
            custom_id = get_unique_short_id()
        url_map = URLMap(
            original=original_link,
            short=custom_id,
        )
        db.session.add(url_map)
        db.session.commit()
        result_url = url_for('index_view', _external=True) + url_map.short
        flash(Markup(
            f'Ваша новая ссылка готова: '
            f'<a href="{result_url}">'
            f'{result_url}</a>'
        ))
    return render_template('index.html', form=form)


@app.route('/<short_id>', methods=['GET'])
def redirect_view(short_id):
    """View-функция для перехода по короткой ссылке"""
    url_map = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_map.original)
