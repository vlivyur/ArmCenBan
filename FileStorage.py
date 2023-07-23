import os
import lxml
import datetime
from Config import FileNames

class FileStorage:
    """ Working with stored files
    """
    def __init__(self, workingDir) -> None:
        self.WorkingDir = os.path.abspath(workingDir)
        if not os.path.exists(self.WorkingDir):
            os.makedirs(self.WorkingDir)
        self.FileList = os.listdir(self.WorkingDir)
        pass

    def IsFileExists(self, curdate):
        """ Checks for file presence in cached list

        Args:
            curdate (datetime): rate date

        Returns:
            bool: True - if the file is already exists
        """
        filename = self.date2FileName(curdate)
        return filename in self.FileList

    def date2FileName(self, curdate):
        """ Create name for downloaded file by template

        Args:
            curdate (datetime): rate date

        Returns:
            string: file name with extension
        """
        return curdate.strftime(FileNames.RatesFileTemplate.value)

    def GetFileName(self, curdate):
        """ Get full path to file with rates

        Args:
            curdate (datetime): rate date

        Returns:
            string: full path to the file
        """
        return os.path.join(self.WorkingDir, self.date2FileName(curdate))

    def GetCurrenciesFileName(self):
        """ File name for file with currencies reference

        Returns:
            string: full path to the file
        """
        return os.path.join(self.WorkingDir, FileNames.CurrenciesFile.value)

    def SaveRatesFile(self, filedate, strResponse):
        """ Add filename to internal list of stored rates

        Args:
            filename (string): a newly stored file name
        """
        with open(self.GetFileName(filedate), 'wb') as outxml:
            outxml.write(strResponse)
        self.FileList.append(self.date2FileName(filedate))

    def GetNextAvailableDateFromFile(self, curdate):
        """ Get next date for rates from file

        Args:
            curdate (datetime): rate date

        Returns:
            datetime: next date of rates from stored file
        """
        filename = self.GetFileName(curdate)
        parser = lxml.etree.XMLParser(remove_blank_text = True)
        try:
            tree = lxml.etree.parse(filename, parser)
            root = tree.getroot()
            nad = root.findall('.//{http://www.cba.am/}NextAvailableDate')
            if len(nad) > 0 and nad[0].text != None and not nad[0].text.isspace():
                return datetime.datetime.fromisoformat(nad[0].text.strip()).replace(tzinfo = datetime.timezone.utc)
            else:
                return None
        except:
            return None

    def SaveCurrenciesFile(self, xmlObj):
        """ Save file with currencies

        Args:
            xmlObj (XML): result of ISOCodesDetailed

        Returns:
            string: XML-string corresponding to {{xmlObj}}
        """
        try:
            with open(self.GetCurrenciesFileName(), 'wb') as outxml:
                response = lxml.etree.tostring(xmlObj, encoding = "UTF-8", xml_declaration = True, pretty_print = True)
                outxml.write(response)
        except:
            print(f"Can't save file {self.GetCurrenciesFileName()}")
