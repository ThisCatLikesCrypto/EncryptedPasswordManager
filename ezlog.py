import eztxt
import datetime
import os

def log(data):
    timenstr = datetime.datetime.now()
    datenstr = datetime.date.today()
    date = str(datenstr)
    if os.name=='nt':
        datewlog = os.getcwd()+ "\\logs\\" + date + ".log"
    else:
        datewlog = os.getcwd()+ "/logs/" + date + ".log"
    time = str(timenstr)
    timewlog = time + ": " + data
    print(timewlog)
    eztxt.appendn(datewlog, timewlog)
