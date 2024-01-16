from flask import jsonify, make_response
from settings.constants import ACTOR_FIELDS, DATE_FORMAT
from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS  # to make response pretty
from controllers.parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
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
            obj = Actor.query.filter_by(id=row_id).first()
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()

    try:
        if 'name' not in data.keys() or 'gender' not in data.keys() or 'date_of_birth' not in data.keys():
            err = 'Could not add new record cause of missed field'
            return make_response(jsonify(error=err), 400)

        dt.strptime(data.get('date_of_birth'), DATE_FORMAT)

        new_record = Actor.create(**data)
        new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
        return make_response(jsonify(new_actor), 200)
    except:
        err = 'Could not add new record'
        return make_response(jsonify(error=err), 400)
def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        exists = Actor.query.filter_by(id=row_id).first() is not None
        if exists:

            allowed = {'id', 'name', 'gender', 'date_of_birth'}
            for key in data.keys():
                if key not in allowed:
                    err = 'Id must be integer'
                    return make_response(jsonify(error=err), 400)

            if 'date_of_birth' in data.keys():
                try:
                    dt.strptime(data.get('date_of_birth'), DATE_FORMAT)
                except:
                    err = 'Date of birthday must be in correct format'
                    return make_response(jsonify(error=err), 400)

            upd_record = Actor.update(row_id, **data)
            upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
            return make_response(jsonify(upd_actor), 200)
        else:
            msg = 'Record was not found'
            return make_response(jsonify(message=msg), 400)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)



def delete_actor():
    """
    Delete actor by id
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

    deleted_actor_id = Actor.delete(row_id)

    if deleted_actor_id == 0:
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    msg = f'Record with id {deleted_actor_id} successfully deleted'
    return make_response(jsonify(message=msg), 200)



def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        actor = Actor.query.filter_by(id=row_id).first()
        if actor is None:
            err = 'Id doesn\'t exist'
            return make_response(jsonify(error=err), 400)

        if 'relation_id' not in data.keys():
            err = 'Relation Id doesn\'t exist'
            return make_response(jsonify(error=err), 400)

        try:
            movie_id = int(data['relation_id'])
        except:
            err = 'Relation Id must be integer'
            return make_response(jsonify(error=err), 400)

        movie = Movie.query.filter_by(id=movie_id).first()
        if movie is None:
            err = 'Movie id is wrong'
            return make_response(jsonify(error=err), 400)

        actor = Actor.add_relation(row_id, movie)  # add relation here
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def actor_clear_relations():
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

        if Actor.query.filter_by(id=row_id).first() is None:
            err = 'Id must be correct'
            return make_response(jsonify(error=err), 400)

        actor = Actor.clear_relations(row_id)
        rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        rel_actor['filmography'] = str(actor.filmography)
        return make_response(jsonify(rel_actor), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

