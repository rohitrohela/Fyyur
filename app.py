# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import datetime
import babel
import dateutil.utils
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from forms import *
from models import db
from models import Venue, Artist, Show

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


@app.route('/venues')
def venues():
    data = []

    for location in (db.session.query(Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()):

        data.append({
            "city": location[0],
            "state": location[1],
            "venues": []
        })

        for venue in (
                db.session.query(Venue.id, Venue.name).filter(Venue.city == location[0],
                                                              Venue.state == location[1]).all()):
            data[len(data) - 1]["venues"].append({
                "id": venue[0],
                "name": venue[1],
                "num_upcoming_shows": 2
            })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    searchTerm = request.form['search_term']
    searchResult = db.session.query(Venue.id, Venue.name).filter(Venue.name.ilike('%' + searchTerm + '%')).all()

    response = {
        "count": len(searchResult),
        "data": []
    }

    for venue in searchResult:
        response["data"].append({
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": len(db.session.query(Show).filter(Show.venueId == venue.id).all())
        })

    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = db.session.query(Venue).filter(Venue.id == venue_id).first()
    pastShows = []
    upcomingShows = []

    past_shows = db.session.query(Show).join(Venue).filter(Show.venueId == venue_id).filter(
        Show.showTime < datetime.now()).all()

    upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venueId == venue_id).filter(
        Show.showTime > datetime.now()).all()

    for past_show in past_shows:
        pastShows.append({
                    "artist_id": past_show.artist.id,
                    "artist_name": past_show.artist.name,
                    "artist_image_link": past_show.artist.image_link,
                    "start_time": str(past_show.showTime)
                })

    for upcoming_show in upcoming_shows:
        upcomingShows.append({
                    "artist_id": upcoming_show.artist.id,
                    "artist_name": upcoming_show.artist.name,
                    "artist_image_link": upcoming_show.artist.image_link,
                    "start_time": str(upcoming_show.showTime)
                })

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(','),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.isLookingForTalent,
        "image_link": venue.image_link,
        "past_shows": pastShows,
        "upcoming_shows": upcomingShows,
        "past_shows_count": len(pastShows),
        "upcoming_shows_count": len(upcomingShows),
    }
    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        form = VenueForm(request.form)

        venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data,
            genres=','.join(form.genres.data),
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website_link=form.website_link.data,
            isLookingForTalent=form.seeking_talent.data,
            seekingDescription=form.seeking_description.data
        )

        db.session.add(venue)
        db.session.commit()
        flash('Venue: {0} created successfully'.format(venue.name))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred creating the Venue: {0}. Error: {1}'.format(venue.name, e))
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Show.query.filter_by(venueId=venue_id).delete()
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = []

    for artist in (db.session.query(Artist.id, Artist.name).all()):
        data.append({
            "id": artist[0],
            "name": artist[1]
        })

    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    searchTerm = request.form['search_term']
    searchResult = db.session.query(Artist.id, Artist.name).filter(Artist.name.ilike('%' + searchTerm + '%')).all()

    response = {
        "count": len(searchResult),
        "data": []
    }

    for artist in searchResult:
        response["data"].append({
            "id": artist.id,
            "name": artist.name,
            "num_upcoming_shows": len(db.session.query(Artist).filter(Show.artistId == artist.id).all())
        })

    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id

    artist = db.session.query(Artist).filter(Artist.id == artist_id).first()
    pastShows = []
    upcomingShows = []

    past_shows = db.session.query(Show).join(Artist).filter(Show.artistId == artist_id).filter(
        Show.showTime < datetime.now()).all()

    upcoming_shows = db.session.query(Show).join(Artist).filter(Show.artistId == artist_id).filter(
        Show.showTime > datetime.now()).all()

    for past_show in past_shows:
        pastShows.append({
            "venue_id" : past_show.venue.id,
            "venue_name": past_show.venue.name,
            "venue_image_link": past_show.venue.image_link,
            "start_time": str(past_show.showTime)
        })

    for upcoming_show in upcoming_shows:
        upcomingShows.append({
            "venue_id": upcoming_show.venue.id,
            "venue_name": upcoming_show.venue.name,
            "venue_image_link": upcoming_show.venue.image_link,
            "start_time": str(upcoming_show.showTime)
        })

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "seeking_venue": artist.isLookingForVenues,
        "image_link": artist.image_link,
        "past_shows": pastShows,
        "upcoming_shows": upcomingShows,
        "past_shows_count": len(pastShows),
        "upcoming_shows_count": len(upcomingShows),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artistDb = db.session.query(Artist).filter(Artist.id == artist_id).first()
    artist = {
        "id": artistDb.id,
        "name": artistDb.name,
        "genres": artistDb.genres,
        "city": artistDb.city,
        "state": artistDb.state,
        "phone": artistDb.phone,
        "website": artistDb.website_link,
        "facebook_link": artistDb.facebook_link,
        "seeking_venue": artistDb.isLookingForVenues,
        "seeking_description": artistDb.seekingDescription,
        "image_link": artistDb.image_link
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing

    try:
        artist = db.session.query(Artist).filter(Artist.id == artist_id).first()

        form = ArtistForm(request.form)
        artist.name = form.name.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.genres = ','.join(form.genres.data)
        artist.facebook_link = form.facebook_link.data
        artist.image_link = form.image_link.data
        artist.website_link = form.image_link.data
        artist.isLookingForVenues = form.seeking_venue.data
        artist.seekingDescription = form.seeking_description.data

        db.session.commit()
        flash('Artist: {0} was successfully updated'.format(artist.name))
    except Exception as e:
        # TODO: on unsuccessful db insert, flash an error instead.
        db.session.rollback()
        flash('An error occurred while updating Artist: {0}. Error: {1}'.format(artist.name, e))
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venueDb = db.session.query(Venue).filter(Venue.id == venue_id).first()
    venue = {
        "id": venueDb.id,
        "name": venueDb.name,
        "genres": venueDb.genres,
        "address": venueDb.address,
        "city": venueDb.city,
        "state": venueDb.state,
        "phone": venueDb.phone,
        "website": venueDb.website_link,
        "facebook_link": venueDb.facebook_link,
        "seeking_talent": venueDb.isLookingForTalent,
        "seeking_description": venueDb.seekingDescription,
        "image_link": venueDb.image_link
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    try:
        venue = db.session.query(Venue).filter(Venue.id == venue_id).first()

        form = VenueForm(request.form)
        venue.name = form.name.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.address = form.address.data
        venue.phone = form.phone.data
        venue.genres = ','.join(form.genres.data)
        venue.facebook_link = form.facebook_link.data
        venue.image_link = form.image_link.data
        venue.website_link = form.website_link.data
        venue.seekingDescription = form.seeking_description.data
        venue.isLookingForTalent = form.seeking_talent.data

        db.session.commit()
        flash('Venue: {0} was successfully updated'.format(venue.name))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating Venue: {0}. Error: {1}'.format(venue.name, e))
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
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    try:
        form = ArtistForm(request.form)
        artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=form.genres.data,
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            website_link=form.image_link.data,
            isLookingForVenues=form.seeking_venue.data,
            seekingDescription=form.seeking_description.data
        )
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist: {0} created successfully'.format(artist.name))
    except Exception as e:
        db.session.rollback()
        flash('An error occurred creating the Artist: {0}. Error: {1}'.format(artist.name, e))
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = []

    showList = Show.query.all()
    for show in showList:
        data.append({
            "venue_id": show.venueId,
            "venue_name": show.venue.name,
            "artist_id": show.artistId,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": str(show.showTime)
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    try:
        form = ShowForm(request.form)
        newShow = Show(
            artistId=form.artist_id.data,
            venueId=form.venue_id.data,
            showTime=form.start_time.data
        )

        db.session.add(newShow)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception as e:
        db.session.rollback()
        flash('Show could not be listed because : ' + str(e))
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
