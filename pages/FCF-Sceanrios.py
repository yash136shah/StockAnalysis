import numpy as np
import matplotlib.pyplot as plt 
import streamlit as st 

st.title("FCF Multiples Scenario")

def scenario():
        from matplotlib import colors
        col1,col2 = st.columns(2)
        with col1:
            period = st.slider('Forecast Period (Years):',5,30,10)
        with col2:
            tgr = (st.slider('Terminal Growth Rate (%) :',0,10,2))/100
        #FCFs = {}
        PVs = {}
        growth = []
        discount_Rate = []

        growth = []
        discount_Rate = []

        for gro in range(30,0,-1):
             growth.append(gro)
             for dro in range(1,31):
                    if gro not in discount_Rate:
                        discount_Rate.append(dro)
                    #FCFs[gro,dro]=0
                    PVs[gro,dro]=0
                    for i in range(0,period+2):
                        #FCFs[gro,dro]+=(1*(1+gro/100))**i

                        try:
                            PVs[gro,dro]+=((1*(1+gro/100))**i)/((1+dro/100)**i)         
                            if i == period+1:
                                    PVs[gro,dro]-=((1*(1+gro/100))**i)/((1+dro/100)**i)   
                                    tva=((1*(1+gro/100))**i)*(1+gro/100)
                                    tv=(tva*(1+tgr))/((dro/100 - tgr))

                                        #FCFs[gro,dro]+=tv
                                    PVs[gro,dro]+= tv/((1+dro/100)**i)
                                    #except:
                                        #FCFs[gro,dro] = 0
                                        #PVs[gro,dro] = 0

                        except:
                            PVs[gro,dro]=0


        PVASS=[]
        for g in growth:
            x =[]
            PVASS.append(x)
            for d in discount_Rate:
              x.append(int((PVs[(g,d)])))

        PVA = np.array(PVASS)


        fig, ax = plt.subplots(figsize=(10,10))

        cmap = colors.ListedColormap(['black','black','white','lightgreen','green','yellow','orange','red','darkred','maroon'])
        bounds=[-0,0,5,10,15,45,75,100,200,2000]
        norm=colors.BoundaryNorm(bounds, cmap.N)

        im = ax.imshow(PVA,cmap=cmap,norm=norm)

        # Show all ticks and label them with the respective list entries
        ax.set_yticks(np.arange(len(growth)), labels=growth)
        ax.set_xticks(np.arange(len(discount_Rate)), labels=discount_Rate)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

        # Loop over data dimensions and create text annotations.
        for i in range(len(discount_Rate)):
            for j in range(len(growth)):
                text = ax.text(j, i,PVA[i, j],
                               ha="center", va="center", color="b")


        plt.ylabel("Growth Rate")
        plt.xlabel("Discount Rate")
        plt.colorbar(im, ax=ax)
        ax.set_title("Scenario of FCF multiple")
        st.pyplot(fig)

scenario()
