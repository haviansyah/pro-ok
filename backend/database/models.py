from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from bson.objectid import ObjectId

class User(db.Document):
    fullname = db.StringField()
    username = db.StringField()
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)

    def hash_password(self):
       self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

        
class Matakuliah(db.Document):
    kode_matakuliah = db.StringField(required=True,unique=True)
    nama_matakuliah = db.StringField(required=True)
    sikap = db.StringField()
    keterampilan = db.StringField()
    pengetahuan = db.StringField()
    token = db.ListField(db.StringField())
    meta = {'strict': False}



class Jurusan(db.Document):
    kode_jurusan = db.StringField(requied=True,unique=True)
    nama_jurusan = db.StringField(required=True)
    matakuliah_list = db.ListField(db.ReferenceField(Matakuliah))
    meta = {'strict': False}
    
    @property
    def matakuliah(self):
        return [ Matakuliah.objects().get(id=matkul.id).to_mongo() for matkul in self.matakuliah_list  ]



class Kompetensi(db.Document):
    kode_kompetensi = db.StringField(required=True,unique=True)
    nama_kompetensi = db.StringField(required=True)
    deskripsi = db.StringField()
    sikap = db.StringField()
    keterampilan = db.StringField()
    pengetahuan = db.StringField()
    token = db.ListField(db.StringField())
    meta = {'strict': False}



class Okupasi(db.Document):
    kode_okupasi = db.StringField(required=True,unique=True)
    nama_okupasi = db.StringField(required=True)
    kompetensi_list = db.ListField(db.ReferenceField(Kompetensi))
    @property
    def kompetensi(self):
        return [ Kompetensi.objects().get(id=komp.id).to_mongo() for komp in self.kompetensi_list  ]
    meta = {'strict': False}
    


class GlobalVar(db.Document):
    constant = db.DynamicField()
    current_state = db.DynamicField()
    meta = {'collection':'global_var','strict': False}

