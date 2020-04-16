#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import render_template, request, flash, redirect, url_for

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()

from sqlalchemy import desc, or_
from markupsafe import Markup

import json, sys
import datetime


#Imports the database object from the __init__.py file inside the /app folder
from app import app

#Imports forms
from app.mvc_backend_code.forms import *

#Imports models
from app.mvc_backend_code.models import *


#Function that shows the 10 most-recently created artists and venues
def show_recently_created():
  show_recently_created.artist_data = []
  artist_rows = Artist.query.order_by(desc(Artist.id)).limit(10)

  show_recently_created.venue_data = []
  venue_rows = Venue.query.order_by(desc(Venue.id)).limit(10)

  for artist in artist_rows:
    row = {
      "id": artist.id,
      "name": artist.name
    }

    show_recently_created.artist_data.append(row)

  for venue in venue_rows:
    row = {
      "id": venue.id,
      "name": venue.name
    }

    show_recently_created.venue_data.append(row)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#Home page route
#Displays list of most-recently created artists and venues
@app.route('/')
def index():

  show_recently_created()

  return render_template('pages/home.html', artists=show_recently_created.artist_data, venues=show_recently_created.venue_data)


#  Venues
#  ----------------------------------------------------------------

#Venues page route
#Shows list of venues
@app.route('/venues')
def venues():
  
  venue_data = [] #List of venues

  venue_rows = Venue.query.order_by(Venue.id).all() #Collection of all venues

  #Add each venue to the list
  for venue in venue_rows:
    row = {
      "id": venue.id,
      "name": venue.name
    }

    venue_data.append(row)


  return render_template('pages/venues.html', venues=venue_data)

#Search Venues route
#Returns list of venues that match search criteria (i.e. Venue name)
@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  search_query = request.form.get("search_term")
  
  #Venues that match the search criteria
  venues = Venue.query.filter(Venue.name.ilike(f"%{search_query}%")).order_by(Venue.id).all()
  
  list_venues = []  #List of venues that match the search criteria

  #Loop that adds each matching venue to list_venues
  for venue in venues:
    venue_info = {}

    venue_info["id"] = venue.id
    venue_info["name"] = venue.name

    list_venues.append(venue_info)

  #Dictionary used for Jinja data-rendering on the front-end
  response = {}
  response['count'] = len(list_venues)
  response['data'] = list_venues

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


#Route that displays a specified venue page based on the venue id
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  current_datetime = datetime.today()
  
  #Queries venue information for the venue with the specified id
  venue_data = Venue.query.get(venue_id)
  venue_data.genres = json.loads(venue_data.genres)

  venue_data.past_shows = []
  venue_data.upcoming_shows = []

  past_shows_count = 0
  upcoming_shows_count = 0

  try:
        shows = db.session.query(Artist, Shows.start_time).join(Shows)
        shows = shows.filter(Shows.venue_id == venue_id)                      
        
        #Queries for Past Shows and Upcoming Shows
        past_shows = shows.filter(Shows.start_time <= current_datetime).order_by(desc(Shows.start_time))
        upcoming_shows = shows.filter(Shows.start_time > current_datetime).order_by(Shows.start_time)

        #Looping through Past Shows
        for artist, start_time in past_shows:
            
            venue_data.past_shows.append({
              'artist_id': artist.id,
              'artist_name': artist.name,
              'artist_image_link': artist.image_link,
              'artist_city': artist.city,
              'artist_state': artist.state,
              'start_time': str(start_time)

            })
          
            past_shows_count += 1
          
        
        #Looping through Upcoming Shows
        for artist, start_time in upcoming_shows:

            venue_data.upcoming_shows.append({
              'artist_id': artist.id,
              'artist_name': artist.name,
              'artist_image_link': artist.image_link,
              'artist_city': artist.city,
              'artist_state': artist.state,
              'start_time': str(start_time)
            })

            upcoming_shows_count += 1


        #Setting the number of past and upcoming shows
        venue_data.past_shows_count = past_shows_count
        venue_data.upcoming_shows_count = upcoming_shows_count
    
  except:
        print(sys.exc_info())
        flash('Error: The Venue with ID \"' + str(venue_id) + '\" could not be found!')

  
  return render_template('pages/show_venue.html', venue=venue_data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  
  form = VenueForm(request.form)

  #Venue form data
  venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        genres=form.genres.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        image_link=form.image_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data

      )

  #Checks the number of times a venue name is in the database
  name_count = db.session.query(Venue).filter(form.name.data == Venue.name).count()

  #If the form is valid (i.e. front-end and back-end wise)
  if form.validate():
    
    #If a venue already exists in the database
    if name_count == 1:
      flash("\"" + request.form['name'] + "\" is already in the database! Please enter a new venue.")
      return render_template('forms/new_venue.html', form=form)

    #If a venue does not exist in the database
    else:
      db.session.add(venue)
      db.session.commit()

      show_recently_created()

      flash("\"" + request.form['name'] + '\" was added successfully!')
      return render_template('pages/home.html', form=form, artists=show_recently_created.artist_data, venues=show_recently_created.venue_data)

  #If the form is invalid
  else:
    flash(form.errors)
    return render_template('forms/new_venue.html', form=form)


#Delete Venue route
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
 
  #Deletes the venue
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
    
    flash("The venue with ID \"" + venue_id + "\" has been deleted successfully!")
    return render_template('pages/home.html')

  #Exception code if the venue cannot be deleted
  except:
    print(sys.exc_info())
    db.session.rollback()
    flash("Error: The venue with ID \"" + venue_id + "\" could not be deleted!")

  finally:
    db.session.close()

  return render_template('pages/venues.html')
  

#  Artists
#  ----------------------------------------------------------------

#Artists page route
#Shows list of artists
@app.route('/artists')
def artists():
  
  artist_data = []  #List of artists 

  artist_rows = Artist.query.order_by(Artist.id).all()  #Collection of all artists

  #Append each artist to artist_data
  for artist in artist_rows:
    row = {
      "id": artist.id,
      "name": artist.name
    }

    artist_data.append(row)

  return render_template('pages/artists.html', artists=artist_data)

#Search Artists route
#Returns list of artists that match search criteria (i.e. Artist name)
#To see results, press the "Enter" key after typing your search
@app.route('/artists/search', methods=['POST'])
def search_artists():
  
  search_query = request.form.get("search_term")

  #Artists who match the search criteria
  artists = Artist.query.filter(Artist.name.ilike(f"%{search_query}%")).order_by(Artist.id).all()

  list_artists = [] #List of artists that match the criteria

  #Add each artist to list_artists
  for artist in artists:
    artist_info = {}
    artist_info["id"] = artist.id
    artist_info["name"] = artist.name
    
    list_artists.append(artist_info)

  
  #Dictionary used for Jinja data-rendering on the front-end
  response = {}
  response["count"] = len(list_artists)
  response["data"] = list_artists


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


#Route that displays a specified artist page based on the artist id
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  
    current_datetime = datetime.today()
    
    #Queries artist information for the artist with the specified id
    artist_data = Artist.query.get(artist_id)
    artist_data.genres = json.loads(artist_data.genres)

    artist_data.past_shows = []
    artist_data.upcoming_shows = []

    past_shows_count = 0
    upcoming_shows_count = 0
    
    try:
        shows = db.session.query(Venue, Shows.start_time).join(Shows)   
        shows = shows.filter(Shows.artist_id == artist_id)                      
        
        #Queries for Past Shows and Upcoming Shows
        past_shows = shows.filter(Shows.start_time <= current_datetime).order_by(desc(Shows.start_time))
        upcoming_shows = shows.filter(Shows.start_time > current_datetime).order_by(Shows.start_time)

        #Looping through Past Shows
        for venue, start_time in past_shows:
          
          artist_data.past_shows.append({
                'venue_id': venue.id,
                'venue_name': venue.name,
                'venue_image_link': venue.image_link,
                'venue_city': venue.city,
                'venue_state': venue.state,
                'start_time': str(start_time)
                })
            
          past_shows_count += 1

        
        #Looping through Upcoming Shows
        for venue, start_time in upcoming_shows:
          
          artist_data.upcoming_shows.append({
                'venue_id': venue.id,
                'venue_name': venue.name,
                'venue_image_link': venue.image_link,
                'venue_city': venue.city,
                'venue_state': venue.state,
                'start_time': str(start_time)
                })
            
          upcoming_shows_count += 1

        #Setting the number of Past and Upcoming Shows
        artist_data.past_shows_count = past_shows_count
        artist_data.upcoming_shows_count = upcoming_shows_count


    except:
        print(sys.exc_info())
        flash('Error: The Artist with ID' + artist_id + 'could not be found!')

    return render_template('pages/show_artist.html', artist=artist_data)
      
    
#  Update
#  ----------------------------------------------------------------


#Edit Artist Routes
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  artist.genres = json.loads(artist.genres)
  
  form = ArtistForm(
    name = artist.name,
    city = artist.city,
    state = artist.state,
    phone = artist.phone,
    genres = artist.genres,
    website_link = artist.website_link,
    image_link = artist.image_link,
    facebook_link = artist.facebook_link,
    seeking_venues = artist.seeking_venues,
    seeking_description = artist.seeking_description


  )
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)

#Route that edits information about a specific artist (based on the artist id)
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  form = ArtistForm()
  
  #Retreives artist-specific information
  artist = Artist.query.get(artist_id)
  
  """
  Removes the first and last square brackets before the form is submitted
  #Otherwise, there are two sets of square bracket pairs, causing the genre labels to look strange on the front-end
  """
  artist.genres = json.dumps(artist.genres[0])
  artist.genres = json.dumps(artist.genres[len(artist.genres) - 1])

  #If the form is valid
  if form.validate():
    try:
      artist.name = form.name.data,
      artist.city = form.city.data,
      artist.state = form.state.data,
      artist.phone = form.phone.data,
      artist.genres = form.genres.data
      artist.facebook_link = form.facebook_link.data,
      artist.website_link = form.website_link.data,
      artist.image_link = form.image_link.data,
      artist.seeking_venues = form.seeking_venues.data,
      artist.seeking_description = form.seeking_description.data

      db.session.add(artist)
      db.session.commit()

      flash("Artist " + "\"" + request.form['name'] + "\"" + " has been updated successfully!")
      return redirect(url_for('show_artist', artist_id=artist_id))


    except:
      db.session.rollback()
      print(sys.exc_info())

      flash("ERROR: Artist " + request.form['name'] + "could not be updated!")
      return render_template('forms/edit_artist.html', form=form, artist=artist)

    finally:
      db.session.close()

  #If the form is not valid
  else:
    flash(form.errors)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


#Edit Venue Routes
#For code-specific comments, please refer to "edit_artist" above
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue = Venue.query.get(venue_id)
  venue.genres = json.loads(venue.genres)

  """[genre.replace('[', '') for genre in venue.genres]
  [genre.replace(']', '') for genre in venue.genres]"""


  form = VenueForm(
    name = venue.name,
    city = venue.city,
    state = venue.state,
    address = venue.address,
    phone = venue.phone,
    genres = venue.genres,
    facebook_link = venue.facebook_link,
    website_link = venue.website_link,
    image_link = venue.image_link,
    seeking_talent = venue.seeking_talent,
    seeking_description = venue.seeking_description

  )

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  venue.genres = json.dumps(venue.genres[0])
  venue.genres = json.dumps(venue.genres[len(venue.genres) - 1])


  if form.validate():
    try:
      venue.name = form.name.data,
      venue.city = form.city.data,
      venue.address = form.address.data,
      venue.state = form.state.data,
      venue.phone = form.phone.data,
      venue.genres = form.genres.data
      venue.facebook_link = form.facebook_link.data,
      venue.website_link = form.website_link.data,
      venue.image_link = form.image_link.data,
      venue.seeking_talent = form.seeking_talent.data,
      venue.seeking_description = form.seeking_description.data

      db.session.add(venue)
      db.session.commit()

      flash("Venue " + "\"" + request.form['name'] + "\"" + " has been updated successfully!")
      return redirect(url_for('show_venue', venue_id=venue_id))


    except:
      db.session.rollback()
      print(sys.exc_info())

      flash("ERROR: Venue " + request.form['name'] + "could not be updated!")
      return render_template('forms/edit_venue.html', form=form, venue=venue)

    finally:
      db.session.close()

  
  else:
    flash(form.errors)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


#  Create Artist Routes
#  ----------------------------------------------------------------

#For code-specific comments, please refer to the "Create Venue" section above
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)

  artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        website_link=form.website_link.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        seeking_venues=form.seeking_venues.data,
        seeking_description=form.seeking_description.data

      )


  name_count = db.session.query(Artist).filter(form.name.data == Artist.name).count()

  if form.validate():
    if name_count == 1:
      flash("\"" + request.form['name'] + "\" is already in the database! Please enter a new artist.")
      return render_template('forms/new_artist.html', form=form)

    else:
      db.session.add(artist)
      db.session.commit()

      show_recently_created()
      
      flash("\"" + request.form['name'] + '\" was added successfully!')
      return render_template('pages/home.html', form=form, artists=show_recently_created.artist_data, venues=show_recently_created.venue_data)


  else:
    flash(form.errors)
    return render_template('forms/new_artist.html', form=form)


#  shows
#  ----------------------------------------------------------------

#Shows route
@app.route('/shows')
def shows():
  
  try:
    
    current_datetime = datetime.today()

    #Retrieves show information via join statements with the Artist and Venue tables
    show_info = db.session.query(Shows.venue_id, Venue.name, Shows.artist_id, Artist.name, Artist.image_link, Shows.start_time).join(Venue).join(Artist)
    
    #Queries for Past Shows and Upcoming Shows
    past_shows = show_info.filter(Shows.start_time <= current_datetime).order_by(desc(Shows.start_time))
    upcoming_shows = show_info.filter(Shows.start_time > current_datetime).order_by(Shows.start_time)
    
    #Variables that keep track of past and upcoming shows
    past_shows_count = past_shows.count()
    upcoming_shows_count = upcoming_shows.count()

    show_info.num_past_shows = past_shows_count
    show_info.num_upcoming_shows = upcoming_shows_count

    #Lists of past and upcoming shows
    show_info.list_past_shows = []
    show_info.list_upcoming_shows = []

    #Displays past shows
    for shows_data in past_shows:
      show_venue_id=shows_data[0]
      show_venue_name=shows_data[1]
      show_artist_id=shows_data[2]
      show_artist_name=shows_data[3]
      show_artist_image_link=shows_data[4]
      show_start_time=shows_data[5]
      

      show_info.list_past_shows.append({
      "venue_id": show_venue_id,
      "venue_name": show_venue_name,
      "artist_id": show_artist_id,
      "artist_name": show_artist_name,
      "artist_image_link": show_artist_image_link,
      "start_time": str(show_start_time)
      
      })

    
    #Displays upcoming shows
    for shows_data in upcoming_shows:
      show_venue_id=shows_data[0]
      show_venue_name=shows_data[1]
      show_artist_id=shows_data[2]
      show_artist_name=shows_data[3]
      show_artist_image_link=shows_data[4]
      show_start_time=shows_data[5]
      

      show_info.list_upcoming_shows.append({
      "venue_id": show_venue_id,
      "venue_name": show_venue_name,
      "artist_id": show_artist_id,
      "artist_name": show_artist_name,
      "artist_image_link": show_artist_image_link,
      "start_time": str(show_start_time)
      

      })

  except:
    print(sys.exc_info())
    flash('Error: The shows could not be displayed!')

  
  return render_template('pages/shows.html', show=show_info)


#Create Show routes
@app.route('/shows/create', methods=['GET'])
def create_shows():

  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  form = ShowForm(request.form)

  #Populates shows table with Artist and Venue ids based on the Artist and Venue Name
  get_artist_id = db.session.query(Artist.id).filter(form.artist_name.data==Artist.name).first()
  get_venue_id = db.session.query(Venue.id).filter(form.venue_name.data==Venue.name).first()

  
  #Represents each show instance
  show = Shows(
    artist_id=get_artist_id,
    venue_id=get_venue_id,
    start_time=form.start_time.data
  )

  #Variables that check the existence of the entered Artist and Venue names
  artistname_count = db.session.query(Artist).filter(form.artist_name.data==Artist.name).count()
  venuename_count = db.session.query(Venue).filter(form.venue_name.data==Venue.name).count()

  """
  The following two queries check if a show exists in the database with any of the following combinations:

  1. Artist and Start Time
  2. Venue and Start Time
  3. Artist, Venue, and Start Time
  """
  start_time_join_query = db.session.query(Shows, Artist.name, Venue.name).join(Artist).join(Venue)
  
  start_time_count = start_time_join_query.filter(
    or_(form.artist_name.data == Artist.name, form.venue_name.data == Venue.name), 
    form.start_time.data == Shows.start_time
  ).count()


  

  #If the form is valid
  if form.validate():

    #If the artist and venue exist
    if artistname_count == 1 and venuename_count == 1:
      
      #If a start date & time already exists with a given artist and/or venue
      if start_time_count == 1:
        message = "ERROR: A show with " + Markup("<b>ONE</b>") + " of the following combinations exists in the database! Please check the \"Shows\" page!" \
        + Markup("<br /><br />") \
        + Markup("<b>1)</b>") + " Artist and Start Time " \
        + Markup("<b style='margin-left: 10px;'>2)</b>") + " Venue and Start Time " \
        + Markup("<b style='margin-left: 10px;'>3)</b>") + " Artist, Venue, and Start Time" 

        flash(message)
        return render_template('forms/new_show.html', form=form)

      else:
        db.session.add(show)
        db.session.commit()

        show_recently_created()

        flash("The show was submitted successfully! It can be viewed on the \"Shows\" page.")
        return render_template('pages/home.html', form=form, artists=show_recently_created.artist_data, venues=show_recently_created.venue_data)

    #If the artist and/or venue does NOT exist
    else:
    
      if artistname_count != 1 and venuename_count == 1:
        flash("ERROR: Artist " + "\"" + request.form['artist_name'] + "\" does NOT exist in the database!")

      elif artistname_count == 1 and venuename_count != 1:
        flash("ERROR: Venue " + "\"" + request.form['venue_name'] + "\" does NOT exist in the database!")

      else:
        flash("ERROR: The entered Artist and Venue do NOT exist in the database!")

      return render_template('forms/new_show.html', form=form)
  
  #If the form is invalid
  else:
    flash(form.errors)
    return render_template('forms/new_show.html', form=form)

