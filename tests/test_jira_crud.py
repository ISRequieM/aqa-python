from jira.jira import *
import random

jira_rest = JiraRestActions(JiraParameters.user, JiraParameters.password, JiraParameters.project_key)

issue_keys = {}
updated_summary = "updated_summary_by_istonik" + str(random.randint(1, 1000))

def test_setup():
    jira_rest.authenticate()

def test_create_issue_missing_field():
    issue_fields = {}
    result = jira_rest.createIssue("Bug", issue_fields)
    assert result.get("status_code") == 400
    assert str(result.get("errors")).__contains__("You must specify a summary of the issue.")


def test_create_issue_too_big_summary():
    issue_fields = {'summary': 'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarys'
                               'ome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysom'
                               'e_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_s'
                               'ummarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summa'
                               'rysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome'
                               '_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary'
                               'some_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summarysome_summary'}
    result = jira_rest.createIssue("Bug", issue_fields)
    assert result.get("status_code") == 400
    assert str(result.get("errors")).__contains__("Summary must be less than 255 characters.")


def test_create_issue():
    issue_fields = {'summary': 'some_summary', 'description': 'some_description'}
    result = jira_rest.createIssue("Bug", issue_fields)
    assert result.get("status_code") == 201
    assert (result.get("success") == True) and str(result.get("issueKey")).__contains__(jira_rest.projectKey)
    issue_keys["key1"] = result.get("issueKey")


def test_update_issue():
    issue_key = issue_keys.get("key1")
    issue_fields = {"summary": updated_summary, "description": "changed_description", "priority": {"name": "High"}}
    result = jira_rest.updateIssue(issue_key, issue_fields)
    assert result.get("status_code") == 204
    assert result.get("success") == True
    result = jira_rest.assignIssue(JiraParameters.user, issue_keys.get("key1"))
    assert result.get("status_code") == 204
    assert result.get("success") == True


def test_query_issues():
    result = jira_rest.query_issues_by_like_value_in_field("summary", updated_summary)
    assert result.get("status_code") == 200
    assert result.get("success")==True
    body = result.get("body")
    assert body.get("total") == 1 and body.get("issues")[0].get("key") == issue_keys.get("key1")


def test_delete_issues():
    result = jira_rest.delete_issue(issue_keys.get("key1"))
    assert result.get("status_code") == 204
    assert result.get("success")==True
