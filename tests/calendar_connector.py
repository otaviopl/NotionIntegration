import unittest
from unittest.mock import MagicMock
from calendar_connector import *


class TestGetEvents(unittest.TestCase):
        
    def mock_calendar(self):
        self.mock_services = MagicMock()
    
    def test_get_events_success(self):

        events_data = {
            'items': [
                {'summary': 'Evento 1', 'start': {'dateTime': '2024-06-30T10:00:00Z'}},
                {'summary': 'Evento 2', 'start': {'dateTime': '2024-07-01T14:00:00Z'}}
            ]}

        self.mock_service.events().list().execute.return_value = events_data

        with unittest.mock.patch('googleapiclient.discovery.build', return_value=self.mock_service):
            result = get_events()

        self.assertEqual(len(result), 2)
        self.assertIn('Evento 1', [event['summary'] for event in result])
        self.assertIn('Evento 2', [event['summary'] for event in result])