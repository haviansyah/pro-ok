from pymongo import MongoClient

class Database():
    
    def __init__(self,dbname):
        self.dbname = dbname
        self.client = MongoClient('localhost', 27017)

    def mongo(self):
        return self.client[self.dbname]

db = Database("prook").mongo()

def flatten(l):
    flat_list = []
    for sublist in l:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def get_constant():
    try :
        constant = db.global_var.find_one({'constant' : {'$exists' : True}})
        return constant["constant"]
    except Exception as e:
        print(str(e))

def get_jurusan(kode_jurusan):
    try :
        jurusan = db.jurusan.find_one({"kode_jurusan" : kode_jurusan})
        return jurusan
    except Exception :
        print(Exception)

def get_all_jurusan():
    try :
        jurusan = db.jurusan.find({})
        return jurusan
    except Exception :
        print(Exception)

def get_all_matakuliah():
    jurusans = get_all_jurusan()
    matkul = [mk for mk in [jurusan["matakuliah"] for jurusan in jurusans] if mk != None]
    hasil = flatten(matkul)
    return hasil


def get_matakuliah(kode_jurusan):
    jurusan = get_jurusan(kode_jurusan)
    return jurusan["matakuliah"]


def get_okupasi(kode_okupasi):
    try :
        okupasi = db.okupasi.find_one({"kode_okupasi" : kode_okupasi})
        return okupasi
    except Exception :
        print(Exception)

def get_all_okupasi():
    try :
        okupasi = db.okupasi.find({})
        return okupasi
    except Exception :
        print(Exception)

def get_all_kompetensi():
    okupasis = get_all_okupasi()
    matkul = [mk for mk in [okupasi["kompetensi"] for okupasi in okupasis if "kompetensi" in okupasi] if mk != None]
    hasil = flatten(matkul)
    return hasil


def get_kompetensi(kode_okupasi):
    okupasi = get_okupasi(kode_okupasi)
    return okupasi["kompetensi"]

if __name__ == "__main__":
    # print(get_matakuliah("00000000002")[-1])
    print(get_all_kompetensi())