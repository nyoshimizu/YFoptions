"""
This will download then analyze options chains.
"""


class options(object):

    def __init__(self, symbol):
        self.symbol = symbol

        self.expirationdates = []
        # dict of options, keys are date and values are list of information (see
        # fieldnames)
        self.calls = dict()
        self.puts = dict()

            self.fieldnames = ['symbol',
                               'type',
                               'expiration date',
                               'strike',
                               'contract name',
                               'last price',
                               'bid',
                               'ask',
                               'change',
                               'change%',
                               'volume',
                               'open interest',
                               'implied volatility'
                               ]

    def datetoPOSIXtime(self, date):
        """
        Convert date (as mm/dd/yyyy string) to POSIX time

        date: date desired as string

        returns: int of epoch time
        """

        from calendar import timegm
        from datetime import datetime

        date = datetime.strptime(date, "%m/%d/%Y").timetuple()

        POSIXtime = timegm(date)

        POSIXtime = int(round(POSIXtime))

        return POSIXtime


    def getdates(self):
        """
        Get possible exercise dates from Yahoo Finance

        Returns list of POSIX time of option exercise dates available
        """

        URL = 'https://finance.yahoo.com/quote/' \
              + self.symbol \
              + '/options'

        from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options
        chromedriverpath = \
                'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        # chop = webdriver.ChromeOptions()
        # adblockpath = \
        #  'C:\Program Files (x86)\Google\Chrome\Application\Adblock_v3.8.6.crx'
        # chop.add_extension(self.adblockpath)
        driver = webdriver.Chrome(executable_path=chromedriverpath)
                                       # chrome_options=chop)

        # Get list of options expiration dates
        driver.get(URL)

        dropdown = driver.find_elements_by_xpath(
            "//div[contains(@class, 'drop-down-selector')]")

        if len(dropdown) != 1:
            raise ValueError("Search for exercise dates failed.")

        dropdown = dropdown[0]
        optiondates = [option for option in
                       dropdown.find_elements_by_tag_name("option")]
        dates = [int(optiondate.get_attribute("value"))
                 for optiondate in optiondates]

        self.expirationdates = dates

        driver.close()

        return dates


    def getoptionschain(self):
        """
        Get optionschain from Yahoo Finance
        """

        from bs4 import BeautifulSoup
        import re

        from selenium import webdriver
        # from selenium.webdriver.chrome.options import Options
        chromedriverpath = \
            'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
        # chop = webdriver.ChromeOptions()
        # adblockpath = \
        #  'C:\Program Files (x86)\Google\Chrome\Application\Adblock_v3.8.6.crx'
        # chop.add_extension(self.adblockpath)
        driver = webdriver.Chrome(executable_path=chromedriverpath)
        # chrome_options=chop)

        self.calls = dict()
        self.puts = dict()

        # Get all available exercise dates
        if not self.expirationdates:
           self.expirationdates = self.getdates()

        for date in self.expirationdates:
            URL = 'https://finance.yahoo.com/quote' \
                  + '/' + self.symbol \
                  + '/options?date=' \
                  + str(date)

            driver.get(URL)
            html = driver.page_source

            soup = BeautifulSoup(html, 'html.parser')

            callsperdate = []

            callnum = len(soup.find(
                                    "table",
                                    class_=re.compile("^calls table-bordered")
                                    ).find("tbody")
                          )

            for rowidx in range(callnum):

                callrows = soup.find(
                            "table",
                            class_=re.compile("^calls table-bordered")
                            ).find("tbody"
                            ).find("tr",
                                   class_=re.compile("^data-row"+str(rowidx))
                            )

                newcall = dict()

                newcall['symbol'] = self.symbol

                newcall['type'] = 'call'

                newcall['expiration date'] = date

                newcall['strike'] = float(
                            callrows.find("td",
                                          class_=re.compile("^data-col0"))
                            .a.contents[0].replace(',', '')
                            )

                newcall['contract name'] = (callrows.find(
                                            "td",
                                            class_=re.compile("^data-col1"))
                                            .a.contents[0])

                newcall['last price'] = float(callrows.find(
                                            "td",
                                            class_=re.compile("^data-col2"))
                                            .contents[0])

                newcall['bid'] = float(callrows.find(
                                       "td", class_=re.compile("^data-col3"))
                                       .contents[0])

                newcall['ask'] = float(callrows.find(
                                       "td", class_=re.compile("^data-col4"))
                                       .contents[0])

                newcall['change'] = float(callrows.find(
                                          "td", class_=re.compile("^data-col5"))
                                          .find("span").contents[0])

                newcall['change%'] = float(callrows.find(
                                           "td",
                                           class_=re.compile("^data-col6"))
                                           .find("span").contents[0][:-1])

                newcall['volume'] = float(callrows.find(
                                          "td", class_=re.compile("^data-col7"))
                                          .contents[0].replace(',', ''))

                newcall['open interest'] = float(callrows.find(
                                          "td", class_=re.compile("^data-col8"))
                                          .contents[0].replace(',', ''))

                newcall['implied volatility'] = float(callrows.find(
                                              "td",
                                              class_=re.compile("^data-col9"))
                                              .contents[0][:-1])

                callsperdate += [newcall]

            self.calls[date] = callsperdate

            putsperdate = []

            putnum = len(soup.find(
                            "table",
                            class_=re.compile("^puts table-bordered")
                            ).find("tbody")
                         )

            for rowidx in range(putnum):
                putrows = soup.find(
                        "table",
                        class_=re.compile("^puts table-bordered")
                    ).find("tbody"
                           ).find("tr",
                                  class_=re.compile("^data-row" + str(rowidx))
                                  )

                newput = dict()

                newput['symbol'] = self.symbol

                newput['type'] = 'put'

                newput['expiration date'] = date

                newput['strike'] = float(
                            putrows.find("td", class_=re.compile("^data-col0"))
                            .a.contents[0].replace(',', '')
                            )

                newput['contract name'] = (putrows.find(
                                            "td",
                                            class_=re.compile("^data-col1"))
                                            .a.contents[0])

                newput['last price'] = float(putrows.find(
                                        "td", class_=re.compile("^data-col2"))
                                        .contents[0])

                newput['bid'] = float(putrows.find(
                                "td", class_=re.compile("^data-col3"))
                                .contents[0])

                newput['ask'] = float(putrows.find(
                                "td", class_=re.compile("^data-col4"))
                                .contents[0])

                newput['change'] = float(putrows.find(
                                    "td", class_=re.compile("^data-col5"))
                                    .find("span").contents[0])

                newput['change%'] = float(putrows.find(
                                    "td", class_=re.compile("^data-col6"))
                                    .find("span").contents[0][:-1])

                newput['volume'] = float(putrows.find(
                                    "td", class_=re.compile("^data-col7"))
                                    .contents[0].replace(',', ''))

                newput['open interest'] = float(putrows.find(
                                            "td",
                                            class_=re.compile("^data-col8"))
                                            .contents[0].replace(',', ''))

                newput['implied volatility'] = float(putrows.find(
                                            "td",
                                            class_=re.compile("^data-col9"))
                                            .contents[0][:-1])

                putsperdate += [newput]

            self.puts[date] = putsperdate

        driver.close()

    def checkdata(self):
        """
        Check to see if symbol exists in CSV data for current date
        """
        import csv
        import os
        from datetime import date

        today = date.today()
        todayyear = "{}".format(today.year)
        todaymonth = "{0:02d}".format(today.month)
        todayday = "{0:02d}".format(today.day)

        filename = "../data/" \
                   + todayyear+todaymonth+todayday+"_options.csv"

        if not os.path.isfile(filename):
            return -1

        with open(filename, 'r', newline='') as datafile:

            reader = csv.DictReader(datafile)

            for row in reader:
                exampledate = list(self.calls.keys())[0]
                if row['symbol'] == self.calls[exampledate][0]['symbol']: # self.symbol:
                    return 1

            return 0

    def writedata(self):

        import csv

        from datetime import date

        today = date.today()
        todayyear = "{}".format(today.year)
        todaymonth = "{0:02d}".format(today.month)
        todayday = "{0:02d}".format(today.day)

        filename = "../data/" \
                   + todayyear + todaymonth + todayday + "_options.csv"

        # Check if data already exists
        checkdata_return = self.checkdata()
        if checkdata_return == 1:
            return 1

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)

            if checkdata_return == -1:
                writer.writeheader()

            calldates = self.calls.keys()

            for date in calldates:
                for call in self.calls[date]:

                    newrow = dict()
                    for field in self.fieldnames:
                        newrow[field] = call[field]

                    writer.writerow(newrow)

            putdates = self.puts.keys()

            for date in putdates:
                for put in self.puts[date]:

                    newrow = dict()
                    for field in self.fieldnames:
                        newrow[field] = put[field]

                    writer.writerow(newrow)

    def readdata(self):

        import csv
        import os
        from datetime import date

        today = date.today()
        todayyear = "{}".format(today.year)
        todaymonth = "{0:02d}".format(today.month)
        todayday = "{0:02d}".format(today.day)

        filename = "../data/" \
                   + todayyear + todaymonth + todayday + "_options.csv"

        if not os.path.isfile(filename):
            return -1

        self.calls = dict()
        self.puts = dict()

        with open(filename, 'r') as datafile:

            reader = csv.DictReader(datafile)

            for row in reader:

                symbol = row['symbol']
                type = row['type']
                date = row['expiration date']

                if symbol != self.symbol:
                    continue

                if type == 'call':
                    if date not in self.calls.keys():
                        self.calls[date] = []
                    self.calls[date] += [row]

                if type == 'put':
                    if date not in self.puts.keys():
                        self.puts[date] = []
                    self.puts[date] += [row]
