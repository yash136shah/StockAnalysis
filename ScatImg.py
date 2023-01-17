import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf 
import datetime
import plotly.express as px 
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import  streamlit_toggle as tog
from load_data_2 import load_data_All
from plotly.subplots import make_subplots
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from eodhd import APIClient
import os
import urllib, json
import re
from Hmap import rhmap

st.set_page_config(layout="wide")



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
st5 = "Ratio "
IS = "IS"
BS = "BS"
CF = "CF"
OT = "Ratio"



market_select =  st.sidebar.radio("Market:",("USA","Canada","India"),index=2)

if market_select == "USA":
        benchmark = "SPY"
        descriptive_screener = ["EXCHANGE"]
        dfC = AdfC[AdfC["Market Code"]=="US"]
        dfF = AdfF[AdfF["Market Code"]=="US"]
        dfQ = AdfQ[AdfQ["Market Code"]=="US"]
        

elif market_select == "India":
        benchmark = '^NSEI'
        descriptive_screener = []
        dfC = AdfC[AdfC["Market Code"]=="IND"]
        dfF = AdfF[AdfF["Market Code"]=="IND"]
        dfQ = AdfQ[AdfQ["Market Code"]=="IND"]


elif market_select == "Canada":
        benchmark = '^GSPTSE'
        descriptive_screener=[]
        dfC = AdfC[AdfC["Market Code"]=="CAN"]
        dfF = AdfF[AdfF["Market Code"]=="CAN"]
        dfQ = AdfQ[AdfQ["Market Code"]=="CAN"]

        #IS bifurcation IND and CAN

statements =dfM["Statement Category"].unique().tolist()
stTotals =dfM["Statement Totals "].unique().tolist()
cs ={}
for stmen in statements:
    stList = dfM[dfM["Statement Category"] == stmen]["title"].to_list()
    cs[stmen] = stList 

cst = {}
for stmen in stTotals:
    stList = dfM[dfM["Statement Totals "] == stmen]["title"].to_list()
    cst[stmen] = stList 


# SEARCH NAME 
name_search = st.sidebar.radio('Search Company:',('Sector & Industry', "Peers", "Screener",'Individually'),index=0,horizontal=True)



metdf=dfF[dfF[year]==dfF[year].max()]
diff_cols = metdf.columns.difference(dfC.columns)
#Filter out the columns that are different. You could pass in the df2[diff_cols] directly into the merge as well.
selcols = diff_cols.tolist()+ [coName]
selcolmetdf = metdf[selcols]
metdfC = dfC.merge(selcolmetdf,left_on=coName,right_on=coName,how="left")   
unnamed = metdfC.columns[metdfC.columns.str.startswith('Unnamed')]
metdfC.drop(unnamed,axis=1,inplace=True)



if name_search == 'Sector & Industry':
    sstype = st.sidebar.radio("Select Sector",("single","multi-select","all"),index=0,key="sector",horizontal=True)

    #ROW 1 of Selection
    col1,col2,col3 = st.columns(3)
    with col1:
  
        if sstype=="all":
            sectors=st.multiselect("Sector:",metdfC[sector].unique(),default=metdfC[sector].unique())
        elif sstype=="multi-select":
            sectors =st.multiselect("Sector:",metdfC[sector].unique(),default=metdfC[sector].unique()[0])

        else:
            sectors =st.selectbox("Sector:",metdfC[sector].unique(),index=0)
            sectors = sectors.split("-")

        ss = metdfC[metdfC[sector].isin(sectors)]



    if len(sectors) == 0:   # ERROR RAISED IF NO SECTOR
        st.error("Please Enter a Sector")
        st.stop()


    with col2:
        
        industrys =st.multiselect("Industry:",ss[industry].unique(),default=ss[industry].unique()[:2])
        all = st.checkbox("Select all",key="industry")
        if all:
             industrys = ss[industry].unique()
        else:
             industrys = industrys

    
    if len(industrys) == 0:        # ERROR RAISED IF NO INDUSTRY 
        st.error("Please Enter a Industry")
        st.stop()


    #ROW 2 of Selection 

    if market_select == "USA":
        with col3:
            #isc = metdfC[(metdfC[sector].isin(sectors)) & (metdfC[industry].isin(industrys))]    #infoselected for country
            country = st.multiselect("Country:",metdfC["COUNTRY"].unique(),default=metdfC["COUNTRY"].unique()[0])
            all = st.checkbox("Select all",key="country")
            if all:
                    country = metdfC["COUNTRY"].unique()
            else:
                country  = country

        if len(country) == 0:        # ERROR RAISED IF NO COUNTRY SELECTED
            st.error("Please Enter Country")
            st.stop()


        ism = metdfC[(metdfC[sector].isin(sectors)) & (metdfC[industry].isin(industrys)) & (metdfC["COUNTRY"].isin(country))] #infoselected for marketcap
        
        if len(ism) == 0:
            st.error("This Country has no Companies!")
            st.stop()
    
    else:
        ism = metdfC[(metdfC[sector].isin(sectors)) & (metdfC[industry].isin(industrys))]
    

    col1,col2,col3 = st.columns(3)


    mega = 100*1000000000
    large = 20*1000000000
    mid = 1*1000000000
    mid2 = 0.5*1000000000


    nmg = len(ism[(ism[marketCap] >= mega)])
    nl = len(ism[(ism[marketCap] >= large) & (ism[marketCap] <= mega)])
    ml = len(ism[(ism[marketCap] >= mid) & (ism[marketCap] <= large)])
    ms = len(ism[(ism[marketCap] >= mid2) & (ism[marketCap] <= mid)])
    sm = len(ism[(ism[marketCap] <= mid2)])

    with col1:
        mscale_selected = st.select_slider('Market Cap Scale',
        options=['small','mid-small','mid-large', 'large', 'mega'],value="large")

    if mscale_selected == "mega":
        st.write(f"{nmg}-companies in Mega Scale (>100B)")
        minmc=(ism[ism[marketCap] >= mega][marketCap].min())/1000000000
        maxmc = (ism[ism[marketCap] >= mega][marketCap].max())/(1000000000)
        qumc = (ism[ism[marketCap] >= mega][marketCap].quantile(q=0.75)/1000000000)


    elif mscale_selected == "large":
        st.write(f"{nl}-companies in Large Scale (20B-100B)")
        minmc=(ism[(ism[marketCap] >= large) & (ism[marketCap] <= mega)][marketCap].min()/1000000000)
        maxmc = (ism[(ism[marketCap] >= large) & (ism[marketCap] <= mega)][marketCap].max()/1000000000)
        qumc = (ism[(ism[marketCap] >= large) & (ism[marketCap] <= mega)][marketCap].quantile(q=0.75)/1000000000)



    elif mscale_selected == "mid-large":
        st.write(f"{ml}-companies in Mid Scale (1B-20B)") 
        minmc=(ism[(ism[marketCap] >= mid) & (ism[marketCap] <= large)][marketCap].min()/1000000000)
        maxmc =(ism[(ism[marketCap] >= mid) & (ism[marketCap] <= large)][marketCap].max()/1000000000)
        qumc = (ism[(ism[marketCap] >= mid) & (ism[marketCap] <= large)][marketCap].quantile(q=0.75)/1000000000)


    elif mscale_selected == "mid-small":
        st.write(f"{ms}-companies in Mid-Small Scale (0.5B-1B)")
        minmc=(ism[(ism[marketCap] >= mid2) & (ism[marketCap] <= mid)][marketCap].min()/1000000000)
        maxmc = (ism[(ism[marketCap] >= mid2) & (ism[marketCap] <= mid)][marketCap].max()/1000000000)
        qumc = (ism[(ism[marketCap] >= mid2) & (ism[marketCap] <= mid)][marketCap].quantile(q=0.75)/1000000000)


    elif mscale_selected == "small":
        st.write(f"{sm}-companies in Small Scale (<500m)") 
        minmc=(ism[(ism[marketCap] <= mid2)][marketCap].min()/1000000000)
        maxmc = (ism[(ism[marketCap] <= mid2)][marketCap].max()/1000000000)
        qumc = (ism[(ism[marketCap] <= mid2)][marketCap].quantile(q=0.75)/1000000000)



        

    with col2:
        st.write(" ")
        mc_s = st.number_input('Select Min Market Cap (Billion $):',value=minmc)

    with col3:
        st.write(" ")
        mc_e = st.number_input('Select Max Market Cap (Billion $):',value=maxmc,min_value=0.0,max_value=20000.0)


    mcs = mc_s * 1000000000
    mce = mc_e * 1000000000

    if mce<mcs: # Error With Market Cap 
        st.error("Market Cap Max can not be smaller than Market Cap Min")
        st.stop()



 

    #NAME SECTION 
    isdfn= ism[(ism[marketCap]>=mcs) & (ism[marketCap]<=mce)].sort_values(by=marketCap,ascending=False)


    mcapindex = metdfC.columns.tolist().index(marketCap)
    peindex = metdfC.columns.tolist().index(pe)

    col1,col2,col3,col4 = st.columns(4)
    indusindex = metdfC.columns.tolist().index(industry)
    with col1:   
        x_axis_met = st.selectbox("Select X-Axis",metdfC.columns,index=mcapindex,key="xaxispc")

    with col2:
        y_axis_met = st.selectbox("Select Y-Axis",metdfC.columns,index=peindex,key="yaxispc")

    with col3: 
        marker_size = st.selectbox("Marker Size",metdfC.columns,index=mcapindex,key="markersize")

    with col4: 
        marker_color = st.selectbox("Marker Color",metdfC.columns,index=indusindex,key="markercolor")

 
    fig = px.scatter(isdfn,x=x_axis_met,y=y_axis_met,color=marker_color,size=marker_size,size_max=40,text=coName)
    
    for x,y,logo in zip(isdfn[x_axis_met],isdfn[y_axis_met],isdfn["LOGOURL"]):
        try:
            fig.add_layout_image(dict(
                x=x,
                y=y,
                source=logo,
                xref="x",
                yref="y",
                sizex=20,
                sizey=20,xanchor="center",
                yanchor="middle",
                opacity=0.5)
                )
        except:
            pass

    st.plotly_chart(fig,use_container_width=True)

    st.image("https://eodhistoricaldata.com/img/logos/US/MSFT.png", width=60)