#Basic Stock Viewer That Pulls Data From Yahoo Finance.
#Only Uses Day-To-Day Data
#Uses Plotly For Data Visualization and Panda Data Structures

#time
import time

#pandas
import pandas as pd
from pandas_datareader import data
from pandas.plotting import register_matplotlib_converters

#plotly
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots

register_matplotlib_converters()
pd.core.common.is_list_like=pd.api.types.is_list_like

def setup():
    print('Enter the earliest date you want to view data from (YYYY-MM-DD): ')
    date_string_past=input('--------> ')
    loopflag=0
    while loopflag==0:
        if len(date_string_past)!=10:
            print('Invalid date format!')
            print('Enter the earliest date you want to view data from (YYYY-MM-DD): ')
            date_string_past=input('--------> ')
        else:
            loopflag=1

    print('Enter the latest date you want to view data from (YYYY-MM-DD): ')
    date_string_present=input('--------> ')
    loopflag=0

    while loopflag==0:
        if len(date_string_present)!=10:
            print('Invalid date format!')
            print('Enter the latest date you want to view data from (YYYY-MM-DD): ')
            date_string_present=input('--------> ')
        else:
            loopflag=1

    number_of_stocks=int(input('How many stocks do you want to look at? '))
    ticker=[None]*number_of_stocks
    StockData=[None]*number_of_stocks
    return GetData(ticker,date_string_past,date_string_present,StockData)

def GetData(x,date1,date2,StockData):
    
    for i in range(len(x)):
        x[i]=input('Enter '+str(i+1)+' Stock Symbol: ')
        print('Retrieving Stock Data On '+x[i]+'...')

        #start = time.time()
        StockData[i]= data.get_data_yahoo(x[i],date1,date2)
        #done = time.time()
        #elapsed = done - start
        #print(elapsed)

        print('Received!')

    bigbussy=['High','high','Low','Open','Close','Volume','Adj Close']
    
    loopflag=0
    while loopflag==0:
        print('Type either High/Low/Open/Close/Volume/Adj Close To See Specific Stock Movement')
        selectedbussy=input('--------> ')
        
        if selectedbussy!='High' and selectedbussy!='high' and selectedbussy!='HIGH' and selectedbussy!='Close' and selectedbussy!='close' and selectedbussy!='CLOSE' and selectedbussy!='Volume' and selectedbussy!='volume' and selectedbussy!='vol' and selectedbussy!='VOL' and selectedbussy!='Vol' and selectedbussy!='Vol.' and selectedbussy!='Adj Close' and selectedbussy!='adj close' and selectedbussy!='Adj close' and selectedbussy!='adj Close' and selectedbussy!='ADJ CLOSE' and selectedbussy!='Low' and selectedbussy!='LOW' and selectedbussy!='low' and selectedbussy!='OPEN' and selectedbussy!='Open' and selectedbussy!='open':
            print('Invalid text format or wrong entry. Try Again.')
        
        elif selectedbussy=='high' or selectedbussy=='HIGH':
            selectedbussy='High'
            loopflag=1

        if selectedbussy=='close' or selectedbussy=='CLOSE':
            print(selectedbussy)
            selectedbussy='Close'
            print(selectedbussy)
            loopflag=1

        elif selectedbussy=='volume' or selectedbussy=='vol' or selectedbussy=='VOL' or selectedbussy=='Vol' or selectedbussy=='Vol.':
            selectedbussy='Volume'
            loopflag=1

        elif selectedbussy=='adj close' or selectedbussy=='Adj close' or selectedbussy=='adj Close' or selectedbussy=='ADJ CLOSE':
            selectedbussy='Adj Close'
            loopflag=1
        elif selectedbussy=='OPEN' or selectedbussy=='open':
            selectedbussy='Open'
            loopflag=1
        elif selectedbussy=='LOW' or selectedbussy=='low':
            selectedbussy='Low'
            loopflag=1

        
    for i in range(len(bigbussy)):
        if bigbussy[i]==selectedbussy:
            parameter=bigbussy[i]

    sandp=data.get_data_yahoo('^GSPC',date1,date2)
    dji=data.get_data_yahoo('^DJI',date1,date2)
    nasdaq=data.get_data_yahoo('^IXIC',date1,date2)

    return PlotData(StockData,sandp,dji,nasdaq,x,parameter)  

def PlotData(Stocks,sandp,dji,nasdaq,Symbol,parameter):
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
                    name=parameter+' of '+Symbol[i]+' Stock Over Time'), 
                    row=i+1, 
                    col=1)
            fig.append_trace(go.Scatter(x=sandp.index,
                y=sandp[parameter],
                name=parameter+' of S&P 500 Over Time'),
                row=1,
                col=2)
            fig.append_trace(go.Scatter(x=dji.index,
                y=sandp[parameter],
                name=parameter+' of Dow Jones Industrial Average Over Time'),
                row=2,
                col=2)    
            fig.append_trace(go.Scatter(x=nasdaq.index,
                y=nasdaq[parameter],
                name=parameter+' of Nasdaq Average Over Time'),
                row=3,
                col=2)
        else:
            sstring=str(Symbol)[2:-2]
            print(Stocks)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=Stocks[0].index, y=Stocks[0][parameter], 
                name=parameter+' of '+sstring+' Stock Over Time'))
        fig.show()
        print('input new option? (y/n): ')
        loopflag2=1
        loopflag3=0
        while loopflag2==1:
            yesno=input('--------> ')
            if yesno=='y' or yesno=='Y' or yesno=='Yes' or yesno=='yes' or yesno=='YES':
                while loopflag3==0:
                    print('Type either High/Low/Open/Close/Volume/Adj Close (case sensitive) Close To See Specific Stock Movement')
                    parameter=input('--------> ')
                    
                    if  parameter!='High' and parameter!='high' and parameter!='HIGH' and parameter!='Close' and parameter!='close' and parameter!='CLOSE' and parameter!='Volume' and parameter!='volume' and parameter!='vol' and parameter!='VOL' and parameter!='Vol' and parameter!='Vol.' and parameter!='Adj Close' and parameter!='adj close' and parameter!='Adj close' and parameter!='adj Close' and parameter!='ADJ CLOSE' and parameter!='Low' and parameter!='LOW' and parameter!='low' and parameter!='OPEN' and parameter!='Open' and parameter!='open':
                        print('Invalid text format or wrong entry. Try Again.')
                    if parameter=='high' or parameter=='HIGH':
                        selectedbussy='High'
                        loopflag2=0
                        loopflag3=1
                    elif parameter=='close' or parameter=='CLOSE':
                        parameter='Close'
                        loopflag2=0
                        loopflag3=1
                    elif parameter=='volume' or parameter=='vol' or parameter=='VOL' or parameter=='Vol' or parameter=='Vol.':
                        parameter='Volume'
                        loopflag2=0
                        loopflag3=1
                    elif parameter=='adj close' or parameter=='Adj close' or parameter=='adj Close' or parameter=='ADJ CLOSE':
                        parameter='Adj Close'
                        loopflag2=0
                        loopflag3=1
                    elif parameter=='OPEN' or parameter=='open':
                        parameter='Open'
                        loopflag2=0
                        loopflag3=1
                    elif parameter=='LOW' or parameter=='low':
                        parameter='Low'
                        loopflag2=0
                        loopflag3=1 

            elif yesno=='n' or yesno=='n' or yesno=='No' or yesno=='no' or yesno=='NO':
                loopflag2=0
        
        print('Do you want to view a new batch of stocks? (y/n)')
        while loopflag2==0:
            yesno=input('--------> ')
            if yesno=='y' or yesno=='Y' or yesno=='Yes' or yesno=='yes' or yesno=='YES':
                setup()
                loopflag2=1
            elif yesno=='n' or yesno=='n' or yesno=='No' or yesno=='no' or yesno=='NO':
                print('Goodbye')
                loopflag2=1
                loopflag=1
                
            else:
                print('Wrong Character Input. Please Try Again')
setup()
