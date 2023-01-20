import streamlit as st
import s3fs
import os
import pandas as pd 
from io import StringIO
import numpy as np
from numerize import numerize as nu


# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)


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

@st.experimental_memo
def load_data_All(country="IND"):
    if country == "US":
        infoType = ["CompanyInfo","AF","Officers","Listings","SharesOutstanding","EarningHistorical","EarningTrend","EarningAnnual"]
    
    else:
        infoType = ["CompanyInfo","AF","QF","Officers","Listings","SharesOutstanding","EarningHistorical","EarningTrend","EarningAnnual"]

    dictDf = {} 
    listDf = []

    try:
        for info in infoType:                        
                    f = fs.open(f"streamlitstockanalysis/{country}-EOD/{country}_{info}.csv") 
                    url = f.read().decode("utf-8")
                    df = pd.read_csv(StringIO(url),sep=",",header=0,low_memory=False)
                    df["Market Code"] = country
                    listDf.append(df)
                    
                    mergeDf = pd.concat(listDf)
                    mergeDf.reset_index(drop=True,inplace=True) 
                    dictDf[info] = mergeDf
                    listDf = []


    except:
        pass
    
    #only US
    f = fs.open(r"streamlitstockanalysis/US-EOD/US_Shareholders.csv") 
    url = f.read().decode("utf-8")
    dfSh = pd.read_csv(StringIO(url),sep=",",header=0,low_memory=False)
    
    #tview 
    f = fs.open(r"streamlitstockanalysis/india_america_canada_2023-01-04.csv") 
    url = f.read().decode("utf-8")
    dfT = pd.read_csv(StringIO(url),sep=",",header=0,low_memory=False)
    
    #metRef
    f = fs.open(r"streamlitstockanalysis/MetricRef.csv") 
    url = f.read().decode("utf-8")
    dfM = pd.read_csv(StringIO(url),sep=",",header=0,low_memory=False)

    dfOff = dictDf["Officers"]
    dfEH = dictDf["EarningHistorical"]
    dfET = dictDf["EarningTrend"]
    dfEA = dictDf["EarningAnnual"]
    dfCI = dictDf["CompanyInfo"] 
    


    frames = [dfSh,dfOff,dfEH,dfET,dfEA,dfCI,dfT,dfM]
       
    for df in frames:    
        df.columns = df.columns.str.lstrip()
    

    dfCI.loc[dfCI["EXCHANGE"]=="TO",["YF TICKER"]] = dfCI["TICKER"] + ".TO"
    dfCI.loc[dfCI["EXCHANGE"]=="NSE",["YF TICKER"]] = dfCI["TICKER"] + ".NS"
    dfCI.loc[dfCI["EXCHANGE"].isin(['NASDAQ', 'NYSE', 'NYSE MKT', 'BATS', 'NYSE ARCA']),["YF TICKER"]] = dfCI["TICKER"]


    dfC = dfCI.merge(dfT,left_on="TICKER",right_on="Ticker",how="left")
    dfC.drop_duplicates('NAME',inplace=True)
    dfC.replace(r'^\s+$', np.nan, regex=True,inplace=True)

    dfC.fillna(0,inplace=True)

    nameInfo = dfC[["TICKER","NAME"]]
    nameInfo.rename(columns={"NAME":"Company Name"},inplace=True)

    dfSH = dfSh.merge(nameInfo,left_on="TICKER",right_on="TICKER",how="left")
    dfOff = dfOff.merge(nameInfo,left_on="TICKER",right_on="TICKER",how="left")
    dfEH = dfEH.merge(nameInfo,left_on="TICKER",right_on="TICKER",how="left")
    dfET = dfET.merge(nameInfo,left_on="TICKER",right_on="TICKER",how="left")
    dfEA= dfEA.merge(nameInfo,left_on="TICKER",right_on="TICKER",how="left")


    mdata=[]
    for i in dfC['MARKET CAPITALIZATION']:
        mdata.append(nu.numerize(i))

    dfC['Current Market Cap'] = mdata 

    mcap0=dfC.index[dfC['MARKET CAPITALIZATION']==0]
    dfC.drop(labels=mcap0,axis=0,inplace=True)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    colnumeric = dfC.select_dtypes(include=numerics).columns
    dfC[colnumeric]=dfC[colnumeric].fillna(0)



    selected_info=dfC[["YF TICKER",'TICKER','NAME','SECTOR','INDUSTRY','MARKET CAPITALIZATION','Current Market Cap','SHARES OUTSTANDING']]


    #QUARTERLY FS     

    dfQI = dictDf["QF"]  

    dfQI.columns = dfQI.columns.str.lstrip()

    dfQ = dfQI.merge(selected_info,left_on="TICKER",right_on='TICKER',how="left")

    dfQ['Value 2'] = dfQ['CASH'] + dfQ['CASH AND EQUIVALENTS'] + dfQ['SHORT TERM INVESTMENTS'] + dfQ['LONG TERM INVESTMENTS'].fillna(0) - dfQ['MINORITY INTEREST'].fillna(0) - dfQ['TOTAL LIAB'].fillna(0)

    dfQ['Net Profit Margin'] = dfQ['NET INCOME']/dfQ['TOTAL REVENUE']                     
    dfQ['Operating Profit Margin'] = dfQ['EBIT']/dfQ['TOTAL REVENUE']
    dfQ['EBITDA Margin'] = dfQ['EBITDA']/dfQ['TOTAL REVENUE']
    dfQ['Gross Profit Margin'] = dfQ['GROSS PROFIT']/dfQ['TOTAL REVENUE']
    dfQ['DATE']=pd.to_datetime(dfQ['DATE']).dt.date
    dfQ['C/R'] = dfQ['TOTAL CURRENT ASSETS'].fillna(0)/dfQ['TOTAL CURRENT LIABILITIES'].fillna(0)
    dfQ['D/E'] = (dfQ['LONG TERM DEBT'].fillna(0) + dfQ['SHORT LONG TERM DEBT TOTAL'].fillna(0))/dfQ['TOTAL STOCKHOLDER EQUITY'].fillna(0)
    dfQ['ROIC'] = dfQ['EBIT']/(dfQ['LONG TERM DEBT'].fillna(0) + dfQ['SHORT LONG TERM DEBT TOTAL'].fillna(0) + dfQ['TOTAL STOCKHOLDER EQUITY'].fillna(0))



    # ANNUAL FINANCIAL STATEMENT 

    dfFI =  dictDf["AF"]  
    dfFI.columns = dfFI.columns.str.lstrip()
    dfFI["DATE"]=dfFI["DATE"].astype("datetime64")
    dfFI["YEAR"]=dfFI["DATE"].dt.year
    dfFI.dropna(subset=["YEAR"],inplace=True)
    dfFI["YEAR"]=dfFI["YEAR"].astype("int")


    dfF = dfFI.merge(selected_info,left_on="TICKER",right_on='TICKER',how="left")



    fillnaCols = dfF.select_dtypes(include=["float64","int"]).columns
    dfF[fillnaCols]=dfF[fillnaCols].fillna(0)

    dfF['Value 2'] = dfF['CASH'] + dfF['CASH AND EQUIVALENTS'] + dfF['SHORT TERM INVESTMENTS'] + dfF['LONG TERM INVESTMENTS'] - dfF['MINORITY INTEREST'] - dfF['TOTAL LIAB']
    dfF['Net Profit Margin'] = dfF['NET INCOME']/dfF['TOTAL REVENUE']                     
    dfF['Operating Profit Margin'] = dfF['OPERATING INCOME']/dfF['TOTAL REVENUE']
    dfF['EBITDA Margin'] = dfF['EBITDA']/dfF['TOTAL REVENUE']
    dfF['Gross Profit Margin'] = dfF['GROSS PROFIT']/dfF['TOTAL REVENUE']
    dfF['DATE']=pd.to_datetime(dfF['DATE']).dt.date
    dfF['C/R'] = dfF['TOTAL CURRENT ASSETS']/dfF['TOTAL CURRENT LIABILITIES']
    dfF['D/E'] = (dfF['LONG TERM DEBT'] + dfF['SHORT LONG TERM DEBT TOTAL'])/dfF['TOTAL STOCKHOLDER EQUITY']
    dfF['ROIC'] = dfF['EBIT']/(dfF['LONG TERM DEBT'] + dfF['SHORT LONG TERM DEBT TOTAL'] + dfF['TOTAL STOCKHOLDER EQUITY'])



    dfF['Fair Value (30)'] = ((dfF['FREE CASH FLOW']*30)+(dfF['Value 2']))/dfF['SHARES OUTSTANDING']
    dfF['Fair Value (15)'] =((dfF['FREE CASH FLOW']*15)+(dfF['Value 2']))/dfF['SHARES OUTSTANDING']
    dfF['Fair Value (45)'] =((dfF['FREE CASH FLOW']*45)+(dfF['Value 2']))/dfF['SHARES OUTSTANDING']

    
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
    

    #Screener Section 
    met_list = [rev_type,fcf,roic,gm,ebitda_m,npm,d_e,c_r]
    label = [-2,-1,0,1,2,3]
    colnameg = [" 10y-growth"," 5y-growth"," 3y-growth"," 1y-growth"]
    colnameav = [" 10y-average"," 5y-average"," 3y-average"," 1y-average"]

    for metrics in met_list:
        for co in colnameg+colnameav:
            try:
                if metrics in [rev_type,fcf,roic,npm]:
                        bins = [-100000,-0.1,0,0.07,0.15,0.3,100000]

                elif metrics == c_r:
                        bins = [0,0.05,0.2,0.75,1.5,2.5,100000]
                        labels=[-2,-1,0,1,2,3]  
                
                elif metrics ==d_e:
                        bins = [0,0.05,1,1.5,3,5,100000]
                
                else:
                    bins = [-100000,-0.1,0,0.1,0.25,0.5,100000]
                        
                multidfC[f'{metrics}{co}-scale'] = pd.cut(multidfC[f'{metrics}{co}'],bins=bins,labels=label)
            
            except:
                pass
        

        field = "field"
        headerName = "headerName"
        children = "children"

        numtypes = ["int64","float64","int32","float32"]
        datetypes = ["datetime64[ns]"]

        #Name Field 
            
        group_name = {}
        group_name[headerName] = "Company Name"
        children_name = []
        cddict = {}
        cddict[field] = coName
        cddict["pinned"] = "left"
        cddict["filter"] ='agSetColumnFilter'
        children_name.append(cddict)
        group_name[children]=children_name


        #PRIMARY SCREENERS 
        primary_screeners = [sector,industry,"Market Cap Scale",marketCap,"COUNTRY"]


        children_primary = []
        cddict = {}

        for i in primary_screeners:
            cddict[field] = i  
                
            if i == sector:
                cddict["columnGroupShow"] = "close"
            
            else:
                cddict["columnGroupShow"] = "open"


            if multidfC[i].dtype in numtypes:
                cddict["filter"] ='agNumberColumnFilter' 
            else:
                cddict["filter"] ='agSetColumnFilter'

            children_primary.append(cddict)
            cddict = {}
        group_primary = {}
        group_primary[headerName]="Primary Screener"
        group_primary[children]=children_primary

        
        # DESCRIPTIVE SCREENERS
        coledr = ["Rating","Earnings Date"]
        edate=[]
        for col in dfT.columns:
            for c in coledr:         
                if c in col:
                    edate.append(col)

        descriptive_screener = []
        ds = descriptive_screener+edate
        
        children_descriptive = []
        cddict = {}
        count = 0

        for i in ds:
            cddict[field] = i 
            if count == 0: 
                cddict["columnGroupShow"] = "close"
                
            else:
                cddict["columnGroupShow"] = "open"
            if multidfC[i].dtype in numtypes:
                cddict["filter"] ='agNumberColumnFilter' 
            elif multidfC[i].dtype in datetypes:
                cddict["filterType"] ='date' 
            else:
                cddict["filter"] ='agSetColumnFilter'
            children_descriptive.append(cddict)
            cddict = {}
            count += 1

        group_descriptive = {}
        group_descriptive[headerName]="Descriptive Screener"
        group_descriptive[children]=children_descriptive



        # CURRENT FUNDAMENTAL SCREENER 
        
        children_fundamental = []
        cddict = {}
        count = 0

        for i in dfM['title'].unique():
            cddict[field] = i 
            if i in [roic,gm,ebitda_m,npm,d_e,c_r,rev_type,fcf]: 
                if count <= 1:
                    cddict["columnGroupShow"] = "close"
                else:
                    cddict["columnGroupShow"] = "open"
                count += 1
            
            else:
                cddict["hide"] = True

            if i in multidfC.columns.tolist():
                if multidfC[i].dtype in numtypes:
                    cddict["filter"] ='agNumberColumnFilter' 
                else:
                    cddict["filter"] ='agTextColumnFilter'
            children_fundamental.append(cddict)
            cddict = {}
            

        group_fundamental = {}
        group_fundamental[headerName]="Current Fundamental Screener"
        group_fundamental[children]=children_fundamental
        

        #  Technical Filter 
        coldfT = dfT.columns[3:].tolist()
        coldfT.append("SHARES OUTSTANDING")
        tdfT = []
        for co in coldfT:
            if co not in edate:
                tdfT.append(co)

        children_technical = []
        cddict = {}
        count = 0

        for i in tdfT:
            cddict[field] = i 
            if i in [pe,pcf]: 
                cddict["columnGroupShow"] = "close"
                
            else:
                cddict["columnGroupShow"] = "open"
            if multidfC[i].dtype in numtypes:
                cddict["filter"] ='agNumberColumnFilter' 
            else:
                cddict["filter"] ='agTextColumnFilter'
            children_technical.append(cddict)
            cddict = {}
            count += 1

        group_technical = {}
        group_technical[headerName]="Technical Screener"
        group_technical[children]=children_technical


        ### GROWTH FILTERS 
        gcols10 = [col for col in multidfC.columns if '10y-growth' in col]
        gcols5 = [col for col in multidfC.columns if '5y-growth' in col]
        gcols3 = [col for col in multidfC.columns if '3y-growth' in col]        
        gcols1 = [col for col in multidfC.columns if '1y-growth' in col]
                        
        gcol = gcols10 + gcols5 + gcols3 + gcols1
        children_growth = []
        cddict = {}
        for i in gcol:
            cddict[field] = i 
            if i in  [f"{rev_type}{colnameg[3]}",f"{fcf}{colnameg[3]}"] :
                cddict["columnGroupShow"] = "close"
            elif i in  [f"{rev_type}{colnameg[2]}",f"{fcf}{colnameg[2]}"] :
                cddict["columnGroupShow"] = "open"
            elif i in  [f"{rev_type}{colnameg[1]}",f"{fcf}{colnameg[1]}"] :
                cddict["columnGroupShow"] = "open"
            elif i in  [f"{rev_type}{colnameg[0]}",f"{fcf}{colnameg[0]}"] :
                cddict["columnGroupShow"] = "open"


            else:
                cddict["hide"] = True

            if multidfC[i].dtype in numtypes:
                cddict["filter"] ='agNumberColumnFilter' 
            else:
                cddict["filter"] ='agTextColumnFilter' 
            
            children_growth.append(cddict)
            cddict = {}
            

        group_growth = {}
        group_growth[headerName]="Growth Screener"
        group_growth[children]=children_growth


        # AVERAGE SCREENERS 
        acols10 = [col for col in multidfC.columns if '10y-average' in col]
        acols5 = [col for col in multidfC.columns if '5y-average' in col]
        acols3 = [col for col in multidfC.columns if '3y-average' in col]
        acols1 = [col for col in multidfC.columns if '1y-average' in col]

        acol = acols10 + acols5 + acols3 + acols1
        avg_met = [gm,ebitda_m,npm,d_e,c_r]
        children_average = []
        cddict = {}
        for i in acol:
            cddict[field] = i 
            
            if i in  [f"{gm}{colnameav[3]}",f"{ebitda_m}{colnameav[3]}",f"{npm}{colnameav[3]}",f"{d_e}{colnameav[3]}",f"{c_r}{colnameav[3]}"] :
                cddict["columnGroupShow"] = "close"
            elif i in  [f"{gm}{colnameav[2]}",f"{ebitda_m}{colnameav[2]}",f"{npm}{colnameav[2]}",f"{d_e}{colnameav[2]}",f"{c_r}{colnameav[2]}"]:
                cddict["columnGroupShow"] = "open"
            elif i in  [f"{gm}{colnameav[1]}",f"{ebitda_m}{colnameav[1]}",f"{npm}{colnameav[1]}",f"{d_e}{colnameav[1]}",f"{c_r}{colnameav[1]}"] :
                cddict["columnGroupShow"] = "open"
            elif i in  [f"{gm}{colnameav[0]}",f"{ebitda_m}{colnameav[0]}",f"{npm}{colnameav[0]}",f"{d_e}{colnameav[0]}",f"{c_r}{colnameav[0]}"] :
                cddict["columnGroupShow"] = "open"


            else:
                cddict["hide"] = True

            if multidfC[i].dtype in numtypes:
                cddict["filter"] ='agNumberColumnFilter' 
            else:
                cddict["filter"] ='agTextColumnFilter' 
            
            children_average.append(cddict)
            cddict = {}
            

        group_average = {}
        group_average[headerName]="Average Screener"
        group_average[children]=children_average


        # RATING SCREENERES 
        cols = [col for col in multidfC.columns if 'scale' in col]
        
        children_rating = []
        cddict = {}
        for i in cols:
            cddict[field] = i 
            if i in  [f"{rev_type}{colnameg[1]}-scale",f"{fcf}{colnameg[1]}-scale",f"{gm}{colnameav[1]}-scale",f"{ebitda_m}{colnameav[1]}-scale",f"{npm}{colnameav[1]}-scale",f"{d_e}{colnameav[1]}-scale",f"{c_r}{colnameav[1]}-scale"] :
                cddict["columnGroupShow"] = "close"
            elif i in i in  [f"{rev_type}{colnameg[0]}-scale",f"{fcf}{colnameg[0]}-scale",f"{gm}{colnameav[0]}-scale",f"{ebitda_m}{colnameav[0]}-scale",f"{npm}{colnameav[0]}-scale",f"{d_e}{colnameav[0]}-scale",f"{c_r}{colnameav[0]}-scale"]:            cddict["columnGroupShow"] = "open"
            
            else:
                cddict["hide"] = True

            
            cddict["filter"] ='agSetColumnFilter'
            
            children_rating.append(cddict)
            cddict = {}
            

        group_rating = {}
        group_rating[headerName]="RATINGS"
        group_rating[children]=children_rating



        gridOptions = {
        "columnDefs": [group_name,group_primary,group_descriptive,
                group_fundamental,
                group_technical,
                group_growth,
                group_average,
                group_rating],

        "defaultColDef": {"selection_mode":"multiple", 
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
        
        

    return dfC,dfF,multidfC,dfQ,dfM,dfT,dfSH,dfOff,dfEA,dfEH,dfET,gridOptions



