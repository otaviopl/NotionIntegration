import unittest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
print(sys.path)
from calendar_connector.calendar_connector import get_events

class TestGoogleCalendar(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.mock_list = self.mock_service.events().list()
        self.mock_execute = self.mock_list.execute

    def test_get_events_success(self):
        
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
        self.assertIn('Evento 2', [event['summary'] for event in result])

if __name__ == "__main__":
    unittest.main()