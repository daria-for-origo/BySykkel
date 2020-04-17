import traceback
from urllib.request import Request, urlopen
from ride.BySykkelError import print_exception, print_error

'''
https://oslobysykkel.no/apne-data/sanntid
Identifikasjon i header
Alle spørringer til vårt sanntids-API bør sende headeren Client-Identifier.
Denne bør inneholde en verdi som beskriver applikasjonen som kaller APIet. 
Verdien bør inneholde navnet på ditt firma/organisasjon, 
deretter en strek og navn på applikasjonen, 
som mittfirma-reiseplanlegger eller mittfirma-bymonitor.
'''

def get_content(url, client_id):

    if client == "":
        print_error("Mandatory parameter Client-ID is missing")
        return "{}" 

    if len(client) < 7:
        print_error("Client-ID is too short")
        return "{}" 
    
    try:
        req = Request(url)
        req.add_header('Client-Identifier', client_id)
        return urlopen(req).read()
    except Exception as ex:
        ex.args  += (url,)
        print_exception(ex, traceback.format_exc())
        return "{}"
