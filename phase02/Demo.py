import requests
from phase02.dataFixtures import *


def test_login_to_jira():

    jiraUrl='http://jira.hillel.it:8080/rest/auth/1/session'

    auth_data = getauthjson("Ilya_Sotnik", "Installed_12345")
    headers = get_contenttype_header()
    r = requests.post(jiraUrl, json=auth_data, headers=headers)
    print("STATUS CODE: " + str(r.status_code))
    print("Responce is: " + str(r.content))
    print("Responce is: " + str(r.text))

    assert r.status_code is 200


test_login_to_jira()
