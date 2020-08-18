import unittest
import requests
import responses


class TestCase(unittest.TestCase):

  @responses.activate  
  def testExample(self):
    responses.add(**{
      'method'         : responses.GET,
      'url'            : 'http://localhost:5000/ping',
      'body'           : '{"ping": "pong"}',
      'status'         : 404,
      'content_type'   : 'application/json',
    })

    response = requests.get('http://localhost:5000/ping')

    self.assertEqual({'ping': 'pong'}, response.json())
    self.assertEqual(200, response.status_code)