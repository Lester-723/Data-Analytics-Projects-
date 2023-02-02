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
           
    
    def individual_data(self, fill_method : str):
        yf.pdr_override()
        valid_fill_methods = ['linear', 'forward', 'backward']
        if fill_method not in valid_fill_methods:
                raise ValueError(f"Invalid fill method. Choose one of {valid_fill_methods}")
        for ticks in self.tickers:
                individual_stock_data = pdr.DataReader(ticks, self.start_date)
                if individual_stock_data.isnull().values.any(): # check if dataframe contains any missing values
                        if fill_method == 'forward':
                                individual_stock_data.ffill(inplace=True) # forward fill missing values
                        elif fill_method == 'backward':
                                individual_stock_data.bfill(inplace=True) # backward fill missing values
                        else:
                                individual_stock_data.interpolate(method=fill_method, inplace=True) # linear fill missing values
        Returns_Analysis.stock_dict.update({f"{ticks}_stock" : individual_stock_data})


    def download_stocks(self, fill_method , column_name : str):
        yf.pdr_override()
        valid_fill_methods = ['linear', 'forward', 'backward']
        if method not in valid_fill_methods:
                raise ValueError(f"Invalid fill method. Choose one of {valid_fill_methods}")
        self.column_name = column_name
        for ticks in self.tickers:
                stock_data = pdr.DataReader(ticks, self.start_date)[column_name]
                stock_data.fillna(method= method, inplace=True)
                Returns_analysis.Stock_Data[ticks] = stock_data
        return Returns_analysis.Stock_Data


    def get_returns(self,return_type):
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
            individual_return = self.get_returns(self.return_type).mean()*250*100

            print(f"The {self.return_type} return of the stocks are {round(individual_return,2)}")
        

    def portfolio_return(self,weights = list):
            import sys
            weights = np.array(weights)
            self.weights = weights
            if round(sum(weights),2)!= 1 :
                raise ValueError(f"Sum of the weight of the porfolio should be 1,The sum of your weights are {sum(weights)}")
                if len(weights) != Returns_Analysis.Stock_Data.shape[1]:
                    sys.exit("The weights of individual security does not match the no. of securities")
            annual_returns = np.dot(self.get_returns(self.return_type).mean()*250, weights)

            print(f"The annual returns of the portfolio is {round(annual_returns, 2)}% ")


    def individual_risk_factor(self):
                risk_factor = pd.DataFrame(np.sqrt(self.get_returns(self.return_type).var()*250))
                print(risk_factor)

                print(f"The lowest risk factor is{risk_factor.min()}")

    def portfolio_variance(self):
        if self.weights is None:
            raise ValueError("Weights are not specified")
        returns = self.get_returns(self.return_type)
        cov_matrix = np.cov(returns.T)
        portfolio_variance = np.dot(self.weights.T, np.dot(cov_matrix, self.weights))
        print(f"The portfolio variance is {round(portfolio_variance, 2)}")
