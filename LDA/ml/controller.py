import pandas as pd
from ml.lda import LDA
from db.getdata import *
from db.update import update
from datetime import datetime
from ml.preprocessing import Preprocessing
from db.update import update_matakuliah, update_kompetensi
from bson import ObjectId

def trainFromDB():
    mk = get_all_matakuliah()
    kp = get_all_kompetensi()
    df_mk = pd.DataFrame(mk)
    df_kp = pd.DataFrame(kp)
    df_all = df_kp.append(df_mk,ignore_index=True, sort=False)
    df_all = df_all.dropna(subset=["token"])
    dictionary, corpus, lda, tfidf = LDA(df_all["token"]).train_tfidf(num_topics=85)
    # timestring = datetime.today().strftime('%Y-%m-%d-%H:%M:%S');
    timestring = "_trained"
    
    dictionary_file_name = "dictionary"+timestring+".gensim"
    lda_file_name = "lda"+timestring+".model"

    #Saving Trained Data
    dictionary.save("models/"+dictionary_file_name) 
    lda.save("models/"+lda_file_name)

    #Update Global Var
    update(lda_file_name,dictionary_file_name) 

    return dictionary, corpus, lda


def preprocessing(data):
    collection = data["collection"]
    id = data["id"]
    id = ObjectId(id)

    if collection == "kompetensi":
        kompetensi = get_kompetensi(id)
        keterampilan = kompetensi["keterampilan"]
        pengetahuan = kompetensi["pengetahuan"]
        text = keterampilan + " " + pengetahuan
        token = Preprocessing().preprocess(text)
        print(token)
        update_kompetensi(id, token)

    if collection == "matakuliah":
        matakuliah = get_matakuliah(id)
        keterampilan = matakuliah["keterampilan"]
        pengetahuan = matakuliah["pengetahuan"]
        text = keterampilan + " " + pengetahuan
        token = Preprocessing().preprocess(text)
        print(token)
        update_matakuliah(id, token)

    trainFromDB()


