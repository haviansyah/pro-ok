from db.mongodb import Database

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
    matakuliah_list = db.matakuliah.find({})
    matakuliah = [matakuliah for matakuliah in matakuliah_list]
    return matakuliah


def get_matakuliah(id):
    matakuliah = db.matakuliah.find_one({"_id" : id})
    return matakuliah

def get_jurusan_matakuliah(id):
    jurusan = get_jurusan(id)
    matakuliah_list = jurusan["matakuliah_list"]
    matakuliah = [get_matakuliah(matkul) for matkul in matakuliah_list ]
    return matakuliah


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
    kompetensi_list = db.kompetensi.find({})
    kompetensi = [kompetensi for kompetensi in kompetensi_list]
    return kompetensi

def get_kompetensi(id):
    kompetensi = db.kompetensi.find_one({"_id" : id})
    return kompetensi

def get_okupasi_kompetensi(kode_okupasi):
    okupasi = get_okupasi(kode_okupasi)
    kompetensi_list = okupasi["kompetensi_list"]
    kompetensi = [get_kompetensi(kompeten) for kompeten in kompetensi_list ]
    return kompetensi

if __name__ == "__main__":
    # print(get_matakuliah("00000000002")[-1])
    print(get_all_kompetensi())