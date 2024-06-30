import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
print(sys.path)
from calendar_connector.calendar_connector import get_events

class TestGetEvents(unittest.TestCase,):
		
	def setUp(self):

		self.mock_events = MagicMock()
		self.mock_list = MagicMock()
		self.mock_service = MagicMock()
		self.mock_service.events.return_value = self.mock_events
		self.mock_events.list.return_value = self.mock_list

	def test_get_events_success(self):

		events_data = {
			'items': [
				{'summary': 'Evento 1', 'start': {'dateTime': '2024-06-30T10:00:00Z'}},
				{'summary': 'Evento 2', 'start': {'dateTime': '2024-07-01T14:00:00Z'}}
			]
		}

		self.mock_list.execute.return_value = events_data

		with patch('googleapiclient.discovery.build', return_value=self.mock_service):
			result = get_events()

		self.assertEqual(len(result), 2)
		self.assertIn('Evento 1', [event['summary'] for event in result])
		self.assertIn('Evento 2', [event['summary'] for event in result])


if __name__ == '__main__':
	unittest.main()