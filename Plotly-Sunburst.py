import streamlit as st
import pandas as pd
import plotly.express as px


df = px.data.tips()

# create two figures based on the same data, but with different values
fig1 = px.sunburst(df, path=['day', 'time', 'sex'], values='total_bill')
fig2 = px.sunburst(df, path=['day', 'time', 'sex'], values='tip')
# save the data of each figure so we can reuse that later on
ids1 = fig1['data'][0]['ids']
labels1 = fig1['data'][0]['labels']
parents1 = fig1['data'][0]['parents']
values1 = fig1['data'][0]['values']
ids2 = fig2['data'][0]['ids']
labels2 = fig2['data'][0]['labels']
parents2 = fig2['data'][0]['parents']
values2 = fig2['data'][0]['values']

# create updatemenu dict that changes the figure contents
updatemenus = [{'buttons': [{'method': 'update',
                             'label': 'total_bill',
                             'args': [{
                                  'names': [labels1],
                                  'parents': [parents1],
                                  'ids': [ids1],
                                  'values': [values1]
                                 }]
                              },
                            {'method': 'update',
                             'label': 'tip',
                             'args': [{
                                  'names': [labels2],
                                  'parents': [parents2],
                                  'ids': [ids2],
                                  'values': [values2]
                                 }]
                             }],
                'direction': 'down',
                'showactive': True}]

# create the actual figure to be shown and modified
fig = px.sunburst(values=values1, parents=parents1, ids=ids1, names=labels1, branchvalues='total')
fig.update_layout(updatemenus=updatemenus)
st.plotly_chart(fig)
