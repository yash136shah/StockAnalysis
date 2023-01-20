import streamlit as st
import yfinance as yf
import datetime
import pandas as pd 
from streamlit_plotly_events import plotly_events
from load_data_2 import load_data_All
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import plotly.graph_objects as go
import plotly.express as px 
from streamlit_extras.switch_page_button import switch_page
import  streamlit_toggle as tog

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



#MARKET SELECT 
markets = ["USA","Canada","India"]

if "marketSelect" not in st.session_state:
    st.session_state["marketSelect"] = markets[2]
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelect"])
   
def MarketSelect ():
    st.session_state["marketIndex"] = markets.index(st.session_state["marketSelrad"])

st.session_state["marketSelect"] = st.sidebar.radio("Market:",markets,index=st.session_state["marketIndex"],key="marketSelrad",on_change=MarketSelect)


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



#COMPANY NAME SELECTION 
name_uni = dfC.sort_values(by=marketCap,ascending=False)[coName].dropna().unique()
name_list = []
for i in name_uni:
    name_list.append(i)

if "name_selected_fundamental" not in st.session_state:
    st.session_state["name_selected_fundamental"] = dfC[coName].unique()[0]

if "name_selected" not in st.session_state:
    st.session_state["name_selected"] = []
        #IS bifurcation IND and CAN



#HEADER COLUMNS 
col1,col2,col3,col4 = st.columns([10,1,1,1])

with col1:
    st.header("FUNDAMENTAL ANALYSIS")

with col2:
    homePage = st.button("Home")
    if homePage:
        st.session_state["name_selected"]=st.session_state["name_selected_fundamental"] 
        switch_page("stockAnalysis-2")

with col3:
    if st.button("Technical Analysis"):
        st.session_state["name_selected"]=st.session_state["name_selected_fundamental"] 
        switch_page("Technical")

with col4:
    if st.button("Industry Overview"):
        st.session_state["name_selected"]=st.session_state["name_selected_fundamental"] 
        switch_page("Industry Overview")


try:
    if len(st.session_state["nameSel"])>0:
        defaultName = st.session_state["nameSel"]
    
    st.session_state["name_selected_fundamental"] = st.multiselect("Company Name:",name_list,key="nameSelFundamental",default=defaultName)
    

except:
    try:

        if len(st.session_state["nameSelTechnical"])>0:
            defaultName = st.session_state["nameSelTechnical"]
        
        st.session_state["name_selected_fundamental"] = st.multiselect("Company Name:",name_list,key="nameSelFundamental",default=defaultName)

    except:  
        st.session_state["name_selected_fundamental"] = st.multiselect("Company Name:",name_list,key="nameSelFundamental",default=st.session_state["name_selected"])


if st.button("Change Peer Selection"):
    switch_page("stockAnalysis-2")


if len(st.session_state["name_selected_fundamental"]) == 0:
    st.warning("Select Companies to see Analysis!")
    st.stop()


#TABS
tab1, tab2, tab3 , tab4, tab5, tab6, tab7, tab8,tab9,tab10,tab11,tab12 = st.tabs(["Peer Stats","Radar","Peer Financial Analysis","Common FS","Financial Statements","Value","Business Description","Earnings Date","Links","ShareHolding","Extra Stats","Perform Valuation"])
#color scale
heatmap_colorscale_percent = [[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]]
heatmap_colorscale_growth = [[0,"red"],[0.1,"yellow"],[0.3,"green"],[0.7,"blue"],[1,"purple"]]


period_check = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])][year].unique()

if len(period_check)==0:
    st.warning("No Data Available for these Companies")
    st.stop()


with tab1:
    # PEER STATS 

    #1 Market Cap,PE,PCF
    isdfC = multidfC[multidfC[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False)
    mc_bar = isdfC[[coName,marketCap,pe,pcf]].sort_values(by=marketCap)

    isdf = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])]
    
        
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
    
    isdf = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False)


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
            builder = GridOptionsBuilder.from_dataframe(dfM)
            builder.configure_default_column(groupable=True,editable=True)
            builder.configure_selection(selection_mode="multiple",use_checkbox="enable")
            gridOptionR = builder.build()
            return_mode_value = DataReturnMode.FILTERED_AND_SORTED
            update_mode=GridUpdateMode.MANUAL
            gridOptionR["columnDefs"][1]["rowGroup"]=True     
            grid_rating = AgGrid(dfM,height=400,gridOptions= gridOptionR,update_mode=update_mode,data_return_mode=return_mode_value,theme="streamlit",allow_unsafe_jscode=True) 
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

                for n in st.session_state["name_selected_fundamental"]:                               
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
        isdf = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False)
        periodType = year

    else:
        isdf = dfQ[dfQ[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False)
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

                    for i in range(len(st.session_state["name_selected_fundamental"])):
                        col1,col2,col3=st.columns(3)       
                        with col1:    
                            st.session_state["name_selected_fundamental"][i]


                        with col2:
                            if st.session_state["name_selected_fundamental"][i] in superb:
                                sl_value = "3-Superb"
                            elif st.session_state["name_selected_fundamental"][i] in great:
                                sl_value = "2-Great"
                            elif st.session_state["name_selected_fundamental"][i] in average:
                                sl_value = "1-Average"
                            elif st.session_state["name_selected_fundamental"][i] in negative:
                                sl_value = "-1-Negative"
                            elif st.session_state["name_selected_fundamental"][i] in worst:
                                sl_value = "-2-Worst"
                            elif st.session_state["name_selected_fundamental"][i] in neutral:
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
    
    isdf = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False)
    isdft = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])].sort_values(by=marketCap,ascending=False).transpose()
    
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
    name_FS = st.selectbox("Enter Company Name:",st.session_state["name_selected_fundamental"],index=0,key="Name_FS")
    

    col1,col2 = st.columns(2)

    with col1:
            statement_type = st.radio("Statement Type:",("Income Statement","Balance Sheet","Cash Flow","Ratios"),horizontal=True,key="cfdis")

            
    with col2:
            report_period = st.radio("Report Period:",("Annual","Quarterly"),index=0,horizontal=True,key="FSrp")
            

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
    
  
    sd = datetime.date(2010, 1, 1)
    ed = datetime.date(2025,1,1)
    closeType = "Close"

    # Get Historical Data from YahooFinance
    #@st.experimental_memo
    def ytickData():
        ticker_selected=dfC[dfC[coName].isin(st.session_state["name_selected_fundamental"])].loc[:,updatedTicker].to_list()
        ticker_data = yf.download(ticker_selected,start=sd,end=ed)
        colname = {}
        if len(ticker_selected) == 1:
            tickdata=ticker_data[closeType].to_frame()
            vol_data = ticker_data['Volume'].to_frame()
            colname[ticker_selected[0]]= st.session_state["name_selected_fundamental"][0]

        else:
            tickdata=ticker_data[closeType]
            vol_data = ticker_data['Volume']
            for t in tickdata:
                colname[t]=' '.join(dfC[dfC[updatedTicker]==t][coName].to_list())

        tickdata.rename(columns=colname,inplace=True)
        vol_data.rename(columns=colname,inplace=True)

        return ticker_data,ticker_selected,tickdata,vol_data

    ticker_data,ticker_selected,tickdata,vol_data=ytickData()


    if len(ticker_selected) > 1:
            visdf=dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])&(dfF[year]==2021)].sort_values(by=marketCap,ascending=True).loc[:,[coName,updatedTicker,year,fcf,'Fair Value (30)', 'Fair Value (15)','Fair Value (45)']]
            
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


        sel = dfF[dfF[coName].isin(st.session_state["name_selected_fundamental"])]

        vvs = sel[[coName,updatedTicker,marketCap,year,'Fair Value (30)', 'Fair Value (15)','Fair Value (45)']].sort_values(by=marketCap,ascending=False)
        
        val = vvs.drop(vvs[vvs[updatedTicker] == " "].index)
        
        vv_mcap = val.drop_duplicates(updatedTicker)
        vname_list = vv_mcap[coName].to_list()

        vst_name_selected = st.multiselect("Select Name:",options=vname_list,default=vname_list[:6])
        
        vtick=vv_mcap[vv_mcap[coName].isin(vst_name_selected)][updatedTicker].to_list()
        

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
        bizdes= st.selectbox("See Business Description for:",st.session_state["name_selected_fundamental"],index=0)
        
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
    sel = dfC[dfC[coName].isin(st.session_state["name_selected_fundamental"])]
    earning_date = sel[[coName,'Upcoming Earnings Date','Recent Earnings Date']].set_index(coName)
    earning_date



with tab9:

    def make_clickable(link):
            # target _blank to open new window
            # extract clickable text to display for your link
            text = link.split('=')[0]
            return f'<a target="_blank" href="{link}">{text}</a>'

    if st.session_state["marketSelect"] == "USA":
        name_selected_link = st.selectbox("Select Name:",st.session_state["name_selected_fundamental"],index=0,key="USLink")
        
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
        name_selected_link = st.selectbox("Links:",st.session_state["name_selected_fundamental"],index=0,key="OtherLink")
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
        name_selected_sh = st.selectbox("Select Name:",st.session_state["name_selected_fundamental"],index=0,key="ShareHoldName")
        
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
        
        
        dfSO = dfC[dfC[coName].isin(st.session_state["name_selected_fundamental"])][[coName,"SHARES OUTSTANDING","SHARES FLOAT"]]
        dfSO["SHARES % FLOAT"] = dfSO["SHARES FLOAT"]/dfSO["SHARES OUTSTANDING"]
        dfSO["SHARES % INSIDER"] = 1 - dfSO["SHARES % FLOAT"]
        dfSO.set_index(coName,inplace=True)
        
        figSO = px.bar(dfSO, x=["SHARES % FLOAT","SHARES % INSIDER"],y=dfSO.index,title='%FLOAT vs %INSIDER',text_auto=".2%")

        
        dfShp = dfC[dfC[coName].isin(st.session_state["name_selected_fundamental"])][[coName,"PERCENT INSTITUTIONS","PERCENT INSIDERS"]]
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
            tickerSh = dfC[dfC[coName].isin(st.session_state["name_selected_fundamental"])]["TICKER"].to_list()
        
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
    
    st.dataframe(dfEH[dfEH["Company Name"].isin(st.session_state["name_selected_fundamental"])])
    st.dataframe(dfEA[dfEA["Company Name"].isin(st.session_state["name_selected_fundamental"])])
    st.dataframe(dfET[dfET["Company Name"].isin(st.session_state["name_selected_fundamental"])])
        


with tab12:
        vNameSel = st.selectbox("Select Name:",st.session_state["name_selected_fundamental"])

    
        # WACC - Discount Rate 
        # Growth Rate
        # FCF 

