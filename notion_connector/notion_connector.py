import datetime
import requests
import json

from utils import load_credentials


def collect_tasks_from_control_panel(n_days=7, project_logger=None):
    """
    Connect to Notion API and collect Tasks from 'Control Panel' database.
    TODO: Fix project_logger argument. Can't be None.
    """
    notion_credentials = load_credentials.load_notion_credentials(
        project_logger=project_logger
    )
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
        "Authorization": "Bearer " + notion_credentials["api_key"] + "",
        "Notion-Version": "2022-06-28",
        "content-type": "application/json"
    }

    project_logger.info("Collecting tasks from Notion...")

    response = requests.post(url, json=payload, headers=headers)

    data = json.loads(response.text)
    print('aaaa data',data)
    all_task_data = []

    for d in data["results"]:
        all_task_data.append(
            {
                "name": d["properties"]["Task"]["title"][0]["text"]["content"],
                "deadline": d["properties"]["Deadline"]["date"]["start"],
                "project": d["properties"]["Project"]["select"]["name"]
            }
        )

    sorted_tasks = sorted(all_task_data, key=lambda d: d['deadline'])

    return sorted_tasks