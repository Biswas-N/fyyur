#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *

# Additional imports
import sys
from flask_migrate import Migrate
from models import db, Artist, Venue, Show
from sqlalchemy import func
from datetime import datetime
from flask import jsonify

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# connect to a local postgresql database
db.init_app(app)
migrate = Migrate(app=app, db=db)

#----------------------------------------------------------------------------#
# Models. Models can be found in models.py
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')




#  Venues Controllers
#  ----------------------------------------------------------------

#  Create Venue (Crud)
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # Getting the user's input
  data = {}
  data['name'] = request.form.get('name')
  data['city'] = request.form.get('city')
  data['state'] = request.form.get('state')
  data['address'] = request.form.get('address')
  data['phone'] = request.form.get('phone')
  data['genres'] = request.form.getlist('genres')
  data['image_link'] = request.form.get('image_link')
  data['facebook_link'] = request.form.get('facebook_link')
  data['website'] = request.form.get('website')
  data['seeking_talent'] = True if request.form.get('seeking_talent') == 'y' else False
  data['seeking_description'] = request.form.get('seeking_description')

  try:
    # Try to insert into the table
    newVenue = Venue(**data)
    db.session.add(newVenue)
    db.session.commit()

    # on successful db insert, flash success
    flash('Venue ' + request.form.get('name') + ' was successfully listed!')
  except Exception:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Read Venues (cRud)
#  ----------------------------------------------------------------

# Read all venues
@app.route('/venues')
def venues():
  # Getting all the areas (City and State)
  venueAreas = Venue.query.with_entities(func.count(Venue.id), Venue.city, Venue.state).group_by(Venue.city, Venue.state).all()
  areas = []
  # Iterating through each area and getting venues
  for area in venueAreas:
    areaDict = {}
    areaDict["city"] = area.city
    areaDict['state'] = area.state
    areaDict['venues'] = []

    venues = Venue.query.filter(Venue.state==area.state, Venue.city==area.city).all()
    for venue in venues:
      # print(f"{area.city}, {area.state} - {venue.id}, {venue.name}, {venue.upcoming_shows_count()}")
      venuesDict = {}
      venuesDict['id'] = venue.id
      venuesDict['name'] = venue.name
      venuesDict['num_upcoming_shows'] = venue.upcoming_shows_count()

      areaDict['venues'].append(venuesDict)

    areas.append(areaDict)
  
  return render_template('pages/venues.html', areas=areas)

# Read one venue, based on search
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  data = []
  for venue in venues:
    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.upcoming_shows_count()
    })

  response = {
    "count": len(venues),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

# Read one venue, based on ID
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  
  data = {
    **venue.toJson(),
    "past_shows": [],
    "upcoming_shows": []
  }

  shows = venue.shows
  for show in shows:
    artist = show.artist
    now = datetime.now()

    start_time = show.start_time.strftime("%Y-%m-%dT%H:%M:%S") # Converting datetime to string, Eg: "2019-05-21T21:30:00"
    if now < show.start_time:
      data['upcoming_shows'].append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": start_time
      })
    else:
       data['past_shows'].append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": start_time
      })
  # print(data)
  return render_template('pages/show_venue.html', venue=data)


#  Update Venue (crUd)
#  ----------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)

  venue.name = request.form.get('name')
  venue.city = request.form.get('city')
  venue.state = request.form.get('state')
  venue.address = request.form.get('address')
  venue.phone = request.form.get('phone')
  venue.genres = request.form.getlist('genres')
  venue.image_link = request.form.get('image_link')
  venue.facebook_link = request.form.get('facebook_link')
  venue.website = request.form.get('website')
  venue.seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
  venue.seeking_description = request.form.get('seeking_description')

  db.session.commit()

  return redirect(url_for('show_venue', venue_id=venue_id))


#  Delete Venue (cruD)
#  ----------------------------------------------------------------

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # I know this is not the perfect way of deleting a record
  # But I really wanted to give this a try

  err = False
  try:
    # Try to get the venue
    venue = Venue.query.get_or_404(venue_id)
    db.session.delete(venue)
    db.session.commit()

    # on successful delete, flash success
    flash('Venue ID: ' + venue_id + ' was successfully deleted!')
  except Exception:
    err = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Venue ID: ' + venue_id + ' could not be deleted.')
  finally:
    db.session.close()

  if err:
    return jsonify({'status': 'fail'})
  else:
    return jsonify({'status': 'success'})





#  Artists Controllers
#  ----------------------------------------------------------------

#  Create Artist (Crud)
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # Getting the user's input
  data = {}
  data['name'] = request.form.get('name')
  data['city'] = request.form.get('city')
  data['state'] = request.form.get('state')
  data['phone'] = request.form.get('phone')
  data['genres'] = request.form.getlist('genres')
  data['image_link'] = request.form.get('image_link')
  data['facebook_link'] = request.form.get('facebook_link')
  data['website'] = request.form.get('website')
  data['seeking_venue'] = True if request.form.get('seeking_venue') == 'y' else False
  data['seeking_description'] = request.form.get('seeking_description')

  try:
    # Try to insert into the table
    newArtist = Artist(**data)
    db.session.add(newArtist)
    db.session.commit()

    # on successful db insert, flash success
    flash('Artist ' + request.form.get('name') + ' was successfully listed!')
  except Exception:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


#  Read Artists (cRud)
#  ----------------------------------------------------------------

# Read all artists
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

# Read one artist, based on search
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()

  data = []
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.upcoming_shows_count()
    })

  response = {
    "count": len(artists),
    "data": data
  }
  
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

# Read one artist, based on ID
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  
  data = {
    **artist.toJson(),
    "past_shows": [],
    "upcoming_shows": []
  }

  shows = artist.shows
  for show in shows:
    venue = show.venue
    now = datetime.now()

    start_time = show.start_time.strftime("%Y-%m-%dT%H:%M:%S") # Converting datetime to string, Eg: "2019-05-21T21:30:00"
    if now < show.start_time:
      data['upcoming_shows'].append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": start_time
      })
    else:
       data['past_shows'].append({
        "venue_id": venue.id,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": start_time
      })
  # print(data)
  return render_template('pages/show_artist.html', artist=data)

#  Update Artist (crUd)
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.get_or_404(artist_id)

  artist.name = request.form.get('name')
  artist.city = request.form.get('city')
  artist.state = request.form.get('state')
  artist.phone = request.form.get('phone')
  artist.genres = request.form.getlist('genres')
  artist.image_link = request.form.get('image_link')
  artist.facebook_link = request.form.get('facebook_link')
  artist.website = request.form.get('website')
  artist.seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
  artist.seeking_description = request.form.get('seeking_description')

  db.session.commit()

  return redirect(url_for('show_artist', artist_id=artist_id))


#  Delete Artist (cruD)
#  ----------------------------------------------------------------

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # I know this is not the perfect way of deleting a record
  # But I really wanted to give this a try

  err = False
  try:
    # Try to get the artist
    artist = Artist.query.get_or_404(artist_id)
    db.session.delete(artist)
    db.session.commit()

    # on successful delete, flash success
    flash('Artist ID: ' + artist_id + ' was successfully deleted!')
  except Exception:
    err = True
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Artist ID: ' + artist_id + ' could not be deleted.')
  finally:
    db.session.close()

  if err:
    return jsonify({'status': 'fail'})
  else:
    return jsonify({'status': 'success'})

#  Shows Controller
#  ----------------------------------------------------------------

#  Create Show (Crud)
#  ----------------------------------------------------------------

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # Getting the user's input
  data = {}
  data['venue_id'] = request.form.get('venue_id')
  data['artist_id'] = request.form.get('artist_id')
  data['start_time'] = request.form.get('start_time')
  # print(data)

  try:
    # Try to insert into the table
    newShow = Show(**data)
    db.session.add(newShow)
    db.session.commit()

    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception:
    db.session.rollback()
    print(sys.exc_info())
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Read Shows (cRud)
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  shows = Show.query.all()

  for show in shows:
    # Getting artist and venue data, to avoid multiple calls to sql database
    # while assigning data to the object below
    artist = show.artist
    venue = show.venue

    start_time = show.start_time.strftime("%Y-%m-%dT%H:%M:%S") # Converting datetime to string, Eg: "2019-05-21T21:30:00"

    data.append({
      "venue_id": venue.id,
      "venue_name": venue.name,
      "artist_id": artist.id,
      "artist_name": artist.name,
      "artist_image_link": artist.image_link,
      "start_time": start_time
    })

  return render_template('pages/shows.html', shows=data)


#  Handler Methods
#  ----------------------------------------------------------------

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
