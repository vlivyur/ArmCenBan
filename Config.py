from configparser import ConfigParser
import datetime
from os import path
from enum import Enum

class ConfigParameters(Enum):
    """ Parts of config file
    """
    Section = 'DEFAULT'
    WorkingDir = 'workingdir'
    StartDate = 'startdate'

class FileNames(Enum):
    """ Default files and directories names
    """
    ConfigFile = 'armcenban.config'
    DefaultWorkingDir = 'ExchangeRatesByDate'
    CurrenciesFile = 'ISOCodesDetailed.xml'
    RatesFileTemplate = '%Y%m%d.xml'

class Config:
    """ Reads and writes config file
    """
    StartDate = datetime.datetime(2000, 1, 1, tzinfo = datetime.timezone.utc)

    def __init__(self, homeDir) -> None:
        """ Reinitialise all parameters from config file

        Args:
            homeDir (string): home directory for main class
        """
        self.WorkingDir = path.abspath(path.join(homeDir, '..', FileNames.DefaultWorkingDir.value))
        self.config = ConfigParser()
        self.config.read(FileNames.ConfigFile.value)
        if ConfigParameters.StartDate.value in self.config[ConfigParameters.Section.value]:
            configdate = datetime.datetime.fromisoformat(self.config[ConfigParameters.Section.value][ConfigParameters.StartDate.value]).replace(tzinfo = datetime.timezone.utc)
            if configdate >= self.StartDate:
                self.StartDate = configdate
        if ConfigParameters.WorkingDir.value in self.config[ConfigParameters.Section.value]:
            self.WorkingDir = path.abspath(self.config[ConfigParameters.Section.value][ConfigParameters.WorkingDir.value])

    def Save(self, lastdate):
        """ Save config file

        Args:
            lastdate (datetime): last imported date
        """
        if lastdate != None:
            self.config[ConfigParameters.Section.value][ConfigParameters.StartDate.value] = lastdate.date().isoformat()
        self.config[ConfigParameters.Section.value][ConfigParameters.WorkingDir.value] = self.WorkingDir
        with open(FileNames.ConfigFile.value, 'w') as confile:
            self.config.write(confile)
