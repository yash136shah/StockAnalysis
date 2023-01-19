import streamlit as st
import pandas as pd
import plotly.express as px
from load_data_2 import load_data_All
import plotly.graph_objects as go
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
from streamlit_extras.switch_page_button import switch_page

from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.set_page_config(layout="wide")



AdfC,AdfF,AmultidfC,dfM,dfT,dfOff,gridOptions = load_data_All()


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


markets = ["USA","Canada","India"]

if "marketSelect" not in st.session_state:
    st.session_state["marketSelect"] = markets[2]
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelect"])

def MarketSelect ():
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelrad"])

st.session_state["marketSelect"] = st.sidebar.radio("Market:",markets,index=st.session_state["marketIndex"],key="marketSelrad",on_change=MarketSelect)

#MARKET SELECT 

if st.session_state["marketSelect"] == "USA":
        benchmark = "SPY"
        descriptive_screener = ["EXCHANGE"]
        dfC = AdfC[AdfC["Market Code"]=="US"]
        dfF = AdfF[AdfF["Market Code"]=="US"]
        #dfQ = AdfQ[AdfQ["Market Code"]=="US"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="US"]

elif st.session_state["marketSelect"] == "India":
        benchmark = '^NSEI'
        descriptive_screener = []
        dfC = AdfC[AdfC["Market Code"]=="IND"]
        dfF = AdfF[AdfF["Market Code"]=="IND"]
        #dfQ = AdfQ[AdfQ["Market Code"]=="IND"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="IND"]


elif st.session_state["marketSelect"] == "Canada":
        benchmark = '^GSPTSE'
        descriptive_screener=[]
        dfC = AdfC[AdfC["Market Code"]=="CAN"]
        dfF = AdfF[AdfF["Market Code"]=="CAN"]
        #dfQ = AdfQ[AdfQ["Market Code"]=="CAN"]
        multidfC = AmultidfC[AmultidfC["Market Code"]=="CAN"]

        #IS bifurcation IND and CAN



col1,col2 = st.columns([10,2])

with col1:
    st.header("Industry Stats")

with col2:
    homePage = st.button("Home")
    if homePage:
        switch_page("stockAnalysis-2")



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


with col3:
    #country_list= multidfC[(multidfC[sector].isin(st.session_state["sectorSel"])) & (multidfC[industry].isin(st.session_state["industrySel"]))]["COUNTRY"].unique().tolist()
    country_counts= dfC[(dfC[sector].isin(st.session_state["sectorSel"])) & (dfC[industry].isin(st.session_state["industrySel"]))]["COUNTRY"].value_counts().to_frame()
    country_list = []
    for country in country_counts.index:
        country_list.append(country)
    if "countrySel" not in st.session_state:
        st.session_state["countrySel"] = []
        st.session_state["countryDefault"] = country_list[0]
        st.session_state["countryBoxValue"] = False

    def CountrySel ():   
        st.session_state["countryDefault"] = st.session_state["countrySelrad"]            
    
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


issidf=multidfC[(multidfC[sector].isin(st.session_state["sectorSel"])) & (multidfC[industry].isin(st.session_state["industrySel"]))& (multidfC['COUNTRY'].isin(st.session_state["countrySel"]))]

tab1,tab2 = st.tabs(["Industry Scatter","Industry Wheel"])

with tab1:
    pisdf=issidf[[coName,updatedTicker,sector,industry,marketCap,pe,pcf]].fillna(0)
    fig = px.scatter(pisdf,x=marketCap,y=pe,color=industry,size=marketCap,size_max=80,text=coName,height=400)


    st.plotly_chart(fig,use_container_width=True)

    

with tab2:  
    st.write("Issues with sunburst chart update!")
    #figS = px.sunburst(issidf, path=[sector,industry,"Market Cap Scale",coName], values=marketCap)
    #figS.show()
    #st.plotly_chart(figS,use_container_width=True)





industry_order=multidfC[(multidfC[sector].isin(st.session_state["sectorSel"]))&(multidfC["COUNTRY"].isin(st.session_state["countrySel"]))].groupby(by=industry).sum().sort_values(by=marketCap,ascending=True).index.tolist()

selMdfC = multidfC[(multidfC[sector].isin(st.session_state["sectorSel"])) & (multidfC[industry].isin(st.session_state["industrySel"]))&(multidfC["COUNTRY"].isin(st.session_state["countrySel"]))]

meandfC = selMdfC.groupby(by=[industry,"Market Cap Scale"]).mean().sort_values(by=marketCap,ascending=True).reset_index()

sumdfC = selMdfC.groupby(by=[industry,"Market Cap Scale"]).sum().sort_values(by=marketCap,ascending=True).reset_index()


nco=selMdfC.groupby(industry)["Market Cap Scale"].value_counts().unstack()

#nco=nco.reindex(index = industry_order)

mcaptable = sumdfC.pivot_table(index=industry,columns="Market Cap Scale",values=marketCap)
#mcaptable=mcaptable.reindex(index = industry_order)


petab = meandfC.pivot_table(index=industry ,columns="Market Cap Scale",values=pe)
pcftab = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=pcf)

fig1 = px.bar(mcaptable, x=mcaptable.columns, y=mcaptable.index, orientation='h',text_auto=".2s",title="Market Cap")
fign = px.bar(nco, x=nco.columns, y=nco.index, orientation='h',text_auto=".0f",title = "Number of Companies")

fig3 = px.bar(petab, x=petab.columns, y=petab.index, orientation='h',text_auto=".2f",title= pe)

fig4 = px.bar(pcftab, x=pcftab.columns, y=pcftab.index, orientation='h',text_auto=".2f",title=pcf)


st.header("Overview")

tab1,tab2,tab3 = st.tabs(["Highlights","Growth and Avergaes","Performance & Volatility"])

with tab1:
    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1,use_container_width=True)

    with col2:
        st.plotly_chart(fign,use_container_width=True)


    col1,col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig3,use_container_width=True)

    with col2:
        st.plotly_chart(fig4,use_container_width=True)

with tab2:
    growthcols = [col for col in multidfC.columns if 'growth' in col]
    avgcols = [col for col in multidfC.columns if 'average' in col]

    col1,col2 = st.columns(2)

    with col1:

        def gchart(count=1,mt_type=f"{rev_type} 5y-growth"):
            gindex = growthcols.index(mt_type)
            gmetrics = st.selectbox("Select growth metrics:",growthcols,index=gindex,key=f"grow{count}")
            gtable = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=gmetrics)
            figG = px.bar(gtable, x=gtable.columns, y=gtable.index, orientation='h',text_auto="0.2f",title=gmetrics)
            st.plotly_chart(figG)

        gchart()
        gchart(count=2,mt_type=f"{fcf} 5y-growth")
        
        add_more_g = st.radio("Add more charts:",("Yes","No","Preselect"),index=1,key="growthaddmore")

        if add_more_g == "Yes":
            nchart = st.number_input("Add Chart", min_value=1, max_value=1, value=1)
            count = 3
            for n in range(nchart):
                gchart(count=count)
                count +=1  

        elif add_more_g == "Preselect":
            gchart(count=3,mt_type=f"{rev_type} 10y-growth")
            gchart(count=4,mt_type=f"{fcf} 10y-growth")
        
        else:
            pass



    with col2:

        def avgchart(count=1,mt_type=f"{roic} 5y-average"):
            avgindex = avgcols.index(mt_type)
            avgmetrics = st.selectbox("Select average metrics:",avgcols,index=avgindex,key=f"avgch{count}")
            avgtable = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=avgmetrics)
            figA = px.bar(avgtable, x=avgtable.columns, y=avgtable.index, orientation='h',text_auto=".2f")
            st.plotly_chart(figA)

        avgchart()
        avgchart(count=2,mt_type=f"{ebitda_m} 5y-average")

        add_more_a = st.radio("Add more charts:",("Yes","No","Preselect"),index=1,key="avgaddmore")

        if add_more_a == "Yes":
            nchart = st.number_input("Add Chart", min_value=1, max_value=1, value=1)
            count = 3
            for n in range(nchart):
                avgchart(count=count)
                count +=1  

        elif add_more_a == "Preselect":
            avgchart(count=3,mt_type=f"{npm} 5y-average")
            avgchart(count=4,mt_type=f"{d_e} 5y-average")
            avgchart(count=5,mt_type=f"{c_r} 5y-average")
            
        else:
            pass
        





with tab3:
    col1,col2 = st.columns(2)
    scol1,scol2,scol3,scol4 = st.columns(4)
    sscol1,sscol2 = st.columns(2)
    with col1:
        performancecols = [col for col in multidfC.columns if 'Performance' in col]
        pmetrics = st.selectbox("Select performance metrics:",performancecols)
    
    with scol1:
        bcOrient = st.radio("Chart Orientation:",("Horizontal","Vertical"),index=1,horizontal=True,key="bcoPer")
    with scol2:
        bcGroup = st.radio("Chart Grouping:",("Group","Stacked"),index=0,horizontal=True,key="bcgPer")
        
        perftable = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=pmetrics)


    with sscol1: 
        if bcOrient == "Vertical":
            if bcGroup == "Group":
                figP = px.bar(perftable, x=perftable.index, y=perftable.columns,barmode="group",text_auto="0.2f")
            else:
                figP = px.bar(perftable, x=perftable.index, y=perftable.columns,barmode="stack",text_auto="0.2f")

        else:
            if bcGroup == "Group":
                figP = px.bar(perftable, x=perftable.columns, y=perftable.index,barmode="group",text_auto="0.2f")
            else:
                figP = px.bar(perftable, x=perftable.columns, y=perftable.index,text_auto="0.2f")

        st.plotly_chart(figP)


    with scol3:
        bcOrient = st.radio("Chart Orientation:",("Horizontal","Vertical"),index=1,horizontal=True,key="bcoVol")
    with scol4:
        bcGroup = st.radio("Chart Grouping:",("Group","Stacked"),index=0,horizontal=True,key="bcgVol")
        
        perftable = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=pmetrics)

    with col2:
        voltcols = [col for col in multidfC.columns if 'Volatility' in col]
        voltmetrics = st.selectbox("Select volatility metrics:",voltcols)
        
    with sscol2:
        perftable = meandfC.pivot_table(index=industry,columns="Market Cap Scale",values=voltmetrics)
        if bcOrient == "Vertical":
            if bcGroup == "Group":
                figP = px.bar(perftable, x=perftable.index, y=perftable.columns,barmode="group",text_auto="0.2f")
            else:
                figP = px.bar(perftable, x=perftable.index, y=perftable.columns,barmode="stack",text_auto="0.2f")

        else:
            if bcGroup == "Group":
                figP = px.bar(perftable, x=perftable.columns, y=perftable.index,barmode="group",text_auto="0.2f")
            else:
                figP = px.bar(perftable, x=perftable.columns, y=perftable.index,text_auto="0.2f")

        st.plotly_chart(figP)



st.header("Fundamental Overview")


dfF["Market Cap Scale"] = pd.cut(dfF[marketCap],bins=[0,500000000,1000000000,20000000000,100000000000,100000000000000],labels=["small","mid-small","mid-large","large","mega"])

#&(dfF["COUNTRY"].isin(st.session_state["countrySel"]))
sel_dis_sum = dfF[(dfF[sector].isin(st.session_state["sectorSel"]))&(dfF[industry].isin( st.session_state["industrySel"]))].groupby(by=[industry,"Market Cap Scale",year]).sum().sort_values(by=marketCap).reset_index()
sel_dis_avg = dfF[(dfF[sector].isin(st.session_state["sectorSel"]))&(dfF[industry].isin( st.session_state["industrySel"]))].groupby(by=[industry,"Market Cap Scale",year]).mean().sort_values(by=marketCap).reset_index()




if "tabTitle" not in st.session_state:
    st.session_state["tabTile"] = []
    st.session_state["tabChanged"] = False
    st.session_state["metricCount"] = 0 

def MetricTabChanged(): 
    st.write(st.session_state["metricCount"])
    st.session_state["tabChanged"] = True
    st.session_state["tabTile"][0] = st.session_state["mt1"]


def DisplayMetric(count=1,st_type=st1,mt_type=rev_type):
        #st.subheader(f"METRIC {count}")
        col1, col2,col3 = st.columns(3)

        with col1:
            statements = st.selectbox(
                "Statement Selected:",
                dfM["Statement"].unique(),
                index=dfM["Statement"].unique().tolist().index(st_type),
                key=f"st{count}"
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
                        "Metrics Selected:",
                        mtl,
                        key=f"mt{count}",
                        on_change=MetricTabChanged
                    )

        st.session_state["metricCount"] = count         

        with col3:
            metric_group = st.radio("Summarize metrics by:",("Sum","Avg","Growth"),key=f"rd{count}",horizontal=True)
            if metric_group == "Sum":
                seltdf = sel_dis_sum.pivot_table(index=[industry,"Market Cap Scale"],columns=year,values=metrics,sort=False)
            elif metric_group == "Avg":
                seltdf = sel_dis_avg.pivot_table(index=[industry,"Market Cap Scale"],columns=year,values=metrics,sort=False)
            elif metric_group=="Growth":
                seltdf = sel_dis_sum.pivot_table(index=[industry,"Market Cap Scale"],columns=year,values=metrics,sort=False).pct_change(axis=1)

        


        if metric_group in ["Sum","Avg"]:    
            seltdf.index.names = [industry,"Market Cap Scale"]
            seltdf.reset_index(inplace=True)
            col1,col2 = st.columns(2)
            with col1:
                mscale = seltdf["Market Cap Scale"].unique().tolist()
                mscaleSel = st.multiselect("Market Cap Scale",mscale,default=mscale,key=f"mscaleind{count}")  
                selMtdf = seltdf[seltdf["Market Cap Scale"].isin(mscaleSel)]
            
            with col2:
                period_range = st.slider("Number of Periods:",0,len(selMtdf.columns[2:]),(0,5),key=f"perind{count}")

                ys = period_range[0]
                ye = period_range[1]          
                
                if ys == 0:
                    periods = selMtdf.iloc[:,-ye:].columns.to_list()
                else:
                    periods  = selMtdf.iloc[:,-ye:-ys].columns.to_list()

            bcType = st.radio("Bar Chart Type:",("Grouped","Stacked"),index=1,key=f"bchartT{count}",horizontal=True)

            if bcType == "Grouped":
                    fig = go.Figure()
                    for period in periods:
                                    selmtdf = selMtdf.loc[:,[industry,"Market Cap Scale",period]]
                                    x = []
                                    x.append(selmtdf[industry].to_list())
                                    x.append(selmtdf["Market Cap Scale"])
                                    fig.add_bar(x=x, y=selmtdf[period], name=period)
            
            else:
            
                mcapText = selMtdf["Market Cap Scale"].to_list()                 
                fig = px.bar(selMtdf ,x=industry,y=periods,title=metrics,barmode="group",text=mcapText)
                #fig.update_xaxes(tickangle=45) 

            st.plotly_chart(fig,use_container_width=True)
            
            with st.expander("See Table"):
                col_string = map(str, selMtdf.columns)
                selMtdf.columns = col_string
                dfmetS =  AgGrid(selMtdf,height=200,key=f"tableInd{count}")
            

        else:
            seltdf.index.names = [industry,"Market Cap Scale"]
            seltdf.reset_index(inplace=True)

            col1,col2 = st.columns(2)
            with col1:

                mscale = seltdf["Market Cap Scale"].unique().tolist()
                mscaleSel = st.multiselect("Market Cap Scale",mscale,default=mscale)  
                selMtdf = seltdf[seltdf["Market Cap Scale"].isin(mscaleSel)]
            
                
                selMtdf["Industry-Mcap Scale"] = selMtdf[industry].astype("str")+"-"+selMtdf["Market Cap Scale"].astype("str")
                selMtdf.drop([industry,"Market Cap Scale"],axis=1,inplace=True)
                selMtdf.set_index("Industry-Mcap Scale",inplace=True)
            
            with col2:
                period_range = st.slider("Number of Periods:",0,len(selMtdf.columns),(0,5),key=f"per{count}")

                ys = period_range[0]
                ye = period_range[1]          
                
                if ys == 0:
                    selmdf = selMtdf.iloc[:,-ye:]
                else:
                    selmdf = selMtdf.iloc[:,-ye:-ys]



            fig = px.imshow(selmdf, text_auto=".2%",x=selmdf.columns,y=selmdf.index,aspect="auto",title=f"{metrics}-Growth")
            fig.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=[[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]])
            fig.update_xaxes(dtick=1)  
            fig.update_yaxes(nticks=len(selmdf.index))

            st.plotly_chart(fig,use_container_width=True)
        




add_metrics = st.radio("Metrics Selection:",("Preselected","Select your own Metrics"),index=0,horizontal=True)


if add_metrics == "Preselected":  
    stT = [st1,st2,st4,st3,st3,st3,st3,st3]

    st.session_state["tabTile"] = [rev_type,fcf,assets,roic,ebitda_m,npm,d_e,c_r]


else:
    dfMsel = dfM.iloc[:,:3]
    builder = GridOptionsBuilder.from_dataframe(dfMsel)
    builder.configure_default_column(editable=True,groupable=True,filterable=True,enableRowGroup=True)
    builder.configure_selection(selection_mode = "multiple", use_checkbox=True, rowMultiSelectWithClick=True)
    gridOptionR = builder.build()
    return_mode_value = DataReturnMode.FILTERED_AND_SORTED
    update_mode=GridUpdateMode.MANUAL
    with st.expander("Metrics Table"):
        df = AgGrid(dfMsel,height=400,gridOptions= gridOptionR,update_mode=update_mode,data_return_mode=return_mode_value,theme="streamlit",allow_unsafe_jscode=True)    
    
    stMt = {}
    st.session_state["tabTile"]  = []
    stT = []
    for lis in df["selected_rows"]:
        stType = lis["title"]
        stMt[stType] = lis["Statement"]
        st.session_state["tabTile"] .append(stType)
        stT.append(lis["Statement"])
   


emptyTabs = 10 - len(st.session_state["tabTile"] )
for tab in range(emptyTabs):
    st.session_state["tabTile"].append(" ")
    stT.append(st2)    


if len(st.session_state["tabTile"] )>10 :
        st.warning("Maximum 10 metric selection at once!")
        st.stop()


else:
    

    tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8,tab9,tab10=st.tabs(st.session_state["tabTile"])


    with tab1:
        
        DisplayMetric(count=1,st_type=stT[0],mt_type=st.session_state["tabTile"][0])
        
    with tab2:
        DisplayMetric(count=2,st_type=stT[1],mt_type=st.session_state["tabTile"][1])
        
    with tab3:
        DisplayMetric(count=3,st_type=stT[2],mt_type=st.session_state["tabTile"] [2])
        
    with tab4:
        DisplayMetric(count=4,st_type=stT[3],mt_type=st.session_state["tabTile"] [3])
        
    with tab5:
        DisplayMetric(count=5,st_type=stT[4],mt_type=st.session_state["tabTile"] [4])
        
    with tab6:
        DisplayMetric(count=6,st_type=stT[5],mt_type=st.session_state["tabTile"] [5])
        
    with tab7:
        DisplayMetric(count=7,st_type=stT[6],mt_type=st.session_state["tabTile"] [6])

    with tab8:
        DisplayMetric(count=8,st_type=stT[7],mt_type=st.session_state["tabTile"] [7])

    with tab9:
        DisplayMetric(count=9,st_type=stT[8],mt_type=st.session_state["tabTile"] [8])


    with tab10:
        DisplayMetric(count=10,st_type=stT[9],mt_type=st.session_state["tabTile"] [9])
            
