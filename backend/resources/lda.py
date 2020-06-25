from flask import Response, request
from flask_restful import Resource, reqparse
from database.models import Okupasi, Kompetensi, Jurusan, Matakuliah
from ml.lda import LDA
from mq.mq import sendReTrain, sendTrain
import json.encoder 
from resources.errors import InternalServerError, SchemaValidationError, IdAlreadyExistsError, UpdatingError, DeletingError, NotExistsError, UnauthorizedError
from resources.global_var import get_current_state,edit_current_state
import sys

class LdaStatusApi(Resource):
    def get(self):
        return get_current_state()["status"],200

class LdaAPI(Resource):
    def get(self):
        jmlOkupasi = Okupasi.objects.count()
        jmlKompetensi = Kompetensi.objects.count()
        jmlJurusan = Jurusan.objects.count()
        jmlMatakuliah = Matakuliah.objects.count()
        result = {
            "jumlah_okupasi" : jmlOkupasi,
            "jumlah_kompetensi" : jmlKompetensi,
            "jumlah_jurusan" : jmlJurusan,
            "jumlah_matakuliah" : jmlMatakuliah,
        }
        return result, 200

class LdaTrainAPI(Resource):
    def get(self):
        edit_current_state()
        try:
            sendReTrain()
            result = {
                "status" : "success",
            }
            return result, 200
        except Exception as e:
            raise e
            result = {
                "status" : "error",
            }
            return result,405

class LdaOneAPI(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('kode_jurusan', type=str)
            parser.add_argument('kode_okupasi', type=str)
            parsing = parser.parse_args()
            
            kode_jurusan = parsing["kode_jurusan"]
            kode_okupasi = parsing["kode_okupasi"]

            hasil, total_cocok = LDA().getSimilarity(kode_jurusan,kode_okupasi)
            
            outputs = []
            for h in hasil:
                output = {
                    "nama_kompetensi" :h["nama_kompetensi"], 
                    "cocok" : bool(len(h["kecocokan"]))}
		    #"cocok" : h["kecocokan"]}
                outputs.append(output)
            total_kompetensi = len(outputs);
            status = "success"
        except Exception as e:
            print(e,file=sys.stderr)
            status = "error"
        result = {
            "status" : status,
            "results" : None if status == "error" else {
                "kecocokan" : 0 if total_kompetensi == 0 else total_cocok / total_kompetensi,
                "total_cocok" : total_cocok,
                "total_kompetensi" : len(outputs),
                "result" : outputs}
        }
        

        return result,200

class LdaOneApiDetail(Resource):
    
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('kode_jurusan', type=str)
            parser.add_argument('kode_okupasi', type=str)
            parsing = parser.parse_args()
            
            kode_jurusan = parsing["kode_jurusan"]
            kode_okupasi = parsing["kode_okupasi"]

            hasil, total_cocok = LDA().getSimilarity(kode_jurusan,kode_okupasi)
            
            outputs = []
            for h in hasil:
                output = {
                    "nama_kompetensi" :h["nama_kompetensi"], 
                    # "cocok" : bool(len(h["kecocokan"]))}
		            "cocok" : h["kecocokan"]}
                outputs.append(output)
            total_kompetensi = len(outputs);
            status = "success"
        except Exception as e:
            print(e,file=sys.stderr)
            status = "error"
        result = {
            "status" : status,
            "results" : None if status == "error" else {
                "kecocokan" : 0 if total_kompetensi == 0 else total_cocok / total_kompetensi,
                "total_cocok" : total_cocok,
                "total_kompetensi" : len(outputs),
                "result" : outputs}
        }
        

        return result,200

