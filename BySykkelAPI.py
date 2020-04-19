import ride.BySykkelModel as BySykkelModel
import BySykkelConfig
import sys
import re
'''
Using argparse for extract query parameters from a request 
URI string will be modified to fit the default parser
TODO: find python lib for that or make custom parser
'''
import argparse
parser = argparse.ArgumentParser(description='BySykkel REST API query parameters',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--bikes', dest='bikes', type=int, default=0, help='stasjoner med  tilgjengelige sykkler')
parser.add_argument('--docks', dest='docks', type=int, default=0, help='stasjoner med ledige plasser')
parser.add_argument('--gps', dest='gps', type=str, default="[59.915096,10.7312715]", help='GPS posisjon [lat,lon]')
parser.add_argument('--top', dest='top', type=int, default=0, help='Top results (default all)')

''' 
Format API replies (provide implememntation in request) 
'''
class OutputInterface:
    
    def __init__(self):
        self.examples = list()
 
    def station_format(self) -> str:
        pass
    def list_prefix(self) -> str:
        pass
    def list_suffix(self) ->str:
        pass
    def list_separator(self) -> str:
        pass
    def empty_result(self) -> str:
        pass
    def error(self, error_message) -> str:
        pass
  

class JSONOutput(OutputInterface):

    def station_format(self):
        return '{{"station_id":"{6}","name":"{0}","distance":"{1:.3f}",\
"bikes":"{4}","docks":"{5}","lat":"{2}","lon":{3},"address":"{7}"}}'

    def list_prefix(self):
        return '{"stations":['

    def list_suffix(self):
        return "]}"

    def list_separator(self):
        return ","
    
    def empty_result(self):
        return "{}"

    def error(self, error_message="Mailformed request"):
        template='{{"error":"{0}", "Try" : {1}}}'
        return template.format(error_message, self.examples)


class Request:

    def __init__(self, query_string):
        query_params_split = query_string.split('?')
        self.resource = query_params_split[0]
        self.params = parser.parse_known_args(("--" + query_params_split[-1]).replace("&", "&--").split("&"))[0]
        
'''
API functions 
'''        
def _get_station_by_id(request, output):

    resource_id_split = request.resource.split('/')
    if resource_id_split[-1].isdigit():
        station_id = int(resource_id_split[-1])
        model = BySykkelModel.Source(BySykkelConfig.OnlineGBFS, BySykkelConfig.OnlineClientID)
        model.update(BySykkelModel.GPSLocation.parse(request.params.gps))
        if (station_id in model.info.keys()): 
            return model.info[station_id].format(output.station_format())

    return output.error("Invalid station id:" + resource_id_split[-1])


def _get_all_stations(request, output):
    
    model = BySykkelModel.Source(BySykkelConfig.OnlineGBFS, BySykkelConfig.OnlineClientID)
    model.update(BySykkelModel.GPSLocation.parse(request.params.gps))

    result = output.list_prefix() 
    view = model.status
    if request.params.top != 0:
        view = model.status[0:request.params.top] 
    for value in view: 
        if value.bikes >= request.params.bikes:
            if value.docks >= request.params.docks:
                if (len(result) > len(output.list_prefix())):
                    result += output.list_separator()
                result += value.format(output.station_format())
    result += output.list_suffix()
    return result

def _add_examples(output):
    output.examples = '[\
        "stations",\
        "stations/<id>",\
        "stations?top=k&bikes=n&docks=m&gps=[lat,lon]",\
        "stations/<id>/?gps=[lat,lon]"\
    ]'


'''
API main call
Input:  query 
        optional output interface implementation (JSON by default)
Output: Success: string containing one,several or no stations info
        Failure: error message

'''
def request(query_string, output=JSONOutput()):    
    
    try:
        # Do it before exeting any request and error message will contain examples
        _add_examples(output)

        request = Request(query_string)
        
        if "stations" == request.resource:
            return _get_all_stations(request, output)

        if "stations/" in request.resource:
            return _get_station_by_id(request, output)

        return output.error("Unknown resource:" + request.resource)

    except Exception as ex:
        return output.error("Malformed request:" + query_string)  #Do not expose exception message

    
if __name__ == '__main__':
    print(request(sys.argv[1]))