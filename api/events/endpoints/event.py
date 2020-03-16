from datetime import datetime
from flask import request
from flask_restplus import Resource
from api.events.logic import add_event, delete_event, update_event, watch_event, fund_event, vote_event, get_info_events
from api.events.serializers import create_event, event, edit_event, watch, fund, vote, money, stars
from api.utils import get_id_form_token
from api.restplus import api
from database.models import Event, Tag, tags


ns = api.namespace('events', description='Operations related to events')


@ns.route('/')
class EventCollection(Resource):

    @api.marshal_list_with(event)
    def get(self):
        """
        Returns list of all the events.
        """
        name = request.args.get('name')
        stars = request.args.get('stars')
        if stars is not None:
            stars = float(stars)
        fromDate = request.args.get('fromDate')
        if fromDate is not None:
            fromDate = datetime.strptime(fromDate, "%Y-%m-%dT%H:%M:%S.%f%z")
        toDate = request.args.get('toDate')
        if toDate is not None:
            toDate = datetime.strptime(toDate, "%Y-%m-%dT%H:%M:%S.%f%z")
        location = request.args.get('location')
        tag_filter = request.args.get('tags')
        if tag_filter is not None:
            tag_filter = request.args.get("tags").split(',')

        id_param = request.args.get('id')

        result = Event.query

        if id_param is not None:
            id_list = id_param.split(',')
            result = result.filter(Event.id.in_(id_list))
        if location is not None:
            result = result.filter(Event.location == location)
        if fromDate is not None:
            result = result.filter(Event.event_start_date >= fromDate)
        if toDate is not None:
            result = result.filter(Event.event_end_date <= toDate)
        if name is not None:
            result = result.filter(Event.name.contains(name))
        if stars is not None:
            result = result.filter(Event.stars >= stars)
        if tag_filter is not None:
            result = result.join(tags).join(Tag).filter(Tag.tag_name.in_(tag_filter))

        print(result.all())
        return get_info_events(result.all())

    @api.response(201, 'Event successfully created.')
    @api.expect(create_event)
    def post(self):
        """
        Creates a new event.
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            result_event = add_event(data, user_id)
        except Exception as e:
            api.abort(code=400, message="We had an error with your request, " + str(e))
        return result_event, 201


@ns.route('/<int:id>')
@api.response(404, 'Event not found.')
class EventItem(Resource):
    @api.marshal_with(event)
    def get(self, id):
        """
        Returns an event with its details.
        """
        try:
            result = get_info_events(Event.query.get(id))
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return result

    @api.response(202, 'Event successfully deleted.')
    def delete(self, id):
        """
        Deletes an event.
        """
        try:
            result_event = delete_event(id)
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return result_event.id, 202

    @api.expect(edit_event)
    @api.response(202, 'Event succesfully updated')
    def put(self, id):
        """
        Update the event details
        """
        data = request.json
        try:
            update_event(id, data)
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return id, 202


@ns.route('/<int:id>/watch')
@api.response(404, 'Event not found.')
class EventWatch(Resource):

    @api.expect(watch)
    @api.response(202, 'Event succesfully updated')
    def put(self, id):
        """
        Fav an event
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            watch_event(id, data, user_id)
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return id, 202


@ns.route('/<int:id>/fund')
@api.response(404, 'Event not found.')
class EventFund(Resource):

    @api.expect(fund)
    @api.response(202, 'Event succesfully funded')
    def put(self, id):
        """
        Fund an event with the given money
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            fund_event(id, data, user_id)
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return id, 202


@ns.route('/<int:id>/vote')
@api.response(404, 'Event not found.')
class EventVote(Resource):
    @api.expect(vote)
    @api.response(202, 'Event succesfully funded')
    def put(self, id):
        """
        Vote an event with the given stars
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            vote_event(id, data, user_id)
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))
        return id, 202


@ns.route('/<int:id>/acumulated')
@api.response(404, 'User not found.')
class EventAcumulated(Resource):
    @api.marshal_with(money)
    def get(self, id):
        """
        Returns the money paid to a given event
        """
        try:
            result = Event.query.get(id)
            sum = 0.0
            for x in result.backers:
                sum += x.fund_amount
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return {'money': sum}


@ns.route('/<int:id>/voted')
@api.response(404, 'User not found.')
class EventVoted(Resource):
    @api.marshal_with(stars)
    def get(self, id):
        """
        Returns the average stars of an event
        """
        try:

            result = Event.query.get(id)
            sum = 0.0
            num = 0
            for x in result.votes:
                sum += x.stars
                num = num + 1
            print(sum/num)
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))
        return {'stars': sum/num}
