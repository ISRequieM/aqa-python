def getauthjson(username, password):
        auth_data = {
        "username": username,
        "password": password
        }
        return auth_data

def get_contenttype_header():
    return {'Content-Type': 'application/json'}