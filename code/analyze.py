"""
Run stuff to analyze options chains
"""
from code import options
from code import stests

# For now make manual stock list. Later, can produce list using small-, mid-,
# and large-cap indices.

stocks = ['COST'] #,
          # 'GLW',
          # ]

prices = [170.96]#,
          # 26.80
          # ]


for idx in range(len(stocks)):
    stock = stocks[idx]
    print(stock)
    stockdata = options.options(stock)
    if stockdata.checkdata() != 1:
        stockdata.getoptionschain()
        stockdata.writedata()
    else:
        stockdata.readdata()

    stests.scheck(stockdata, prices[idx])

