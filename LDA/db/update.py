from db.mongodb import Database
from bson import ObjectId
db = Database("prook").mongo()

def update(lda,dictionary):
    db.global_var.update_one(
    {},
    {"$set": {"current_state.dictionary": dictionary, "current_state.lda" : lda ,"current_state.status": "active"},
     "$currentDate": {"lastModified": True}})

def update_kompetensi(id, token):
    db.kompetensi.update_one(
        {"_id" : ObjectId(id)},
        {"$set" : {
            "token" : token
            }
        }
    )

def update_matakuliah(id, token):
    db.matakuliah.update_one(
        {"_id" : ObjectId(id)},
        {"$set" : {
            "token" : token
            }
        }
    )
