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



class Returns_analysis():
    individual_stock_data = pd.DataFrame()
    Stock_Data = pd.DataFrame()
    stock_dict = {}
   
    def __init__(self,tickers : list,start_date):
            self.tickers = tickers
            self.start_date = start_date
           
    
    def individual_data(self):
         yf.pdr_override()
         for ticks in self.tickers:
                individual_stock_data = pdr.DataReader(ticks.title, self.start_date)
                Returns_Analysis.stock_dict.update({f"{ticks.title}_stock" : individual_stock_data})
                
    def download_stocks(self, column_name : str):
            self.column_name = column_name
            yf.pdr_override()
            for ticks in self.tickers:
               Returns_analysis.Stock_Data[ticks.title] = pdr.DataReader(ticks.title, self.start_date)[column_name]
            return Returns_analysis.Stock_Data


    def calculate_returns(self,return_type):
           self.return_type = return_type
           if return_type == "Log":
                returns_data = np.log(Returns_analysis.Stock_Data/Returns_analysis.Stock_Data.shift(1))
           else: 
                returns_data = (Returns_analysis.Stock_Data/Returns_analysis.Stock_Data.shift(1))-1
           return returns_data

    def normalization(self):
            normalized_data = (Returns_analysis.Stock_Data/Returns_analysis.Stock_Data.iloc[0]*100)
            normalized_figure = normalized_data.plot(figsize = (19,6))
            plt.title("Growth Comparison of Stocks")
            return normalized_figure
    
    def individual_return(self):
            individual_return = self.calculate_returns(self.return_type).mean()*250*100

            print(f"The {self.return_type} return of the stocks are {round(individual_return,2)}")
        

    def portfolio_return(self,weights = list):
            import sys
            weights = np.array(weights)
            if round(sum(weights),2)!= 1 :
                raise ValueError(f"Sum of the weight of the porfolio should be 1,The sum of your weights are {sum(weights)}")
                if len(weights) != Returns_Analysis.Stock_Data.shape[1]:
                    sys.exit("The weights of individual security does not match the no. of securities")
            annual_returns = np.dot(self.calculate_returns(self.return_type).mean()*250, weights)

            print(f"The annual returns of the portfolio is {round(annual_returns, 2)}% ")


    def individual_risk_factor(self):
                risk_factor = pd.DataFrame(np.sqrt(self.calculate_returns(self.return_type).var()*250))
                print(risk_factor)

                print(f"The lowest risk factor is{risk_factor.min()}")