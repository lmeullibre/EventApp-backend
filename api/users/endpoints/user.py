from flask import request
from flask_restplus import Resource
from api.users.logic import add_user, update_user, delete_user
from api.users.serializers import create_user, user, edit_user, watching_user, funding_user, voting_user
from api.restplus import api
from database.models import User, Event

ns = api.namespace('users', description='Operations related to users')


@ns.route('/')
class UserCollection(Resource):

    @api.marshal_list_with(user)
    def get(self):
        """
        Returns list of all users
        """
        users = User.query.all()
        return users

    @api.response(201, 'User successfully created.')
    @api.expect(create_user)
    def post(self):
        """
        Creates a new user.
        """
        data = request.json
        try:
            add_user(data)
        except Exception as e:
            api.abort(code=400, message="We had an error with your request, " + str(e))
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'User not found.')
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, id):
        """
        Returns an user with its details.
        """
        try:
            result = User.query.filter(User.id == id).one()
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return result

    @api.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Deletes an user.
        """
        try:
            delete_user(id)
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return None, 204

    @api.expect(edit_user)
    @api.response(205, 'User succesfully updated')
    def put(self, id):
        """
        Edit a given user.
        """
        data = request.json
        try:
            update_user(id, data)
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return None, 205


@ns.route('/<int:id>/watching')
@api.response(404, 'User not found.')
class UserWatching(Resource):

    @api.marshal_with(watching_user)
    def get(self, id):
        """
        Returns the events an user had watch
        """
        try:
            result = User.query.get(id)
            tests = {'events_watching': list(x.id for x in result.watching)}
            print(tests)
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return tests


@ns.route('/<int:id>/funded')
@api.response(404, 'User not found.')
class UserFunded(Resource):
    @api.marshal_with(funding_user)
    def get(self, id):
        """
        Returns the events an user had fund
        """
        try:
            result = User.query.get(id)
            funded_events = {'events_funding': list({'event_id': x.event_id, 'event_name': Event.query.get(x.event_id).name,
                             'funding_amount': x.fund_amount} for x in result.backed)}
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return funded_events


@ns.route('/<int:id>/voted')
@api.response(404, 'User not found.')
class UserVoted(Resource):
    @api.marshal_with(voting_user)
    def get(self, id):
        """
        Returns the events an user had vote
        """
        try:
            result = User.query.get(id)
            voted_events = {'events_voting': list({'event_id': x.event_id, 'stars': x.stars} for x in result.voted)}
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return voted_events
