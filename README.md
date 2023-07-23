# What is it for?
This script downloads all currency rates from Central Bank of Armenia and stores them locally in *.xml files.

First available date is `2000-01-01`. New data appears on working days after 12:00 UTC.

# Installation
It requires [zeep](https://docs.python-zeep.org/) for SOAP requests:
```bash
pip install zeep
```
After first run in the current working directory will be created configuration file `armcenban.config` with path to directory for storing downloaded files and last loaded date:
```
[DEFAULT]
startdate = 2020-12-31
workingdir = ..\ExchangeRatesByDate
```
Last loaded date will be updated with every run of the script. If path set as relational it will be updated with absolute path.

Default parameters are `2000-01-01` and `..\ExchangeRatesByDate`

# Known Errors in Data
- There are some currencies that I can not recognise:
    - TAD from 2000-01-01 to 2000-12-31
    - USM from 2000-01-01 to 2006-12-30
- TM in 2013-05-22 is Turkmenistan manat (TMT)
- There is no internal mechanism (in the CBA) to manage relevance of currency codes. Thus RUR is encountered till 2006-12-30 (it is RUB since 1998-01-01). Similar situation could be in Eurozone as it has been expanding over the years.
