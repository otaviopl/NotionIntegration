import os
import datetime
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configurações globais
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

	service = build('calendar', 'v3', developerKey=API_KEY)
	return service

def get_events(service=None):
	"""Get Events from Google Calendar.

	Args:
		service: Service from Google API.

	Returns:
		Events List.
	"""
	if service is None:
		print('criando servico com build google service\n')
		service = build_google_service()
	
	now = datetime.datetime.utcnow().isoformat() + 'Z'
	events_result = service.events().list(
			calendarId='primary',
		timeMin=now,
		maxResults=10,
		singleEvents=True,
		orderBy='startTime'
	).execute()
	events = events_result.get('items', [])
	print('eventos resgatados',events)

	return events