from flask import Response, request
from database.models import Okupasi, Kompetensi
from flask_restful import Resource

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import InternalServerError, SchemaValidationError, IdAlreadyExistsError, UpdatingError, DeletingError, NotExistsError, UnauthorizedError, errors

from mq.mq import sendReTrain, sendTrain


# Okupasi Controller

class OkupasiApi(Resource):
    def get(self):
        okupasis = Okupasi.objects().to_json()
        return Response(okupasis,mimetype="application/json", status=200)

    def post(self):
        try:
            body = request.get_json()
            movie = Okupasi(**body).save()
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


class OkupasiOneApi(Resource):
    def put(self, id):
        try:
            body = request.get_json()
            Okupasi.objects.get(kode_okupasi=id).update(**body)
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
            okupasi = Okupasi.objects.get(kode_okupasi=id).delete()
            return {'status': "success"}, 200
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]

    def get(self,id):
        try :
            okupasis = Okupasi.objects().get(kode_okupasi=id).to_json()
            return Response(okupasis,mimetype="application/json", status=200)
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]


# Mata Kuliah Controller

class KompetensiApi(Resource):
    def get(self):
        kompetensi = Kompetensi.objects().to_json()
        return Response(kompetensi,mimetype="application/json", status=200)
    
    def post(self):
        try:
            body = request.get_json()
            kompetensi = Kompetensi(**body).save()
            id = kompetensi.id
            sendTrain({
                "collection" : "kompetensi",
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


class KompetensiOneApi(Resource):
    def get(self,id):
        try :
            kompetensi = Kompetensi.objects().get(kode_kompetensi = id).to_json()
            return Response(kompetensi,mimetype="application/json", status=200)
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]

    def put(self,id):
        try:
            body = request.get_json()
            kompet = Kompetensi.objects.get(kode_kompetensi=id)
            kompet.update(**body)
            sendTrain({
                "collection" : "matakuliah",
                "id" : str(kompet.id)
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
            kompetensi = Kompetensi.objects.get(kode_kompetensi=id).delete()
            sendReTrain()
            return {'status': "success"},200
        except DoesNotExist:
            error = errors["NotExistsError"]
            return error["message"],error["status"]
        except Exception :
            error = errors["InternalServerError"]
            return error["message"],error["status"]