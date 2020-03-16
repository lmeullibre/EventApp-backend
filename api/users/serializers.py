from flask_restplus import fields
from api.restplus import api


user = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of an user'),
    'name': fields.String,
    'mail': fields.String,
    'photo': fields.String,
    'birth_date': fields.DateTime,
    'bio': fields.String,
    'telephone': fields.String,
    'instagram': fields.String,

})

create_user = api.model('Create User', {
    'name': fields.String,
    'mail': fields.String,
    'photo': fields.String,
    'birth_date': fields.DateTime,
    'password': fields.String,
    'bio': fields.String,
    'telephone': fields.String,
    'instagram': fields.String,
})

edit_user = api.model('Update User', {
    'name': fields.String,
    'mail': fields.String,
    'photo': fields.String,
    'birth_date': fields.DateTime,
    'bio': fields.String,
    'telephone': fields.String,
    'instagram': fields.String,
})

funded_event = api.model('Funded event', {
    'event_id': fields.Integer(),
    'event_name': fields.String(),
    'funding_amount': fields.Float(),
})


voted_event = api.model('Voted event', {
    'event_id': fields.String(),
    'stars': fields.Float(),
})

watching_user = api.model('Watching User', {
    'events_watching': fields.List(fields.Integer)
})

funding_user = api.model('Funding User', {
    'events_funding': fields.List(fields.Nested(funded_event))
})

voting_user = api.model('Voting User', {
    'events_voting': fields.List(fields.Nested(voted_event))
})
