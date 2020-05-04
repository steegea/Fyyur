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

To start and run your local server, you can create one of the following:

#### Virtualenv
  ```
  $ cd Your_Project_Directory
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```
  
  or 
  
 #### Pipenv
  Alternatively, you can create an **Pipenv** by doing the following:
  ```
  $ cd Your_Project_Directory
  $ pipenv install
  $ pipenv shell  (Activates the Pipenv)
  ```

2. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

3. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 run.py (or python run.py for Windows users)
  ```

4. Navigate to Home page [http://localhost:5000](http://localhost:5000)
