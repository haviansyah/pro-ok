from db.getdata import *
from ml.controller import trainFromDB
from ml.preprocessing import Preprocessing
from bson import ObjectId
from ml.controller import preprocessing
# print(get_jurusan_matakuliah("00000000002"))
# print(get_all_kompetensi())

id = "5e9f931654932d01ca1b07ba"
collection = "kompetensi"
data = {
    "collection" : collection,
    "id" : id
}
preprocessing(data)
