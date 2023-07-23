import lxml
import datetime
import time
from CbaClient import CbaClient
from FileStorage import FileStorage
from Config import Config
import os

# settings
conf = Config(os.path.dirname(__file__))
disk = FileStorage(conf.WorkingDir)
# reference doesn't contain obsolete currencies
currencies = ['ARP', 'ATS', 'BEF', 'BGL', 'BRC', 'BYR', 'DEM', 'EEK', 'ESP', 'FIM', 'FRF', 'GRD', 'IEP', 'ITL', 'NLG', 'PLZ', 'PTE', 'ROL', 'RUR', 'SDR', 'TMM', 'TRL', # disused currencies
              'TAD', 'USM' # unknown codes
              ]
curdate = conf.StartDate

# get currencies
try:
    soapclient = CbaClient()
    rawSOAP = soapclient.ISOCodesDetailed()
    xmlcurr = lxml.etree.fromstring(rawSOAP.text.encode('utf-8')).findall('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')[0].getchildren()[0].getchildren()[0]
    disk.SaveCurrenciesFile(xmlcurr)
    for curr in xmlcurr.findall('.//ISOCodes/ISO'):
        currencies.append(curr.text)
except Exception as e:
    print("Can't get currencies: {e}")

# get new rates
while curdate != None and curdate <= datetime.datetime.now(datetime.timezone.utc):
# check if we have result from that date
    while disk.IsFileExists(curdate):
        nextdate = disk.GetNextAvailableDateFromFile(curdate)
        if nextdate == None:
            break
        else:
            curdate = nextdate
    (resSOAP, xmlresponse) = soapclient.ExchangeRatesByDate(curdate)
    disk.SaveRatesFile(resSOAP.CurrentDate, lxml.etree.tostring(xmlresponse, encoding = "UTF-8", xml_declaration = True, pretty_print = True))
    for rate in resSOAP.Rates.ExchangeRate:
        if rate.ISO not in currencies:
            print(f'{curdate} Currency code {rate.ISO} not found')
    curdate = resSOAP.NextAvailableDate
    if curdate != None:
        nextdate = curdate = curdate.replace(tzinfo = datetime.timezone.utc)
        time.sleep(5) # 6000 files in 8.5 hours

conf.Save(nextdate)
