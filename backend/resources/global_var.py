from database.models import GlobalVar

def get_current_state():
    global_var = GlobalVar.objects({}).first()
    return global_var.current_state

def edit_current_state():
    global_var = GlobalVar.objects({}).first()
    global_var.update(set__current_state__status="train")
