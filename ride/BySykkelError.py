import traceback
from datetime import datetime

#defines SilentRun 
import BySykkelConfig  

'''
Uniform program error messages 
Error timestamp is usefull for applications running over a long time
'''

def print_exception(ex, trace):
    if not BySykkelConfig.SilentRun:
        template = "Reported at {0}\n{1} Arguments:\n{2!r}"
        message = template.format(datetime.now(), trace, ex.args)
        print(message)

def print_error(message):
    if not BySykkelConfig.SilentRun:
        template = "Reported at {0}\n{1}"
        print(template.format(datetime.now(), message))