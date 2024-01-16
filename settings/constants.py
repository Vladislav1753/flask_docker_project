import os
# db connection URL (In order to submit your project do NOT change this value!!!)

DB_URL = os.environ['DB_URL']

#os.environ.get('DB_URL')

#if DB_URL is None:
#    DB_URL = 'postgresql+psycopg2://test_user:password@localhost:5432/test_db'

# entities properties
ACTOR_FIELDS = ['id', 'name', 'gender', 'date_of_birth']
MOVIE_FIELDS = ['id', 'name', 'year', 'genre']

# date of birth format
DATE_FORMAT = '%d.%m.%Y'