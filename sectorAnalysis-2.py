import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from load_data_2 import load_data_All


st.set_page_config(layout="wide")

market_select =  st.sidebar.radio("Select Market:",("USA","Canada","India"),index=2)




AdfC,AdfF,AmultidfC,dfM,dfT,dfOff,dfEA,dfEH,dfET,gridOptions = load_data_All()


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


metdf=dfF[dfF[year]==dfF[year].max()]
diff_cols = metdf.columns.difference(dfC.columns)
#Filter out the columns that are different. You could pass in the df2[diff_cols] directly into the merge as well.
selcols = diff_cols.tolist()+ [coName]
selcolmetdf = metdf[selcols]
metdfC = dfC.merge(selcolmetdf,left_on=coName,right_on=coName,how="left")   
unnamed = metdfC.columns[metdfC.columns.str.startswith('Unnamed')]
metdfC.drop(unnamed,axis=1,inplace=True)


growth_cols = dfM[dfM['Multi-Year Format']=="growth"]["title"].unique().tolist() 
avg_cols = dfM[dfM['Multi-Year Format']=="average"]["title"].unique().tolist()  
colListg = growth_cols+[coName,year]
colLista = avg_cols+[coName,year]

year_list=dfF[year].unique().tolist()
year_list.sort(reverse=True)

dfFg = dfF[colListg]
dfF10g=dfFg[dfFg[year].isin(year_list[:11])]
dfF5g=dfFg[dfFg[year].isin(year_list[:6])]
dfF3g=dfFg[dfFg[year].isin(year_list[:4])]
dfF1g=dfFg[dfFg[year].isin(year_list[:2])]
grL = [dfF10g,dfF5g,dfF3g,dfF1g]
dfFa = dfF[colLista]
dfF10a=dfFa[dfFa[year].isin(year_list[:10])]
dfF5a=dfFa[dfFa[year].isin(year_list[:5])]
dfF3a=dfFa[dfFa[year].isin(year_list[:4])]
dfF1a=dfFa[dfFa[year].isin(year_list[:2])]
avL = [dfF10a,dfF5a,dfF3a,dfF1a]


colnameg = [" 10y-growth"," 5y-growth"," 3y-growth"," 1y-growth"]
colnameav = [" 10y-average"," 5y-average"," 3y-average"," 1y-average"]
growthlist = []
count = 0
for yg in grL:
    yg=yg.pivot_table(index=coName,columns=year,values=growth_cols).groupby(level=0,axis=1).pct_change(axis=1)
    ayg=yg.groupby(level=0,axis=1).mean()
    col_list = ayg.columns.tolist()
    col_list =  [x + colnameg[count] for x in col_list]
    ayg.columns = col_list 
    growthlist.append(ayg)
    count += 1

averagelist = []
countav=0
for ya in avL:
    ya=ya.pivot_table(index=coName,columns=year,values=avg_cols)
    ayg=ya.groupby(level=0,axis=1).mean()
    col_list = ayg.columns.tolist()
    col_list =  [x + colnameav[countav] for x in col_list]
    ayg.columns = col_list 
    averagelist.append(ayg)
    countav += 1

multilist = growthlist + averagelist
multiyeardfC = pd.concat(multilist,axis=1).reset_index()
multidfC = metdfC.merge(multiyeardfC,left_on=coName,right_on=coName)
multidfC["Market Cap Scale"] = pd.cut(multidfC[marketCap],bins=[0,500000000,1000000000,20000000000,100000000000,100000000000000],labels=["small","mid-small","mid-large","large","mega"])




meandfC = multidfC.groupby(by=[sector,"Market Cap Scale"]).mean().sort_values(by=marketCap,ascending=True).reset_index()
sumdfC = multidfC.groupby(by=[sector,"Market Cap Scale"]).sum().sort_values(by=marketCap,ascending=True).reset_index()

nco=multidfC.groupby(sector)["Market Cap Scale"].value_counts().unstack()
#nco=nco.reindex(index = sector_order)

mcaptable = sumdfC.pivot_table(index=sector,columns="Market Cap Scale",values=marketCap)
#mcaptable=mcaptable.reindex(index = sector_order)

petab = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=pe)
pcftab = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=pcf)

fig1 = px.bar(mcaptable, x=mcaptable.columns, y=mcaptable.index, orientation='h',text_auto=".2s",title="Market Cap")
fign = px.bar(nco, x=nco.columns, y=nco.index, orientation='h',text_auto=".0f",title = "Number of Companies")

fig3 = px.bar(petab, x=petab.columns, y=petab.index, orientation='h',text_auto=".2f",title= pe)

fig4 = px.bar(pcftab, x=pcftab.columns, y=pcftab.index, orientation='h',text_auto=".2f",title=pcf)


tab1,tab2,tab3 = st.tabs(["Sector Overview","Growth and Avergaes","Performance & Volatility"])

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
            gtable = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=gmetrics)
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
            avgtable = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=avgmetrics)
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

    with col1:
        performancecols = [col for col in multidfC.columns if 'Performance' in col]
        pmetrics = st.selectbox("Select performance metrics:",performancecols)
        perftable = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=pmetrics)
        figP = px.bar(perftable, x=perftable.columns, y=perftable.index, orientation='h',text_auto="0.2f")
        st.plotly_chart(figP)

    with col2:
        voltcols = [col for col in multidfC.columns if 'Volatility' in col]
        voltmetrics = st.selectbox("Select volatility metrics:",voltcols)
        perftable = meandfC.pivot_table(index=sector,columns="Market Cap Scale",values=voltmetrics)
        figP = px.bar(perftable, x=perftable.columns, y=perftable.index, orientation='h',text_auto="0.2f")
        st.plotly_chart(figP)


st.header("FUNDAMENTAL METRICS")


sel_dis_sum = dfF.groupby(by=[sector,year]).sum().sort_values(by=marketCap).reset_index()
sel_dis_avg = dfF.groupby(by=[sector,year]).mean().sort_values(by=marketCap).reset_index()

def DisplayMetric(count=1,st_type=st1,mt_type=rev_type):
        st.subheader(f"METRIC {count}")
        col1, col2,col3 = st.columns(3)

        with col1:
            statements = st.selectbox(
                "Select Statement:",
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
                        "Select Metrics:",
                        mtl,
                        key=f"mt{count}"
                    )
        

        with col3:
            metric_group = st.radio("See metrics by:",("Sum","Avg","Growth"),key=f"rd{count}",horizontal=True)
            if metric_group == "Sum":
                seltdf = sel_dis_sum.pivot_table(index=[sector],columns=year,values=metrics,sort=False)
            elif metric_group == "Avg":
                seltdf = sel_dis_avg.pivot_table(index=[sector],columns=year,values=metrics,sort=False)
            elif metric_group=="Growth":
                seltdf = sel_dis_sum.pivot_table(index=[sector],columns=year,values=metrics,sort=False).pct_change(axis=1)
        if metric_group in ["Sum","Avg"]:
            fig = px.bar(seltdf,x=seltdf.index,y=seltdf.columns,title=metrics,barmode="group")

        else:
            fig = px.imshow(seltdf.values, text_auto=".2%",x=seltdf.columns,y=seltdf.index,aspect="auto",title=f"{metrics}-Growwth")
            fig.update_coloraxes(colorbar_tickformat=".0%",cmin=0,cmax=1,colorscale=[[0,"red"],[0.1,"yellow"],[0.3,"orange"],[0.7,"green"],[1,"blue"]])
            fig.update_xaxes(dtick=1)   
            fig.update_yaxes(nticks=len(seltdf.index))

        st.plotly_chart(fig,use_container_width=True)





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
        DisplayMetric(count=count)
        count +=1

elif add_metrics == "Preselect":   
        DisplayMetric(count=2,st_type=st1,mt_type=fcf)
        DisplayMetric(count=3,st_type=st2,mt_type=roic)
        DisplayMetric(count=4,st_type=st3,mt_type=ebitda_m)
        DisplayMetric(count=5,st_type=st3,mt_type=npm)
        DisplayMetric(count=6,st_type=st4,mt_type=d_e)
        DisplayMetric(count=7,st_type=st4,mt_type=c_r)
else:
    pass



