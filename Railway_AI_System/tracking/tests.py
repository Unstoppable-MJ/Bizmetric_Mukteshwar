from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status

class TrainStatusAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('requests.get')
    def test_get_train_status_success(self, mock_get):
        # Mocking a successful response from RapidAPI
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": True,
            "message": "Success",
            "data": {
                "current_station_name": "New Delhi",
                "delay": 15,
                "next_station_name": "Mathura Jn",
                "status_as_of": "Departed from New Delhi at 10:15"
            }
        }

        response = self.client.get('/api/train/12051/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['current_station'], "New Delhi")
        self.assertEqual(response.data['delay'], "15 mins")
        self.assertEqual(response.data['next_station'], "Mathura Jn")
        self.assertEqual(response.data['train_status_message'], "Departed from New Delhi at 10:15")

    @patch('requests.get')
    def test_get_train_status_not_found(self, mock_get):
        # Mocking a 404 response from RapidAPI (e.g. invalid train number)
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "status": False,
            "message": "Invalid train number"
        }

        response = self.client.get('/api/train/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], "Invalid train number")

    @patch('requests.get')
    def test_get_train_status_timeout(self, mock_get):
        # Mocking a timeout error
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        response = self.client.get('/api/train/12051/')
        
        self.assertEqual(response.status_code, status.HTTP_504_GATEWAY_TIMEOUT)
        self.assertEqual(response.data['error'], "API request timed out.")
