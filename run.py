import requests
import json
import datetime
import os.path
import base64

from jinja2 import Environment, FileSystemLoader

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from email.mime.text import MIMEText


SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
    ]


# Filter the Tasks search using this number of days in the future.
DAYS_TO_CONSIDER = 7

# Name that will be shown in the email greetings.
DISPLAY_NAME = "Carlos"


def load_notion_credentials():
    """
    Load Notion credentials from 'notion_credentials.json' file.
    """
    notion_keys = {}
    with open("notion_credentials.json", "r") as notion_credentials:
        notion_keys = json.load(notion_credentials)
    return notion_keys


def collect_tasks_from_control_panel(n_days=7):
    """
    Connect to Notion API and collect Tasks from 'Control Panel' database.
    """
    notion_credentials = load_notion_credentials()
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=n_days)
    one_week = today + delta
    one_week = one_week.isoformat()

    url = "https://api.notion.com/v1/databases/" + \
        notion_credentials["database_id"] + "/query"

    payload = {
        "filter": {
            "and": [
                {
                    "property": "DONE",
                    "checkbox": {"equals": False},
                },
                {
                    "property": "Deadline",
                    "date": {"before": str(one_week)}
                }
            ]
        }
    }

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + notion_credentials["notion_key"] + "",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    print("Collecting tasks from Notion...")

    response = requests.post(url, json=payload, headers=headers)

    data = json.loads(response.text)

    all_task_data = []

    for d in data["results"]:
        all_task_data.append(
            {
                "name": d["properties"]["Task"]["title"][0]["text"]["content"],
                "deadline": d["properties"]["Deadline"]["date"]["start"],
            }
        )

    return all_task_data


def gmail_connect():
    """
    Create a Google GMail connection using GCloud credentials.
    This method expects a 'credentials.json' local file and
    a token.json file is created after validating credentials.
    """
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())


def build_email_body(all_tasks):
    """
    Build the email HTML using Jinja2. Template is in template/ folder.
    """
    environment = Environment(loader=FileSystemLoader("templates/"))
    template = environment.get_template("email_template.html")
    context = {
        "username": DISPLAY_NAME,
        "all_tasks": all_tasks
    }

    return template.render(context)


def send_email_with_tasks(all_tasks):
    """
    Considering a already created token.json file based on GCloud credentials,
    send an email using GMail API.
    """

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    email_message = build_email_body(all_tasks)

    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(email_message, 'html')

        message['To'] = 'carlos@raccoon.ag'
        message['From'] = 'carlosplfilho@gmail.com'
        message['Subject'] = 'Carlos\'s Notion Bot - Tasks'

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }

        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None

    return send_message


if __name__ == "__main__":
    all_tasks = collect_tasks_from_control_panel(n_days=DAYS_TO_CONSIDER)
    send_email_with_tasks(all_tasks)
