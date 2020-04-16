# Fyyur

(Pronounced "fire")

### Description

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Tech Stack


* **SQLAlchemy ORM**
* **PostgreSQL**
* **Python** and **Flask**
* **Flask-Migrate**
* **HTML**, **CSS**, and **Javascript**

### Main Files: Project Structure

  ```
  ├── run.py ***Main app driver file ***
  ├── config.py *** Defines Database URI ***
  ├── README.md
  ├── requirements.txt *** The dependencies to install ***
  ├── error.log
  
  
  /app: Folder that contains:
  
  * Back-end Python logic (i.e. models, controllers, forms)
  * Migration files (when the database schema is updated)
  
  ├── /app
      ├──/mvc_backend_code
          ├── models.py
          ├── controllers.py
          ├── forms.py
          
      ├──/migrations
      ├──__init__.py
      
  ├── /front_end
      ├── static
      │   ├── css 
      │   ├── font
      │   ├── ico
      │   ├── img
      │   └── js
      └── templates
          ├── errors
          ├── forms
          ├── layouts
          └── pages
  ```

### Development Setup

To start and run the local development server,

1. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
