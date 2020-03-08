import traceback
from urllib.request import Request, urlopen
from BySykkelError import print_exception, print_error

'''
https://oslobysykkel.no/apne-data/sanntid
Identifikasjon i header
Alle spørringer til vårt sanntids-API bør sende headeren Client-Identifier.
Denne bør inneholde en verdi som beskriver applikasjonen som kaller APIet. 
Verdien bør inneholde navnet på ditt firma/organisasjon, 
deretter en strek og navn på applikasjonen, 
som mittfirma-reiseplanlegger eller mittfirma-bymonitor.
'''

def get_content(url, client):
    try:
        req = Request(url)
        req.add_header('Client-Identifier', client)
        return urlopen(req).read()
    except Exception as ex:
        print_exception(ex, traceback.format_exc())
        return "{}"
