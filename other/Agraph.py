import streamlit
from streamlit_agraph import agraph, Node, Edge, Config

nodes = []
edges = []
nodes.append( Node(id="Tech", 
                   label="Technology", 
                   size=25, 
                   shape="circularImage",
                   image="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
            ) # includes **kwargs
nodes.append( Node(id="META", 
                   label="META Platforms",
                   size=25,
                   shape="circularImage",
                   image="https://eodhistoricaldata.com/img/logos/US/MSFT.png") 
            )
edges.append( Edge(source="META",  
                   target="Tech", 
                   # **kwargs
                   ) 
            ) 

config = Config(width=1600, 
                height=1600, 
                # **kwargs
                ) 



return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)

                      
