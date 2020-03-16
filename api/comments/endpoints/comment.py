from flask import request
from flask_restplus import Resource
from api.comments.logic import add_comment, delete_comment, get_info_comments
from api.comments.serializers import create_comment, comment
from api.utils import get_id_form_token
from api.restplus import api
from database.models import Comment, Event, User

ns = api.namespace('comments', description='Operations related to comments')


@ns.route('/')
class CommentCollection(Resource):

    @api.marshal_list_with(comment)
    def get(self):
        """
        Returns list of all the comments
        """
        comments = Comment.query.order_by(Comment.id.desc()).all()
        return get_info_comments(comments)

    @api.response(201, 'Comment successfully created.')
    @api.expect(create_comment)
    def post(self):
        """
        Creates a new comment
        """
        data = request.json
        auth_header = request.headers.get('Authtoken')
        user_id = get_id_form_token(auth_header)
        try:
            add_comment(data, user_id)
        except Exception as e:
            api.abort(code=400, message="We had an error with your request, " + str(e))
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Comment not found.')
class CommentItem(Resource):

    @api.marshal_with(comment)
    def get(self, id):
        """
        Returns a particular comment with its details
        """
        try:
            comment = get_info_comments(Comment.query.get(id))
        except Exception as e:
            api.abort(code=404, message="Comment not found" + str(e))
        return comment

    @api.response(204, 'comment successfully deleted.')
    def delete(self, id):
        """
        Deletes a particular comment
        """
        try:
            delete_comment(id)
        except Exception as e:
            api.abort(code=404, message="Comment not found" + str(e))
        return None, 204


@ns.route('/event/<int:id>')
@api.response(404, 'Event not found')
class CommentsEvent(Resource):

    @api.marshal_list_with(comment)
    def get(self, id):
        """
        Returns all comments from a given event
        """
        try:
            Event.query.filter(Event.id == id).one()
        except Exception as e:
            api.abort(code=404, message="Event not found" + str(e))

        comments = Comment.query.filter(Comment.event_id == id).order_by(Comment.id.desc()).all()
        return get_info_comments(comments)


@ns.route('/user/<int:id>')
@api.response(404, 'User not found')
class CommentsUser(Resource):

    @api.marshal_list_with(comment)
    def get(self, id):
        """
        Returns all comments from a given user
        """
        try:
            User.query.filter(User.id == id).one()
        except Exception as e:
            api.abort(code=404, message="User not found" + str(e))

        comments = Comment.query.filter(Comment.event_id == id).order_by(Comment.id.desc()).all()
        return get_info_comments(comments)
