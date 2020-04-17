import unittest

#For global SilentRun and OfflineRun
import BySykkelConfig 
BySykkelConfig.SilentRun = True
BySykkelConfig.OfflineRun = True

import ride.BySykkelOffline as BySykkelData
import ride.BySykkelModel as BySykkelModel 

import json


class TestOfflineDataPresence(unittest.TestCase):

    def test_illegal(self):
        content = BySykkelData.get_content("offline/foo.json", "foo")
        self.assertEqual(content, '{}')


    def test_gbfs_presence(self):
        content = BySykkelData.get_content(BySykkelConfig.OfflineGBFS)
        self.assertFalse(content == '{}')

    
    def test_station_info_presence(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        content = BySykkelData.get_content(gbfs.station_info_url)
        self.assertFalse(content == '{}')

    def test_station_status_presence(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        content = BySykkelData.get_content(gbfs.station_status_url)
        self.assertFalse(content == '{}')

    def test_gbfs_system_info_presence(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        content = BySykkelData.get_content(gbfs.system_info_url)
        self.assertFalse(content == '{}')


class TestModelLoaders(unittest.TestCase):
  
    def test_system_info(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        system_info = BySykkelModel.SystemInfo(gbfs.system_info_url, "")

        self.assertEqual(system_info.name, "Oslo Bysykkel")
        self.assertEqual(system_info.phone_number, "+4791589700")
        self.assertEqual(system_info.email, "post@oslobysykkel.no")
        self.assertEqual(system_info.format("{2}-{0}-{1}"), 
        "post@oslobysykkel.no-UIP Oslo Bysykkel AS-+4791589700")

    def test_station_dictionary_info(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        js = json.loads(BySykkelData.get_content(gbfs.station_info_url, ""))
        station_info = BySykkelModel.StationDict(js)
        self.assertEqual(len(station_info.dictionary), 4)
    
    def test_station_dictionary_status(self):
        gbfs = BySykkelModel.GbfsInfo(BySykkelConfig.OfflineGBFS, "")
        js = json.loads(BySykkelData.get_content(gbfs.station_status_url, ""))
        station_status = BySykkelModel.StationDict(js)
        self.assertEqual(len(station_status.dictionary), 4)


class TestStationStatus(unittest.TestCase):
    def setUp(self):
        station_static_data = dict()
        station_static_data["name"] = "Station 11"
        station_static_data["address"] = "From earth, to the left"
        station_static_data["lat"] = 25
        station_static_data["lon"] = 25
    
        self.station_status = BySykkelModel.StationStatus(station_static_data)


    def test_station_status_init(self):
        self.assertEqual(self.station_status.name, "Station 11")
        self.assertEqual(self.station_status.distance, 0)
        self.assertEqual(self.station_status.bikes, 0)
        self.assertEqual(self.station_status.docks, 0)

    def test_station_status_update(self):
        station_dynamic_data = dict()
        station_dynamic_data["is_renting"] = True
        station_dynamic_data["is_returning"] = True
        station_dynamic_data["num_bikes_available"] = 12
        station_dynamic_data["num_docks_available"] = 42

        self.station_status.update_status(station_dynamic_data)
        self.assertEqual(self.station_status.bikes, 12)
        self.assertEqual(self.station_status.docks, 42)

        station_dynamic_data["is_renting"] = False
        station_dynamic_data["num_bikes_available"] = 13
        station_dynamic_data["num_docks_available"] = 41
        self.station_status.update_status(station_dynamic_data)
        self.assertEqual(self.station_status.bikes, 0)
        self.assertEqual(self.station_status.docks, 41)

        station_dynamic_data["is_returning"] = False
        self.station_status.update_status(station_dynamic_data)
        self.assertEqual(self.station_status.docks, 0)


    def test_station_status_distance(self):

        #Simply test some distance is calculated and updated.
        #Correctness belongs to GPSLocation distance calculation and is out of scope
        self.station_status.update_distance(BySykkelModel.GPSLocation(24,24))
        self.assertFalse(self.station_status.distance == 0)

        #Distance to itself is 0 and easy to check
        self.station_status.update_distance(BySykkelModel.GPSLocation(25,25))
        self.assertEqual(self.station_status.distance, 0)


class TestModelSource(unittest.TestCase):

    GBFS = "offline/gbfs.json"

    gps_loc = BySykkelModel.GPSLocation(25,25)
    gps_update_loc = BySykkelModel.GPSLocation(25.1,25)

    def setUp(self):
        self.source = BySykkelModel.Source(BySykkelConfig.OfflineGBFS, "")
        updated = self.source.update(self.gps_loc)

    def sumBikes(self):
        sum = 0
        for row in self.source.status:
            sum += row.bikes
        return sum

    def sumDocks(self):
        sum = 0
        for row in self.source.status:
            sum += row.docks
        return sum
        
    def test_source_init(self):
        self.assertEqual(len(self.source.status), 3)
        self.assertEqual(self.sumBikes(), 7)
        self.assertEqual(self.sumDocks(), 7)

    def test_source_skip_update(self):
        updated = self.source.update(self.gps_loc)
        self.assertEqual(updated, False)
        
        

    def test_source_update_location(self):
        updated = self.source.update(self.gps_update_loc)
        self.assertEqual(updated, True)
        self.assertEqual(len(self.source.status), 3)
        self.assertEqual(self.sumBikes(), 7)
        self.assertEqual(self.sumDocks(), 7)
        #TODO: Add location change test

    def test_source_update_info(self):
        #Switch to newer version of station_info
        self.source.gbfs.station_info_url = "offline/station_info_update.json"
        updated = self.source.update(self.gps_update_loc)
        self.assertEqual(updated, True)
        self.assertEqual(len(self.source.status), 2) #Lysaker is removed from info
        self.assertEqual(self.sumBikes(), 6)
        self.assertEqual(self.sumDocks(), 6)

    def test_source_update_status(self):
        #Switch to newer version of station_status
        self.source.gbfs.station_status_url = "offline/station_status_update.json"
        updated = self.source.update(self.gps_loc)
        self.assertEqual(updated, True)
        self.assertEqual(len(self.source.status), 3) #Lysaker not returning, 7 Juni not renting 
        self.assertEqual(self.sumBikes(), 5)
        self.assertEqual(self.sumDocks(), 6)
        

    def test_source_update_info_and_status(self):
        #Switch to newer version of both info and status
        self.source.gbfs.station_info_url = "offline/station_info_update.json"
        self.source.gbfs.station_status_url = "offline/station_status_update.json"
        updated = self.source.update(self.gps_loc)
        self.assertEqual(updated, True)
        self.assertEqual(len(self.source.status), 3) #Lysaker removed Station 11 added
        self.assertEqual(self.sumBikes(), 12)
        self.assertEqual(self.sumDocks(), 14)


if __name__ == '__main__':
    unittest.main()