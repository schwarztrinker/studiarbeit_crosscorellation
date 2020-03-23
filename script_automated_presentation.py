import networkx as nx
import matplotlib.pyplot as plt

import mysql.connector as sql



def main():

    mydb = sql.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="crosscorr"
    )

    #### SQL Abfrage
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM u1 where score>=0.3 and ymax>=0.3")
    	
    myresultArray = mycursor.fetchall()

    for data in myresultArray: 
        print(data)

    G = nx.MultiDiGraph()

    for data in myresultArray:
        G.add_node(data[0])
        G.add_node(data[1])

    for data in myresultArray:
        if data[4]<0:
            G.add_edge(data[0],data[1], s=data[4])
        else: 
            G.add_edge(data[1], data[0], s=data[4])

    pos = nx.spring_layout(G)
    plt.figure()    

    nx.draw(G,pos,edge_color='black',width=1,linewidths=1, node_size=100, node_color='grey',alpha=0.9, labels={node:node for node in G.nodes()})

    nx.draw_networkx_edge_labels(G,pos, font_color='black', font_size=6.0, font_family='sans-serif')

    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
