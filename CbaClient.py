import zeep #pip install zeep
from enum import Enum

class WsdlParams(Enum):
    """
    """
    UrlCbaApi = 'http://api.cba.am/exchangerates.asmx?wsdl'

class CbaClient:
    """ Working with API of Central Bank of Armenia
    """
    def ISOCodesDetailed(self):
        """ Detailed list of currencies

        Returns:
            string: xml of ISOCodesDetailedResult
        """
        client = zeep.Client(wsdl = WsdlParams.UrlCbaApi.value)
        with client.settings(raw_response = True):
            return client.service.ISOCodesDetailed()

    def ExchangeRatesByDate(self, curdate):
        """ Retrieves all available rates of the specified date

        Args:
            curdate (datetime): specific date

        Returns:
            (envelope, ExchangeRatesByDateResult): (rates, responce)
        """
        history = zeep.plugins.HistoryPlugin()
        client = zeep.Client(wsdl = WsdlParams.UrlCbaApi.value, plugins = [history])
        with client.settings(raw_response = False):
            resSOAP = client.service.ExchangeRatesByDate(curdate.isoformat().replace('+00:00', 'Z'))
        return (resSOAP,
                history.last_received['envelope'].findall('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')[0].getchildren()[0].getchildren()[0])
