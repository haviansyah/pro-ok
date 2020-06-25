from gensim import corpora, matutils
from gensim.models import LdaMulticore
import pandas as pd
from database.models import *
from resources.global_var import *

class LDA():
    def getModel(self):
        dictionary_file = get_current_state()["dictionary"]
        lda_file = get_current_state()["lda"]
        dictionary = corpora.Dictionary.load("../LDA/models/"+dictionary_file)
        model = LdaMulticore.load("../LDA/models/"+lda_file)
        return dictionary, model

    def cossine(self, p, q):
        sims = matutils.cossim(p, q)
        return sims

    def getKompetensiOkupasi(self, kode_okupasi):
        okupasi     = Okupasi.objects().get(kode_okupasi = kode_okupasi)
        kompetensi  = okupasi.kompetensi
        return kompetensi

    def getMatkulJurusan(self, kode_jurusan):
         jurusan    = Jurusan.objects().get(kode_jurusan = kode_jurusan)
         matkul     = jurusan.matakuliah
         return matkul

    def getSimilarity(self, kode_jurusan, kode_okupasi, all = False):
        dictionary, lda = self.getModel()
        
        matakuliahs = self.getMatkulJurusan(kode_jurusan)
        kompetensis = self.getKompetensiOkupasi(kode_okupasi)
        hasil = []
        total_cocok = 0
        
        for kompetensi in kompetensis :
            nama_kompetensi = kompetensi["nama_kompetensi"]
            cocok = []
            vec_bow_k = dictionary.doc2bow(kompetensi["token"])
            vec_lda_k = lda[vec_bow_k]
            for matakuliah in matakuliahs :
                vec_bow_m = dictionary.doc2bow(matakuliah["token"])
                vec_lda_m = lda[vec_bow_m]            
                sim = self.cossine(vec_lda_k,vec_lda_m)
                if not all :
                    if sim > 0.6 :
                        nama_m = matakuliah["nama_matakuliah"]
                        cocok.append([nama_m,sim])
                else :
                    nama_m = matakuliah["nama_matakuliah"]
                    cocok.append([nama_m,sim])
            hasil.append({
                "nama_kompetensi" : nama_kompetensi,
                "kecocokan" : cocok
            })
            if len(cocok) > 0 : total_cocok += 1
        
        return hasil, total_cocok

        
        
        