import sys
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

    sqlStatement = "SELECT * From u1 where score>=0.6 and ymax>=0.2"

    if len(sys.argv) > 1:
        sqlStatement = ""+sys.argv[1]+""

    mycursor.execute(sqlStatement)
    	
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

    pos = nx.spring_layout(G,k=1,iterations=100)
    figure = plt.figure()    

    nx.draw(G,pos,edge_color='black',width=1,linewidths=1, node_size=1000, node_color='pink',alpha=0.9, labels={node:node for node in G.nodes()})

    nx.draw_networkx_edge_labels(G,pos, font_color='black', font_size=6.0, font_family='sans-serif')


    ####  PDF Plot
    ###figure.savefig('./out.pdf', bbox_inches='tight', dpi=1000)

    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
