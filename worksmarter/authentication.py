import ws_database as db

def login(username, password):
    is_valid_login = False
    user=None
    temp_admin = db.get_user(username)
    if(temp_admin != None):
        if(temp_admin["password"]==password):
            is_valid_login=True
            admin={"username":username,
                  "first_name":temp_admin["first_name"],
                  "last_name":temp_admin["last_name"]}

    return is_valid_login, admin
