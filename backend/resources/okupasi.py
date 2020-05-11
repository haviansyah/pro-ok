from flask import Response, request
from database.models import Okupasi, Kompetensi
from flask_restful import Resource

from mongoengine.errors import FieldDoesNotExist, \
NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError
from resources.errors import InternalServerError, SchemaValidationError, IdAlreadyExistsError, UpdatingError, DeletingError, NotExistsError, UnauthorizedError, errors
from resources.helper import JSONEncoder
from mq.mq import sendReTrain, sendTrain


# Okupasi Controller

class OkupasiApi(Resource):
    def get(self):
        columns = ["id","Kode Okupasi","Nama Okupasi","Jumlah Kompetensi"]
        okupasis = Okupasi.objects()
        okupasi_list = []
        for okupasi in okupasis:
            new_okupasi = [
                okupasi["id"],
                okupasi["kode_okupasi"],
                okupasi["nama_okupasi"],
                len(okupasi["kompetensi_list"])
            ]
            okupasi_list.append(new_okupasi)
        result = {
            "columns" : columns,
            "data" : okupasi_list
        }
        return Response(JSONEncoder().encode(result),mimetype="application/json", status=200)

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
        columns = ["id","Kode Kompetensi","Nama Kompetensi","Sikap","Keterampilan","Pengetahuan"]
        kompetensis = Kompetensi.objects()
        kompetensi_list = []
        for kompetensi in kompetensis:
            new_kompetensi = [
                kompetensi["id"],
                kompetensi["kode_kompetensi"],
                kompetensi["nama_kompetensi"],
                kompetensi['sikap'],
                kompetensi['keterampilan'],
                kompetensi['pengetahuan']
            ]
            kompetensi_list.append(new_kompetensi)
        result = {
            'columns' : columns,
            'data' : kompetensi_list
        }
        return Response(JSONEncoder().encode(result),mimetype="application/json", status=200)
    
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