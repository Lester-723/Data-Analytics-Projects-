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



class Returns_analysis():
    individual_stock_data = pd.DataFrame()
    closing_stock_data = pd.DataFrame()
    
   
    def __init__(self,tickers : list,start_date):
        self.tickers = tickers
        self.start_date = start_date
        
           
    
    def individual_data(self,stock_dict):
        yf.pdr_override()
        if type(stock_dict) != dict:
                raise TypeError(f"Data type should be of type dictionary")
        for ticks in self.tickers:
                Returns_analysis.individual_stock_data = pdr.DataReader(ticks, self.start_date)
                stock_dict.update({f"{ticks}_stock" : Returns_analysis.individual_stock_data})
        


    def download_stocks_closing(self, column_name: str):
        yf.pdr_override()
        self.column_name = column_name
        for ticks in self.tickers:
                Returns_analysis.closing_stock_data[ticks] = pdr.DataReader(ticks, self.start_date)[column_name]
        return Returns_analysis.closing_stock_data


    def fill_values(self, fill_method : str): 
        valid_fill_methods = ["linear", "forward", "backward"]
        if fill_method not in valid_fill_methods:
                raise ValueError(f"Invalid fill method. Choose one of the fill methods {valid_fill_methods}")
        elif fill_method == "forward":
                Returns_analysis.closing_stock_data.fillna(method= "ffill", inplace= True)
        elif fill_method == "backward":
                Returns_analysis.closing_stock_data.fillna(method = "bfill", inplace= True)
        else:
                Returns_analysis.closing_stock_data.interpolate(method= "linear", inplace = True)
        return Returns_analysis.closing_stock_data

    def data_distribution(self):
        user_input = str(input("What kind of data distribution would you like to see"))
        distribution_types = ["normal" , "other"]
        colors = ["r", "y","g", "b", "m"]
        if user_input == "normal":
                for ticker in self.tickers:
                    mean = Returns_analysis.closing_stock_data[ticker].mean()
                    median =  Returns_analysis.closing_stock_data[ticker].sort_values(ascending= True).median()
                    mode = Returns_analysis.closing_stock_data[ticker].mode()[0]
                    std = Returns_analysis.closing_stock_data[ticker].std()
                    plt.axvline(mean, c = "#40E0D0")#plotting a vertical line to showcase the mean
                    plt.axvline(mode, c = "#800000")#plotting a vertival line to showcase the mode 
                    x = np.linspace(mean-3*std, mean+3*std,100)#xaxis 
                    y = scipy.stats.norm.pdf(x,mean,std)#yaxis
                    plt.plot(x, y, 'r', linewidth=2, label = ticker)
                    one_std_below, one_std_above = mean-std,mean+std
                    two_std_below, two_std_above = mean-2*std,mean+2*std
                    three_std_below , three_std_above = mean-3*std,mean+3*std
                    plt.fill_between(x,y, where = ((x >= one_std_below) & (x <= one_std_above)), color='green', alpha=0.2)
                    plt.fill_between(x,y, where= ((x >= two_std_below) & (x <= two_std_above)), color='yellow', alpha=0.2)
                    plt.fill_between(x,y, where= ((x >= three_std_below) & (x <= three_std_above)), color='blue', alpha=0.2)
                    plt.legend()
                    plt.show()
        elif user_input == "other":
                visual_method = ["box", "hist"]
                user_visual_decision = str(input(f"Choose the one of the following distributions {visual_method}"))
                Returns_analysis.closing_stock_data.plot(kind = user_visual_decision, subplots = True, figsize = (15,9), color = random.choice(colors))
                
        else : 
            sys.exit(f"This function cannot run with the value you entered. Please select from the follwing  {distribution_types}")
        

    def get_returns(self,return_type):
        self.return_type = return_type
        if return_type == "Log":
                returns_data = np.log(Returns_analysis.closing_stock_data/Returns_analysis.closing_stock_data.shift(1))
        else: 
                returns_data = (Returns_analysis.closing_stock_data/Returns_analysis.closing_stock_data.shift(1))-1
        return returns_data

    def normalization(self):
        normalized_data = (Returns_analysis.closing_stock_data/Returns_analysis.closing_stock_data.iloc[0]*100)
        if Returns_analysis.closing_stock_data.shape[1] > 5:
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
        if len(weights) != Returns_Analysis.closing_stock_data.shape[1]:
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