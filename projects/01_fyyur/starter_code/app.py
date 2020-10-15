#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import logging
import sys
from datetime import datetime
from logging import FileHandler, Formatter

import babel
import dateutil.parser
from flask import (Flask, Response, flash, redirect, render_template, request,
                   url_for)
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms.validators import (ValidationError)
from models import *
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    areas = list(set(Venue.query.with_entities(Venue.city, Venue.state).all()))
    data = []
    for area in areas:
        venues = Venue.query.filter_by(city=area[0]).all()
        data.append({
            "city": area[0],
            "state": area[1],
            "venues": [{
                'id': v.id,
                'name': v.name
            } for v in venues]
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search = request.form.get('search_term', '')
    query = Venue.query.filter(Venue.name.ilike(f"%{search}%")).all()

    response = {
        "count":
            len(query),
        "data": [{
            "id":
                venue.id,
            "name":
                venue.name,
            "num_upcoming_shows":
                len(
                    list(
                        filter(
                            lambda show: show.start_time >= datetime.utcnow(),
                            venue.shows)))
        } for venue in query]
    }
    return render_template('pages/search_venues.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    data = venue
    data.genres = data.genres.split(',')

    shows = data.shows
    past_shows = list(
        filter(lambda show: show.start_time < datetime.utcnow(), shows))
    upcoming_shows = list(
        filter(lambda show: show.start_time >= datetime.utcnow(), shows))

    data.upcoming_shows = [{
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
    } for show in upcoming_shows]

    data.past_shows = [{
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time)
    } for show in past_shows]

    data.past_shows_count = len(past_shows)
    data.upcoming_shows_count = len(upcoming_shows)
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    try:
        if not form.validate_on_submit():
            raise ValidationError()
        venue = Venue(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            genres=','.join(request.form.getlist('genres')),
            facebook_link=request.form['facebook_link'],
            seeking_talent=True
            if request.form.get('seeking_talent', None) == 'y' else False,
            seeking_description=request.form['seeking_description'],
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] +
              ' could not be listed.')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    name = ''
    try:
        venue = Venue.query.get(venue_id)
        name = venue.name
        db.session.delete(venue)
        db.session.commit()
        flash('Venue ' + name + ' was successfully deleted!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Venue ' + name + ' could not be deleted.')
    finally:
        db.session.close()
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = []
    for artist in artists:
        data.append({"id": artist.id, "name": artist.name})
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', '')
    query = Artist.query.filter(Artist.name.ilike(f"%{search}%")).all()
    response = {
        "count":
            len(query),
        "data": [{
            "id":
                artist.id,
            "name":
                artist.name,
            "num_upcoming_shows":
                len(
                    list(
                        filter(
                            lambda show: show.start_time >= datetime.utcnow(),
                            artist.shows)))
        } for artist in query]
    }
    return render_template('pages/search_artists.html',
                           results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    data = artist
    data.genres = data.genres.split(',')

    shows = data.shows
    past_shows = list(
        filter(lambda show: show.start_time < datetime.utcnow(), shows))
    upcoming_shows = list(
        filter(lambda show: show.start_time >= datetime.utcnow(), shows))

    data.upcoming_shows = [{
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
    } for show in upcoming_shows]

    data.past_shows = [{
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": str(show.start_time)
    } for show in past_shows]

    data.past_shows_count = len(past_shows)
    data.upcoming_shows_count = len(upcoming_shows)
    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    artist.genres = artist.genres.split(',')
    form = ArtistForm(data=artist.__dict__)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm()
    try:
        if not form.validate_on_submit():
            raise ValidationError()
        artist = Artist.query.get(artist_id)
        form = ArtistForm(obj=artist)
        form.populate_obj(artist)
        artist.genres = ','.join(artist.genres)
        db.session.add(artist)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    venue.genres = venue.genres.split(',')
    form = VenueForm(data=venue.__dict__)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()

    try:
        if not form.validate_on_submit():
            raise ValidationError()
        venue = Venue.query.get(venue_id)
        form = VenueForm(obj=venue)
        form.populate_obj(venue)
        venue.genres = ','.join(venue.genres)
        db.session.add(venue)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm()

    try:
        if not form.validate_on_submit():
            raise ValidationError()
        artist = Artist(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            image_link=request.form['image_link'],
            website=request.form['website'],
            genres=','.join(request.form.getlist('genres')),
            facebook_link=request.form['facebook_link'],
            seeking_venue=True
            if request.form.get('seeking_venue', None) == 'y' else False,
            seeking_description=request.form['seeking_description'],
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Artist ' + request.form['name'] +
              ' could not be listed.')
    finally:
        db.session.close()

    return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = [{
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": str(show.start_time),
    } for show in shows]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    form = ShowForm()

    try:
        if not form.validate_on_submit():
            raise ValidationError()
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time'],
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()

    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
