from flask import request
from flask_restplus import Resource
# from api.events.logic import add_event, delete_event
from api.events.serializers import create_report, report
from api.events.logic import add_report, delete_report
from api.utils import get_id_form_token
from api.restplus import api
from database.models import Report

ns = api.namespace('events/report', description='Operations related to reports of the events')


@ns.route('/')
class ReportCollection(Resource):

    @api.marshal_list_with(report)
    def get(self):
        """
        Returns list of all the reports.
        """
        reports = Report.query.all()
        print(reports)
        return reports

    @api.response(201, 'Event successfully created.')
    @api.expect(create_report)
    def post(self):
        """
        Creates a new report.
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            add_report(data, user_id)
        except Exception as e:
            api.abort(code=400, message="We had an error with your request, " + str(e))
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Event not found.')
class EventItem(Resource):

    @api.marshal_with(report)
    def get(self, id):
        """
        Returns a report with its details.
        """
        try:
            result = Report.query.filter(Report.event_id == id).all()
        except Exception as e:
            api.abort(code=404, message="Report not found" + str(e))
        return result

    @api.response(204, 'Report successfully deleted.')
    def delete(self, id):
        """
        Deletes a report.
        """
        try:
            delete_report(id)
        except Exception as e:
            api.abort(code=404, message="Report not found" + str(e))
        return None, 204
