import re
import urllib.request

from bs4 import BeautifulSoup


class EpsonPrinterAPI(object):
    def __init__(self, ip):
        """Initialize the link to the printer status page."""
        self._resource = "http://" + ip + "/PRESENTATION/HTML/TOP/PRTINFO.HTML"
        self._resource2 = "http://" + ip + "/status/statsupl.asp"
        self._available_resource = None
        self.data = None
        self.available = True
        self.update()

    def getSensorValue(self, sensor):
        if self._available_resource == self._resource2:
            return self._getSensorValueStatSupl(sensor)
        return self._getSensorValuePrtInfo(sensor)

    def _getSensorValuePrtInfo(self, sensor):
        """To make it the user easier to configre the cartridge type."""
        sensorCorrected = "";
        #_LOGGER.debug("Color to fetch: " + sensor)
        if sensor == "black":
            sensorCorrected = "K"
        elif sensor == "magenta":
            sensorCorrected = "M"
        elif sensor == "cyan":
            sensorCorrected = "C"
        elif sensor == "yellow":
            sensorCorrected = "Y"
        elif sensor == "clean":
            sensorCorrected = "Waste"
        else:
            return 0;

        try:
            search = "Ink_" + sensorCorrected + ".PNG' height='"
            result = self.data.index(search)
            startPos = result + len(search)
            valueRaw = self.data[startPos:startPos + 2]
            """In case the value is a single digit, we will get a ' char, remove it."""
            return int(valueRaw.replace("'", "")) * 2
        except Exception as e:
            #_LOGGER.error("Unable to fetch level from data: " + str(e))
            return 0

    def _getSensorValueStatSupl(self, sensor):
        """To make it the user easier to configre the cartridge type."""
        sensorCorrected = "";
        #_LOGGER.debug("Color to fetch: " + sensor)
        if sensor == "black":
            sensorCorrected = "bk"
        # TODO others?
        else:
            return 0

        try:
            img = self.data.find(lambda tag: tag.name == "img" and tag.has_attr("src") and bool(re.search(r"/%s\d+.png" % re.escape(sensorCorrected), tag["src"])))
            return int(img.next_sibling.string.strip().strip("%"))
        except Exception as e:
            #_LOGGER.error("Unable to fetch level from data: " + str(e))
            return 0

    def update(self):
        if self._resource:
            self._update(self._resource)
            if self.available:
                self._resource2 = None
                return
        if self._resource2:
            self._update(self._resource2, parse=True)
            if self.available:
                self._resource = None

    def _update(self, resource, parse=False):
        try:
            """Just fetch the HTML page."""
            response = urllib.request.urlopen(resource)
            data = response.read().decode("utf-8")
            self.available = True
            if parse:
                self.data = BeautifulSoup(data, "html.parser")
            else:
                self.data = data
            self._available_resource = resource
        except Exception as e:
            #_LOGGER.error("Unable to fetch data from your printer: " + str(e))
            self.available = False



