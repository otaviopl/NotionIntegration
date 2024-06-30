import unittest
from unittest.mock import MagicMock, patch
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from calendar_connector.calendar_connector import get_events
API_KEY=os.getenv('API_KEY')

class TestGoogleCalendar(unittest.TestCase):
	def setUp(self):
		load_dotenv()
		
		self.google_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
		
		if not self.google_credentials:
			self.skipTest("GOOGLE_APPLICATION_CREDENTIALS not set in environment variables")


	'''def test_get_events_success(self):
		
		events_data = {
			'items': [
				{'summary': 'Evento 1', 'start': {'dateTime': '2024-06-30T10:00:00Z'}},
				{'summary': 'Evento 2', 'start': {'dateTime': '2024-07-01T14:00:00Z'}}
			]
		}

		self.mock_execute.return_value = events_data

		with patch('googleapiclient.discovery.build', return_value=self.mock_execute.retun_value):
			result = get_events(service=self.mock_service)

		print('aaa', result)
		self.assertEqual(len(result), 2)
		self.assertIn('Evento 1', [event['summary'] for event in result])
		self.assertIn('Evento 2', [event['summary'] for event in result])'''
	
	def test_get_real_events(self):

		events = get_events()
	
		print('aaa', events)
		self.assertGreater(len(events), 0, "No events found")		
	
		event_summaries = [event['summary'] for event in events]
		self.assertIn('teste', event_summaries, "Event with summary 'teste' not found")

			

if __name__ == "__main__":
	unittest.main()