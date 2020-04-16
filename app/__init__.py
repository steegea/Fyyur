#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import dateutil.parser
import babel

import logging
from logging import Formatter, FileHandler

#Flask imports
from flask import Flask, render_template

from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


# Application object
app = Flask(__name__, template_folder= "../front_end/templates", static_folder="../front_end/static")

# Configuration statement
app.config.from_object('config')

#Connects the app to different libraries
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE, MMMM d, y 'at' h:mma"
  elif format == 'medium':
      format="EE, MM dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime



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


