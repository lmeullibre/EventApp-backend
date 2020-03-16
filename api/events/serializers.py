from flask_restplus import fields
from api.restplus import api


event = api.model('Event', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a proposta'),
    'name': fields.String(required=True, description='Name of the event'),
    'description': fields.String(required=True, description='Description of the event'),
    'goal': fields.Float,
    'lat': fields.Float,
    'long': fields.Float,
    'funding_start_date': fields.DateTime,
    'funding_end_date': fields.DateTime,
    'creation_date': fields.DateTime,
    'reports': fields.Integer(),
    'event_start_date': fields.DateTime,
    'event_end_date': fields.DateTime,
    'location': fields.String,
    'user_creator': fields.Integer(),
    'tags': fields.List(fields.String(attribute='tag_name')),
    'stars': fields.Float,
    'photo': fields.String(),
    'user_creator_name': fields.String()
})

create_event = api.model('Create Event', {
    'name': fields.String(required=True, description='Name of the event'),
    'description': fields.String(required=True, description='Description of the event'),
    'funding_start_date': fields.DateTime,
    'funding_end_date': fields.DateTime,
    'goal': fields.Float,
    'lat': fields.Float,
    'long': fields.Float,
    'event_start_date': fields.DateTime,
    'event_end_date': fields.DateTime,
    'location': fields.String,
    'tags': fields.List(fields.String),
    'photo': fields.String()
})

edit_event = api.model('Edit Event', {
    'description': fields.String(required=True, description='Description of the event'),
    'event_start_date': fields.DateTime,
    'event_end_date': fields.DateTime,
    'funding_end_date': fields.DateTime,
    'location': fields.String,
    'lat': fields.Float,
    'long': fields.Float,
    'tags': fields.List(fields.String)
})

report = api.model('Report', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a report'),
    'event_id': fields.Integer(),
    'content': fields.String,
})

create_report = api.model('Create Report', {
    'event_id': fields.Integer(),
    'content': fields.String,
})

watch = api.model('Watch Event', {
})

fund = api.model('Fund Event', {
    'fund_amount': fields.Float(),
})

vote = api.model('Vote Event', {
    'stars': fields.Integer(),
})

money = api.model('Money Event', {
    'money': fields.Float(),
})

stars = api.model('Stars Event',{
    'stars': fields.Float(),
})
