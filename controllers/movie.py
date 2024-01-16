from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from controllers.parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        film = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(film)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        try:
            obj = Movie.query.filter_by(id=row_id).first()
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    required_fields = ['name', 'genre', 'year']
    if not all(field in data for field in required_fields):
        err = 'Missing required fields: {}'.format(', '.join(required_fields))
        return make_response(jsonify(error=err), 400)
    if 'year' in data:
        try:
            year_int = int(data['year'])
        except:
            err = 'Year must be integer'
            return make_response(jsonify(error=err), 400)

    new_movie = Movie.create(**data)



    new_movie_data = {k: v for k, v in new_movie.__dict__.items() if k in MOVIE_FIELDS}
    return make_response(jsonify(new_movie_data), 200)

def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        exists = Movie.query.filter_by(id=row_id).first() is not None
        if exists:

            allowed = {'id', 'name', 'genre', 'year'}
            for key in data.keys():
                if key not in allowed:
                    err = 'Id must be integer'
                    return make_response(jsonify(error=err), 400)

            if 'year' in data.keys():
                try:
                    int(data['year'])
                except:
                    err = 'Year must be integer'
                    return make_response(jsonify(error=err), 400)

            upd_record = Movie.update(row_id, **data)
            upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
            return make_response(jsonify(upd_movie), 200)
        else:
            msg = 'Record was not found'
            return make_response(jsonify(message=msg), 400)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()

    if 'id' not in data:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be an integer'
        return make_response(jsonify(error=err), 400)

    deleted_movie_id = Movie.delete(row_id)

    if deleted_movie_id == 0:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    msg = f'Record with id {deleted_movie_id} successfully deleted'
    return make_response(jsonify(message=msg), 200)

def movie_add_relation():
    """
    Add actor to movie's cast
    """

    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        movie = Movie.query.filter_by(id=row_id).first()
        if movie is None:
            err = 'Id doesn\'t exist'
            return make_response(jsonify(error=err), 400)

        if 'relation_id' not in data.keys():
            err = 'Relation Id doesn\'t exist'
            return make_response(jsonify(error=err), 400)

        try:
            actor_id = int(data['relation_id'])
        except:
            err = 'Relation Id must be integer'
            return make_response(jsonify(error=err), 400)

        actor = Actor.query.filter_by(id=actor_id).first()
        if actor is None:
            err = 'Actor Id doesn\'t exist'
            return make_response(jsonify(error=err), 400)

        movie = Movie.add_relation(row_id, actor)  # add relation here
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        if Movie.query.filter_by(id=row_id).first() is None:
            err = 'Id must be correct'
            return make_response(jsonify(error=err), 400)

        movie = Movie.clear_relations(row_id)
        rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
