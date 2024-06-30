import unittest
from unittest.mock import MagicMock
from calendar_connector import *


class TestGetEvents(unittest.TestCase):
        
    def mock_calendar(self):
        self.mock_services = MagicMock()