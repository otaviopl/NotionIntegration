import os
import datetime
import requests
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
NOTION_API_URL = "https://api.notion.com/v1/pages"
API_KEY=os.getenv('API_KEY')

headers = {
	"Authorization": f"Bearer {NOTION_API_KEY}",
	"Content-Type": "application/json",
	"Notion-Version": "2022-06-28"
}

def build_google_service():
	"""Google Calendar service builder."""
	if os.path.exists("../token_calendar.json"):
		creds = Credentials.from_authorized_user_file("../token_calendar.json", SCOPES)
	service = build("calendar", "v3", credentials=creds)
	
	return service

def get_events(service=None):
	"""Get all Events from Google Calendar.

	Args:
		api_key: API key from Google Cloud.
		service: Service from Google API.

	Returns:
		Events List.
	"""
	if service is None:
		print('Creating service with API key\n')
		service = build_google_service()
	
	events = []
	page_token = None

	now = datetime.datetime.utcnow().isoformat() + "Z" 
	try:
		while True:

			events_result = service.events().list(
				calendarId="primary",
				timeMin=now,
				maxResults=10,
				singleEvents=True,
				orderBy="startTime",
			).execute()

			print('events_result',events_result)
			events.extend(events_result.get('items', []))
			page_token = events_result.get('nextPageToken')
			if not page_token:
				break
		if not events:
			print('No events found.')
		else:
			print(f'Fetched {len(events)} events.')
		return events
	except Exception as e:
		print('An error occurred:', e)
		return []