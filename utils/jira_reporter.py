import os
import time
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()

# בתוך jira_reporter.py - עדכון לפונקציית report_jira_bug

def report_jira_bug(test_name, summary, description, priority="Medium", labels=None):
    try:
        jira = JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_TOKEN"))
        )
        project_key = os.getenv("JIRA_PROJECT_KEY")
        
        # חיפוש באג קיים (נשאר אותו דבר כדי למנוע כפילויות לפי שם הטסט)
        jql_query = f'project = "{project_key}" AND summary ~ "{test_name}" AND status != "Done"'
        existing_issues = jira.search_issues(jql_query)
        
        if existing_issues:
            issue_key = existing_issues[0].key
            jira.add_comment(issue_key, f"🔄 Test failed again on {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return issue_key, False 

        # יצירת באג חדש עם עדיפות ותגיות
        issue_dict = {
            'project': project_key,
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Bug'},
            'priority': {'name': priority},
            'labels': labels or ['Automation-Bot', 'Playwright'] # תגיות ברירת מחדל
        }
        
        new_issue = jira.create_issue(fields=issue_dict)
        return new_issue.key, True
        
    except Exception as e:
        print(f"❌ Jira error: {e}")
        return None, False

def add_attachment_to_jira(issue_key, file_path):
    try:
        jira = JIRA(
            server=os.getenv("JIRA_URL"),
            basic_auth=(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_TOKEN"))
        )
        issue = jira.issue(issue_key)
        with open(file_path, 'rb') as f:
            jira.add_attachment(issue=issue, attachment=f)
        print(f"📸 Screenshot attached to {issue_key}")
    except Exception as e:
        print(f"❌ Failed to attach screenshot to Jira: {e}")