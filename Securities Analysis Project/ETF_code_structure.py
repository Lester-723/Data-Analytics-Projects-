
import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf




class ETF_analysis():
    closing_stock_data = pd.DataFrame()
    
   
    def __init__(self,tickers : list,start_date ,end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date 
        
           
    
    def ETF_data_extraction(self):
        yf.pdr_override()
        ETF_type = str(input(("Enter the type of ETF")))#ensure the list of tickers correspond with the ETF type
        data = {ticks : pdr.DataReader(ticks, self.start_date, self.end_date) for ticks in self.tickers}
        for ticker,df in data.items():
             df["Symbol"] = ticker
             combined_df = pd.concat(data.values())
             combined_df["Series"] = ETF_type
        return combined_df

    def to_excel_sheets(self,filename):
        self.ETF_data_extraction().to_excel(filename)
        

        
        




        
           


 
