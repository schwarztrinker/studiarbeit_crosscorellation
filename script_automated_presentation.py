import sys
import networkx as nx
import matplotlib.pyplot as plt


import mysql.connector as sql

def main():
    ### DEFINITION DER ZUGANGSADTEN ZUR DB
    mydb = sql.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="crosscorr"
    )
    
    #### SQL Abfrage
    mycursor = mydb.cursor()

    sqlStatement = "SELECT machine1, machine2, avg(score), avg(ymax), avg(timeGap) FROM u2 WHERE score>=0.5 AND ymax>=0.5  GROUP BY machine1, machine2" 

    if len(sys.argv) > 1:
        sqlStatement = ""+sys.argv[1]+""

    mycursor.execute(sqlStatement)
    	
    myresultArray = mycursor.fetchall()


    ##ERSTELLE MULTIDIREKTIONALEN GRAPH
    G = nx.MultiDiGraph()


    ### COLOR MAP
    color_map = []
    weights =[]


    ### ERSTELLE ALLE KNOTEN
    for data in myresultArray:
        G.add_node(data[0])
        G.add_node(data[1])


    ### SCHREIBE KANTEN DES SQL ARRAYS
    for data in myresultArray:
        if data[4]<0:
            G.add_edge(data[0],data[1], s=format(data[4], '.0f'))
        else: 
            G.add_edge(data[1], data[0], s=format(data[4], '.0f'))

    ### ZÄHLE EIN UND AUSGEHENDE KANTEN DER KNOTEN
    for node in G:
        edgesIn = G.in_edges(node)
        edgesOut = G.out_edges(node)

        color_map.append(edgeColorSwitcher(len(edgesIn), len(edgesOut)))
    
    #### BETA WEIGHTS
    #for edge in G.edges(data=True):
    #    if int(edge[2]['s'])<=10:
    #        weights.append(2)
    #    else:
    #        weights.append(1)


    ### ERRECHNE GRAFIK 
    pos = nx.spring_layout(G,k=0.6,iterations=200)

    ## PLOT FIG
    figure = plt.figure()    


    
    ## MALE GRAFIK MIT KONTENFARBEN UND KNOTENLABELS
    nx.draw(G,pos,edge_color='black',width=1,linewidths=1, node_size=500, node_color=color_map,alpha=0.9, labels={node:node for node in G.nodes()})
    ### SCHREIBE LABELS DER KANTEN
    nx.draw_networkx_edge_labels(G,pos, font_color='black', font_size=6.0, font_family='sans-serif')


    ####  PDF Plot
    #figure.savefig('./out.png', bbox_inches='tight', dpi=1000, quality=95,orientation='portrait')

    plt.axis('off')
    plt.show()


### RETURN NODE COLOR

def edgeColorSwitcher(edgesIn, edgesOut):
    ## EDGE INS
    if edgesIn==1 and edgesOut==0:
        return 'lightgreen'
    elif edgesIn==2 and edgesOut==0:
        return 'limegreen'
    elif edgesIn==3 and edgesOut==0:
        return 'forestgreen'
    elif edgesIn>=4 and edgesOut==0:
        return 'darkgreen'
    ## BOTH
    elif (edgesIn==1 or edgesIn==2) and (edgesOut==1 or edgesOut==2):
        return 'khaki'
    elif (edgesIn==3 or edgesIn==4) and (edgesOut==3 or edgesOut==4) :
        return 'orange'
    elif edgesIn>4 and edgesOut>4:
        return 'darkorange'
    ### EdgeOUT
    elif edgesIn==0 and edgesOut==1:
        return 'lightcoral'
    elif edgesIn==0 and edgesOut==2:
        return 'indianred'
    elif edgesIn==0 and edgesOut==3:
        return 'red'
    elif edgesIn==0 and edgesOut>=4:
        return 'darkred'
    else: return 'gold'

if __name__ == "__main__":
    main()


