from flask_restplus import Resource, fields
from database.models import User
from api.restplus import api
from flask import request
from database import db
from database.models import RefreshToken
import settings
import jwt
import datetime
import hashlib


ns = api.namespace('users/auth', description='Operations related to authentication')

return_token_model = api.model('ReturnToken', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})

login_model = api.model('LoginModel', {
    'mail': fields.String(required=True),
    'password': fields.String(required=True)
})


@ns.route('/')
@api.response(401, 'User or password incorrect')
class Login(Resource):

    @api.response(200, 'Login ok')
    @api.expect(login_model)
    def post(self):
        data = request.json
        user = User.query.filter_by(mail=data['mail']).first()
        if not user:
            api.abort(code=400, message="Incorrect username or password")

        if user.password == data['password']:
            _access_token = jwt.encode({'uid': user.id,
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       settings.PASSWORD_JWT).decode('utf-8')
            _refresh_token = jwt.encode({'uid': user.id,
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                                         'iat': datetime.datetime.utcnow()},
                                        settings.PASSWORD_JWT).decode('utf-8')

            user_agent_string = request.user_agent.string.encode('utf-8')
            user_agent_hash = hashlib.md5(user_agent_string).hexdigest()

            refresh_token = RefreshToken.query.filter_by(user_agent_hash=user_agent_hash).first()

            if not refresh_token:
                refresh_token = RefreshToken(user_id=user.id, refresh_token=_refresh_token,
                                             user_agent_hash=user_agent_hash)
            else:
                refresh_token.refresh_token = _refresh_token

            db.session.add(refresh_token)
            db.session.commit()
            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        api.abort(401, 'Incorrect username or password')


class Refresh(Resource):
    @api.expect(api.model('RefreshToken', {'refresh_token': fields.String(required=True)}), validate=True)
    @api.response(200, 'Success', return_token_model)
    def post(self):
        _refresh_token = request.json['refresh_token']

        try:
            payload = jwt.decode(_refresh_token, settings.PASSWORD_JWT)

            refresh_token = RefreshToken.query.filter_by(user_id=payload['uid'], refresh_token=_refresh_token).first()

            if not refresh_token:
                raise jwt.InvalidIssuerError

            # Generate new pair

            _access_token = jwt.encode({'uid': refresh_token.user_id,
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       settings.PASSWORD_JWT).decode('utf-8')
            _refresh_token = jwt.encode({'uid': refresh_token.user_id,
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
                                         'iat': datetime.datetime.utcnow()},
                                        settings.PASSWORD_JWT).decode('utf-8')

            refresh_token.refresh_token = _refresh_token
            db.session.add(refresh_token)
            db.session.commit()

            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        except jwt.ExpiredSignatureError as e:
            raise e
        except (jwt.DecodeError, jwt.InvalidTokenError)as e:
            raise e
        except Exception as e:
            api.abort(401, 'Unknown token error' + str(e))
