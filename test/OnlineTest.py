import unittest
unittest.TestLoader.sortTestMethodsUsing = None

import ride.BySykkelOnline as BySykkelData
import ride.BySykkelModel as BySykkelModel

#For global SilentRun
import BySykkelConfig  


class TestOnlineMethods(unittest.TestCase):

    GBFS = "https://gbfs.urbansharing.com/oslobysykkel.no/gbfs.json"
    CLIENT_ID = "Daria-for-Origo"
    
    BySykkelConfig.SilentRun = True

    def test_gbfs_reachable(self):
        content = BySykkelData.get_content(self.GBFS, self.CLIENT_ID)
        self.assertFalse(content == '{}', self.GBFS + " is not reachable")

    def test_client_id_is_mandatory(self):
        content = BySykkelData.get_content(self.GBFS, "")
        self.assertEqual(content, '{}', "Client ID must be mandatory")

    def test_client_id_is_decent(self):
        content = BySykkelData.get_content(self.GBFS, "1234")
        self.assertEqual(content, '{}', "Client ID must be at least 6 bytes long")


    def test_unreachable_returns_empty(self):
        content = BySykkelData.get_content("https://gbfs.urbansharing.com/oslobysykkel.no/bogus_address", 
                                            self.CLIENT_ID)
        self.assertEqual(content, '{}', "Invalid destinations must return empty json")

    
    
    def test_gbfs_addresses(self):
        gbfs = BySykkelModel.GbfsInfo(self.GBFS, self.CLIENT_ID)
        content = BySykkelData.get_content(gbfs.system_info_url, self.CLIENT_ID)
        self.assertFalse(content == '{}', gbfs.system_info_url + " is invalid/not reachable")
        content = BySykkelData.get_content(gbfs.station_info_url, self.CLIENT_ID)
        self.assertFalse(content == '{}')
        content = BySykkelData.get_content(gbfs.station_status_url, self.CLIENT_ID)
        self.assertFalse(content == '{}')
        


if __name__ == '__main__':
    unittest.main()