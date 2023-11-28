import json
import os
import unittest
from unittest.mock import patch, MagicMock
from world_leagues import WorldLeagues


class TestWorldLeagues(unittest.TestCase):

    @patch('world_leagues.http.client.HTTPSConnection')
    @patch('world_leagues.JsonSerializer')
    def test_get_league_from_cache(self, mock_serializer, mock_connection):
        # Set up the mock serializer
        mock_serializer_instance = mock_serializer.return_value
        mock_leagues_file = os.path.join(os.path.dirname(__file__), "assets", "mock_leagues.json")
        mock_serializer_instance.read.return_value = json.load(open(mock_leagues_file))

        # Set up the mock HTTP connection
        mock_response = MagicMock()
        mock_response.read.return_value = b'{}'
        mock_connection_instance = mock_connection.return_value
        mock_connection_instance.getresponse.return_value = mock_response

        # Create an instance of WorldLeagues
        world_leagues = WorldLeagues(serializer='json')

        # Call the get_league method
        result = world_leagues.get_league(league_id=1)

        # Assert the result
        self.assertEqual(result, {'league': {'id': 1, 'name': 'Mock League'}})
        mock_serializer_instance.read.assert_called_once()
        mock_connection_instance.request.assert_not_called()

    @patch('world_leagues.http.client.HTTPSConnection')
    @patch('world_leagues.JsonSerializer')
    def test_get_league_from_api(self, mock_serializer, mock_connection):
        # Set up the mock serializer
        mock_serializer_instance = mock_serializer.return_value
        mock_serializer_instance.read.return_value = {}

        # Set up the mock HTTP connection
        mock_response = MagicMock()
        mock_leagues_file = os.path.join(os.path.dirname(__file__), "assets", "mock_leagues.json")
        mock_serializer_instance.read.return_value = json.load(open(mock_leagues_file))

        mock_connection_instance = mock_connection.return_value
        mock_connection_instance.getresponse.return_value = mock_response

        # Create an instance of WorldLeagues
        world_leagues = WorldLeagues(serializer='json')

        # Call the get_league method
        result = world_leagues.get_league(league_id=1)

        # Assert the result
        self.assertEqual(result, {'league': {'id': 1, 'name': 'Mock League'}})
        mock_serializer_instance.read.assert_called_once()
        mock_connection_instance.request.assert_called_once()


if __name__ == '__main__':
    unittest.main()
