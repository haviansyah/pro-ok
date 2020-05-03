from db.getdata import get_constant

def run():
    db_get = get_constant()
    for key,val in db_get.items():
        exec(key + '="'+ val+'"',globals())

run()