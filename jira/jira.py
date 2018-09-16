import requests
import json
from jira.json_fixtures import *

class JiraParameters():
    url = "http://jira.hillel.it:8080"
    auth_endpoint = "/rest/auth/1/session"
    issue_endpoint = "/rest/api/2/issue"
    search_endpoint = "/rest/api/2/search?jql="
    project_key = "AQAPYTHON"
    user = "Ilya_Sotnik"
    password = "Installed_12345"


class JiraRestActions:
    def __init__(self, user, password, projectKey):
        self.userName = user
        self.userPassword = password
        self.projectKey = projectKey
        self.cookies = {}

    def authenticate(self):
        jiraUrl = JiraParameters.url+JiraParameters.auth_endpoint
        body = getauthjson(self.userName, self.userPassword)
        header = get_contenttype_header("json")
        auth_r = requests.post(jiraUrl, json=body, headers=header)
        responseJson = json.loads(str(auth_r.text))
        if auth_r.status_code == 200:
            print("Succefully authenticated!")
            self.cookies = {"JSESSIONID": responseJson.get("session").get("value")}
            return responseJson.get("session").get("value")
        else:
            print("Authenticate attempt was unsuccessful")
            return "Failed"

    def createIssue(self, issueType, issue_fields):
        headers = get_contenttype_header("json")
        endpoint_url = JiraParameters.url+JiraParameters.issue_endpoint
        issue_body = get_create_issue_json(issueType, self.projectKey, issue_fields)
        create_r = requests.post(endpoint_url, json=issue_body, headers=headers, cookies=self.cookies)
        responseJson = json.loads(str(create_r.text))
        if create_r.status_code == 201:
            print("Issue created: "+responseJson.get("key"))
            return {"success": True, "issueKey": responseJson.get("key")}
        else:
            print("Failed to create issue: "+str(responseJson.get("errors")))
            return {"success": False, "errors": responseJson.get("errors")}

    def updateIssue(self, issueKey, issue_fields):
        headers = get_contenttype_header("json")
        endpoint_url = JiraParameters.url+JiraParameters.issue_endpoint+"/"+str(issueKey)
        body = {"fields": issue_fields}
        update_r = requests.put(endpoint_url, json=body, headers=headers, cookies=self.cookies)
        if update_r.status_code == 204:
            print("Issue "+issueKey+" updated successfully")
            return {"success": True}
        else:
            print("Unable to update issue "+issueKey)
            return {"success": False}

    def assignIssue(self, username, issueKey):
        headers = get_contenttype_header("json")
        body = {"name": username}
        endpoint_url = JiraParameters.url + JiraParameters.issue_endpoint + "/" + str(issueKey)+"/assignee"
        assign_r = requests.put(endpoint_url, json=body, headers=headers, cookies=self.cookies)
        if assign_r.status_code == 204:
            print("Issue "+issueKey+" assigned successfully to "+username)
            return {"success": True}
        else:
            print("Unable to  assign issue "+issueKey+"to "+username)
            return {"success": False}

    def query_issues_by_exact_value_in_field(self, field, value):
        headers = get_contenttype_header("json")
        endpoint_url = JiraParameters.url+JiraParameters.search_endpoint+field+"="+value
        search_r = requests.get(endpoint_url, cookies=self.cookies, headers=headers)
        if search_r.status_code == 200:
            return {"success": True, "body": json.loads(str(search_r.text))}
        else:
            return{"success": False, "body": search_r.text}

    def query_issues_by_like_value_in_field(self, field, value):
        headers = get_contenttype_header("json")
        endpoint_url = JiraParameters.url+JiraParameters.search_endpoint+field+"~"+value
        search_r = requests.get(endpoint_url, cookies=self.cookies, headers=headers)
        if search_r.status_code == 200:
            return {"success": True, "body": json.loads(str(search_r.text))}
        else:
            return{"success": False, "body": search_r.text}

    def delete_issue(self, issueKey):
        headers = get_contenttype_header("json")
        endpoint_url = JiraParameters.url+JiraParameters.issue_endpoint+"/"+str(issueKey)
        delete_r = requests.delete(endpoint_url, headers=headers, cookies=self.cookies)
        if delete_r.status_code == 204:
            print("Issue " + issueKey + " deleted successfully")
            return {"success": True}
        else:
            print("Unable to delete issue " + issueKey)
            return {"success": False}