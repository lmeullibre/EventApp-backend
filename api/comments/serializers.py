from flask_restplus import fields
from api.restplus import api

comment = api.model('Comment', {
    'id': fields.Integer(),
    'user_id': fields.Integer(),
    'user_name': fields.String(),
    'user_photo': fields.String(),
    'text': fields.String(),
})

create_comment = api.model('Add Comment', {
    'event_id': fields.Integer(required=True, description='Event where the comment was posted'),
    'text': fields.String(),
})
