from .jurusan import JurusanApi, JurusanOneApi, MatakuliahApi, MatakuliahOneApi
from .okupasi import *
from .lda import *
from .auth import SignupApi, LoginApi, MeApi


def initialize_routes(api):

    api.add_resource(SignupApi,'/api/auth/signup')
    api.add_resource(LoginApi,'/api/auth/login')
    api.add_resource(MeApi,'/api/me')

    api.add_resource(JurusanApi,'/api/jurusan')
    api.add_resource(JurusanOneApi,'/api/jurusan/<id>')
    api.add_resource(MatakuliahApi,'/api/matakuliah')
    api.add_resource(MatakuliahOneApi,'/api/matakuliah/<id>')

    api.add_resource(OkupasiApi,'/api/okupasi')
    api.add_resource(OkupasiOneApi,'/api/okupasi/<id>')
    api.add_resource(KompetensiApi,'/api/kompetensi')
    api.add_resource(KompetensiOneApi,'/api/kompetensi/<id>')

    api.add_resource(LdaOneAPI,'/api/lda')
    api.add_resource(LdaOneApiDetail,'/api/lda-detail')
    api.add_resource(LdaTrainAPI,'/api/lda/train')


    api.add_resource(LdaAPI,'/api/dashboard')
    api.add_resource(LdaStatusApi,'/api/lda/status')
