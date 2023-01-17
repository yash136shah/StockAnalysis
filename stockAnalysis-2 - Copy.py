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
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px 
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide")






AdfC,AdfF,AmultidfC,AdfQ,dfM,dfT,dfSh,dfOff,dfEA,dfEH,dfET,gridOptions = load_data_All()


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
    st.session_state["marketSelect"] = markets[0]
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelect"])

def MarketSelect ():
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelrad"])

st.session_state["marketSelect"] = st.sidebar.radio("Market:",markets,index=st.session_state["marketIndex"],key="marketSelrad",on_change=MarketSelect)




if st.session_state["marketSelect"] == "USA":
        benchmark = "SPY"
        descriptive_screener = ["EXCHANGE"]
        dfC = AdfC[AdfC["Market Code"]=="US"]
        dfF = AdfF[AdfF["Market Code"]=="US"]
        dfQ = AdfQ[AdfQ["Market Code"]=="US"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="US"]

elif st.session_state["marketSelect"] == "India":
        benchmark = '^NSEI'
        descriptive_screener = []
        dfC = AdfC[AdfC["Market Code"]=="IND"]
        dfF = AdfF[AdfF["Market Code"]=="IND"]
        dfQ = AdfQ[AdfQ["Market Code"]=="IND"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="IND"]


elif st.session_state["marketSelect"] == "Canada":
        benchmark = '^GSPTSE'
        descriptive_screener=[]
        dfC = AdfC[AdfC["Market Code"]=="CAN"]
        dfF = AdfF[AdfF["Market Code"]=="CAN"]
        dfQ = AdfQ[AdfQ["Market Code"]=="CAN"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="CAN"]

        #IS bifurcation IND and CAN



# SEARCH NAME BY: 
name_search = st.sidebar.radio('Search Company:',('Sector & Industry', "Peers", "Screener",'Individually'),index=0,horizontal=True)




if name_search == 'Sector & Industry':
    sstype = st.sidebar.radio("Select Sector",("single","multi-select","all"),index=0,key="sector",horizontal=True)

    #ROW 1 of Selection
    col1,col2,col3 = st.columns(3)
    with col1:
        if "sectorSel" not in st.session_state:
            st.session_state["sectorSel"] = multidfC[sector].unique()[0]
            st.session_state["sectorDefault"] = st.session_state["sectorSel"]
            st.session_state["sectorBoxValue"] = False

        def SectorSel ():   
            st.session_state["sectorDefault"] = st.session_state["sectorSelrad"]            
        #st.session_state["sectorSel"] = multidfC[sector].unique()[0]
        #st.session_state["sectorDefault"] = st.session_state["sectorSel"]
        st.session_state["sectorSel"] = st.multiselect("Sector:",multidfC[sector].unique(),default=st.session_state["sectorDefault"] ,key="sectorSelrad",on_change=SectorSel)
        
        def SectorAllSel():
            if st.session_state["sectorBoxValue"] == True: 
                    st.session_state["sectorBoxValue"] = False
            else:
                    st.session_state["sectorBoxValue"] = True

        all = st.checkbox("Select all",value=st.session_state["sectorBoxValue"],key="sectorAll",on_change=SectorAllSel)
        if all:
             st.session_state["sectorSel"] = multidfC[sector].unique()



    if len(st.session_state["sectorSel"]) == 0:   # ERROR RAISED IF NO SECTOR
        st.error("Please Enter a Sector")
        st.stop()


    with col2:
        industry_list = multidfC[multidfC[sector].isin(st.session_state["sectorSel"])][industry].unique().tolist()
        if "industrySel" not in st.session_state:
                st.session_state["industrySel"] = industry_list[:2]
                st.session_state["industryDefault"] = st.session_state["industrySel"]
                st.session_state["industryBoxValue"] = False

        def IndustrySel ():   
            st.session_state["industryDefault"] = st.session_state["industrySelrad"]            
        st.session_state["industrySel"] = industry_list[:2]
        st.session_state["industryDefault"] = st.session_state["industrySel"]
        st.session_state["industrySel"] = st.multiselect("Industry:",options=industry_list,default=st.session_state["industryDefault"],key="industrySelrad",on_change=IndustrySel)
        
        def IndustryAllSel():
            if st.session_state["industryBoxValue"] == True: 
                    st.session_state["industryBoxValue"] = False
            else:
                    st.session_state["industryBoxValue"] = True

        all_ind = st.checkbox("Select all",value=st.session_state["industryBoxValue"],key="industryAll",on_change=IndustryAllSel)
        
        if len(st.session_state["industrySel"]) == 0:        # ERROR RAISED IF NO INDUSTRY 
            st.error("Please Enter a Industry")
            st.stop()

        industryOverview = st.checkbox("See Industry Overview")

        if industryOverview:
            switch_page("Industry-Analysis-2")


    #ROW 2 of Selection 

    with col3:
        #country_list= dfC[(dfC[sector].isin(st.session_state["sectorSel"])) & (dfC[industry].isin(st.session_state["industrySel"]))]["COUNTRY"].unique().tolist()
        country_counts= dfC[(dfC[sector].isin(st.session_state["sectorSel"])) & (dfC[industry].isin(st.session_state["industrySel"]))]["COUNTRY"].value_counts().to_frame()
        country_list = []
        for country in country_counts.index:
            country_list.append(country)

        if "countrySel" not in st.session_state:
            st.session_state["countrySel"] = country_list[0]
            st.session_state["countryDefault"] = st.session_state["countrySel"]
            st.session_state["countryBoxValue"] = False

        def CountrySel ():   
            st.session_state["countryDefault"] = st.session_state["countrySelrad"]            
        st.session_state["countrySel"] = country_list[0]
        st.session_state["countryDefault"] = st.session_state["countrySel"]
        st.session_state["countrySel"] = st.multiselect("Country:",options=country_list,default=st.session_state["countryDefault"],key="countrySelrad",on_change=CountrySel)
        
        def CountryAllSel():
           if st.session_state["countryBoxValue"] == True: 
                st.session_state["countryBoxValue"] = False
           else:
                st.session_state["countryBoxValue"] = True

        all_country = st.checkbox("Select all",value=st.session_state["countryBoxValue"], key="countryAll",on_change=CountryAllSel)
        if all_country:
                st.session_state["countrySel"]  = country_list

        if len(st.session_state["countrySel"]) == 0:        # ERROR RAISED IF NO COUNTRY SELECTED
            st.error("Please Enter Country")
            st.stop()


    ism = multidfC[(multidfC[sector].isin(st.session_state["sectorSel"])) & (multidfC[industry].isin(st.session_state["industrySel"])) & (multidfC["COUNTRY"].isin(st.session_state["countrySel"]))] #infoselected for marketcap
    



    col1,col2,col3 = st.columns(3)


    mega = 100*1000000000
    large = 20*1000000000
    mid = 1*1000000000
    mid2 = 0.5*1000000000
    
    with col1:
            mscale_selected = st.select_slider('Market Cap Scale',
            options=['small','mid-small','mid-large', 'large', 'mega'],value="large")

    @st.cache(suppress_st_warning=True)
    def McapSlide():
        nmg = len(ism[(ism[marketCap] >= mega)])
        nl = len(ism[(ism[marketCap] >= large) & (ism[marketCap] <= mega)])
        ml = len(ism[(ism[marketCap] >= mid) & (ism[marketCap] <= large)])
        ms = len(ism[(ism[marketCap] >= mid2) & (ism[marketCap] <= mid)])
        sm = len(ism[(ism[marketCap] <= mid2)])

        

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

        return minmc,maxmc


    minmc,maxmc = McapSlide()

        
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


    tab1,tab2 = st.tabs(["Peer Chart","Company List"])

    if "name_selected" not in st.session_state:
        st.session_state["name_selected"] = []
    
    if "name_selected_chart" not in st.session_state:
        st.session_state["name_selected_chart"] = []
        st.session_state["name_selected_table"] = []
    
    
    with tab1:
        
        multidfCNum = multidfC.select_dtypes(include=["int","float"])
        multidfCStr = multidfC.select_dtypes(include=["object"])
        mcapindex = multidfCNum.columns.tolist().index(marketCap)
        peindex = multidfCNum.columns.tolist().index(pe)
        indusindex = multidfCStr.columns.tolist().index(industry)
        col1,col2,col3,col4 = st.columns(4)
        
        with col1:   
            x_axis_met = st.selectbox("Select X-Axis",multidfCNum.columns,index=mcapindex,key="xaxispc")

        with col2:
            y_axis_met = st.selectbox("Select Y-Axis",multidfCNum.columns,index=peindex,key="yaxispc")

        with col3: 
            marker_size = st.selectbox("Marker Size",multidfCNum.columns,index=mcapindex,key="markersize")

        with col4: 
            marker_color = st.selectbox("Marker Color",multidfCStr.columns,index=indusindex,key="markercolor")

        fig = px.scatter(isdfn,x=x_axis_met,y=y_axis_met,color=marker_color,size=marker_size,size_max=40,text=coName)

        col1,col2,col3,col4 = st.columns([1,1,4,4])
        x_min = isdfn[x_axis_met].min()
        x_max = isdfn[x_axis_met].max()
        mcapList = isdfn[x_axis_met].to_list()
        mcapList.sort()

        #with col1:
        #    xValMin=st.number_input("Min X-axis value",min_value=x_min,max_value=x_max,value=x_min)
        #with col2:
        #    xValMax=st.number_input("Max X-axis value",min_value=x_min,max_value=x_max,value=x_max)
        
        #fig.update_layout(xaxis_range=[xValMin,xValMax])

        selection = plotly_events(fig,click_event=False,select_event=True)
        
        # CLICKABLE EVENTS GENERATED 
        st.session_state["name_selected_chart"]= []
        for el in selection:
            try:
                x=el['x']      
                y=el['y']
                nsdf=multidfC[(multidfC[x_axis_met]==(x)) & (multidfC[y_axis_met]==(y))]
            
                name_sel = nsdf[coName].item()
                if name_sel not in st.session_state["name_selected_chart"]:
                    st.session_state["name_selected_chart"].append(name_sel)
            
            except:
                pass
        
        

    with tab2:      
        return_mode_value = DataReturnMode.FILTERED_AND_SORTED
        update_mode=GridUpdateMode.MANUAL
        gridOptions["rowSelection"] = "multiple"
        gridOptions["columnDefs"][0]["children"][0]["checkboxSelection"]=True
        
        grid_returnSI = AgGrid(isdfn,height=400,gridOptions=gridOptions,data_return_mode=return_mode_value,update_mode=update_mode,theme="streamlit",allow_unsafe_jscode=True)      
        screendfC = grid_returnSI['selected_rows']

        st.session_state["name_selected_table"]= []
        for i in screendfC:
            if i[coName] not in st.session_state["name_selected_table"]:
                st.session_state["name_selected_table"].append(i[coName])
    
    
    name_combo=st.session_state["name_selected_table"]+st.session_state["name_selected_chart"]
    
    st.session_state["name_selected"] = [*set(name_combo)]
    
    name_selected=st.multiselect("Company Name Selected:",isdfn[coName].unique(),default=st.session_state["name_selected"])
    
    if len(name_selected) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select or Select from select box - to perform Analysis.")
        st.stop()

        
    

elif name_search == "Peers":
    #Enter Name
    name_uni = multidfC.sort_values(by=marketCap,ascending=False)[coName].dropna().unique()
    name_list = []
    for i in name_uni:
        name_list.append(i)
    name_enter = st.selectbox("Enter Company Name:",name_list)

    # Selected Names Sector,Industry,Country
    peers_by = st.radio("See Peers by:",("Sector and Industry wise","Market Cap"),index=0,horizontal=True)
    
    # MET SELECTION 
    issi = multidfC[multidfC[coName]==name_enter]
    sector_in = issi[sector].item()
    industry_in = issi[industry].item()
    

    if peers_by == "Market Cap":   
        col1,col2 = st.columns(2)
        
        
        dfCms = multidfC.sort_values(by=marketCap,ascending=False).reset_index()

        isel = dfCms.index[dfCms[coName]==name_enter].item()
        with col1:
            rop = st.slider("Range of Peers:",2,20)
            iselu = isel + rop
            iseld = isel - rop
            if isel <=rop:
                pmdf = dfCms.iloc[:rop*2]

            else:
                pmdf =  dfCms.iloc[iseld:iselu]
        
        if st.session_state["marketSelect"] == "USA":
            
            with col2:    
                country_in = issi["COUNTRY"].item()
                country_selected = st.multiselect("Country:",pmdf["COUNTRY"].unique(),country_in)
                selall = st.checkbox("Select All",key="countryselall")
                if selall:
                     country_selected = pmdf["COUNTRY"].unique()
                ispmdf=pmdf[pmdf["COUNTRY"].isin(country_selected)]
        else:
                ispmdf = pmdf
                
         
#range_y
    else:
        col1,col2,col3 = st.columns(3)
        
        with col1:
            sector_selected = st.multiselect("Sector:",multidfC[sector].unique(),sector_in)
        
        with col2:
            inudstry_list = multidfC[multidfC[sector].isin(sector_selected)][industry].unique().tolist()
            industry_selected = st.multiselect("Industry:",inudstry_list,industry_in)
            sel_all = st.checkbox("Select All")
            if sel_all:
                industry_selected = inudstry_list

        if st.session_state["marketSelect"] == "USA":
            with col3:
                country_in = issi["COUNTRY"].item()
                pseldf=multidfC[(multidfC[sector].isin(sector_selected)) & (multidfC[industry].isin(industry_selected))]
        
                country_selected = st.multiselect("Country:",pseldf["COUNTRY"].unique(),country_in)
                selall = st.checkbox("Select All",key="countryselall")
                if selall:
                     country_selected = pseldf["COUNTRY"].unique()

            issidf=multidfC[(multidfC[sector].isin(sector_selected)) & (multidfC[industry].isin(industry_selected))& (multidfC["COUNTRY"].isin(country_selected))]
            
        else:
            issidf=multidfC[(multidfC[sector].isin(sector_selected)) & (multidfC[industry].isin(industry_selected))]
        
        pisdf=issidf.sort_values(by=marketCap,ascending=False).reset_index()
        
        isel = pisdf.index[pisdf[coName]==name_enter].item()

        rop = st.slider("Range of Peers:",2,20)
        iselu = isel + rop
        iseld = isel - rop
        if isel <=rop:
           ispmdf = pisdf.iloc[:rop*2]

        else:
           ispmdf =  pisdf.iloc[iseld:iselu]

        

    mcapindex = multidfC.columns.tolist().index(marketCap)
    peindex = multidfC.columns.tolist().index(pe)
    col1,col2,col3,col4 = st.columns(4)
    indusindex = multidfC.columns.tolist().index(industry)
    with col1:   
        x_axis_met = st.selectbox("Select X-Axis",multidfC.columns,index=mcapindex,key="xaxispc")

    with col2:
        y_axis_met = st.selectbox("Select Y-Axis",multidfC.columns,index=peindex,key="yaxispc")

    with col3: 
        marker_size = st.selectbox("Marker Size",multidfC.columns,index=mcapindex,key="markersize")

    with col4: 
        marker_color = st.selectbox("Marker Color",multidfC.columns,index=indusindex,key="markercolor")

    fig = px.scatter(ispmdf,x=x_axis_met,y=y_axis_met,color=marker_color,size=marker_size,size_max=40,text=coName)

    xh = issi[x_axis_met].tolist()
    yh= issi[y_axis_met].tolist()
    fig.add_trace(go.Scatter(x=xh, y=yh, mode = 'markers',marker_symbol = 'star',marker_size = 60,opacity=0.5,fillcolor="orange",name=issi[coName].item()))
    fig.update_layout(dragmode='select',newselection=dict(line=dict(color='blue')), activeselection=dict(fillcolor='yellow'))

    selection = plotly_events(fig,click_event=False,select_event=True)

        
        



   
    # CLICKABLE EVENTS GENERATED 
    name_selected=[]
    for el in selection:
        x=el['x']
        y=el['y']
        nsdf=multidfC[(multidfC[x_axis_met]==(x)) & (multidfC[y_axis_met]==(y))]
        name_sel = nsdf[coName].item()
        if name_sel not in name_selected:
            name_selected.append(name_sel)

    if len(name_selected) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select - to perform Analysis.")
        st.stop()
    
    name_selected=st.multiselect("Company Name Selected:",ispmdf[coName].unique(),default=name_selected)

elif name_search == "Screener":
    
    return_mode_value = DataReturnMode.FILTERED_AND_SORTED
    update_mode=GridUpdateMode.SELECTION_CHANGED
    
    col1,col2 = st.columns([12,2])
    with col2:
        resetFilter = st.button("Reset Filters")
     

    if resetFilter:
        grid_return = AgGrid(multidfC,height=400,gridOptions=gridOptions,data_return_mode=return_mode_value,theme="streamlit",allow_unsafe_jscode=True,key="resetAg")      
        screendfC = grid_return['data']
    
    else:
        grid_return = AgGrid(multidfC,height=400,gridOptions=gridOptions,data_return_mode=return_mode_value,theme="streamlit",allow_unsafe_jscode=True,key="Aggrid")    
        screendfC = grid_return['data']

    try:
        xindex = screendfC.columns.tolist().index(marketCap)
        yindex = screendfC.columns.tolist().index(pe)
    except:
        xindex = screendfC.columns.tolist().index(marketCap)
        yindex = len(screendfC.columns) - 1

    col1,col2,col3,col4 = st.columns(4)
    indusindex = screendfC.columns.tolist().index(industry)
    
    with col1:   
        x_axis_met = st.selectbox("Select X-Axis",screendfC.columns,index=xindex,key="xaxispc")

    with col2:
        y_axis_met = st.selectbox("Select Y-Axis",screendfC.columns,index=yindex,key="yaxispc")

    with col3: 
        marker_size = st.selectbox("Marker Size",screendfC.columns,index=xindex,key="markersize")

    with col4: 
        marker_color = st.selectbox("Marker Color",screendfC.columns,index=indusindex,key="markercolor")

    fig = px.scatter(screendfC,x=x_axis_met,y=y_axis_met,color=marker_color,size=marker_size,size_max=40,text=coName)
    
    name_star = []
    for name in grid_return['selected_rows']:
        name_star.append(name[coName])
        
    issi = screendfC[screendfC[coName].isin(name_star)]
    xh = issi[x_axis_met].to_list()
    yh= issi[y_axis_met].to_list()
  
    fig.add_trace(go.Scatter(x=xh, y=yh, mode ='markers',marker_symbol = 'star',marker_size = 60,opacity=0.5,fillcolor="orange",name="selected companies"))

    selection = plotly_events(fig,click_event=False,select_event=True)


        

    # CLICKABLE EVENTS GENERATED 
    name_selected=[]
    for el in selection:
        x=el['x']
        y=el['y']
        nsdf=screendfC[(screendfC[x_axis_met]==(x)) & (screendfC[y_axis_met]==(y))]
        name_sel = nsdf[coName].item()
        if name_sel not in name_selected:
            name_selected.append(name_sel)

    if len(name_selected) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select - to perform Analysis.")
        st.stop()


    name_selected=st.multiselect("Company Name Selected:",screendfC[coName].unique(),default=name_selected)


# NAME SEARCH INDIVIDUALLY
else:
    name_uni = dfC.sort_values(by=marketCap,ascending=False)[coName].dropna().unique()
    name_list = []
    for i in name_uni:
        name_list.append(i)
    name_selected = st.multiselect("Enter Company Name:",name_list,default=name_list[0])



if len(name_selected) == 0 :
    st.warning("No Companies Selected! Change above selections to continue!")
    st.stop()

#if len(name_selected)>30:
#    st.warning("Max 30 companies can be selected at a time!")
#   st.stop()




st.header("TECHNICAL ANALYSIS")

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




def ytickData():
    ticker_selected=dfC[dfC[coName].isin(name_selected)].loc[:,updatedTicker].to_list()
    ticker_data = yf.download(ticker_selected,start=sd,end=ed)
    colname = {}
    if len(ticker_selected) == 1:
        tickdata=ticker_data[closeType].to_frame()
        vol_data = ticker_data['Volume'].to_frame()
        colname[ticker_selected[0]]= name_selected[0]

    else:
        tickdata=ticker_data[closeType]
        vol_data = ticker_data['Volume']
        for t in tickdata:
            colname[t]=' '.join(dfC[dfC[updatedTicker]==t][coName].to_list())

    tickdata.rename(columns=colname,inplace=True)
    vol_data.rename(columns=colname,inplace=True)

    return ticker_data,ticker_selected,tickdata,vol_data

ticker_data,ticker_selected,tickdata,vol_data=ytickData()



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
    indexData = tickdata.copy()
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
    

    
    ds,de = st.select_slider("Date Range:",options=date_list,value=(date_list[0],date_list[-1]),key="indexdatesl")

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
        rsi_name = st.selectbox("Select Company:",name_selected,index=0)
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


            @st.experimental_memo
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
                return fig
            
            @st.experimental_memo
            def optimum ():
                
                RSI.table()    

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
                fig


                                
              



        
        RSI.signal()
        fig = RSI.chart()
        st.plotly_chart(fig,use_container_width=True)
        
        with st.expander("See Table:"):
            rsi_signal


        get_optimum = st.button("Get Optimum")

        if get_optimum:
            fig=RSI.optimum()
            st.plotly_chart(fig,use_container_width=True)
            

    

with tab5:
    ema_name = st.selectbox("Select Company:",name_selected,index=0,key="emas")
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
            
            optimumEMA = pd.DataFrame()
            
            profit = []
            ema_range = [] 
            for i in range(10,110,10):
                for u in range(250,10,-10):
                    if (u-i) < 10:
                        pass

                    else:
                        EMA.signal(i,u,display="No")
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
        EMA.optimum()



with tab6:
    isdfC = dfC[dfC[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)
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
                per_name = st.selectbox("Select Company:",name_selected,index=0,key="pname")
                ticker_selected_perf=dfC[dfC[coName]==per_name].loc[:,updatedTicker].to_list()

                if len(name_selected) == 1: 
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

        date_list=tickdata.index.date
        ds,de = st.select_slider("Date Range:",options=date_list,value=(date_list[0],date_list[-1]),key="Hmapdatesl")
        def HeatMap():
            mrh = pd.DataFrame()  
            
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

            st.plotly_chart(fig,use_container_width=True)

        Hmap = HeatMap()
            



with tab9:
    try:
        option_name= st.selectbox("See Options for:",name_selected,index=0)
        
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




st.header("FUNDAMENTAL ANALYSIS")
#TABS

tab1, tab2, tab3 , tab4, tab5, tab6, tab7, tab8,tab9,tab10,tab11,tab12 = st.tabs(["Peer Stats","Radar","Peer Financial Analysis","Common FS","Financial Statements","Value","Business Description","Earnings Date","Links","ShareHolding","Extra Stats","Perform Valuation"])
#color scale
heatmap_colorscale_percent = [[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]]
heatmap_colorscale_growth = [[0,"red"],[0.1,"yellow"],[0.3,"green"],[0.7,"blue"],[1,"purple"]]


period_check = dfF[dfF[coName].isin(name_selected)][year].unique()

if len(period_check)==0:
    st.warning("No Data Available for these Companies")
    st.stop()


with tab1:
    # PEER STATS 

    #1 Market Cap,PE,PCF
    isdfC = dfC[dfC[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)
    mc_bar = isdfC[[coName,marketCap,pe,pcf]].sort_values(by=marketCap)

    isdf = dfF[dfF[coName].isin(name_selected)]
    
        
    isrdf = isdf.pivot_table(index=coName,columns=year,values=rev_type)
    ismdf = isdf.pivot_table(index=coName,columns=year,values=marketCap)


    col1,col2 = st.columns([3,10])

    with col1:
        def PSCTR():
            pradio = psct
            return pradio

        psct = st.radio('Chart Type:',("Bar","Pie"),index=0,horizontal=True,on_change=PSCTR)
        
        pradio = PSCTR()
        if pradio == "Bar":
            fig1=px.bar(isdf,x=marketCap,y=coName,title=marketCap,animation_frame=year, animation_group=coName,text_auto='.2s',orientation="h")
            fig2= px.bar(isdf, x=rev_type, y=coName,title=rev_type,animation_frame=year, animation_group=coName,text_auto='.2s',orientation="h")
            fig1.update_yaxes(dtick=1)
            fig2.update_yaxes(dtick=1)
            fig1.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
            fig2.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})
            
        
        else:
            colname_last = isrdf.columns[-1]
            colname_first = isrdf.columns[0]
            colname = st.number_input("Select Year:",value=colname_last,max_value=colname_last,min_value=colname_first)
            revpie=isrdf.loc[:,colname].to_frame(name=colname)
            mcpie = ismdf.loc[:,colname].to_frame(name=colname)
            fig1 = px.pie(mcpie,values=colname, names=mcpie.index,title="Market Cap")
            fig2= px.pie(revpie, values=colname, names=revpie.index,title=rev_type)
    
            

    with col2:
        
        st.write(" ")

    

    col1,col2 = st.columns(2)
    
    
    fig3 = px.bar(mc_bar, x=pe, y=coName, text_auto='.2f',orientation='h')
    fig4 = px.bar(mc_bar, x=pcf, y=coName,text_auto='.2f', orientation='h')


    with col1:
        st.plotly_chart(fig1)

    with col2:
        st.plotly_chart(fig2)


    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig3)
    with col2:
        st.plotly_chart(fig4)


# DIFFUSION 
with tab2:


    # PERIOD SELECTION 
    
    #period_selected=st.multiselect("Period:",options=dfF[year].unique(),default=dfF[year].unique()[:2])
    
    isdf = dfF[dfF[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)


    col1,col2,col3 = st.columns(3)    
    with col1:
        period_type = st.radio("Period Type:",("Multi-Year","Single Year"),horizontal=True)

    period = sorted(isdf[year].unique())

    
    if period_type == "Multi-Year":
        sy,ey=st.select_slider("Year:",options=period,value=(period[-4],period[-1]))
    
    else:
        yeMax=max(period)
        
        ye=st.slider("Year:",min_value=2010, max_value=2022,value=2021)
    
    with col2:
        met_selection_type = st.radio("Metrics",("Preselected","Choose your own"),index=0,horizontal=True)
    
    if met_selection_type == "Preselected":
            met_list = [rev_type,fcf,gm,ebitda_m,npm,d_e,c_r,roic]
            growth_met = dfM[dfM["Multi-Year Format"]=="growth"]["title"].tolist()
            avg_met = dfM[dfM["Multi-Year Format"]=="average"]["title"].tolist()


    else:
        with st.expander("Create Your Radar"):
            dfRM = dfM.iloc[:,5:]
            builder = GridOptionsBuilder.from_dataframe(dfRM)
            builder.configure_default_column(groupable=True,editable=True)
            builder.configure_selection(selection_mode="multiple",use_checkbox="enable")
            gridOptionR = builder.build()
            grid_rating = AgGrid(dfRM,height=400,gridOptions= gridOptionR,theme="streamlit",allow_unsafe_jscode=True) 
            selmet=grid_rating['selected_rows']
            dfRMS = grid_rating['data']
            growth_met = dfRMS[dfRMS["Multi-Year Format"]=="growth"]["title"].tolist()
            avg_met = dfRMS[dfRMS["Multi-Year Format"]=="average"]["title"].tolist()

            met_list = []
            for i in range(len(selmet)):
                met_list.append(selmet[i]['title'])


    with col3:
        rating_type = st.radio("Rating Type",("Relative","Absolute"),index=0,horizontal=True)

    if rating_type == "Absolute":
        with st.expander("Set Rating Scale"):
                ratingabsdf = pd.DataFrame()
                ratingabsdf['index'] = ["extreme(-)","Worst","Negative","Neutral","Average","Great","extreme(+)"]
                ratingabsdf.set_index('index')
                for metrics in met_list:
                    if metrics in [rev_type,fcf,roic,npm]:
                            bins = [-100000,-0.1,0,0.07,0.15,0.3,100000]

                    elif metrics == c_r:
                            bins = [0,0.05,0.2,0.75,1.5,2.5,100000]
                            labels=[-2,-1,0,1,2,3]  
                    
                    elif metrics ==d_e:
                            bins = [0,0.05,1,1.5,3,5,100000]
                    
                    else:
                        bins = [-100000,-0.1,0,0.1,0.25,0.5,100000]

                    
                    ratingabsdf.loc[:,metrics]=bins
                
                
                builder = GridOptionsBuilder.from_dataframe(ratingabsdf)
                builder.configure_default_column(editable=True)
                gridOptionR = builder.build()
                grid_rating = AgGrid(ratingabsdf,height=400,gridOptions= gridOptionR,theme="streamlit",allow_unsafe_jscode=True)  
                absrate = grid_rating['data']


    def radar_cal():
        raddf = pd.DataFrame()
        radlis  = []
        for metrics in met_list:
            isdfme= isdf.pivot_table(index=coName,columns=year,values=metrics,sort=False)
            
            if metrics in growth_met:
                        if period_type == "Single Year":
                            isdfmet = isdfme.loc[:,ye-1:ye].pct_change(axis=1).mean(axis=1)

                        else:
                            isdfmet = isdfme.loc[:,sy:ey].pct_change(axis=1).mean(axis=1)        
                
            else:
                if period_type == "Single Year":
                    isdfmet= isdfme.loc[:,ye].mean(axis=1)
                
                else:
                    isdfmet= isdfme.loc[:,sy:ey].mean(axis=1)
            
            spsdf = isdfmet.to_frame()

            if rating_type == "Absolute":
                labels=[-2,-1,0,1,2,3]
                spsdf[f"{metrics}"]=pd.cut(spsdf[0],bins=absrate[metrics].values.tolist(),labels=labels,right=False)

                radlis.append(spsdf.drop(0,axis=1))

            else:
                superb=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.9)].index)
                great =list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.7)].index)
                average = list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.55)].index)
                neutral= list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.4)].index)
                negative=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.25)].index)
                worst=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.1)].index)

                for n in name_selected:                               
                    if n in superb:
                        raddf.loc[metrics,n] = 3
                    elif n in great:
                        raddf.loc[metrics,n] = 2
                    elif n in average:
                        raddf.loc[metrics,n] = 1
                    elif n in negative:
                        raddf.loc[metrics,n] = -1
                    elif n in worst:
                        raddf.loc[metrics,n] = -2
                    elif n in neutral:
                        raddf.loc[metrics,n] = 0
                    else:
                        raddf.loc[metrics,n] = 0
            
        
        if rating_type == "Absolute":
            radardata=pd.concat(radlis,axis=1).transpose()
        else:
            radardata=raddf

        col1,col2,col3 = st.columns(3)
        col = col1
        for name in radardata:
            with col:
                fig = go.Figure(data=go.Scatterpolar(r=radardata[name],theta=radardata.index,fill='toself'))

                fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                    visible=True
                    ),
                ),
                showlegend=False,
                title = name
                )

                st.plotly_chart(fig)
            if col == col1:
                col = col2
            
            elif col == col2:
                col = col3
            
            else:
                col = col1
        


    if met_selection_type == "Choose your own":
        runradar = st.button("Run")
        if runradar:
            radar_cal()



    else:    
        radar_cal()
    # RATING SCALE - RELATIVE 

    #0.9,0.7,0.55,0.4,0.25,0.1 
    


# FUNDAMENTAL SECTION 

with tab3:
    # PEER FINANCIAL ANALYSIS 

    st.header("Financial Statement Analyis")

    #Info Selected Data Frame = isdf 
    #Info Selected Pivot DF = ispdf 
    #gt = growth table 
    #fig1 = absolute values chart 
    #fig2 = growth chart dfM[
    
    reportPeriod = st.radio("Report Period:",("Annual","Quarter"),index=0,horizontal=True)

    if reportPeriod == "Annual":
        isdf = dfF[dfF[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)
        periodType = year

    else:
        isdf = dfQ[dfQ[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)
        periodType = Date


    # Metric  1
    def DisplayMetric(count=1,st_type=st1,mt_type=rev_type,gt_display_overide=True):
        st.subheader(f"METRIC {count}")
        col1, col2,col3 = st.columns(3)

        with col1:
            statements = st.selectbox(
                "Select Statement:",
                dfM["Statement"].unique(),
                index=dfM["Statement"].unique().tolist().index(st_type),
                key=f"stk{count}"
            )
            ms = dfM[dfM["Statement"]==(statements)]
        
        try:
            mtl=ms["title"].unique().tolist()  #metriclist
            mtl[mtl.index(mt_type)] = mtl[0]
            mtl[0] = mt_type

        except:
            mtl = ms["title"].unique().tolist() 

        
        
        with col2:
            metrics = st.selectbox(
                "Select Metrics:",
                mtl,
                key=f"mt{count}"
            )
        try:
            ispdf = isdf.pivot_table(columns=periodType,index=coName,values=metrics,sort=False)#.sort_index()
            gt = ispdf.pct_change(axis=1)
            
        except:
            st.warning("No Financial Data for selected companies")

        with col3:
                period_range = st.slider("Number of Periods:",0,len(ispdf.columns),(0,5),key=f"per{count}")

                ys = period_range[0]
                ye = period_range[1]            
                
                if ys == 0:
                    ispdfS = ispdf.iloc[:,-ye:]
                    gtf = gt.iloc[:,-ye:]
                    

                else:
                    ispdfS = ispdf.iloc[:,-ye:-ys]
                    gtf = gt.iloc[:,-ye:-ys]

        try:
            
                    #ROW 2 
            col1,col2,col3,col4,col5 = st.columns([10,2,2,2,2])

            
            with col1:
                bcType = st.radio("Bar Chart Grouping:",("Date-wise","Company-wise"),index=1,horizontal=True)
                if bcType == "Company-wise":
                    fig1 = go.Figure()
                    for col in ispdfS.columns.to_list():
                        fig1.add_trace(go.Bar(x=ispdfS.index, y=ispdfS[col], name = str(col)))

                else:
                    ispdfST = ispdfS.transpose()  
                    fig1 = px.bar(ispdfST, x=ispdfST.index,y=ispdfST.columns,barmode='group',title=f"{metrics}")


            with col2:

                if gt_display_overide == True:
                    gt_display = tog.st_toggle_switch(label="See Growth Chart", 
                                                        key=f"gtog{count}", 
                                                        default_value=True, 
                                                        label_after = False, 
                                                        inactive_color = '#D3D3D3', 
                                                        active_color="#11567f", 
                                                        track_color="#29B5E8"
                                                        )

                else:
                    gt_display = tog.st_toggle_switch(label="See Growth Chart", 
                                                        key=f"gtog{count}", 
                                                        default_value=False, 
                                                        label_after = False, 
                                                        inactive_color = '#D3D3D3', 
                                                        active_color="#11567f", 
                                                        track_color="#29B5E8"
                                                        )

            if gt_display ==True:
                with col3:
                    fgvalues = st.selectbox("Filter Values",("See All","Greater Than","Greater than & Equal to","Less Than","Less Than & Equal to","In Between"))
                
                if fgvalues == "In Between":
                    with col4:
                        numsf = st.number_input("Number from(in %):",min_value=-10000,max_value=10000,value=0)
                    with col5:
                        numef = st.number_input("Number to(in %):",min_value=-10000,max_value=10000,value=10)
                else:
                    with col4:
                        numf = st.number_input("Number(in %):",min_value=-10000,max_value=10000,value=0)


                if fgvalues == "Greater Than":
                        gtf=gt[gt>(numf/100)]
                
                elif fgvalues == "Greater than & Equal to":
                        gtf=gt[gt>=(numf/100)]
                
                elif fgvalues == "Less Than":
                        gtf=gt[gt<(numf/100)]

                elif fgvalues == "Less Than & Equal to":
                        gtf=gt[gt<=(numf/100)]
                
                elif fgvalues == "In Between":
                        gtf=gt[gt>=(numsf/100)&gt<=(numef/100)]


                col1,col2 = st.columns(2)

                with col1:
                    st.plotly_chart(fig1,use_container_width=True)

                with col2:
                    

                    
                    
                    fig2 = px.imshow(gtf.values, text_auto=".2%", x=gtf.columns,y=gtf.index,aspect="auto",title=f"{metrics}-Growth")                    
                    fig2.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=heatmap_colorscale_growth)

                    #fig2.update_xaxes(dtick=1)
                    st.plotly_chart(fig2)
                
            else:
                st.plotly_chart(fig1,use_container_width=True)
        


        except:
            st.warning("No Financial Data for selected companies")



        with st.expander("Add Comment"):     
                    col1, col2, col3 = st.columns(3)


                    with col1:        
                        st.subheader("Company Name")
                    
                    with col2:
                        st.subheader(f"{metrics}-Rating")
                        if gt_display_overide==True:
                            ptype=st.radio("Select Type:",("Absolute","Growth"),horizontal=True,key=f"ratp{count}",index=1)
                        else:
                            ptype=st.radio("Select Type:",("Absolute","Growth"),horizontal=True,key=f"ratp{count}",index=1)

                        # HAVE TO WORK ON THIS                    
                        if ptype =="Absolute":
                            sps = ispdf.mean(axis=1)
                            spsdf = sps.to_frame()

                            # add parameteres 
                            s = st.number_input("Superb:",key=f"sup{count}")
                            g = st.number_input("Great:",key=f"gret{count}")
                            a = st.number_input("Avg:",key=f"a{count}")
                            neu = st.number_input("Neutral:",key=f"neu{count}")
                            neg = st.number_input("Negative:",key=f"neg{count}")
                            wor = st.number_input("Worst:",key=f"wor{count}")
                        
                            superb=list(spsdf[spsdf[0]>s].index)
                            great =list(spsdf[(spsdf[0]>g)&(spsdf[0]<s)].index)
                            average =list(spsdf[(spsdf[0]>a)&(spsdf[0]<g)].index)
                            neutral =list(spsdf[(spsdf[0])>neu&(spsdf[0]<a)].index)
                            negative =list(spsdf[(spsdf[0]>neg)&(spsdf[0]>neg)].index)
                            worst =list(spsdf[spsdf[0]<wor].index)
                            
                        else:
                            
                            sps=gtf.mean(axis=1)

                            spsdf = sps.to_frame()
                        
                            superb=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.9)].index)
                            great =list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.7)].index)
                            average = list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.55)].index)
                            neutral= list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.4)].index)
                            negative=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.25)].index)
                            worst=list(spsdf[spsdf[0]>spsdf[0].quantile(q=0.1)].index)
                            

                    with col3:
                        st.subheader("Enter Comment")

                    for i in range(len(name_selected)):
                        col1,col2,col3=st.columns(3)       
                        with col1:    
                            name_selected[i]


                        with col2:
                            if name_selected[i] in superb:
                                sl_value = "3-Superb"
                            elif name_selected[i] in great:
                                sl_value = "2-Great"
                            elif name_selected[i] in average:
                                sl_value = "1-Average"
                            elif name_selected[i] in negative:
                                sl_value = "-1-Negative"
                            elif name_selected[i] in worst:
                                sl_value = "-2-Worst"
                            elif name_selected[i] in neutral:
                                sl_value = "0-Neutral"
                            else:
                                sl_value = "0-Neutral"


                            ratsli=st.select_slider("Rating",options=["-2-Worst","-1-Negative","0-Neutral","1-Average","2-Great","3-Superb"],value=sl_value,key=f"ratslid{count}-{i}")
                            

                            if ratsli == "3-Superb":
                                rating = 3
                            
                            elif ratsli == "2-Great":
                                rating = 3
                            elif ratsli == "1-Avergae":
                                rating = 1
                            elif ratsli == "0-Neutral":
                                rating = 0
                            elif ratsli == "-1-Negative":
                                rating = -1
                            elif ratsli == "-2-Worst":
                                rating = -2
                            else: 
                                rating =0 

                        with col3:

                            if st.session_state["marketSelect"] == "USA":
                                fsacomment_usa = st.text_input("Comment:",key=f"fsat{count}-{i}-USA") 

                            elif st.session_state["marketSelect"] == "India":
                                fsacomment_ind = st.text_input("Comment:",key=f"fsat{count}-{i}-IND")                  
                            
                            elif st.session_state["marketSelect"] == "Canada":
                                fsacomment_can = st.text_input("Comment:",key=f"fsat{count}-{i}-CAN")                  






    DisplayMetric()


    add_metrics = st.radio("Add More Metrics:",("Yes","No","Preselect"),index=1,horizontal=True)

    if add_metrics == "Yes":
        col1,col2 = st.columns([1,10])        
        with col1:
            num_of_charts = st.number_input("Add Charts:",value=1)

        with col2:
            st.write(" ")


        count = 2 
        for n in range(num_of_charts):
            DisplayMetric(count=count,gt_display_overide=False)
            count +=1

    elif add_metrics == "Preselect":   
            DisplayMetric(count=2,st_type=st2,mt_type=fcf)
            DisplayMetric(count=3,st_type=st3,mt_type=roic,gt_display_overide=False)
            DisplayMetric(count=4,st_type=st4,mt_type=ebitda_m,gt_display_overide=False)
            DisplayMetric(count=5,st_type=st4,mt_type=npm,gt_display_overide=False)
            DisplayMetric(count=6,st_type=st5,mt_type=d_e,gt_display_overide=False)
            DisplayMetric(count=7,st_type=st5,mt_type=c_r,gt_display_overide=False)
    else:
        pass



with tab4:
    
    isdf = dfF[dfF[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False)
    isdft = dfF[dfF[coName].isin(name_selected)].sort_values(by=marketCap,ascending=False).transpose()
    
    col1,col2,col3 = st.columns(3)

    
    selected_statements =[IS,BS,CF]
    with col1:
        statements = st.selectbox(
            "Select Statement:",
            selected_statements,
            index=0,
            key=f"stkcs"
        )
        ms = dfM[dfM["Statement"]==(statements)]
    
    statementsCat =dfM["Statement Category"].unique().tolist()
    stTotals =dfM["Statement Totals "].unique().tolist()
    cs ={}
    for stmen in statementsCat:
        stList = dfM[dfM["Statement Category"] == stmen]["title"].to_list()
        cs[stmen] = stList 

    cst = {}
    for stmen in stTotals:
        stList = dfM[dfM["Statement Totals "] == stmen]["title"].to_list()
        cst[stmen] = stList 


    if statements == IS:
        mt_type = revenue
        cat_key = {"Expense":cs["expense"],"Income":cs["income"],"Others":cs["others"]}
    
    elif statements == BS:
        mt_type = assets
        cat_key = {"Balance Sheet Totals":cst["bsTotal"],"Current Assets":cs["currentAssets"],"Non-Current Assets":cs["noncurrentAssets"],"Intangibles":cs["intangibles"],"Current Liabilities":cs["currentLiab"],"Non-Current Liabilities":cs["noncurrentLiab"],"Equity":cs["equity"],"Tax":cs["tax"]}

    elif statements == CF:
        mt_type = cfo
        cat_key = {"Cash Flow Totals":cst["cfTotal"],"Operating CF":cs["operations"],"Investing CF":cs["investments"],"Financing CF":cs["financing"]}

    else:
        mt_type = revenue
        cat_key = {"Expense":cs["expense"],"Income":cs["income"],"Others":cs["others"]}



    with col2:
        selCat = st.selectbox("Select Category",cat_key.keys())

    sel_base = dfM[dfM["Statement"]==( statements)]
    metric_base = sorted(sel_base['title'].unique().tolist())
    
    corps = st.radio("Display:",("Common Sized","Per Share"),horizontal=True)

    if corps == "Common Sized":
        with col3:
            baseMet = st.selectbox(
                "Select Metrics to base common size on:",
                metric_base,
                index=metric_base.index(mt_type),
                key=f"mtcs"
        )
        tick_format = "0.2%"
        bar_text = "0.2%"

    else: 
        baseMet = 'Total Shares Outstanding'
        tick_format = "0.2f"
        bar_text = "0.2f"


    period_range = st.slider("Number of Periods:",0,len(isdf[year].unique()),(0,4),key=f"percs")

    ys = period_range[0]
    ye = period_range[1]
    
    try:
        cat_key[selCat].remove(baseMet)
        selected_info =cat_key[selCat]
    except:
            selected_info = cat_key[selCat]


    col1, col2 = st.columns(2)
    col = col1
    
    for metrics in selected_info:
        with col:
            isdf[f"{metrics}-cs"] = isdft.loc[metrics]/isdft.loc[baseMet].replace(0,1)
            ispdf = isdf.pivot_table(index=coName,columns=year,values=f"{metrics}-cs",sort=False)
            try:
                if ys == 0:
                    fig = px.bar(ispdf,x=ispdf.index,y=ispdf.columns[-ye:],title=f"{metrics}",text_auto=bar_text ,barmode="group")
                    
                
                else:
                    fig = px.bar(ispdf,x=ispdf.index,y=ispdf.columns[-ye:ys],title=f"{metrics}",text_auto=bar_text ,barmode="group")
                
                if corps == "Common Sized":
                    fig.update_layout(yaxis_tickformat = tick_format)
                

                st.plotly_chart(fig)

            except:
                pass
                        
            
            
        
        if col == col1:
            col = col2
        
        elif col == col2:
            col = col1
        

with tab5:
    name_FS = st.selectbox("Enter Company Name:",name_selected,index=0,key="Name_FS")
    

    col1,col2 = st.columns(2)

    with col1:
            statement_type = st.radio("Statement Type:",("Income Statement","Balance Sheet","Cash Flow","Ratios"),horizontal=True,key="cfdis")

            
    with col2:
            report_period = st.radio("Report Period:",("Annual","Quarterly"),index=1,horizontal=True,key="FSrp")
            

    if statement_type == "Income Statement":
        stFS = "IS"

    elif statement_type == "Balance Sheet":
        stFS = "BS"

    elif statement_type == "Cash Flow":
        stFS = "CF"

    elif statement_type == "Ratios":
        stFS = "Ratio"
    
    metSt = dfM[dfM["Statement"]==stFS].sort_values(by="Metric Order",ascending=True)["title"].to_list()
    colFS = [Date]
    for m in metSt:
        colFS.append(m)
    
    if report_period == "Annual":
        DF = dfF[dfF[coName]==name_FS][colFS]
    
    else:
        DF = dfQ[dfQ[coName]==name_FS][colFS]

    dfFS = DF.dropna(subset=[Date])
    dfFS.set_index(Date,inplace=True)
    
    dfFST = dfFS.transpose()

    dfFSG= dfFS.sort_index().pct_change()
    
    
    col1,col2 = st.columns(2)
    with col1:
        met_options = dfFS.columns.to_list()
        if 'metSel' not in st.session_state:
            st.session_state['metSel']=met_options[:2]
        
        st.session_state['metSel']=st.multiselect("Select Metrics:",options=met_options,default=met_options[:2])
        
        
    with col2:
        period_range = st.slider("Number of Periods:",0,len(dfFS.index),(0,5),key=f"FSper")
        ys = period_range[0]
        ye = period_range[1]            
        
        dfFS = dfFS.sort_index(ascending=False).iloc[ys:ye]

        
        dfFSGT= dfFSG[st.session_state['metSel']].sort_index(ascending=False).transpose().iloc[:,ys:ye]
        
    
    fig_is = px.bar(dfFS,x=dfFS.index,y=dfFS[st.session_state['metSel']].columns,barmode="group",title=f"{statement_type}-Annual")

    fig_isg = px.imshow(dfFSGT.values,x=dfFSGT.columns,y=dfFSGT.index, text_auto=".2%",title=f"{statement_type}-Annual Growth")
    fig_isg.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=heatmap_colorscale_growth)
    

    col1,col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_is)
    with col2:
        st.plotly_chart(fig_isg)
    
    with st.expander("See Table:"):
        col_string = map(str, dfFST.columns)
        dfFST.columns = col_string
        dfFST.reset_index(inplace=True)
        builder = GridOptionsBuilder.from_dataframe(dfFST)
        builder.configure_default_column(editable=True,groupable=True,filterable=True,enableRowGroup=True)
        builder.configure_selection(selection_mode = "multiple", rowMultiSelectWithClick=True)
        gridOptionR = builder.build()
        return_mode_value = DataReturnMode.FILTERED_AND_SORTED
        update_mode=GridUpdateMode.MANUAL
        dfFSTab =  AgGrid(dfFST,gridOptions= gridOptionR,update_mode=update_mode,data_return_mode=return_mode_value,theme="streamlit",key=f"FSAgTable")

    
    metSelected = []
    for sr in dfFSTab['selected_rows']:
        metSelected.append(sr["index"])


    st.session_state['metSel'] = metSelected
    






with tab6:

    # VALUE CHART 
    st.header("Value Analysis")
    if len(ticker_selected) > 1:
            visdf=dfF[dfF[coName].isin(name_selected)&(dfF[year]==2021)].sort_values(by=marketCap,ascending=True).loc[:,[coName,updatedTicker,year,fcf,'Fair Value (30)', 'Fair Value (15)','Fair Value (45)']]
            
            close_last=ticker_data[closeType].iloc[-1].to_frame()

            close_last.rename(columns={close_last.columns.item():"Close"},inplace=True)
            close_last.index.name = "Ticker"
            
            close_last.reset_index(inplace = True)
            
            vc=visdf.merge(close_last,left_on=updatedTicker,right_on="Ticker",how="inner")
            vc.drop([updatedTicker,"Ticker"],axis=1,inplace=True)
            vc['Close - % of FV 15'] = vc['Close']/vc['Fair Value (15)'] - 1
            vc['Close - % of FV 30'] = vc['Close']/vc['Fair Value (30)'] - 1
            vc['Close - % of FV 45'] = vc['Close']/vc['Fair Value (45)'] - 1
            
            negfcf = vc[vc[fcf]<=0][coName].unique().tolist()
            vc.loc[vc[coName].isin(negfcf),['Close - % of FV 15','Close - % of FV 30','Close - % of FV 45']] = 0
        
            fig=px.bar(vc,x=['Close - % of FV 30','Close - % of FV 15', 'Close - % of FV 45'],y=coName,orientation="h",barmode='overlay',color_discrete_sequence=["yellow", "green", "red"],text_auto="0.2%",title="Close % of Fair Value")
            st.plotly_chart(fig,use_container_width=True)

            with st.expander("See Table"):
                AgGrid(vc,height=300,theme="streamlit")

    # VALUE CHART 
    
    def value_chart():
        # Get Historical Data from YahooFinance

        if len(ticker_selected) == 1:
            price=ticker_data[closeType].to_frame().reset_index()
            price.rename(columns={closeType:ticker_selected[0]},inplace=True)
        else:
            price=ticker_data[closeType].reset_index()
            
        
        price['Year']=price['Date'].dt.year
        price.set_index(['Date','Year'],inplace=True)


        sel = dfF[dfF[coName].isin(name_selected)]

        vvs = sel[[coName,updatedTicker,marketCap,year,'Fair Value (30)', 'Fair Value (15)','Fair Value (45)']].sort_values(by=marketCap,ascending=False)
        
        val = vvs.drop(vvs[vvs[updatedTicker] == " "].index)
        
        vv_mcap = val.drop_duplicates(updatedTicker)
        vname_list = vv_mcap[coName].to_list()

        vname_selected = st.multiselect("Select Name:",options=vname_list,default=vname_list[0])
        
        vtick=vv_mcap[vv_mcap[coName].isin(vname_selected)][updatedTicker].to_list()
        

        col1,col2 = st.columns(2)
        col = col1
        for i in vtick:
            with col:
                price_info=price[i].to_frame().reset_index()
                vv=val[val[updatedTicker]==i].drop([updatedTicker,marketCap],axis=1)
                info=price_info.merge(vv,left_on='Year',right_on=year,how="left").drop(['Year'],axis=1)
                name_of_tick = dfC[dfC[updatedTicker]==i][coName].item()
                fig = px.line(info,x='Date',y=[i,'Fair Value (30)', 'Fair Value (15)','Fair Value (45)'],title=f"{name_of_tick}-{i}")
                st.plotly_chart(fig)
            
            if col == col1:
                col = col2
            else:
                col = col1

                        

    st.subheader("Value Chart")
    value_chart()



with tab7:
    try:
        bizdes= st.selectbox("See Business Description for:",name_selected,index=0)
        
        biz_descrip=dfC[dfC[coName]==(bizdes)].loc[:,"DESCRIPTION"].item()

        st.write(biz_descrip)

    
        officers = dfOff[dfOff["Company Name"]==bizdes]

        offCols = [] 
        for cols in officers:
            if cols not in ["TICKER","Market Code","Company Name"]:
                    offCols.append(cols)
        
        st.write("Management Info")
        st.dataframe(officers[offCols].reset_index(drop=True))


    except:
        st.write("Select a different Company Name or reload page!")



with tab8:
    # EARNINGS 
    st.subheader("Earning Dates")
    sel = dfC[dfC[coName].isin(name_selected)]
    earning_date = sel[[coName,'Upcoming Earnings Date','Recent Earnings Date']].set_index(coName)
    earning_date



with tab9:

    def make_clickable(link):
            # target _blank to open new window
            # extract clickable text to display for your link
            text = link.split('=')[0]
            return f'<a target="_blank" href="{link}">{text}</a>'

    if st.session_state["marketSelect"] == "USA":
        name_selected_link = st.selectbox("Select Name:",name_selected,index=0,key="USLink")
        
        cik_ticker = dfC[dfC[coName]==(name_selected_link)]["CIK"].astype("int").item()
        tickerLink = dfC[dfC[coName]==(name_selected_link)]["TICKER"].item()

        dfL = pd.DataFrame()
        dfL["LINKS"]=name_selected_link
        dfL["Company Website"] = dfC[dfC[coName]==(name_selected_link)]["WEBURL"]
        dfL["10-K"]=fr"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_ticker}&type=10-K&dateb=&owner=include&count=40&search_text="
        dfL["10-Q"]=fr"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik_ticker}&type=10-Q&dateb=&owner=include&count=40&search_text="
        dfL["Insider"]=f"https://www.sec.gov/cgi-bin/own-disp?action=getissuer&CIK={cik_ticker}"
        dfL["Subsidiary"]=f"https://www.sec.gov/cgi-bin/own-disp?action=getowner&CIK={cik_ticker}"
        dfL["Wiki"]=f"https://en.wikipedia.org/wiki/{name_selected_link}"
        dfL["Insider Activity"]=f"https://www.nasdaq.com/market-activity/stocks/{tickerLink}/insider-activity"
        dfL["Analyst Rating"]=f"https://www.nasdaq.com/market-activity/stocks/{tickerLink}/analyst-research"	
        dfL["Trading View"]=f"https://www.tradingview.com/chart/{tickerLink}"
        dfL["Stock Charts P&F"]=f"https://stockcharts.com/freecharts/pnf.php?c={tickerLink},P"

        dfL.set_index("LINKS",inplace=True)
        isdf = dfL.transpose()
        
    
        # link is the column with hyperlinks
        for col in isdf.columns:
            isdf[col] = isdf[col].apply(make_clickable)
        

        isdf = isdf.to_html(escape=False)

        st.write(isdf, unsafe_allow_html=True)


    else: 
        name_selected_link = st.selectbox("Links:",name_selected,index=0,key="OtherLink")
        name_selected_link
        tickerLink = dfC[dfC[coName]==(name_selected_link)]["TICKER"].item()
        webUrl = dfC[dfC[coName]==(name_selected_link)]["WEBURL"]
        
        dfL = pd.DataFrame()
        dfL["LINKS"]= " "
        dfL["Company Website"] = webUrl
        dfL["Trading View"] = f"https://www.tradingview.com/chart/{tickerLink}"
        dfL["Stock Charts P&F"] = f"https://stockcharts.com/freecharts/pnf.php?c={tickerLink}.IN,P"
        dfL["Stock Charts Seasonality"] = f"https://stockcharts.com/freecharts/seasonality.php?symbol={tickerLink}.IN"
        dfL["Market Smith"]=f"https://marketsmithindia.com/mstool/evaluation.jsp#/symbol/{tickerLink}"

        dfL.set_index("LINKS",inplace=True)
        
        isdf = dfL.transpose()
        
        for col in isdf.columns:
            isdf[col] = isdf[col].apply(make_clickable)
        
        isdf = isdf.to_html(escape=False)
        
        st.write(isdf, unsafe_allow_html=True)
    
    
with tab10: 
    shareholdAnal = st.radio("See",("Individually","Peer Comparison"),index=0,horizontal=True)

    if shareholdAnal == "Individually":
        name_selected_sh = st.selectbox("Select Name:",name_selected,index=0,key="ShareHoldName")
        
        dfSO = dfC[dfC[coName]==name_selected_sh][[coName,"SHARES OUTSTANDING","SHARES FLOAT"]]
        dfSO["SHARES % FLOAT"] = dfSO["SHARES FLOAT"]/dfSO["SHARES OUTSTANDING"]
        dfSO["SHARES % INSIDER"] = 1 - dfSO["SHARES % FLOAT"]
        dfSO.set_index(coName,inplace=True)
        dfSO = dfSO[["SHARES % FLOAT","SHARES % INSIDER"]].transpose()
        dfSO.index.name="Shares"
        dfSO.reset_index(inplace=True)

        figSO = px.pie(dfSO, values=name_selected_sh,names="Shares",title='%FLOAT vs %INSIDER')

        
        dfShp = dfC[dfC[coName]==name_selected_sh][[coName,"PERCENT INSTITUTIONS","PERCENT INSIDERS"]]
        dfShp.set_index(coName,inplace=True)
        dfShp = dfShp.transpose()
        dfShp.index.name = "Holding Percent"
        dfShp.reset_index(inplace=True)

        figP = px.pie(dfShp, values=name_selected_sh,names="Holding Percent",title='%INSTITUTE vs %INSIDER')


        col1,col2 = st.columns(2)

        with col1:
            st.plotly_chart(figSO)

        with col2:
            st.plotly_chart(figP)
            

        if st.session_state["marketSelect"] == "USA":
            tickerSh = dfC[dfC[coName]==name_selected_sh]["TICKER"].item()
            
            holdingType = st.radio("Holder Type:",("Institutions","Funds","Both"),index=2,horizontal=True)
            
            dfSh.columns = dfSh.columns.str.rstrip()

            
            if holdingType == "Instituions":
                dfSH = dfSh[(dfSh["TICKER"]==tickerSh)&(dfSh["HOLDER TYPE"]=="Institutions")]

            elif holdingType == "Funds":
                dfSH = dfSh[(dfSh["TICKER"]==tickerSh)&(dfSh["HOLDER TYPE"]=="Funds")]
            
            else:
                dfSH = dfSh[dfSh["TICKER"]==tickerSh]
                
            fig = px.pie(dfSH, values='TOTAL SHARES', names='NAME', title='SHAREHOLDING%')
            st.plotly_chart(fig)

            
            #figS = go.Figure()

            #figS.add_trace(go.Sunburst(
            #    labels=dfSh["NAME"],
            #    parents=dfSh["HOLDER TYPE"],
            #    values=dfSh['TOTAL SHARES'],
            #    domain=dict(column=1),
            #   maxdepth=2,
            #    insidetextorientation='radial'
            #))

            #st.plotly_chart(figS)
            with st.expander("See Table"):
                dfSH


    else:
        
        
        dfSO = dfC[dfC[coName].isin(name_selected)][[coName,"SHARES OUTSTANDING","SHARES FLOAT"]]
        dfSO["SHARES % FLOAT"] = dfSO["SHARES FLOAT"]/dfSO["SHARES OUTSTANDING"]
        dfSO["SHARES % INSIDER"] = 1 - dfSO["SHARES % FLOAT"]
        dfSO.set_index(coName,inplace=True)
        
        figSO = px.bar(dfSO, x=["SHARES % FLOAT","SHARES % INSIDER"],y=dfSO.index,title='%FLOAT vs %INSIDER',text_auto=".2%")

        
        dfShp = dfC[dfC[coName].isin(name_selected)][[coName,"PERCENT INSTITUTIONS","PERCENT INSIDERS"]]
        dfShp["PERCENT INSTITUTIONS"] =dfShp["PERCENT INSTITUTIONS"]/100
        dfShp["PERCENT INSIDERS"]=dfShp["PERCENT INSIDERS"]/100
        dfShp["PERCENT OTHERS/PUBLIC"] = 1 - (dfShp["PERCENT INSTITUTIONS"] + dfShp["PERCENT INSIDERS"])
        dfShp.set_index(coName,inplace=True)
        
        figP = px.bar(dfShp, x=["PERCENT INSTITUTIONS","PERCENT OTHERS/PUBLIC","PERCENT INSIDERS"],y=dfShp.index,title='%INSTITUTE vs %INSIDER',text_auto=".2%")


        col1,col2 = st.columns(2)

        with col1:
            st.plotly_chart(figSO)

        with col2:
            st.plotly_chart(figP)
            
        
        if st.session_state["marketSelect"] == "USA":
            tickerSh = dfC[dfC[coName].isin(name_selected)]["TICKER"].to_list()
        
            dfSH = dfSh[dfSh["TICKER"].isin(tickerSh)]
            

            columnOrder = []
            col3 = ["Company Name","TICKER","HOLDER TYPE"]
            for cols in col3:
                columnOrder.append(cols)

            for cols in dfSH:
                if cols not in columnOrder:
                    columnOrder.append(cols)

            colShAg = []
            col_dict = {}
            for col in columnOrder:
                col_dict["field"]=col
                colShAg.append(col_dict)
                col_dict = {} 

            gridOptions = {
            "columnDefs": colShAg,
                            
            "defaultColDef": {
                            "selection_mode":"multiple", 
                            "use_checkbox":False, 
                            "rowMultiSelectWithClick":True, 
                            "suppressRowDeselection":True,
                            "enableRowGroup": True,
                            "filter":True, 
                            "floatingFilter": True,
                            "floatingFilterComponent":"x",
                            "sortable":True,
                            "resizable":True,
                            "applyMiniFilterWhileTyping": True,
                                },
            "enableRangeSelection": True,
            "enableCharts": True,
            "enableChartToolPanelsButton": True,  
            "sideBar": ['filters','columns'],
                }
            
            return_mode_value = DataReturnMode.FILTERED_AND_SORTED
            update_mode=GridUpdateMode.MANUAL
            gSH = AgGrid(dfSH,height=300,gridOptions=gridOptions,data_return_mode=return_mode_value,update_mode=update_mode,theme="streamlit",allow_unsafe_jscode=True)

            




with tab11:
    
    st.dataframe(dfEH[dfEH["Company Name"].isin(name_selected)])
    st.dataframe(dfEA[dfEA["Company Name"].isin(name_selected)])
    st.dataframe(dfET[dfET["Company Name"].isin(name_selected)])
        


with tab12:
        pvname_selected = st.selectbox("Select Name:",name_selected)

    
        # WACC - Discount Rate 
        # Growth Rate
        # FCF 

