import json
from flask import Response, request
from database.models import Jurusan, Matakuliah
from flask_restful import Resource
from bson import json_util
from mq.mq import sendReTrain, sendTrain
from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from resources.errors import InternalServerError, SchemaValidationError, IdAlreadyExistsError, UpdatingError, DeletingError, NotExistsError, UnauthorizedError, errors

# Jurusan Controller

class JurusanApi(Resource):
    def get(self):
        columns = [k for k,v in Jurusan._fields.items()]
        jurusans = Jurusan.objects().to_json()
        return Response(json.dumps(columns),mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            movie = Jurusan(**body).save()
            id = movie.id
            return {'id': str(id)}, 200
        except(FieldDoesNotExist, ValidationError):
            error = errors["SchemaValidationError"]
            return error["message"],error["status"]
        except NotUniqueError:
            error = errors["IdAlreadyExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]


class JurusanOneApi(Resource):
    def put(self, id):
        try:
            body = request.get_json()
            Jurusan.objects.get(kode_jurusan=id).update(**body)
            return {'status': "success"}, 200
        except(FieldDoesNotExist, ValidationError):
            error = errors["SchemaValidationError"]
            return error["message"],error["status"]
        except NotUniqueError:
            error = errors["IdAlreadyExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]
    
    def delete(self,id):
        try:
            jurusan = Jurusan.objects.get(kode_jurusan=id).delete()
            return {'status': "success"}, 200
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]

    def get(self,id):
        try :
            jurusan = Jurusan.objects().get(kode_jurusan = id).to_json()
            return Response(jurusan,mimetype="application/json", status=200)
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]


# Mata Kuliah Controller
class MatakuliahApi(Resource):
    def get(self):
        matakuliah = Matakuliah.objects().to_json()
        return Response(matakuliah,mimetype="application/json", status=200)
    
    def post(self):
        try:
            body = request.get_json()
            matakuliah = Matakuliah(**body).save()
            id = matakuliah.id
            sendTrain({
                "collection" : "matakuliah",
                "id" : str(id)
            })
            return {'id': str(id)}, 200
        except(FieldDoesNotExist, ValidationError):
            error = errors["SchemaValidationError"]
            return error["message"],error["status"]
        except NotUniqueError:
            error = errors["IdAlreadyExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]


class MatakuliahOneApi(Resource):
    def get(self,id):
        try :
            matakuliah = Matakuliah.objects().get(kode_matakuliah = id).to_json()
            return Response(matakuliah,mimetype="application/json", status=200)
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]

    def put(self,id):
        try:
            body = request.get_json()
            matkul = Matakuliah.objects.get(kode_matakuliah=id)
            matkul.update(**body)
            sendTrain({
                "collection" : "matakuliah",
                "id" : str(matkul.id)
            })
            return {'status': "success"}, 200
        except(FieldDoesNotExist, ValidationError):
            error = errors["SchemaValidationError"]
            return error["message"],error["status"]
        except NotUniqueError:
            error = errors["IdAlreadyExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]

    def delete(self,id):
        try :
            matakuliah = Matakuliah.objects.get(kode_matakuliah=id).delete()
            sendReTrain()
            return {'status': "success"},200
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]
