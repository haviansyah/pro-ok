from flask import request
from flask import Response, request
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.models import User
from flask_restful import Resource
import datetime

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id':str(id)}, 200

class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error' : 'Email or password invalid'},401
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {'accessToken': access_token}, 200

class MeApi(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = User.objects.get(id=user_id)
        return Response(user.to_json(),mimetype="application/json", status=200)
