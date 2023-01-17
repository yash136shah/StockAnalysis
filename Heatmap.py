import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import stockDatabase as sd 
import datetime
import plotly.express as px
from load_data_2 import load_data_All


st.set_page_config(layout="wide")

market_select =  st.sidebar.radio("Select Market:",("USA","Canada","India"))




AdfC,AdfF,AdfQ,dfM,dfT,dfSh,dfOff,dfEA,dfEH,dfET = load_data_All()


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
d_e = 'D/E'
c_r = 'C/R'
pe = 'TRAILINGPE'
pcf = 'PEG RATIO'
st1 = "IS"
st2 = "CF"
st3 = "Ratio "
st4 = "Ratio "
st5 = "Ratio "
IS = "IS"
BS = "BS"
CF = "CF"
OT = "Ratio"



if market_select == "USA":
        benchmark = "SPY"
        descriptive_screener = ["EXCHANGE"]
        dfC = AdfC[AdfC["Market Code"]=="US"]
        dfF = AdfF[AdfF["Market Code"]=="US"]
        

elif market_select == "India":
        benchmark = '^NSEI'
        descriptive_screener = []
        dfC = AdfC[AdfC["Market Code"]=="IND"]
        dfF = AdfF[AdfF["Market Code"]=="IND"]


elif market_select == "Canada":
        benchmark = '^GSPTSE'
        descriptive_screener=[]
        dfC = AdfC[AdfC["Market Code"]=="CAN"]
        dfF = AdfF[AdfF["Market Code"]=="CAN"]


st.header("HEATMAP")




sectors = st.sidebar.multiselect(
    "Select Sector:",
    options = dfF[sector].unique(),
    default = dfF[sector].unique()
)
ss = dfF[dfF[sector].isin(sectors)]


industrys = st.sidebar.multiselect(
    "Select Industry:",
    options = ss[industry].unique(),
    default = dfF[industry].unique(),
)


ssi = dfF[(dfF[sector].isin(sectors))&(dfF[industry].isin(industrys))].fillna(0)

min_mc = int(ssi[marketCap].min())
max_mc = int(round((ssi[marketCap].max())/1000000,0) + 1)
q1_mc =  int(round((ssi[marketCap].quantile(q=0.75))/1000000,0))
q2_mc =  int(round((ssi[marketCap].quantile(q=0.25))/1000000,0))


if min_mc == q1_mc :
    mc_s,mc_e  = st.select_slider(
        'Select Market Cap (Million $)',
        options=[min_mc,q1_mc,max_mc],
        value=(min_mc, max_mc))

else:
    mc_s,mc_e  = st.select_slider(
    'Select Market Cap (Million $)',
    options=[min_mc, q2_mc, q1_mc,max_mc],
    value=(q1_mc, max_mc))


mcs = mc_s * 1000000
mce = mc_e * 1000000




sel = dfF[(dfF[sector].isin(sectors))&(dfF[industry].isin(industrys))&(dfF[marketCap]>mcs)&(dfF[marketCap]<mce)].sort_values(by=marketCap,ascending=False)



name_selected =sel[coName].unique()[:300]






# Enter Date 




def rhmap():
    global mrheat,ed,sd

    

    mrh = pd.DataFrame()  




    dtcol1,dtcol2 = st.columns(2)

    with dtcol1:
        sdp = st.date_input(
            "Enter Start Date",
            datetime.date(2022, 1, 1),min_value=datetime.date(2010, 1, 1),max_value=datetime.date(2025,1,1))

    # ISSUE WITH END DATE = CANT FIND YESTERDAY AND FOR TODAY YFINANCE GIVES NA 
    today = datetime.date.today()
    with dtcol2:
                edp = st.date_input("Enter End Date",min_value=datetime.date(2010, 1, 1),max_value=today,key="perioded")
    
    ticker_selected=dfC[dfC[coName].isin(name_selected)].loc[:,updatedTicker].to_list()
    ticker_data = yf.download(ticker_selected,start=sdp,end=edp)

    cldf = ticker_data["Close"].dropna()

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

    return st.plotly_chart(fig,use_container_width=True)
    





run = st.checkbox("Get Chart")


if run:
    rhmap()
    