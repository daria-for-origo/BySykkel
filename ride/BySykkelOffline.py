import traceback
from BySykkelError import print_exception, print_error

'''
Set of json files in offline/ folder simulates 
actual real time data from
https://oslobysykkel.no/apne-data/sanntid 

Should you be so unlucky to be offline, you can still work on the program
However, the biggest advantage of offline data is the ability 
to edit data and create various test cases.

(Full coverage test is out of the scope for this project due to time restrictions)

Look for <Offline Test> in the project for more info
NB! Use --gbfs offline/gbfs.json for offline test
'''

def get_content(file, client):
    try:
        f=open(file, "r", encoding='utf-8')
        return f.read()
    except Exception as ex:
        print_exception(ex, traceback.format_exc())
        return "{}"