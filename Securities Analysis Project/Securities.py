"""
Financial Securities 
-------



Requires:
    - pandas
    - pandas_datareader
      from pandas_datareader import data as pdr
    - yfinance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot
from pandas_datareader import data as pdr
import yfinance as yf

class Stock_analysis():
    individual_stock_data = pd.DataFrame()
    Stock_Data = pd.DataFrame()
        
    def __init__(self,tickers : list,start_date):
            self.tickers = tickers
            self.start_date = start_date
            stock_dict = {} 

    
    def individual_data(self):
         for ticks in self.tickers:
                individual_stock_data = pdr.DataReader(ticks, self.start_date)
                stock_dict.update({f"{ticks}_stock" : individual_stock_data})
                
                
    def download_stocks(self, column_name : str):
            self.column_name = column_name
            yf.pdr_override()
            for ticks in self.tickers:
                Stock_analysis.Stock_Data[ticks] = pdr.DataReader(ticks, self.start_date)[column_name]
            return Stock_analysis.Stock_Data

        

    def return_calculator(self,return_type):
        
            self.return_type = return_type
            if return_type == "Log":
                returns_data = np.log(Stock_analysis.Stock_Data/Stock_analysis.Stock_Data.shift(1))
            if return_type == "Simple": 
                returns_data = (Stock_analysis.Stock_Data/Stock_analysis.Stock_Data.shift(1))-1
            return returns_data

    def normalization(self):
            normalized_data = (Stock_analysis.Stock_Data/Stock_analysis.Stock_Data.iloc[0]*100)
            normalized_figure = normalized_data.plot(figsize = (15,6))
            plt.title("Growth Comparison of Stocks")
            return normalized_figure
    
    def individual_return():
            individual_return = self.return_calculator(self.return_type).mean()*250
            print(f"The {self.return_type} return of {ticks for ticks in self.tickers} is {round(individual_return,2)} %")
        

    def portfolio_return(self,weights = list):
            import sys
            weights = np.array(weights)
            if sum(weights)!= 1:
                raise ValueError(f"Sum of the weight of the porfolio should be 1,The sum of your weights are {sum(weights)}")
                if len(weights) != Stock_analysis.Stock_Data.shape[1]:
                    sys.exit("The weights of individual security does not match the no. of securities")
            annual_returns = np.dot(self.return_calculator(self.return_type).mean()*250, weights)
            print(f"The annual returns of the portfolio is {round(annual_returns, 2)}% ")

    
    
