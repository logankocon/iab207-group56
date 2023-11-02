from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', events = events)

@main_bp.route('/search')
def search():
    search = request.args.get('search', default='', type=str)
    filter_option = request.args.get('filter', default='description', type=str)

    if search == '':
        if filter_option == 'Filter by Genre':
            events = db.session.scalars(db.select(Event)).all()
        else:
            query = '%' + filter_option + '%'
            events = Event.query.filter(Event.genre.like(query)).all()

        return render_template('index.html', events = events)
    print(search)
    print(filter_option)

    return redirect(url_for('main.index'))