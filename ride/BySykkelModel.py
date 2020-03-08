import traceback
import json

'''
<Offline Test> option
Uncomment next and comment import BySykkelOnline line
'''
#import BySykkelOffline as BySykkelData
import BySykkelOnline as BySykkelData

from math import radians, sin, cos, acos
from datetime import datetime
from BySykkelError import print_exception, print_error

    
class GPSLocation:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon


    def __str__(self):
        return "[" + str(self.lat) + "," + str(self.lon) + "]"

    def distance(self, other):
        '''
        Lazy bird distance calculation
        Actual bicycle roads calculation would be much better here
        Alas
        '''
        slat = radians(self.lat)
        slon = radians(self.lon)
        olat = radians(other.lat)
        olon = radians(other.lon)
        return 6371.01 * acos(sin(slat)*sin(olat) + cos(slat)*cos(olat)*cos(slon - olon))

    def parse(input):
        '''
        Parse "[ lat, lon ]" string 
        '''
        pair = eval(input)
        return GPSLocation(pair[0], pair[1])


class GbfsImfo:
    '''
    Auto-discovery-fil som lenker til alle de andre filene som er publisert av systemet.
    See https://oslobysykkel.no/apne-data/sanntid

    For the sake of this program is considred static and is read only once, upon initialization
    '''
    def __init__(self, url, client_id):
        self.system_info_url = "system_information tag unknown to gbfs"
        self.station_info_url = "station_information tag unknown to gbfs"
        self.station_status_url = "station_status tag unknonw to gbfs "
        self.ok = False
        try:
            js = json.loads(BySykkelData.get_content(url, client_id))
            self.last_updated = js["last_updated"]
            for item in js["data"]["nb"]["feeds"]:
                if item["name"] == "system_information":
                    self.system_info_url = item["url"]
                if item["name"] == "station_information":
                    self.station_info_url = item["url"]
                if item["name"] == "station_status":
                    self.station_status_url = item["url"]
            self.ok = True
        except Exception as ex:
                print_exception(ex, traceback.format_exc())

    def __str__(self):
        template = "GBFS status:\nsystem_info_url={0}\nstation_info_url={1}\nstation_status_url={2}"
        return template.format(self.system_info_url, self.station_info_url, self.station_status_url)


class SystemInfo:
    '''
    Maskinlesbar grunnleggende informasjon om Oslo Bysykkel
    See https://oslobysykkel.no/apne-data/sanntid

    Nice to have for presentation purposes
    '''
    def __init__(self, url, client_id):
        self.operator = "Missing system info"
        self.phone_number = ""
        self.email = ""
        try:
            js = json.loads(BySykkelData.get_content(url, client_id))
            self.operator = js["data"]["operator"]
            self.name = js["data"]["name"]
            self.phone_number = js["data"]["phone_number"]
            self.email = js["data"]["email"]
        except Exception as ex:
                print_exception(ex, traceback.format_exc())

    
    def format(self, template="Operated by {0}, ring {1} or email {2}"):
        return template.format(self.operator, self.phone_number, self.email)

    def __str__(self):
        return self.format()


class StationDict:
    '''
    Station (_information and _status) json files have similar structure 
    infor and status are connected by station_id key

    Hence, StationDict is a dictionary for keeping either info or status json per station_id 
    '''
    def __init__(self, js):
        self.timestamp = js["last_updated"]
        self.dictionary = dict()
        try:
            for info in js["data"]["stations"]:
                self.dictionary[int(info["station_id"])] = info
        except Exception as ex:
                print_exception(ex, traceback.format_exc())

    def printAll(self):
        for id in self.dictionary:
            print(id, self.dictionary[id])


class StationStatus:
    '''
    Keep all information about each station - both static and real time 
    There is much more information available about each station,
    but for this small app that suffice

    This app is proud to present a data model that contains station distance to the user
    That's why it is also a part of the class.
    Two methods change the instance state: 
        update_status using newly read json
        update_distance using newly updated user location
    '''
    def __init__(self, station_info):
        self.bikes = 0
        self.docks = 0
        self.distance = 0
        self.name = "O Brother, Where Art Thou?"  
        try:
            self.name = station_info["name"]
            self.address = station_info["address"]
            self.location = GPSLocation(station_info["lat"], station_info["lon"])
        except Exception as ex:
            print_exception(ex, traceback.format_exc())
            
    def __str__(self):
        template = "{0}:{1},{2},{3}"
        return template.format(self.name, self.bikes, self.docks, self.location)

    def update_status(self, js):
        self.bikes = js["num_bikes_available"] if js["is_renting"] > 0 else 0  
        self.docks = js["num_docks_available"] if js["is_returning"] > 0 else 0

    def update_distance(self, gps_location):
        self.distance = self.location.distance(gps_location)
    
    def sortKey(self):
        return self.distance

class Source:
    '''
    BySykkel real time data put together 
    '''
    def __init__(self, gbfs_url, client_id):
        self.client_id = client_id
        self.gbfs = GbfsImfo(gbfs_url, client_id)
        self.system = SystemInfo(self.gbfs.system_info_url, client_id)
        self.info = dict()
        self.status = list()
        self.status_timestamp = 0
        self.info_timestamp = 0
        self.location = GPSLocation(0,0)
      
    def _update_distance(self, gps_location):
        '''
        Update user current location
        '''
        for s in self.status:
            s.update_distance(gps_location)
        self.sort()

    
    def _load_info(self):
        '''
        Loads information from station_information 
        return False if no new data has been loaded  
        '''
        try:
            js = json.loads(BySykkelData.get_content(self.gbfs.station_info_url, self.client_id))
            si = StationDict(js)
            if (si.timestamp <= self.status_timestamp):
                return False
            self.info.clear()
            for key, info in si.dictionary.items():
                self.info[key] = StationStatus(info)
        except Exception as ex:
            print_exception(ex, traceback.format_exc())
            return False
        return True

    def _update_status(self):
        '''
        Loads information from station_status 
        return False if no new data has been loaded  
        '''
        force_update = self._load_info()
        js = json.loads(BySykkelData.get_content(self.gbfs.station_status_url, self.client_id))
        ss = StationDict(js)
        if (not force_update and ss.timestamp <= self.status_timestamp):
            return False 
        self.status.clear()
        for key, info in ss.dictionary.items():
            try:
                s = self.info[key]
                s.update_status(info)
                self.status.append(s)
            except KeyError:
                s = StationStatus({})
                s.update_status(info)
                self.status.append(s) # Interesting to see how many key errors are there
            except Exception as ex:
                print_exception(ex, traceback.format_exc())
                return False
        return True
    
    def update(self, gps_location):
        '''
        Force the source to update its data
        return False if neither location nor status have been changed  
        '''

        location_changed = self.location != gps_location
        status_changed = self._update_status()

        if not location_changed and not status_changed:
            return False;

        self.location = gps_location
        self._update_distance(self.location)
        self.sort()
       
        return True
    
    def sort(self) :
        '''
        Seems silly to provide a sort in a model nowdays when
        so many widgets can do the same, but for those who can find it usefull ...
        '''
        self.status.sort(key=lambda stationstatus: stationstatus.sortKey())
