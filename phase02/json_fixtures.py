def getauthjson(username, password):
        auth_data = {
            "username": username,
            "password": password
            }
        return auth_data

def get_contenttype_header(contentType):
    return {'Content-Type': 'application/'+contentType}


def get_create_issue_json(issueType, projectKey, values):
    issue_body = {
        "fields": {
           "project":
           {
              "key": projectKey
           },
           "issuetype": {
              "name": issueType
           }
         }
        }
    for key, value in values.items():
        issue_body["fields"][key] = value
    return issue_body
