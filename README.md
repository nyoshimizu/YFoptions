# Background
This package scrapes YF for options contract information using Selenium and Beautiful Soup.
It will download a list of available expiration dates for a given equity, then download options information
such as strike price, bids and asks, implied volatility, etc. that are available on the site. Note that the
information sometimes seems to be outdated or incorrect in comparison to information from privately available
data (e.g. from a brokerage).

# Usage
An object is created for each equity which stores the options contracts information:

```python
from code import options
equityoptions = options("XYZ")
```

The object has three important variables.
* expirationdates: A list of expiration dates available for the equity in epoch time.
* calls and puts: These variables contain the options contracts information. They are dictionaries where the
keys are the expiration date and the values are lists. These lists contain dictionaries, where the keys
are the options contract information (e.g. strike price, ask, etc.) and the values are the corresponding
information.

The information that is available is listed in the fieldnames variable:
```python
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
```

The object has a few important methods.
* getdates() will load the available expiration dates for the equity, saving them to the expirationdates variable.
* getoptionschain() will download all the options, both calls and puts, to the calls and puts variables.
* writedata() will write the data to a CSV file located in ./data
* readdata() will load the data from a CSV file into the object.

Therefore, typical usage will consist of:

```python
from code import options
myoptions = options.("XYZ")
myoptions.getdates()
myoptions.getoptionschain()
myoptions.writedata()
```

# Requirements
This code requires Selenium and Beautiful Soup
ChromeDriver is by Selenium, and should be downloaded. The code assumes it is located at
"C:\Program Files (x86)\Google\Chrome\Application\\".


# Todo:
* Full loading of the pages can be delayed by some very slow ads. In the short term, that can be mitigated
by canceling the page load (e.g. by pressing 'escape') to allow the program to continue. An explicit condition
(e.g. timer or existence of certain web elements) could be implemented to prevent excessive page load times.

