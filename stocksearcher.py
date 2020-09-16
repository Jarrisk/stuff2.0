#Basic Stock Viewer That Pulls Data From Yahoo Finance.
#Only Uses Day-To-Day Data
#Uses Plotly For Data Visualization and Panda Data Structures

#misc
import typing
from typing_extensions import Coroutine
typing.Coroutine = Coroutine
from pyppeteer import launch
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import datetime
import time
import pdb

#pandas
import pandas as pd
from pandas_datareader import data
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
pd.core.common.is_list_like=pd.api.types.is_list_like
#plotly
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#yahoo fin 
import yahoo_fin.stock_info as yf
#csv
import csv

#Allows User Input So They Can Decide What Function To Use
def setup():
    print('-----------------------')
    print('What Do You Want To Do? (type 0-7)')
    #done
    print('0. Exit')
    #done
    print('1. Look at Most Active Stocks Of The Day')
    #done
    print('2. Look at biggest gainers/losers of the day')
    #done
    print('3. Get Quote For Company')
    #done
    print('4. Research/Compare Stock Prices')
    #done
    print('5. Get Key Stats')
    
    #tickers_dow tickers_nasdaq tickers_sp500 tickers_other 
    print('6. See Composition of Indexs')
    #
    #get_holders [current]
    print('7. Look at what institutions own particular Stock(s)')

    #get_financials() [current], get_splits, get_earnings()(might not use this) [current], get_dividends() [historical]
    #print('8. Look At Fundamentals Of One or More Businesses')
    #

    done='done'
    number=input('--------> ')

    if number=='0':
        exit()
    elif number=='1':
        mostactive()
    elif number=='2':
        gainersandlosers()
    elif number=='3':
        Symbol=[]
        loopflag=1
        while loopflag==1:
            print('Enter Stock Symbol (type "done" if done): ')
            y=input('--------> ')
            if y.lower()!=done:
                Symbol.append(y)  
                print('Received!')  
            elif y.lower()==done:
                loopflag=0       
        quote(Symbol)
    elif number=='4':
        loopflag=1
        Symbol=[]
        while loopflag==1:
            print('Enter Stock Symbol (type "done" if done): ')
            y=input('--------> ')
            if y.lower()!=done:
                Symbol.append(y)
            if y.lower()==done:
                loopflag=0

        IndexData=[None]*3
        MAString=['','']
        MAint=[0,0]
        GetData(Symbol,IndexData,MAString,MAint)
    elif number=='5':
        StockData=[]
        loopflag=1
        while loopflag==1:
            print('Enter Stock Symbol (type "done" if done): ')
            y=input('--------> ')
            if y.lower()!=done:
                StockData.append(y)
                print('Received!')  
            elif y.lower()==done:
                loopflag=0       
        Stats(StockData)
    elif number=='6':
        tickers()
    elif number=='8':
        exit()
        StockData=[]
        loopflag=1
        while loopflag==1:
            print('Enter Stock Symbol (type "done" if done): ')
            y=input('--------> ')
            if y.lower()!=done:
                StockData.append(y)  
                print('Received!')  
            elif y.lower()==done:
                loopflag=0       
        print('Type 1 To Look At Yearly Fundumentals')
        print('Type 2 To Look At Quarterly Fundumentals')
        print('Type 3 To Look At Both')
        y=input('--------> ')
        Fundumentals(x,y)
    return 

#Queries For Most Active Stocks
def mostactive():
    active=yf.get_day_most_active()
    print('---------------------------------------------Most Active------------------------------------')
    pd.set_option('display.max_rows', None)
    
    #print(active)
    print(active[['Symbol','Name','% Change','Volume','PE Ratio (TTM)']])
    return 
#Queries For Biggers Gainers and Losers On A Given Day. Can Be Resorted.
def gainersandlosers():
    print('Press 1 To Sort By % Change, 2 To Sort By Volume, 3 To Sort By PE Ratio')
    sort=input('--------> ')  
    
    gainers=yf.get_day_gainers()
    quote=[None]*len(gainers)
    losers=yf.get_day_losers()

    if sort=='1':
        gainers=gainers.sort_values(by='% Change', ascending=False)
        losers=losers.sort_values(by='% Change', ascending=True)
    elif sort=='2':
        gainers=gainers.sort_values(by='Volume', ascending=False)
        losers=losers.sort_values(by='Volume', ascending=False)
    elif sort=='3':
        gainers=gainers.sort_values(by='PE Ratio (TTM)', ascending=False)
        losers=losers.sort_values(by='PE Ratio (TTM)', ascending=False)

    pd.set_option('display.max_rows', None)
    print('------------------GAINERS------------------')
    print(gainers[['Symbol','Name','% Change','Volume','PE Ratio (TTM)']])
    print('------------------LOSERS-------------------')
    print(losers[['Symbol','Name','% Change','Volume','PE Ratio (TTM)']])
    
    loopflag=0
    while loopflag==0:
        print('Type 0 To Go To Exit and 1 For Setup')
        F=input('--------> ')
        if F=='0':
            exit()
        if F=='1':
            setup()
        
        print('Invalid Answer')
    return

#Retrieves Quote For Stock
def quote(Symbol):
    quote=[None]*len(Symbol)
    for i in range(len(Symbol)):
        x=str(Symbol[i])
        print('------------'+x+' QUOTE------------------')
        quote[i]=yf.get_quote_table(x)
        print('Quote Price: '+str(quote[i]['Quote Price'])+'\nMarket Cap: '+str(quote[i]['Market Cap'])+'\nPE Ratio (TTM): '+str(quote[i]['PE Ratio (TTM)'])+'\nEPS (TTM): '+str(quote[i]['EPS (TTM)'])+'\nDay\'s Range: '+str(quote[i]['Day\'s Range'])
        +'\n52 Week Range: '+str(quote[i]['52 Week Range'])+'\n1y Target Est: '+str(quote[i]['1y Target Est'])+'\nBeta (5Y Monthly): '+str(quote[i]['Beta (5Y Monthly)'])+'\nAverage Volume: '+str(quote[i]['Avg. Volume'])+'\nVolume: '+str(quote[i]['Volume'])
        +'\nAsk: '+str(quote[i]['Ask'])+'\nBid: '+str(quote[i]['Bid']+'\nEarnings Date: '+str(quote[i]['Earnings Date'])))
    print('----------------------------------------')
    print('Type 0 To Go To Exit and 1 For Setup')
    loopflag=0
    while loopflag==0:
        F=input('--------> ')
        if F=='0':
            exit()
        if F=='1':
            setup()
        print('Invalid Answer')
    #pdb.set_trace()
    return

#Retrieves Statistics And Graphs Them For Specified Stocks
def Stats(Symbol):
    parameter=['Market Cap (intraday)','Enterprise Value','Trailing P/E','Forward P/E','PEG Ratio (5 yr expected)',
    'Price/Sales (ttm)','Price/Book','Enterprise Value/Revenue','Enterprise Value/EBITDA']
    stockcolors=['#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2','#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2']
    StockData=[]    
    pd.set_option('display.max_columns', None)
    DateString={}

    for i in range(len(Symbol)):
        Symbol[i]=Symbol[i].upper()
        print('Retrieving Statistics Data On '+Symbol[i]+'...')
        StockData.append(yf.get_stats_valuation(Symbol[i]))
        print('Received!')
        for col in StockData[i].columns[1:]:
            if Symbol[i] in DateString:
                DateString[Symbol[i]].append(col)
            else:
                DateString[Symbol[i]]=[col[12:21]]
        
        DateString[Symbol[i]]=DateString[Symbol[i]][::-1]
        for j in range(2):
            for k in range(len(StockData[i].iloc[0])-1):
                number=StockData[i].iloc[j][k+1]
                if isinstance(number,str)==True:
                    for letter in number:
                        if letter=='B' or letter=='M' or letter=='T' or letter=='k':
                            StockData[i].iloc[j][k+1]=number.replace(letter,'')
                            StockData[i].iloc[j][k+1]=float(StockData[i].iloc[j][k+1])
                            if letter=='B':
                                StockData[i].iloc[j][k+1]=(StockData[i].iloc[j][k+1])*1e9
                            elif letter=='M':
                                StockData[i].iloc[j][k+1]=(StockData[i].iloc[j][k+1])*1e6
                            elif letter=='T':
                                StockData[i].iloc[j][k+1]=(StockData[i].iloc[j][k+1])*1e12
                            elif letter=='k':
                                StockData[i].iloc[j][k+1]=(StockData[i].iloc[j][k+1])*1e3   
                    StockData[i].iloc[j][k+1]=float(StockData[i].iloc[j][k+1])
               
                    
                     
    for i in range(len(Symbol)):
        fig = make_subplots(rows=9, cols=1)
        for j in range(len(parameter)):
                fig.add_trace(go.Scatter(x=DateString[Symbol[i]], 
                    y=StockData[i].loc[j][::-1],
                    name=parameter[j],
                    line=dict(color=stockcolors[j])), 
                    row=j+1,
                    col=1)
                fig.update_layout(
                title=Symbol[i]+' Stats Over ~5 Quarters (Up To Present Period of Current Quarter)',
                legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=2.5),
                paper_bgcolor='rgba(189, 195, 199, 1)',
                plot_bgcolor='rgba(189, 195, 199, 1)',
                #xaxis_title="X Axis Title",
                #yaxis_title="X Axis Title",
                #legend_title="Legend Title",
                #xaxis_title="X Axis Title",
                #yaxis_title="X Axis Title",
                #legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=12,
                color="#87693A"))
        
                
                
        fig.show()
    loopflag=0
    string=['yes','y','n','no']
    while loopflag==0:
        print('Do You Want To See The Stock Charts For These Companies? (y/n)')
        y=input('--------> ')
        if y.lower()==string[0] or y.lower()==string[1]:
            IndexData=[None]*3
            MAString=['','']
            MAint=[0,0]
            GetData(Symbol,IndexData,MAString,MAint)
        elif y.lower()==string[2] or y.loiwer()==string[3]:
            setup()

    return

#Returns List of Tickers On The 3 Main Indexs
def tickers():
    loopflag=0
    while loopflag==0:
        print('Which Index Composition Do You Want To View? (type 0-4)\n1. DOW JONES\n2. NASDAQ\n3. S&P 500\n4. View All')
        tickerinput=input('--------> ')
        if tickerinput=='1':
            dow=yf.tickers_dow()
            print('--------------------DOW JONES--------------------')
            print(dow)
            loopflag=1
        elif tickerinput=='2':
            print('--------------------NASDAQ--------------------')
            nasdaq=yf.tickers_nasdaq()
            print(nasdaq)
            loopflag=1
        elif tickerinput=='3':
            print('--------------------S&P 500--------------------')
            sandp=yf.tickers_sp500()
            print(sandp)
            loopflag=1
        elif tickerinput=='4':
            print('--------------------DOW JONES--------------------')
            dow=yf.tickers_dow()
            print(dow)
            print('--------------------NASDAQ--------------------')
            nasdaq=yf.tickers_nasdaq()
            print(nasdaq)
            print('--------------------S&P 500--------------------')
            sandp=yf.tickers_sp500()
            print(sandp)
            loopflag=1
        else: 
            print('Invalid Input')
    print(type(nasdaq))
    loopflag=0
    while loopflag==0:
        print('What Would You Like To Do Next? (Type 1-3)')
        print('1. Save Composition To CSV\n2. Save Quote Information For Tickers On Index To CSV\n3. Exit')
        IndexNextStep=input('--------> ')
        if IndexNextStep=='1':  
            if tickerinput=='1':
                savefilename='DowJonesIndexComp.csv'
                file = open(savefilename, 'w+', newline ='') 
                with file:     
                    write = csv.writer(file) 
                    write.writerows([dow])
                loopflag=1
            elif tickerinput=='2':
                savefilename='NASDAQOIndexComp.csv'
                file = open(savefilename, 'w+', newline ='') 
                with file:     
                    write = csv.writer(file) 
                    write.writerows([nasdaq]) 
                loopflag=1
            elif tickerinput=='3':
                savefilename='SP500IndexComp.csv'
                file = open(savefilename, 'w+', newline ='') 
                with file:     
                    write = csv.writer(file) 
                    write.writerows([sandp]) 
                loopflag=1
            elif tickerinput=='4':              
                savefilename='DowJonesIndexComp.csv'
                file = open(savefilename, 'w+', newline ='') 
                with file:     
                    write = csv.writer(file) 
                    write.writerows([dow])
                loopflag=1
                savefilename2='NASDAQIndexComp.csv'
                file = open(savefilename2, 'w+', newline ='')
                with file:     
                    write = csv.writer(file) 
                    write.writerows([nasdaq])
                loopflag=1
                
                savefilename3='SP500IndexComp.csv'
                file = open(savefilename3, 'w+', newline ='')
                with file:     
                    write = csv.writer(file) 
                    write.writerows([sandp])
                    
#Retrieves Data For Stock Researcher, Allows User To Decided Which Stocks/Rolling Averages
#To Use
def GetData(Symbol,IndexData,MAString,MAint):
    StockData=[]
    loopflag=1
    
    while loopflag==1:
        date_string=['','']
        datestring_inp=['Enter the earliest date you want to view data from (YYYY-MM-DD): ','Enter the latest date you want to view data from (YYYY-MM-DD): ']
        for i in range(len(datestring_inp)):
            print(datestring_inp[i])
            date_string[i]=input('--------> ')
            while loopflag==1:
                if len(date_string[i])!=10:
                    print('Invalid date format, should be YYYY-MM-DD.\n'+datestring_inp[i])
                    #date_string[i]=input('--------> ')
                else:
                    loopflag=0
            try:
                date0=datetime.datetime.strptime(date_string[i], '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format, should be YYYY-MM-DD.")
        
        
        
    for i in range(len(Symbol)):
        Symbol[i]=Symbol[i].upper()
        print('Retrieving Stock Data On '+Symbol[i]+'...')
        StockData.append(data.get_data_yahoo(Symbol[i],date_string[0],date_string[1]))
        print('Received!')

    
    
    IndexString=['^DJI','^IXIC','^GSPC']
    for i in range(len(IndexData)):
        print('...')
        IndexData[i]= data.get_data_yahoo(IndexString[i],date_string[0],date_string[1])
        
    
    print('What Do You Want To Plot? (Enter 1-6 To Select Option)\n1.High\n2.Low\n3.Open\n4.Close\n5.Volume\n6.Adj Close')
    while loopflag==0:
        
        selectedparameter=input('--------> ')
        
        if selectedparameter!='1' and selectedparameter!='2' and selectedparameter!='3' and selectedparameter!='4' and selectedparameter!='5' and selectedparameter!='6':
            print('Invalid Input. Type 1-6 To Select Option.')
        elif selectedparameter=='1':
            selectedparameter='High'
            loopflag=1
        elif selectedparameter=='2':
            selectedparameter='Low'
            loopflag=1
        elif selectedparameter=='3':
            selectedparameter='Open'
            loopflag=1
        elif selectedparameter=='4':
            selectedparameter='Close'
            loopflag=1
        elif selectedparameter=='5':
            selectedparameter='Volume'
            loopflag=1
        elif selectedparameter=='6':
            selectedparameter='Adj Close'
            loopflag=1
        
    while loopflag==1:
        print('Do You Want Custom Moving Averages (automatically set to 50 and 100 day if no)? (type either y/n)')
        MAOption0=input('--------> ') 
        MAStringArray=['y','yes','n','no']
        if MAOption0.lower()==MAStringArray[0] or MAOption0.lower()==MAStringArray[1]:
            print('Select # Of Days For 1st MA')
            MAOption1=input('--------> ')
            print('Select # Of Days For 2nd MA')
            MAOption2=input('--------> ')
            MAint=[int(MAOption1),int(MAOption2)]
            MAString=[MAOption1+' day MA ',MAOption2+' day MA ']
            loopflag=0
        elif MAOption0.lower()==MAStringArray[2] or MAOption0.lower()==MAStringArray[3]:
            MAOption1='50'
            MAOption2='100'
            MAint=[int(MAOption1),int(MAOption2)]
            MAString=[MAOption1+' day MA ',MAOption2+' day MA ']
            loopflag=0
        else:
            print('Invalid Response, Try Again')
    return PlotData(StockData,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)  

#Callback Function For GetData To Plot Retrieved Data
def PlotData(Stocks,IndexData,Symbol,parameter,MAString,MAint,date_string):
    stockcolors=['#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2','#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2''#60669F','#996672','#8CB54A','#34CB92','#FF0015','#1A8283','#8CCF30','#629D63','#7C3AC5','#694DB2']
    MA1colors=['#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269','#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269''#669F60','#25DA30','#4A8CB5','#9234CB','#0015FF','#82831A','#CF308C','#9D6362','#C57C3A','#4DB269']
    MA2colors=['#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D','#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D''#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D','#9F6066','#DA3025','#B54A8C','#E91627','#15FF00','#831A82','#308CCF','#63629D','#3AC57C','#B2694D']
    indexcolors=['#847E7B','#9E9061','#816C93']
    indexma1colors=['#D22D38','#DB3D24','#e817bc']
    indexma2colors=['#30CFBF','#3D24DB','#27D867']
    
    for i in range(len(Symbol)):
        Stocks[i][MAString[0]] = Stocks[i][parameter].rolling(MAint[0]).mean()
        Stocks[i][MAString[1]] = Stocks[i][parameter].rolling(MAint[1]).mean()

    IndexString=['Dow Jones Industrial Average ','NASDAQ ','S&P 500 ']
    
    for i in range(len(IndexString)):
        IndexData[i][MAString[0]] = IndexData[i][parameter].rolling(MAint[0]).mean()
        IndexData[i][MAString[1]] = IndexData[i][parameter].rolling(MAint[1]).mean()
    
    print('Type "1" To Not see MA, "2" to see only see '+MAString[0]+', "3" to see '+MAString[1]+', and "4" to see both')
    loopflag=1
    while loopflag==1:
        MA=input('--------> ')
        if MA!='1' and MA!='2' and MA!='3' and MA!='4':
            print('Please Try Again')
        else:
            loopflag=0 
    while loopflag==0:
        if len(Stocks)>1:
            if len(Stocks)>3:
                fig = make_subplots(rows=len(Stocks), cols=2)
            else:
                fig = make_subplots(rows=3, cols=2)
            
            for i in range(len(Stocks)):
                fig.add_trace(go.Scatter(x=Stocks[i].index, 
                    y=Stocks[i][parameter],
                    name=Symbol[i]+' Stock\'s '+parameter+' from '+date_string[0]+' to '+date_string[1],
                    line=dict(color=stockcolors[i])), 
                    row=i+1,
                    col=1)
                if MA=='3' or MA=='4':
                    fig.add_trace(go.Scatter(x=Stocks[i].index,y=Stocks[i][MAString[0]],name=MAString[0]+'of the '+parameter+' of '+Symbol[i]+' Stock from '+date_string[0]+' to '+date_string[1], line=dict(color=MA1colors[i], width=.5)),row=i+1,col=1)
                if MA=='2' or MA=='4':
                    fig.add_trace(go.Scatter(x=Stocks[i].index,y=Stocks[i][MAString[1]],name=MAString[1]+'of the '+parameter+' of '+Symbol[i]+' Stock from '+date_string[0]+' to '+date_string[1],line=dict(color=MA2colors[i], width=.5)),row=i+1,col=1)
            
            for i in range(len(IndexData)):
                fig.append_trace(go.Scatter(x=IndexData[i].index,
                    y=IndexData[i][parameter],
                    name=IndexString[i]+' '+parameter+' from '+date_string[0]+' to '+date_string[1],
                    line=dict(color=indexcolors[i])),
                    row=i+1,
                    col=2)
                if MA=='3' or MA=='4':
                    fig.add_trace(go.Scatter(x=IndexData[i].index,y=IndexData[i][MAString[0]],name=MAString[0]+'of the '+parameter+' of '+IndexString[i]+' from '+date_string[0]+' to '+date_string[1], line=dict(color=indexma1colors[i], width=.5)),row=i+1,col=2)
                if MA=='2' or MA=='4':
                    fig.add_trace(go.Scatter(x=IndexData[i].index,y=IndexData[i][MAString[1]],name=MAString[1]+'of the '+parameter+' of '+IndexString[i]+' from '+date_string[0]+' to '+date_string[1],line=dict(color=indexma2colors[i], width=.5)),row=i+1,col=2)
        else:
            sstring=str(Symbol)[2:-2]
            
            fig = make_subplots(rows=3, cols=2)
            fig.add_trace(go.Scatter(x=Stocks[0].index, y=Stocks[0][parameter], 
                name=sstring+' Stock\'s '+parameter+' from '+date_string[0]+' to '+date_string[1],line=dict(color=indexcolors[i])),row=1,col=1)
            if MA=='3' or MA=='4':
                fig.add_trace(go.Scatter(x=Stocks[0].index,y=Stocks[0][MAString[0]],name=MAString[0]+'for the'+parameter+' of '+sstring+' Stock from '+date_string[0]+' to '+date_string[1], line=dict(color=indexma1colors[i], width=.5)),row=1,col=1)
            if MA=='2' or MA=='4':
                fig.add_trace(go.Scatter(x=Stocks[0].index,y=Stocks[0][MAString[1]],name=MAString[1]+'for the'+parameter+' of '+sstring+' Stock from '+date_string[0]+' to '+date_string[1],line=dict(color=indexma2colors[i], width=.5)),row=1,col=1)
            
            for i in range(len(IndexData)):
                fig.append_trace(go.Scatter(x=IndexData[i].index,
                    y=IndexData[i][parameter],
                    name=parameter+' of '+IndexString[i]+'Over Time',
                    line=dict(color=indexcolors[i])),
                    row=i+1,
                    col=2)
                if MA=='3' or MA=='4':
                    fig.add_trace(go.Scatter(x=IndexData[i].index,y=IndexData[i][MAString[0]],name=MAString[0]+'of the '+parameter+' of '+IndexString[i]+' from '+date_string[0]+' to '+date_string[1], line=dict(color='orange', width=.5)),row=i+1,col=2)
                if MA=='2' or MA=='4':
                    fig.add_trace(go.Scatter(x=IndexData[i].index,y=IndexData[i][MAString[1]],name=MAString[1]+'of the '+parameter+' of '+IndexString[i]+' from '+date_string[0]+' to '+date_string[1],line=dict(color='green', width=.5)),row=i+1,col=2)
        titlestring=date_string[0]+' to '+date_string[1]+' '+parameter+' of '
        print(titlestring)
        symbolstring=[]
        for i in range(len(Symbol)):
            num=str(i+1)
            #pdb.set_trace()
            symbolstring.append(Symbol[i])
        
        print(symbolstring)
        symbolstring=str(symbolstring)[1:-1]
        

        print(symbolstring)
        titlestring=titlestring+symbolstring
        #fig.layout = Layout(
        #   
        #    
        #)
        fig.update_layout(title=titlestring,
                legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="right",
                x=2.5),
                paper_bgcolor='rgba(189, 195, 199, 1)',
                plot_bgcolor='rgba(189, 195, 199, 1)',
                #xaxis_title="X Axis Title",
                #yaxis_title="X Axis Title",
                #legend_title="Legend Title",
                font=dict(
                family="Courier New, monospace",
                size=12,
                color="#87693A"))
        
        fig.show()
        
        loopflag2=1
        loopflag3=0
        diffstatsanswerstring=['y','yes','n','no']
        while loopflag2==1:
            print('Want to see different stock numbers (opening/close/etc) for the same ticker(s)? (y/n): ')
            yesno=input('--------> ')
            if diffstatsanswerstring[0]==yesno.lower() or diffstatsanswerstring[1]==yesno.lower():
                while loopflag3==0:
                    print('What Do You Want To Plot? (Enter 1-6 To Select Option)\n1.High\n2.Low\n3.Open\n4.Close\n5.Volume\n6.Adj Close')
                    selectedparameter=input('--------> ')
                    if selectedparameter!='1' and selectedparameter!='2' and selectedparameter!='3' and selectedparameter!='4' and selectedparameter!='5' and selectedparameter!='6':
                        print('Invalid text format or wrong entry. Try Again.')
                    elif selectedparameter=='1':
                        selectedparameter='High'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1    
                    elif selectedparameter=='2':
                        selectedparameter='Low'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1
                    elif selectedparameter=='3':
                        selectedparameter='Open'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1
                    elif selectedparameter=='4':
                        selectedparameter='Close'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1
                    elif selectedparameter=='5':
                        selectedparameter='Volume'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1
                    elif selectedparameter=='6':
                        selectedparameter='Adj Close'
                        PlotData(Stocks,IndexData,Symbol,selectedparameter,MAString,MAint,date_string)
                        loopflag=1
            elif diffstatsanswerstring[2]==yesno.lower() or diffstatsanswerstring[3]==yesno.lower():
                loopflag2=0
            else:
                print('Invalid Input.')
        
            
        loopflag=1
    return setup()    

setup()