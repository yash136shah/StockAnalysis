import streamlit as st
from streamlit_plotly_events import plotly_events
from load_data_2 import load_data_All
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import plotly.graph_objects as go
import plotly.express as px 
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

def MarketSelect ():
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelrad"])

st.session_state["marketSelect"] = st.sidebar.radio("Market:",markets,index=st.session_state["marketIndex"],key="marketSelrad",on_change=MarketSelect)


if "name_selected" not in st.session_state:
    st.session_state["name_selected"] = []

if "name_selected_chart" not in st.session_state:
    st.session_state["name_selected_chart"] = []
    st.session_state["name_selected_table"] = []

if "name_selected_SI" not in st.session_state:
    st.session_state["name_selected_SI"] = []

try: 
    st.session_state["name_selected"] = st.session_state["nameSelFundamental"] 
except:
    pass

try:
    st.session_state["name_selected"] = st.session_state["nameSelTechnical"]
except:
    pass

if len(st.session_state["name_selected"] )>0:
    st.warning("You have some old selections!")
    def ClearName():
            st.session_state["name_selected"] = []
            try:
                st.session_state["nameSelFundamental"] =[]
            
            except:
                pass
            try:
                st.session_state["nameSelTechnical"] =[]
            
            except:
                pass

    clearName = st.button("Clear old selection",on_click=ClearName)


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
        #IS bifurcation IND and CAN

        
# SEARCH NAME BY
nameSearchoptions = ['Sector & Industry', "Peers", "Screener",'Individually']

if "name_search" not in st.session_state:
    st.session_state["name_search"] = nameSearchoptions[0]
    st.session_state["name_searchIndex"] = nameSearchoptions.index(st.session_state["name_search"])

def NameSearch():
    st.session_state["name_searchIndex"] = nameSearchoptions.index(st.session_state["nameSerrad"])

col1,blankCol = st.columns([5,10])

with col1:
    st.session_state["name_search"] = st.selectbox('Search Company by:',nameSearchoptions,index=st.session_state["name_searchIndex"],key="nameSerrad",on_change=NameSearch,
                                                  help="There are 3 ways to search companies:\n1) Sector&Industry-helps you screen down companies based on Sector,Industry,Country,Market Cap \n2) Screener - Multiple metrics to screen companies on! \n3)Peers - finding peers based on a Company Name \nHowever,if you want to search companies individually or have personalized selection - just head straight to one of the analysis page!")




if st.session_state["name_search"]== 'Sector & Industry':

    #ROW 1 of Selection
    col1,col2,col3 = st.columns(3)
    with col1:
        if "sectorSel" not in st.session_state:
            st.session_state["sectorSel"] = []
        if "sectorDefault" not in st.session_state:
            st.session_state["sectorDefault"] = multidfC[sector].unique()[0]
            st.session_state["sectorBoxValue"] = False

        def SectorSel ():   
            st.session_state["sectorDefault"] = st.session_state["sectorSelrad"]
            
        sectorOptions=multidfC[sector].unique().tolist() + ["All"]
        
        containerSector = st.container()
        
        
        def SectorAllSel():
            if st.session_state["sectorBoxValue"] == True: 
                    st.session_state["sectorBoxValue"] = False
            else:
                    st.session_state["sectorBoxValue"] = True
        
        
        all = st.checkbox("Select all",value=st.session_state["sectorBoxValue"],key="sectorAll",on_change=SectorAllSel)
        if all:
            st.session_state["sectorSel"] = containerSector.multiselect("Sector:",sectorOptions,default="All" ,key="sectorSelrad",on_change=SectorSel)
        
        else:
            st.session_state["sectorSel"] = containerSector.multiselect("Sector:",sectorOptions,default=st.session_state["sectorDefault"],key="sectorSelrad",on_change=SectorSel)
            
        if "All" in st.session_state["sectorSel"]:
            st.session_state["sectorSel"] = multidfC[sector].unique()
    
    
    if len(st.session_state["sectorSel"]) == 0:   # ERROR RAISED IF NO SECTOR
        st.error("Please Enter a Sector")
        st.stop()

  
    with col2:
        
        industry_list = multidfC[multidfC[sector].isin(st.session_state["sectorSel"])][industry].unique().tolist()
        industryOptions = industry_list + ["All"]
        if "industrySel" not in st.session_state:
                st.session_state["industrySel"] = [] 
                st.session_state["industryDefault"] = industry_list[:2]
                st.session_state["industryBoxValue"] = False
        
        

        def IndustrySel ():   
            st.session_state["industryDefault"] = st.session_state["industrySelrad"]            
 
        def IndustryAllSel():
            if st.session_state["industryBoxValue"] == True: 
                    st.session_state["industryBoxValue"] = False
            else:
                    st.session_state["industryBoxValue"] = True

        
        
        containerIndustry = st.container()
        all_ind = st.checkbox("Select all",value=st.session_state["industryBoxValue"],key="industryAll",on_change=IndustryAllSel)
        
        if all_ind:
            st.session_state["industrySel"] = containerIndustry.multiselect("Industry:",options=industryOptions,default="All",key="industrySelrad",on_change=IndustrySel)
         
        else:
             st.session_state["industryDefault"] = industry_list[:2]
             st.session_state["industrySel"] = containerIndustry.multiselect("Industry:",options=industryOptions,default=st.session_state["industryDefault"],key="industrySelrad",on_change=IndustrySel)
         
    
        if "All" in st.session_state["industrySel"]:
            st.session_state["industrySel"] = industry_list
            
        if len(st.session_state["industrySel"]) == 0:        # ERROR RAISED IF NO INDUSTRY 
            st.error("Please Enter a Industry")
            st.stop()
        
        industryOverview = st.checkbox("See Industry Overview")

        if industryOverview:
            switch_page("Industry Overview")


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

    containerName = st.container()
    containerSelMode = st.container()
    
    
    tab1,tab2 = st.tabs(["Peer Chart","Peer Table"])
    
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
        
        
        #try:
         #   issi = multidfC[multidfC[coName].isin(st.session_state["name_selected_SI"])]
         #   xh = issi[x_axis_met].tolist()
         #   yh= issi[y_axis_met].tolist()
         #   fig.add_trace(go.Scatter(x=xh, y=yh, mode = 'markers',marker_symbol = 'star',marker_size = 60,opacity=0.5,fillcolor="orange",name="Selected Companies"))
         #   st.write("working!")
        #except:
         #   pass
        
        col1,col2,col3,col4 = st.columns([1,1,4,4])
        x_min = isdfn[x_axis_met].min()
        x_max = isdfn[x_axis_met].max()
        mcapList = isdfn[x_axis_met].to_list()
        mcapList.sort()

        with col1:
            xValMin=st.number_input("Min X-axis value",min_value=x_min,max_value=x_max,value=x_min)
        with col2:
            xValMax=st.number_input("Max X-axis value",min_value=x_min,max_value=x_max,value=x_max)
        
        fig.update_layout(xaxis_range=[xValMin,xValMax])

        selection = plotly_events(fig,click_event=False,select_event=True)
        
                          
        # CLICKABLE EVENTS GENERATED 
        nameSelectMode = containerSelMode.radio("Selection Mode:",("Continued","Refreshed"),index=1,horizontal=True,help="Continued Selection helps to maintain the selections on changing parameters/selection, whereas Refreshed Selection will change with changing parameters/selection!")

        if nameSelectMode == "Refreshed":
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

        if nameSelectMode == "Refreshed":
            st.session_state["name_selected_table"]= []
        
        for i in screendfC:
            if i[coName] not in st.session_state["name_selected_table"]:
                st.session_state["name_selected_table"].append(i[coName])
    
    

    if "SInameDefault" not in st.session_state:
        st.session_state["SInameDefault"] = []

    name_combo=st.session_state["name_selected_table"]+st.session_state["name_selected_chart"]

    st.session_state["SInameDefault"] = [*set(st.session_state["name_selected"]+name_combo)]
    
    
    def SINameSel ():   
        st.session_state["SInameDefault"] = st.session_state["nameSel"]            
    
    
    try:
        st.session_state["name_selected_SI"]=containerName.multiselect("Company Name Selected:",dfC[coName].unique(),default=st.session_state["SInameDefault"],key="nameSel",on_change=SINameSel)
        
        
    except:
        st.session_state["name_selected_SI"]=containerName.multiselect("Company Name Selected:",dfC[coName].unique(),key="nameSel")

    

    
    if len(st.session_state["name_selected_SI"]) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select or Select from select box - to perform Analysis.")
        st.stop()

        


elif st.session_state["name_search"]== "Peers":
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
        
        #ISSUE ************************************
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

        
   #ISSUE ************************************ Duplicate Names
    # CLICKABLE EVENTS GENERATED 
    st.session_state["name_selected"]=[]
    for el in selection:
        x=el['x']
        y=el['y']
        nsdf=multidfC[(multidfC[x_axis_met]==(x)) & (multidfC[y_axis_met]==(y))]
        name_sel = nsdf[coName].item()
        if name_sel not in st.session_state["name_selected"]:
            st.session_state["name_selected"].append(name_sel)

    if len(st.session_state["name_selected"]) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select - to perform Analysis.")
        st.stop()
    
    st.session_state["name_selected"]=st.multiselect("Company Name Selected:",ispmdf[coName].unique(),default=st.session_state["name_selected"])



elif st.session_state["name_search"]== "Screener":
    
    return_mode_value = DataReturnMode.FILTERED_AND_SORTED
    update_mode=GridUpdateMode.MANUAL
    
    col1,col2 = st.columns([12,2])

    grid_return = AgGrid(multidfC,height=400,gridOptions=gridOptions,update_mode=update_mode,data_return_mode=return_mode_value,theme="streamlit",allow_unsafe_jscode=True,key="Aggrid")    
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


    st.session_state["name_selected"]
    if len(st.session_state["name_selected"])>0:
        for nameSel in st.session_state["name_selected"]:
            if nameSel not in screendfC[coName].unique():
                st.session_state["name_selected"].remove(nameSel)
    st.session_state["name_selected"]
        
    # CLICKABLE EVENTS GENERATED 
    #
    for el in selection:
        x=el['x']
        y=el['y']
        nsdf=screendfC[(screendfC[x_axis_met]==(x)) & (screendfC[y_axis_met]==(y))]
        name_sel = nsdf[coName].item()
        if name_sel not in st.session_state["name_selected"]:
            st.session_state["name_selected"].append(name_sel)

    st.session_state["name_selected"]=st.multiselect("Company Name Selected:",screendfC[coName].unique(),default=st.session_state["name_selected"])

    if len(st.session_state["name_selected"]) == 0:
        st.warning("Select companies on Chart with Box Select or Lasso Select - to perform Analysis.")
        st.stop()



# NAME SEARCH INDIVIDUALLY
else:
    name_uni = dfC.sort_values(by=marketCap,ascending=False)[coName].dropna().unique()
    name_list = []
    for i in name_uni:
        name_list.append(i)
    
    st.session_state["name_selected"] = st.multiselect("Enter Company Name:",name_list,default=name_list[0])





#if len(st.session_state["name_selected"])>30:
#    st.warning("Max 30 companies can be selected at a time!")
#   st.stop()




st.header("⚔ Perform Analysis")

col1,col2 = st.columns(2)

with col1:
    if st.button("📈Technical Analysis"):
        st.session_state["name_selected"]=st.session_state["name_selected_SI"]
        switch_page("Technical Analysis")

with col2:
    if st.button("📊Fundamental Analysis"):
        st.session_state["name_selected"]=st.session_state["name_selected_SI"]
        switch_page("Fundamental Analysis")

