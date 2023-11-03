from flask import Blueprint, render_template, request, redirect, url_for, session
from datetime import datetime
from .models import Event
from . import db
from sqlalchemy import or_, and_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    events = db.session.scalars(db.select(Event)).all()
    for event in events:
        if event.status == "Open" or "Sold Out":
            if datetime.date(datetime.now()) > event.event_date:
                event.status = "Unavaliable"
                db.session.commit()

    return render_template('index.html', events = events)


@main_bp.route('/search')
def search():
    search = request.args['search']
    filter_option = request.args.get('filter', default='description', type=str)

    if search == '':
        
        if filter_option == 'Filter by Genre':
            events = db.session.scalars(db.select(Event)).all()
        elif filter_option == "Other":
            query = ["Jazz", "Rock", "Pop", "Classical", "Hip Hop", "Country", "R&B", "Electronic", "Metal", "Indie"]
            events = Event.query.filter(Event.genre.not_in(query))
        else:
            query = '%' + filter_option + '%'
            events = Event.query.filter(Event.genre.like(query)).all()
         
        return render_template('index.html', events = events)
    else:
        if filter_option == 'Filter by Genre':
            query = '%' + search + '%'
            
            #select all where (event name OR description match)
            events = Event.query.filter(
                        or_(Event.name.like(query), Event.description.like(query))
                    ).all()

        else:
            #select all where (event name OR description match) AND (genre matches)
            search_query = '%' + search + '%'
            filter_query = '%' + filter_option + '%'
            
           
            events = Event.query.filter(
                        and_(
                            or_(
                                Event.name.like(search_query),
                                Event.description.like(search_query)
                            ),
                            Event.genre.like(filter_query)
                        )
                    ).all()

        return render_template('index.html', events = events)



    return redirect(url_for('main.index'))
