import urllib.request

class EpsonPrinterAPI(object):
    def __init__(self, ip):
        """Initialize the link to the printer status page."""
        self._resource = "http://" + ip + "/PRESENTATION/HTML/TOP/PRTINFO.HTML"
        self.data = None
        self.available = True
        self.update()

    def getSensorValue(self, sensor):
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

    def get_mac(self):
        """Get the mac of the printer."""
        try:
            for tr in self.soup.find_all("tr", class_="item-last clearfix"):
                mac = tr.find("td", class_="item-value")
                
                if mac != None:
                    return mac.get_text()
        except:
            return None

    def update(self):
        try:
            """Just fetch the HTML page."""
            response = urllib.request.urlopen(self._resource)
            self.data = response.read().decode("utf-8")
            self.available = True
        except Exception as e:
            #_LOGGER.error("Unable to fetch data from your printer: " + str(e))
            self.available = False



