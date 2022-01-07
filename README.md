## Fyyur

### Dependencies
This project depends on the following
1. [Flask](https://flask.palletsprojects.com/en/2.0.x/)
2. [Babel](https://babeljs.io/)
3. [Sql-Alchemy]https://www.sqlalchemy.org/)
4. [Psycopg2](https://www.psycopg.org/)

### Introduction

Fyyur is a venue and artist booking site that lets an artist find a venue and venue to find an artist. This site lets you post a new artists and venues, create shows linking an artist and a venue.

### Steps to run this application

1. Clone this repo:

   ```
   $ git clone https://github.com/Biswas-N/fyyur.git
   ```

2. Create an environment (using `virtualenv`) and activate the environment (for windows):
   ```
   $ virtualenv env
   $ source env/Scripts/activate
   ```
3. Install the dependencies:

   ```
   $ pip install -r requirements.txt
   ```

4. Edit config.py and add you database path
5. Apply the migrations to the database

   ```
   $ flask db upgrate
   ```

6. Run the development server:

   ```
   $ python3 app.py
   ```

7. Navigate to Home page [http://localhost:8000/](http://localhost:8000/)
