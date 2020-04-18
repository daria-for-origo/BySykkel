import ride.BySykkelModel as BySykkelModel
import BySykkelConfig
import sys

'''
Using argparse for extract query parameters from a request 
'''
import argparse
parser = argparse.ArgumentParser(description='BySykkel REST API query parameters',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)


parser.add_argument('--client_id', dest='client_id', type=str, default=BySykkelConfig.OnlineClientID, help='Client-Identifier for API forespørsel')
parser.add_argument('--bikes', dest='bikes', type=int, default=0, help='stasjoner med  tilgjengelige sykkler')
parser.add_argument('--docks', dest='docks', type=int, default=0, help='stasjoner med ledige plasser')
parser.add_argument('--gps', dest='gps_location', type=str, default="[59.915096,10.7312715]", help='GPS posisjon [lat,lon]')
parser.add_argument('--station_id', dest='station_id', type=int, default=0, help='Specific station (default: all stations')

'''
Produce output in json
'''
json_format='{{"station_id":"{6}","name":"{0}","distance":"{1:.3f}","bikes":"{4}","docks":"{5}","address":"{7}"}}'
json_array_start = '{"stations":['
json_array_end = "]}"
json_array_element_separator=","


class Execute:

    def request(query_string):

        request = parser.parse_known_args(query_string.replace("?", "?--").split("?"))[0]
        
        model = BySykkelModel.Source(BySykkelConfig.OnlineGBFS, request.client_id)
        model.update(BySykkelModel.GPSLocation.parse(request.gps_location))

        if (request.station_id > 0):
            if (request.station_id in model.info.keys()): 
                return model.info[request.station_id].format(json_format)
            else:
                return "{}"
        else: 
            output = json_array_start       
            for value in model.status: 
                if value.bikes >= request.bikes:
                    if value.docks >= request.docks:
                        if (len(output) > len(json_array_start)):
                            output += json_array_element_separator
                        output += value.format(json_format)
            output += json_array_end
            return output

if __name__ == '__main__':
    print(Execute.request(sys.argv[1]))