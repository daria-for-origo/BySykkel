import unittest

import ride.BySykkelAPI as BySykkelAPI
import ride.BySykkelModel as BySykkelModel
import json

#For global SilentRun
import BySykkelConfig 
BySykkelConfig.SilentRun = True

class TestAPIMethods(unittest.TestCase):
    
    def test_1(self):
        result = json.loads(BySykkelAPI.Execute.request("prefix"))
        self.assertTrue(len(result.get("stations")) > 0)

    def test_2(self):
        result1 = json.loads(BySykkelAPI.Execute.request("prefix"))
        result2 = json.loads(BySykkelAPI.Execute.request("prefix?bikes=0?docks=0"))
        self.assertEqual(len(result1.get("stations")), len(result2.get("stations")))

    def test_3(self):
        result1 = json.loads(BySykkelAPI.Execute.request("prefix"))
        result2 = json.loads(BySykkelAPI.Execute.request("prefix?bikes=20?docks=20"))
        self.assertTrue(len(result1.get("stations")) >= len(result2.get("stations")))

    def test_4(self):
        result = json.loads(BySykkelAPI.Execute.request("prefix?station_id=626"))
        self.assertEqual(result.get("station_id", 0), '626')

    def test_5(self):
        result = json.loads(BySykkelAPI.Execute.request("prefix?client_id=123"))
        self.assertEqual(len(result.get("stations")), 0)

    #TODO: Add distance/location test


if __name__ == '__main__':
    unittest.main()