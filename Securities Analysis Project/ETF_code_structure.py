
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from nsepy import get_history
from datetime import date


class ETF_analysis():
    closing_stock_data = pd.DataFrame()
    
   
    def __init__(self,tickers : list,start_date ,end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date 
        
    def ETF_data_extraction(self):
        data = {ticks : get_history(ticks ,date(2012,1,1), date(2022,1,31)) for ticks in self.tickers}
        for ticker,df in data.items():
             combined_df = pd.concat(data.values())  
        return combined_df 
    

    def to_excel_sheets(self,filename):
        self.ETF_data_extraction().to_excel(filename)
        



#  if user_input == "normal":
#     for ticker in self.tickers:
#                     mean = Stock_returns_analysis.closing_stock_data[ticker].mean()
#                     median =  Stock_returns_analysis.closing_stock_data[ticker].sort_values(ascending= True).median()
#                     mode = Stock_returns_analysis.closing_stock_data[ticker].mode()[0]
#                     std = Stock_returns_analysis.closing_stock_data[ticker].std()
#                     plt.axvline(mean, c = "#40E0D0")#plotting a vertical line to showcase the mean
#                     plt.axvline(mode, c = "#800000")#plotting a vertival line to showcase the mode 
#                     x = np.linspace(mean-3*std, mean+3*std,100)#xaxis 
#                     y = scipy.stats.norm.pdf(x,mean,std)#yaxis
#                     plt.plot(x, y, 'r', linewidth=2, label = ticker)
#                     one_std_below, one_std_above = mean-std,mean+std
#                     two_std_below, two_std_above = mean-2*std,mean+2*std
#                     three_std_below , three_std_above = mean-3*std,mean+3*std
#                     plt.fill_between(x,y, where = ((x >= one_std_below) & (x <= one_std_above)), color='green', alpha=0.2)
#                     plt.fill_between(x,y, where= ((x >= two_std_below) & (x <= two_std_above)), color='yellow', alpha=0.2)
#                     plt.fill_between(x,y, where= ((x >= three_std_below) & (x <= three_std_above)), color='blue', alpha=0.2)
#                     plt.legend()
#                     plt.show()

        
        




        
           


 
