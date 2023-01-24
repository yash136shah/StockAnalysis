import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import datetime
import os
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px 
from load_data_2 import load_data_All
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide")







# VARIABLE INITIALIZED 
sector = 'SECTOR'
industry = "INDUSTRY"
coName = "NAME"
year = "YEAR"
marketCap='MARKET CAPITALIZATION'
updatedTicker="YF TICKER"
Date ="DATE"
roic = 'ROIC'
revenue = 'TOTAL REVENUE'
rev_type = "TOTAL REVENUE"
fcf = 'FREE CASH FLOW'
gm = 'Gross Profit Margin'
ebitda_m = 'EBITDA Margin'
npm = 'Net Profit Margin'
assets = "TOTAL ASSETS"
cfo = "TOTAL CASH FROM OPERATING ACTIVITIES"
d_e = 'D/E'
c_r = 'C/R'
pe = 'TRAILINGPE'
pcf = 'PEG RATIO'
st1 = "IS"
st2 = "CF"
st3 = "Ratio "
st4 = "Ratio "
IS = "IS"
BS = "BS"
CF = "CF"
OT = "Ratio"

markets = ["USA","Canada","India"]


#MARKET SELECT 
if "marketSelect" not in st.session_state:
    st.session_state["marketSelect"] = markets[2]
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelect"])




if st.session_state["marketSelect"] == "USA":
        benchmark = "SPY"
        descriptive_screener = ["EXCHANGE"]
        dfC,dfF,multidfC,dfQ,dfM,dfT,dfSH,dfOff,dfEA,dfEH,dfET,gridOptions = load_data_All(country="US")
 

elif st.session_state["marketSelect"] == "India":
        benchmark = '^NSEI'
        descriptive_screener = []
        dfC,dfF,multidfC,dfQ,dfM,dfT,dfSH,dfOff,dfEA,dfEH,dfET,gridOptions = load_data_All(country="IND")


elif st.session_state["marketSelect"] == "Canada":
        benchmark = '^GSPTSE'
        descriptive_screener=[]
        dfC,dfF,multidfC,dfQ,dfM,dfT,dfSH,dfOff,dfEA,dfEH,dfET,gridOptions = load_data_All(country="CAN")
        



name_uni = dfC.sort_values(by=marketCap,ascending=False)[coName].dropna().unique()
name_list = []
for i in name_uni:
    name_list.append(i)

if "name_selected" not in st.session_state:
    st.session_state["name_selected"] = name_list[0]

if "name_selected_technical" not in st.session_state:
    st.session_state["name_selected_techncial"] = dfC[coName].unique()[0]


col1,col2 = st.columns([10,2])

with col1:
    st.header("TECHNICAL ANALYSIS")

with col2:
    homePage = st.button("Home")
    
    if homePage:
        st.session_state["name_selected"]=st.session_state["name_selected_technical"] 
        switch_page("stockAnalysis-2")
    
    if st.button("Fundamental Analysis"):
        st.session_state["name_selected"]=st.session_state["name_selected_technical"] 
        switch_page("Fundamental Analysis")
    
    if st.button("Industry Overview"):
        st.session_state["name_selected"]=st.session_state["name_selected_technical"] 
        switch_page("Industry Overview")


defaultName = []
try:
    if len(st.session_state["nameSel"])>0:
        defaultName = st.session_state["nameSel"]
        
except:
    try:
        if len(st.session_state["nameSelFundamental"])>0:
            defaultName = st.session_state["nameSelFundamental"]
        
    except:  
        defaultName=st.session_state["name_selected"]
        


st.session_state["name_selected_technical"] = st.multiselect("Company Name:",name_list,key="nameSelTechnical",default=defaultName)
 
if st.button("Change Peer Selection"):
    switch_page("stockAnalysis-2")


if len(st.session_state["name_selected_technical"]) == 0:
    st.warning("Select Companies to see Analysis!")
    st.stop()



# ENTER DATE
dtcol1,dtcol2 = st.columns(2)

with dtcol1:
    sd = st.date_input(
        "Enter Start Date",
        datetime.date(2010, 1, 1),min_value=datetime.date(1980, 1, 1),max_value=datetime.date(2025,1,1))

with dtcol2:
    ed = st.date_input("Enter End Date",
        datetime.date.today(),min_value=datetime.date(1980, 1, 1),max_value=datetime.date(2025,1,1))



if ed<sd:
    st.warning("End Date can not be before Start Date")
    st.stop()


#Close Type
close_type = st.radio("Close type:",("Close","Adj Close"),horizontal=True)

if close_type =="Close":
    closeType = "Close"
else:
    closeType = "Adj Close"


# Get Historical Data from YahooFinance


@st.cache(allow_output_mutation=True)
def ytickData(nameSel):
    ticker_selected=dfC[dfC[coName].isin(nameSel)].loc[:,updatedTicker].to_list()
    ticker_data = yf.download(ticker_selected,start=sd,end=ed)
    colname = {}
    if len(ticker_selected) == 1:
        tickdata=ticker_data[closeType].to_frame()
        vol_data = ticker_data['Volume'].to_frame()
        colname[ticker_selected[0]]= st.session_state["name_selected_technical"][0]

    else:
        tickdata=ticker_data[closeType]
        vol_data = ticker_data['Volume']
        for t in tickdata:
            colname[t]=' '.join(dfC[dfC[updatedTicker]==t][coName].to_list())

    tickdata.rename(columns=colname,inplace=True)
    vol_data.rename(columns=colname,inplace=True)

    return ticker_data,ticker_selected,tickdata,vol_data

ticker_data,ticker_selected,tickdata,vol_data=ytickData(st.session_state["name_selected_technical"])



# Price and Indexed Chart 
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9 = st.tabs(['Price','Indexed',"Relative Strength","RSI-Analysis","EMA-Analysis","Technical Rating","Perfromance","HEATMAP","Option-Analysis"])



#Plotting Price 
with tab1:
    fig = make_subplots(rows=2,cols=1,row_heights=[0.7, 0.3],shared_xaxes=True,vertical_spacing=0)

    #fig.add_scatter(y=plot_ps.columns, row=1, col=1)
    colors = px.colors.qualitative.Dark24
    for k,col in enumerate(tickdata):
        
        fig.add_trace(go.Scatter(x=tickdata.index,y=tickdata[col],name=col,legendgroup = col,line=dict(width=2, color=colors[k])),secondary_y = False,row=1, col=1)
        
    for k,col in enumerate(vol_data):
        fig.add_trace(go.Scatter(x=vol_data.index,y=vol_data[col],name=col,legendgroup = col,showlegend=False,line=dict(width=2, color=colors[k])),secondary_y = False,row=2, col=1)

        
    fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,row=1)
    fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,title="Date",row=2,matches="x1")
    fig.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="Price",row=1,col=1)
    fig.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="Volume",row=2)
    fig.update_layout(spikedistance=1000, hoverdistance=10,title="Price-Volume CHART",height=600)
    fig.update_traces(xaxis="x2")
    
    st.plotly_chart(fig,use_container_width=True)



# Plotting Volume 
with tab2:
    col1,col2 = st.columns(2)
    indexData = tickdata.copy()
    
    with col1:
        dtFreq = st.radio("Date Frequency:",("Quarterly","Monthly","Weekly","Daily"),index=1,horizontal=True)
        #indexData.index.resample("M")#strftime("%Y-%m") #tickdata.index.date

        if dtFreq == "Quarterly":
            indexMData=indexData.resample("Q").mean()

        elif dtFreq == "Monthly":
            indexMData=indexData.resample("M").mean()

        elif dtFreq == "Weekly":
            indexMData=indexData.resample("W").mean()

        else:
            indexMData = indexData

        date_list = indexMData.index.date

    with col2:
        if dtFreq == "Daily":
            per_type = st.radio("Period:",("1d","1w","1m","3m","6m","12m","Choose your own Period"),index=6,horizontal=True,key="indexPerType")
        else:
            per_type = "Choose your own Period"
            

    if per_type == "Choose your own Period":
        ds,de = st.select_slider("Date Range:",options=date_list,value=(date_list[0],date_list[-1]),key="indexCP")

    else:
        de = date_list[-1]

        if per_type == "1d":
            ds = date_list[-2]

        elif per_type == "1w":
            ds = date_list[-5]

        elif per_type == "1m":
            ds = date_list[-20]


        elif per_type == "3m":
            ds = date_list[-60]

        elif per_type == "6m":
            ds = date_list[-120]

        elif per_type == "12m":
            ds = date_list[-240]


    def Indexed_Price():
        try:
            idx_close = indexMData.loc[ds:de].reset_index()
        
        except:
            idx_close = indexMData.loc[ds:de].to_frame().reset_index()

        index = idx_close.assign(**idx_close.drop('Date',axis=1).pipe(
    lambda d: d.div(d.shift().bfill()).cumprod().mul(100)))
        
        indexed = index.set_index('Date')
        return indexed
    

    indexed = Indexed_Price()    

    fig1 = px.line(indexed,title=f"Indexed Chart",height=600)
    

    fig1.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,title="Date")
    fig1.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="Price")
    st.plotly_chart(fig1,use_container_width=True)
      
                
        
with tab3:
    if st.session_state["marketSelect"] == "USA":
        col1,col2 = st.columns([3,13])
        with col1:
             benchmark = st.selectbox("Select Benchmark:",options=['SPY','XLE','XLY','XLI','XLF','XLU','XLV','XLP','XLC','XLB','XLRE','XLK'],index=0)
    
    
    def benchmarkData():
        benchmark_data = yf.download(benchmark,start=sd,end=ed)
        bd=benchmark_data[closeType].to_frame()
        bd.rename(columns={bd.columns[0]:benchmark},inplace=True)
        rsdb=pd.concat([ticker_data[closeType],bd],axis=1)
        
        colname = {}
        for t in rsdb:
                if t == benchmark:
                    colname[t] = benchmark
                else:
                    colname[t]=' '.join(dfC[dfC[updatedTicker]==t][coName].to_list())
                
        rsdb.rename(columns=colname,inplace=True)
        return rsdb
    
    rsdb = benchmarkData()


    dtFreq = st.radio("Date Frequency:",("Quarterly","Monthly","Weekly","Daily"),index=1,horizontal=True,key="RSdtFreq")
   
    if dtFreq == "Quarterly":
        rsdbDtF=rsdb.resample("Q").mean()
    
    elif dtFreq == "Monthly":
        rsdbDtF=rsdb.resample("M").mean()
    
    elif dtFreq == "Weekly":
        rsdbDtF=rsdb.resample("W").mean()
    
    else:
        rsdbDtF = indexData
        
    date_list = rsdbDtF.index.date

    ds,de = st.select_slider("Date Range:",options=date_list,value=(date_list[0],date_list[-1]),key="rsdatesli")




    
    def Indexed_Price_RS():
            try:
                adj_close = rsdbDtF.loc[ds:de].reset_index()
            
            except:
                adj_close = rsdbDtF.loc[ds:de].to_frame().reset_index()

            index = adj_close.assign(**adj_close.drop('Date',axis=1).pipe(
        lambda d: d.div(d.shift().bfill()).cumprod().mul(100)))
            
            indexed = index.set_index('Date')
            return indexed
     
    indexedRS=Indexed_Price_RS()


    
    def RS():
        rs = pd.DataFrame()
        for i in range(len(indexedRS.columns)):
            rs[indexedRS.columns[i]] = indexedRS.iloc[:,i]/indexedRS.loc[:,benchmark]
        
        fig = px.line(rs,x=rs.index,y=rs.columns,color_discrete_map={benchmark:"black"},height=600)
        return fig
        
    fig = RS()
    st.plotly_chart(fig,use_container_width=True)    



with tab4:
        def RSI_current_levels():   
            from ta.momentum import rsi

            RSI_S = {} 
            try:
                for i in ticker_data[closeType]:
                        RSI_S[i]=rsi(ticker_data[closeType].loc[:,i],window=14,fillna=False)
            except:
                tick = " "
                for t in ticker_selected:
                    tick = t
                RSI_S[tick]=rsi(ticker_data[closeType],window=14,fillna=False)

            rsipdf = pd.DataFrame.from_dict(RSI_S)

            with st.expander("RSI Current Levels"):
                    st.write(rsipdf.iloc[-1])

        RSI_current_levels()

        # RSI BACKTEST
        rsi_name = st.selectbox("Select Company:",st.session_state["name_selected_technical"],index=0)
        ticker_selected_rsi=dfC[dfC[coName]==rsi_name].loc[:,updatedTicker].to_list()
        ticker_data_rsi = yf.download(ticker_selected_rsi,start=sd,end=ed)
        ticker_sel  = ticker_selected_rsi

        col1,col2 = st.columns(2)

        with col1:
            ob = st.slider("Overbought Levels:",50,100,70)

        with col2:
            os = st.slider("Oversold Levels:",0,50,30)

        st.write("PERFROMANCE SUMMARY")

        def close_price(): 
            global close 
            close = pd.DataFrame()
            close = ticker_data_rsi[closeType]
            return close

        class RSI:

            def table():
                global rsitable
                from ta.momentum import rsi
                global ticker_data_rsi
                global rsidf,RSI_S
                rsitable =rsi(ticker_data_rsi[closeType],window=14,fillna=False)
                rsitable.dropna(inplace=True)
                rsidf = rsitable.to_frame()
                

            
            
            
            def signal():
                global rsidf
                global signalBuy
                global signalSell
                global rsi_signal  
                global ticker_sel
                close_price()
                RSI.table()

                

                signalBuy = []
                signalSell = []
                position = False
                crossingBelowOs = False
                crossingAboveOb = False

                for i in range(len(rsidf)):
                    if rsidf.iloc[i].item()<os:
                        if position == False :
                            crossingBelowOs = True
                
                
                    elif rsidf.iloc[i].item()>os and rsidf.iloc[i].item()<ob :
                        if position == False:
                            if crossingBelowOs == True:
                                signalBuy.append(rsidf.iloc[i].name)
                                position = True
                                crossingBelowOs = False
                        else:
                            if crossingAboveOb == True:
                                signalSell.append(rsidf.iloc[i].name)
                                position = False
                                crossingAboveOb = False
                            
                    
                    elif rsidf.iloc[i].item()>ob:
                        if position == True:
                            if crossingAboveOb == False:
                                crossingAboveOb = True

                    else:
                        pass


                rsi_signal = pd.DataFrame()

                
                
                buy_list=[]  
                buy_date = []

                for i in signalBuy:
                    buy_call = close.loc[i]
                    buy_list.append(buy_call)
                    buy_date.append(i)


                rsi_signal['Buy Date'] = buy_date

                rsi_signal['Buy']=buy_list



                sell_list=[]
                sell_date=[]
                for i in signalSell:
                    sell_call = close.loc[i]
                    sell_list.append(sell_call)
                    sell_date.append(i)

                if len(sell_list) != len(buy_list):    
                    sell_list.append("TBD")
                
                    sell_date.append("TBD")



                rsi_signal['Sell Date']=sell_date    
                rsi_signal['Sell']=sell_list

                

                rsi_signal['Profit/Loss%'] =" "*len(buy_list)

                rsi_signal['Holding Period']=" "*len(buy_list)

                try:
                    if "TBD" in sell_list:
                        rsi_signal['Profit/Loss%'] = ((rsi_signal['Sell'].iloc[0:-1]-rsi_signal['Buy']).iloc[0:-1]/rsi_signal['Buy'].iloc[0:-1])*100
                        rsi_signal['Holding Period'] = rsi_signal['Sell Date'].iloc[0:-1].astype("datetime64") - rsi_signal['Buy Date'].iloc[0:-1]

                    else:

                        rsi_signal['Profit/Loss%']=((rsi_signal['Sell']-rsi_signal['Buy'])/rsi_signal['Buy'])*100

                        rsi_signal['Holding Period'] = rsi_signal['Sell Date'] - rsi_signal['Buy Date']

                    
                    rsi_signal['Buy Date'] = rsi_signal['Buy Date'].dt.strftime("%Y-%m-%d")
                    rsi_signal['Holding Period'] = rsi_signal['Holding Period'].astype('timedelta64[D]')
                    rsi_signal['Sell Date'] = rsi_signal['Sell Date'].dt.strftime("%Y-%m-%d")

                                        
                    
                    
                except:
                    st.write("Some Error in Data! Try another Company!")

                st.write("Cummulative Profit(%):",round(rsi_signal['Profit/Loss%'].sum(),2))
                st.write("Number of Trades:",len(rsi_signal))


            
            def chart():
                global rsi_signal
                
                fig = make_subplots(rows=2, cols=1,row_heights=[0.7, 0.3],shared_xaxes=True,vertical_spacing=0)

                fig.add_trace(go.Scatter(x=ticker_data_rsi[closeType].index, y=ticker_data_rsi[closeType],name=closeType),secondary_y = False,row=1, col=1)

                
                fig.add_trace(go.Scatter(x=rsidf.index, y=rsidf['rsi'],name="RSI"),secondary_y = False,row=2, col=1)
                
                fig.add_trace(go.Scatter(x=rsi_signal["Buy Date"], y=rsi_signal["Buy"],name="Buy Signal",mode='markers', marker_symbol="triangle-up",marker_color="green"),secondary_y = False,row=1, col=1,)

                
                fig.add_trace(go.Scatter(x=rsi_signal["Sell Date"], y=rsi_signal["Sell"],name="Sell Signal",mode='markers', marker_symbol="triangle-down",marker_color="red"),secondary_y = False,row=1, col=1,)


                obl = [ob]*len(rsi_signal)
                osl = [os]*len(rsi_signal)

                fig.add_trace(go.Scatter(x=rsi_signal["Buy Date"], y=osl,name="RSI-Buy",mode='markers', marker_symbol="triangle-up",marker_color="green"),secondary_y = False,row=2, col=1,)
                fig.add_trace(go.Scatter(x=rsi_signal["Sell Date"], y=obl,name="RSI-Sell",mode='markers', marker_symbol="triangle-down",marker_color="black"),secondary_y = False,row=2, col=1,)


                fig.add_hline(y=ob,line_dash="dot", row=2, col=1, line_color="black", line_width=1)
                fig.add_hline(y=os,line_dash="dot", row=2, col=1, line_color="black", line_width=1)

                #fig.update_layout(dragmode='pan', hovermode='x unified')
                
                fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,row=1)
                fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,title="Date",row=2)
                fig.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="Price",row=1,col=1)
                fig.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="RSI",row=2)
                fig.update_layout(spikedistance=1000, hoverdistance=10,title="RSI-CHART",height=600)
                fig.update_traces(xaxis="x2")
                st.plotly_chart(fig,use_container_width=True)
            
            st.cache(allow_output_mutation=True)
            def optimum ():
                
                RSI.table()    
                with st.spinner('processing optimum!'):
                    optimum_rsi = pd.DataFrame() 

                    rsi_range_list=[]
                    profit_sum_list=[]
                    for ob in range(10,50,5):
                        for os in range(90,50,-5):

                            rsi_range = f"{ob}-{os}"

                            rsi_range_list.append(rsi_range)

                            signalBuy = []
                            signalSell = []
                            position = False

                            for i in range(len(rsidf)):
                                if rsidf.iloc[i].item()<ob:
                                    if position == False :
                                        signalBuy.append(rsidf.iloc[i].name)
                                        position = True
                                    else:
                                        pass

                                elif rsidf.iloc[i].item()>os:
                                    if position == True:
                                        signalSell.append(rsidf.iloc[i].name)
                                        position = False
                                    else:
                                        pass
                                else:
                                    pass



                            rsi_signal = pd.DataFrame()

                            buy_list=[]  
                            buy_date = []
                            for i in signalBuy:
                                buy_call = close.loc[i]
                                buy_list.append(buy_call)
                                buy_date.append(i)


                            rsi_signal['Buy Date'] = buy_date

                            rsi_signal['Buy']=buy_list



                            sell_list=[]
                            sell_date=[]
                            for i in signalSell:
                                sell_call = close.loc[i]
                                sell_list.append(sell_call)
                                sell_date.append(i)

                            if len(sell_list) != len(buy_list):    
                                sell_list.append("TBD")
                                sell_date.append("TBD")



                            rsi_signal['Sell Date']=sell_date    
                            rsi_signal['Sell']=sell_list

                            rsi_signal['Profit/Losst%'] =" "*len(buy_list)

                            rsi_signal['Holding Period']=" "*len(buy_list)

                            if "TBD" in sell_list:
                                rsi_signal['Profit/Losst%'] = ((rsi_signal['Sell'].iloc[0:-1]-rsi_signal['Buy']).iloc[0:-1]/rsi_signal['Buy'].iloc[0:-1])*100
                                rsi_signal['Holding Period'] = rsi_signal['Sell Date'].iloc[0:-1].astype("datetime64") - rsi_signal['Buy Date'].iloc[0:-1]

                            else:

                                rsi_signal['Profit/Losst%']=((rsi_signal['Sell']-rsi_signal['Buy'])/rsi_signal['Buy'])*100

                                rsi_signal['Holding Period'] = rsi_signal['Sell Date'] - rsi_signal['Buy Date']


                            profit_sum=rsi_signal['Profit/Losst%'].sum()

                            profit_sum_list.append(profit_sum)


                    optimum_rsi['Range'] =  rsi_range_list
                    optimum_rsi['Profit'] = profit_sum_list
                    optimum_rsi.set_index("Range",inplace=True)
                    fig=px.bar(optimum_rsi,x=optimum_rsi.index,y=optimum_rsi.columns)
                    #[optimum_rsi['Profit']>optimum_rsi['Profit'].mean()]
                    st.plotly_chart(fig,use_container_width=True)


                                
              



        
        RSI.signal()
        RSI.chart()
        
        
        with st.expander("See Table:"):
            rsi_signal


        get_optimum = st.button("Get Optimum")

        if get_optimum:
            st.warning("Please do not change or reload the page! Heavy processing on!")
            RSI.optimum()
            
            

    

with tab5:
    ema_name = st.selectbox("Select Company:",st.session_state["name_selected_technical"],index=0,key="emas")
    ticker_selected_ema=dfC[dfC[coName]==ema_name].loc[:,updatedTicker].to_list()
    ticker_data_ema = yf.download(ticker_selected_ema,start=sd,end=ed)
    ticker_sel  = ticker_selected_ema
    
    col1,col2 = st.columns(2)

    with col1:
        ema1 = st.slider("EMA-1:",5,300,50)

    with col2:
        ema2 = st.slider("EMA-2:",5,300,200)


    def close_price(): 
        global close 
        close = pd.DataFrame()
        close = ticker_data_ema[closeType]

    class EMA:
        

        def table(window=200): 
            global ema 
            from ta.trend import ema_indicator
            
            ematable = ema_indicator(ticker_data_ema[closeType], window=window, fillna= False)

            ema = pd.DataFrame.from_dict(ematable)

            ema.dropna(inplace=True)

            colum = " "
            for col in ema.columns:
                colum = col

            ema.rename(columns={colum:'ema'},inplace=True)

            return ema
        
           
        def signal(ema1,ema2):
            global EMA_Signals,ema_signal,ema_signalSell,ema_signalBuy

            close_price()
            global close 

            EMA_Signals = pd.DataFrame()

            EMA_Signals[closeType] = ticker_data_ema[closeType]
            EMA_Signals[str(ema1)] = EMA.table(ema1)
            EMA_Signals[str(ema2)] = EMA.table(ema2)



            ema_signalBuy = []
            ema_signalSell = []
            position = False

            for i in range(len(EMA_Signals)):
                    if EMA_Signals[str(ema1)].iloc[i]>EMA_Signals[str(ema2)].iloc[i]:
                        if position == False :
                            ema_signalBuy.append(EMA_Signals.iloc[i].name)
                            position = True
                        else:
                            pass

                    elif EMA_Signals[str(ema1)].iloc[i]<EMA_Signals[str(ema2)].iloc[i]:
                        if position == True:
                            ema_signalSell.append(EMA_Signals.iloc[i].name)
                            position = False
                        else:
                            pass
                    else:
                        pass

            
            ema_signal = pd.DataFrame()

            buy_list=[]  
            buy_date = []
            for i in ema_signalBuy:
                buy_call = close.loc[i]
                buy_list.append(buy_call)
                buy_date.append(i)


            ema_signal['Buy Date'] = buy_date

            ema_signal['Buy']=buy_list



            sell_list=[]
            sell_date=[]

            for i in ema_signalSell:
                sell_call = close.loc[i]
                sell_list.append(sell_call)
                sell_date.append(i)

            if len(sell_list) != len(buy_list):    
                sell_list.append("TBD")
                sell_date.append("TBD")



            ema_signal['Sell Date']=sell_date    
            ema_signal['Sell']=sell_list

            ema_signal['Profit/Loss%'] =" "*len(buy_list)

            ema_signal['Holding Period']=" "*len(buy_list)

            if "TBD" in sell_list:
                ema_signal['Profit/Loss%'] = ((ema_signal['Sell'].iloc[0:-1]-ema_signal['Buy']).iloc[0:-1]/ema_signal['Buy'].iloc[0:-1])*100
                ema_signal['Holding Period'] = ema_signal['Sell Date'].iloc[0:-1].astype("datetime64") - ema_signal['Buy Date'].iloc[0:-1]

            else:

                ema_signal['Profit/Loss%']=((ema_signal['Sell']-ema_signal['Buy'])/ema_signal['Buy'])*100

                ema_signal['Holding Period'] = ema_signal['Sell Date'] - ema_signal['Buy Date']



                
            #ema_signal['Buy Date'] = ema_signal['Buy Date'].dt.strftime("%Y-%m-%d")
            ema_signal['Holding Period'] = ema_signal['Holding Period'].astype('timedelta64[D]')

        st.cache(allow_output_mutation=True)     
        def chart():

            EMA.signal(ema1,ema2)
            
            close_price()

            global close 
            
            fig = go.Figure(data=[go.Candlestick(x=ticker_data_ema.index,
                    open=ticker_data_ema['Open'],
                    high=ticker_data_ema['High'],
                    low=ticker_data_ema['Low'],
                    close=ticker_data_ema[closeType],name="Price",increasing_line_color= 'green', decreasing_line_color= 'red')])
            
          
            EMA.table(ema1)

            fig.add_trace(go.Scatter(x=ema.index, y=ema["ema"],name=ema1))

            EMA.table(ema2)
            fig.add_trace(go.Scatter(x=ema.index, y=ema["ema"],name=ema2))

            
            fig.add_trace(go.Scatter(x=ema_signal['Buy Date'], y=ema_signal['Buy'],name="Buy Signal",mode='markers', marker_symbol="triangle-up",marker=dict(color='blue',size=10)))
            fig.add_trace(go.Scatter(x=ema_signal['Sell Date'], y=ema_signal['Sell'],name="Sell Signal",mode='markers', marker_symbol="triangle-down",marker=dict(color='brown',size=10)))


            
            fig.update_xaxes(showspikes=True, spikecolor="black", spikesnap="cursor", spikemode="across",spikethickness=1,title="Date")
            fig.update_yaxes(showspikes=True, spikesnap="cursor",spikecolor="black", spikemode="across",spikethickness=1,title="Price")
            fig.update_layout(spikedistance=1000, hoverdistance=10,title="EMA-CHART",height=600)

            st.plotly_chart(fig,use_container_width=True)
        
        
            
    
        def optimum():
            
            global optimumEMA
            
            with st.spinner('processing optimum!'):

                optimumEMA = pd.DataFrame()
                
                profit = []
                ema_range = [] 
                for i in range(10,110,10):
                    for u in range(250,10,-10):
                        if (u-i) < 10:
                            pass

                        else:
                            EMA.signal(i,u)
                            profit.append(ema_signal.iloc[:,4].sum())
                            ema_range.append(f'{i}-{u}')


                optimumEMA['EMA-RANGE']=ema_range
                optimumEMA['Profit'] = profit 


                fig1= px.histogram(optimumEMA,x="Profit")

                fig2df = optimumEMA.set_index("EMA-RANGE").iloc[0:110]
                
                fig2=px.bar(fig2df,x=fig2df.index,y=fig2df['Profit'])

                
                fig3df = optimumEMA.set_index("EMA-RANGE").iloc[110:]
                fig3=px.bar(fig3df,x=fig3df.index,y=fig3df['Profit'])


                st.plotly_chart(fig1)
                st.plotly_chart(fig2)
                st.plotly_chart(fig3)


        

    EMA.signal(ema1,ema2)
    EMA.chart()
                    
    max_profit = " "
    if round(ema_signal.iloc[:,4].max(),2) < 0:
        max_profit = "NA"
    
    else:
        max_profit = round(ema_signal.iloc[:,4].max(),2)

    max_loss = " "
    if round(ema_signal.iloc[:,4].min(),2) > 0:
        max_loss = "NA"
    
    else:
        max_loss = round(ema_signal.iloc[:,4].min(),2)

    st.write(f"{ema1}-{ema2} EMA")
    st.write('Total Profit/Loss (%):',round(ema_signal.iloc[:,4].sum(),2))
    st.write("Max Profit on single trade (%):",max_profit)
    st.write("Max Loss on single trade (%):",max_loss)
    try:
        st.write("Average Holding Period (days):",round(ema_signal.iloc[:,5].mean()))
    except:
            st.write("Average Holding Period (days):","NA")

    ema_signal


    get_optimum = st.button("Get Optimum",key="emagetopt")

    if get_optimum:
        st.warning("Please do not change or reload the page! Heavy processing on!")
        EMA.optimum()



with tab6:
    isdfC = dfC[dfC[coName].isin(st.session_state["name_selected_technical"])].sort_values(by=marketCap,ascending=False)
    tr=isdfC[[coName,marketCap,'Technical Rating','Moving Averages Rating','Oscillators Rating']].set_index(coName)
    tr



with tab7:

        perf_type = st.radio("Performance Type:",("Yearly","Quarterly","Monthly"),horizontal=True,key="ptype")
        
        if perf_type == "Yearly":      
            x=tickdata.resample("Y").ffill().pct_change().reset_index()
            x['Year'] = x['Date'].dt.year
            z=x.drop("Date",axis=1).set_index("Year")
            t=z.transpose().iloc[:,1:]
            fig = px.imshow(t.values, text_auto=".2%",x= t.columns,y=t.index, height=600)
            fig.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=[[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]])
            st.plotly_chart(fig,use_container_width=True)


        else:
            if perf_type == "Monthly":
                freq = "M"
            else:
                freq = "Q"

            ptm = st.radio("Chart:",("Heatmap","Peer Comparison"),index=0,key="pm",horizontal=True)

            if ptm =="Heatmap":
                per_name = st.selectbox("Select Company:",st.session_state["name_selected_technical"],index=0,key="pname")
                ticker_selected_perf=dfC[dfC[coName]==per_name].loc[:,updatedTicker].to_list()

                if len(st.session_state["name_selected_technical"]) == 1: 
                    isdfOne=ticker_data[closeType].resample(freq).ffill().pct_change().reset_index()
                    isdf = isdfOne

                else:
                    isdfMany=ticker_data[closeType][ticker_selected_perf].resample(freq).ffill().pct_change().reset_index()
                    isdf = isdfMany
                
                isdf['Year'] = isdf['Date'].dt.year
                isdf['Month'] = isdf['Date'].dt.month_name()
                
                
                months= isdf['Month'].unique().tolist()
                ispdf=isdf.pivot_table(index="Year",columns="Month",values=ticker_selected_perf)
                ispdf.columns =ispdf.columns.droplevel()    
                ispdf = ispdf.reindex(columns=months)

                z = ispdf.values
                
                fig = px.imshow(z, text_auto=".2%",x=ispdf.columns,y=ispdf.index,aspect="auto",title=f"Monthly Performance-{per_name}")
                fig.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=[[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]])
                st.plotly_chart(fig,use_container_width=True)
            
            else:
                st.write("Have to work on this!")
        



with tab8:
        perf_type = st.radio("Performance Type:",("1d","1w","1m","3m","6m","12m","Choose your own Period"),index=6,horizontal=True,key="perftype")
        
        date_list=tickdata.index.date
        
        if perf_type == "Choose your own Period":
            ds,de = st.select_slider("Date Range:",options=date_list,value=(date_list[0],date_list[-1]),key="Hmapdatesl")
        
        else:
            de = date_list[-1]

            if perf_type == "1d":
                ds = date_list[-2]
                
            elif perf_type == "1w":
                ds = date_list[-5]
                
            elif perf_type == "1m":
                ds = date_list[-20]


            elif perf_type == "3m":
                ds = date_list[-60]

            elif perf_type == "6m":
                ds = date_list[-120]

            elif perf_type == "12m":
                ds = date_list[-240]

        def HeatMap():
            mrh = pd.DataFrame()  
            
            cldf = ticker_data["Close"].dropna()
            cldf = cldf.loc[ds:de]
            mrh['return']=cldf.iloc[-1]/cldf.iloc[0] - 1
            
            
            color_bin = [-100000000,-0.2,-0.01,0, 0.01, 0.2,100000000]
            mrh['colors'] = pd.cut(mrh['return'], bins=color_bin, labels=['red','indianred','lightpink','lightgreen','green','lime'])
            mrh.index.set_names("Ticker",inplace=True)
            mrh.reset_index(inplace=True)
            si = dfC[dfC[updatedTicker].isin(mrh['Ticker'].to_list())]
            mi = si[[updatedTicker,coName,sector,industry,marketCap]]
            mrheat = mrh.merge(mi,left_on='Ticker',right_on=updatedTicker,how='left')



            from numerize import numerize as nu
            mrheat['return']=mrheat['return'].fillna(0).astype("float64")
            mrheat[marketCap]=mrheat[marketCap].fillna(0).astype("int64")
            
            returns = []
            for i in mrheat['return']:
                returns.append("{:.2%}".format(i))

            marketcap = []
            for i in mrheat[marketCap]:
                    marketcap.append(nu.numerize(i))
            mrheat['return'] = returns
            mrheat['Market Cap (B)'] = marketcap


            mrheat.dropna(subset=[coName,updatedTicker],inplace=True)   #'Market Cap','return','colors'
            
            # extra processing
            mrheat[sector].replace(0,"Others",inplace=True)
            mrheat[industry].replace(0,"Others",inplace=True)




            fig = px.treemap(mrheat, path=[px.Constant("all"),sector,industry,coName,'Market Cap (B)','return'], values = marketCap, color='colors',
                            color_discrete_map ={'(?)':'#262931', 'red':'red', 'indianred':'indianred','lightpink':'lightpink', 'lightgreen':'lightgreen','lime':'lime','green':'green'},height=1000,hover_data = { })

            st.plotly_chart(fig,use_container_width=True)

        Hmap = HeatMap()
            



with tab9:
    try:
        option_name= st.selectbox("See Options for:",st.session_state["name_selected_technical"],index=0)
        
        ticker=dfC[dfC[coName]==(option_name)].loc[:,updatedTicker].to_list()

        ytick = " "
        for i in ticker:
            ytick = i   
    
        yftick = yf.Ticker(ytick)
        opt_expiry_list=yftick.options
        opt_expiry=st.selectbox("Option Expiry",options=opt_expiry_list,index=0)

        opt = yftick.option_chain(opt_expiry)

        opt_type=st.radio("Select Option Type",("Call","Put"),index=0)

        if opt_type =="Call":
            opt.calls
        
        else:
            opt.puts 

         

    except:
        st.write("Select a different Company Name or reload page!")
