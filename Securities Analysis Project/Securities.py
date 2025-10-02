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
import math 
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl 
import scipy.stats
from pandas_datareader import data as pdr
import yfinance as yf
import random 
import sys



class Stock_returns_analysis():
    combined_df = pd.DataFrame()
    closing_stock_data = pd.DataFrame()
    
   
    def __init__(self,tickers : list,start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
           
    
    def merged_data(self):
        yf.pdr_override()
        data = {ticks : pdr.DataReader(ticks, self.start_date, self.end_date) for ticks in self.tickers}
        for ticks, df in data.items(): 
            df.insert(0,column = "Symbol", value = ticks)
            Stock_returns_analysis.combined_df = pd.concat(data.values())        
        return Stock_returns_analysis.combined_df      

    def __len__(self):
        if self.tickers is not None:
            return  len(self.tickers)
        else : 
            return 0

    def __str__(self):
        if self.tickers is not None:
            return f"Stocks: {self.tickers}"
        else : 
            return f"Stocks: None"

    def download_stocks_closing(self, column_name: str):
        yf.pdr_override()
        self.column_name = column_name
        for ticks in self.tickers:
                Stock_returns_analysis.closing_stock_data[ticks] = pdr.DataReader(ticks, self.start_date, self.end_date)[column_name]
        return Stock_returns_analysis.closing_stock_data


    def stock_relationship(self):
        corr = Stock_returns_analysis.closing_stock_data.corr()
        plt.matshow(corr, cmap="coolwarm")
        plt.xticks(range(len(corr.columns)), corr.columns)
        plt.yticks(range(len(corr.columns)), corr.columns)
        plt.show()

    def stock_stats(self): 
        return Stock_returns_analysis.closing_stock_data.aggregate(["max", "min", "mean"])


    def fill_values(self, fill_method : str): 
        valid_fill_methods = ["linear", "forward", "backward"]
        if fill_method not in valid_fill_methods:
                raise ValueError(f"Invalid fill method. Choose one of the fill methods {valid_fill_methods}")
        elif fill_method == "forward":
                Stock_returns_analysis.closing_stock_data.fillna(method= "ffill", inplace= True)
        elif fill_method == "backward":
                Stock_returns_analysis.closing_stock_data.fillna(method = "bfill", inplace= True)
        else:
                Stock_returns_analysis.closing_stock_data.interpolate(method= "linear", inplace = True)
        return Stock_returns_analysis.closing_stock_data

    def data_distribution(self):
        colors = ["r", "y","g", "b", "m"]
        user_input = int(input(f"What kind of data distribution would you like to see, pls enter the number \n1) Histogram \n2 Box plot"))
        if user_input == 1:
            return Stock_returns_analysis.closing_stock_data.plot(kind = "hist", subplots = True, figsize = (15,9), color = random.choice(colors))
            
        elif user_input == 2:
            return Stock_returns_analysis.closing_stock_data.plot(kind = "box", subplots = True, figsize = (15,9), color = random.choice(colors))
            
        else:
            raise ValueError(f"Invalid user input. Choose either 1 or 2") 
           
        

    def get_returns(self,return_type):
        self.return_type = return_type
        if return_type == "Log":
                returns_data = np.log(Stock_returns_analysis.closing_stock_data/Stock_returns_analysis.closing_stock_data.shift(1))
        else: 
                returns_data = (Stock_returns_analysis.closing_stock_data/Stock_returns_analysis.closing_stock_data.shift(1))-1
        return returns_data

    def normalization(self):
        normalized_data = (Stock_returns_analysis.closing_stock_data/Stock_returns_analysis.closing_stock_data.iloc[0]*100)
        if Stock_returns_analysis.closing_stock_data.shape[1] > 5:
            normalized_figure = normalized_data.plot(figsize = (25,10))
        else : 
            normalized_figure = normalized_data.plot(figsize = (19,6))
        plt.title("Growth Comparison of Stocks")
        return normalized_figure
    
    def individual_return(self):
        individual_return = self.get_returns(self.return_type).mean()*250*100

        print(f"The {self.return_type} return of the stocks are \n{round(individual_return,2)}")
        
           
    def portfolio_return(self,weights = list):
        import sys
        weights = np.array(weights)
        self.weights = weights
        if round(sum(weights),2)!= 1 :
                raise ValueError(f"Sum of the weight of the porfolio should be 1,The sum of your weights are {sum(weights)}")
        if len(weights) != Stock_returns_analysis.closing_stock_data.shape[1]:
                    sys.exit("The weights of individual security does not match the no. of securities")
        annual_returns = np.dot(self.get_returns(self.return_type).mean()*250, weights)

        print(f"The annual returns of the portfolio is {round(annual_returns, 2)}% ")


    def individual_risk_factor(self):
        risk_factor = np.sqrt(self.get_returns(self.return_type).var()*250)
        print(risk_factor)

        print(f"The lowest risk factor is {risk_factor.min()}")

    def portfolio_variance(self):
        if self.weights is None:
            raise ValueError("Weights are not specified")
        returns = self.get_returns(self.return_type)
        cov_matrix = np.cov(returns.T)
        portfolio_variance = np.dot(self.weights.T, np.dot(cov_matrix, self.weights))
        print(f"The portfolio variance is {round(portfolio_variance, 2)}")


