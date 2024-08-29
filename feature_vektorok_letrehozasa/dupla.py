import re
import os
import json
import numpy as np
import networkx as nx
import math
import pandas as pd



keys = ['Goals_scored', 'Total_attemps','One_target','Off_target','Blocked','Woodwork','Saves','Corners','Offsides','Total_time_played','Ball_possession','Yellow_cards','Red_cards','Fouls_committed','Fouls_suffered','Passes_attemted','Short_Passes_attemted','Medium_Passes_attemted','Long_Passes_attemted','Passes_completed','Short_Passes_completed','Medium_Passes_completed','Long_Passes_completed','Pass_completion_rate','Short_rate','Medium_rate','Long_rate','Into_the_attacking_third','Into_the_key_area','Into_the_penalty_area']

col1 =['attemps', 'ishometeam', 'Corners', 'Offsides','Ball_Posession','Yellow_cards','Red_cards','Fouls_suffered',
    'passes_attemted','passes_completed','pass_completion_rate']

col2 =['diameter', 'largest_cliques', 'countmax_cliques', 'reciprocity', 'global_clustering','diversity', 'hubs',
      'authorities','pagerank_max','pagerank_mean','pagerank_median', 'assortativity', 'AverageNeighborhood',
      'degree_centralization','betweenness_centralization','closeness_centralization']

col = col1+col2

col_all = ["f_" + elem for elem in col] + ["s_" + elem for elem in col]

def create_modell_with_match_stats(data,team):
    #attemps, ishometeam, Corners, Offsides,Ball_Posession,Yellow_cards,Red_cards,Fouls_suffered
    #passes_attemted,passes_completed,pass_completion_rate
    
    model = []

    attemps = int(data[team][keys[1]].split()[-1])
    model.append(attemps)

    if team == 'FirstTeam':
        model.append(1)
    else:
        model.append(0)

    corners = int(data[team][keys[7]].split()[-1])
    model.append(corners)

    offsides = int(data[team][keys[8]].split()[-1])
    model.append(offsides)
    
    ball_possession =int(data[team][keys[10]].split()[-1].replace("%", ""))
    #last_num = text.split()[-1]
    model.append(ball_possession/100)

    yellow_cards = int(data[team][keys[11]].split()[-1])
    model.append(yellow_cards)

    red_cards = int(data[team][keys[12]].split()[-1])
    model.append(red_cards)

    fouls_suffered = int(data[team][keys[14]].split()[-1])
    model.append(fouls_suffered)

    passes_attemted = int(data[team][keys[15]].split()[-1])
    model.append(passes_attemted)

    passes_completed = int(data[team][keys[19]].split()[-1])
    model.append(passes_completed)

    pass_completion_rate = int(data[team][keys[23]].split()[-1].replace("%", ""))
    model.append(pass_completion_rate/100)

    return model

def get_hubs(G):
    pr = nx.pagerank(G, alpha=0.85, weight='weight', max_iter=100)
    hubs = np.array([pr[node] for node in G.nodes()])
    hubs_threshold = np.percentile(hubs, 75)
    return hubs_threshold

def get_diversity(G):
    entropies = []
    for node in G.nodes():
        incident_weights = [G.get_edge_data(node, neighbor)['weight'] for neighbor in G.successors(node)]
        incident_weights = [x/sum(incident_weights) for x in incident_weights]
        entropy = -sum([p*math.log(p) for p in incident_weights])
        entropies.append(entropy)
    # a csomopontok kozotti atlag entropya 
    return np.median(entropies)
    
def get_authorities(G):
    authorities = nx.hits(G, max_iter=100)[1]
    return np.percentile(list(authorities.values()), 75)

def create_modell_with_pass_network(distances):
    #diameter, largest cliques, countmax cliques, reciprocity, global_clustering,diversity, hubs, authorities
    #pagerank [max,mean,median], assortativity, Average Neighborhood, 
    #degree_centralization,betweenness_centralization,closeness_centralization
    model = []
    G = nx.DiGraph()
    #atalakitas el listava
    edges = []
    for i in range(distances.shape[0]):
        for j in range(distances.shape[0]):
            if distances[i,j] != -1 and distances[i,j] != 0:
                edges.append((i, j, {'weight': distances[i,j]}))
    
    G.add_edges_from(edges)

    
    # kiszámítjuk a legnagyobb távolságot minden csúcspárra
    all_pairs_shortest_path_lengths = dict(nx.all_pairs_dijkstra_path_length(G))
    # kiválasztjuk a legnagyobb távolságok közül a legnagyobbat
    diameter = max(max(lengths.values()) for lengths in all_pairs_shortest_path_lengths.values())
    model.append(diameter)

    # átalakítás irányítatlan grafa
    G_undirected = G.to_undirected()
    # élek súlyozása 1-el
    for (u, v) in G_undirected.edges():
        G_undirected.edges[u,v]['weight'] = 1
    # legnagyobb klika keresése
    cliques = list(nx.find_cliques(G_undirected))
    largest_clique = len(max(cliques, key=len))
    #print("Legnagyobb klika:", largest_clique)

    # maximális klikkek darab számának meghatározása
    max_clique_count = sum(1 for clique in cliques if len(clique) == largest_clique)

    model.append(largest_clique)
    model.append(max_clique_count)

    #reciprocity számítása
    reciprocity = nx.reciprocity(G)
    model.append(reciprocity)
    
    #globalis klaszter számítása
    global_clustering = nx.transitivity(G)
    model.append(global_clustering)

    
    diversity = get_diversity(G)
    model.append(diversity)
        
    hubs = get_hubs(G)
    model.append(hubs)

    authorities = get_authorities(G)
    model.append(authorities)

    # Compute the PageRank
    pr = nx.pagerank(G, weight='weight', alpha=0.85)

    # Print the PageRank scores
    pr_max = max(pr.values())
    pr_values = list(pr.values())
    pr_mean = np.mean(pr_values)
    pr_median = np.median(pr_values)
    model.append(pr_max)
    model.append(pr_mean)
    model.append(pr_median)

    assortativity = nx.degree_assortativity_coefficient(G)
    model.append(assortativity)


    #avg_neigh_degree = nx.average_neighbor_degree(G)
    # 
    avg_neighborhoods = nx.average_neighbor_degree(G)

    # Compute the overall average neighborhood for the graph
    graph_avg_neighborhood = sum(avg_neighborhoods.values()) / len(avg_neighborhoods)

    model.append(graph_avg_neighborhood)

    # Fokszámalapú központosítás
    degree_centralization = nx.algorithms.centrality.degree_centrality(G)

    # Közvetítő pontalapú központosítás
    betweenness_centralization = nx.algorithms.centrality.betweenness_centrality(G, normalized=True, weight=None)

    # Közelségalapú központosítás
    closeness_centralization = nx.algorithms.centrality.closeness_centrality(G)

    model.append(sum(degree_centralization.values()))
    model.append(sum(betweenness_centralization.values()))
    model.append(sum(closeness_centralization.values()))
    
    del G
    return model


def main(ev):
    path1 = "./data/match_stats/" + str(ev)  
    path2 = "./data/pass_network/" + str(ev)
    X_all = []
    y_all = []
    X = []
    y = []
    first = []
    second = []
    counter = 0
    for filename in os.listdir(path1):
        #if os.path.isfile(os.path.join(path, filename)):
            #outfname = re.search(r'^(\d+)_', filename).group(1)
            #output_file = 'data/output/'+str(ev)+'/'+ outfname+'.json'
            #input_file = './data/input/'+str(ev)+'/'+filename
        temp = int(filename.split(".")[0])
        if (temp>= 2027013 and temp<=2027034) or (temp>= 2029263 and temp<=2029384) or (temp>= 2032628 and temp<=2032652) or (temp>= 2035481 and temp<=2035649):
            continue
        firstfile = path1 + '/' + filename
        secondfile = path2 + '/' + filename
        # Első JSON fájl beolvasása
        with open(firstfile, encoding='utf-8') as f:
            data1 = json.load(f)

        # Második JSON fájl beolvasása
        with open(secondfile, encoding='utf-8') as f:
            data2 = json.load(f)

        first = create_modell_with_match_stats(data1,'FirstTeam')
        second = create_modell_with_match_stats(data1,'SecondTeam')
        print(filename)
        first_scored =  int(data1['FirstTeam'][keys[0]].split()[-1])
        second_scored = int(data1['SecondTeam'][keys[0]].split()[-1])
        

       
        distances1 = np.array(data2['fmatrix'])
        #print(distances1)
        #print(distances1)
        #print(distances1[:5, :5])
        #exit()
        distances2 = np.array(data2['smatrix'])
        if distances1.size == 0 or distances2.size == 0:
            counter = counter+1
            continue
        distances1 = distances1[:11, :11]
        distances2 = distances2[:11, :11]
        fmodel = create_modell_with_pass_network(distances1)
        smodel = create_modell_with_pass_network(distances2)
        first_model = first+fmodel
        second_model = second+smodel
        
        X.append(first_model)    
        X.append(second_model)
        X_all.append(first_model+second_model)
        X_all.append(second_model+first_model)
        if(first_scored>second_scored):
            y.append(1)
            y.append(0)
            y_all.append(1)
            y_all.append(0)
        elif(first_scored<second_scored):
            y.append(0)
            y.append(1)
            y_all.append(0)
            y_all.append(1)
        else:
            y.append(0)
            y.append(0)
            y_all.append(0)
            y_all.append(0)
        #break 
    

    df = pd.DataFrame(X_all, columns=col_all)
    df['label'] = y_all
    global XX,yy
    XX = XX + X_all
    yy = yy+y_all
    # DataFrame kiírása CSV fájlba
    df.to_csv('./data/szurt_selejtezo/data'+str(ev)+'.csv', index=False)
    print(counter)
    print(str(ev) + " ev kesz!")


XX=[]
yy=[]
main(2020)
main(2021)
main(2022)
main(2023)

df = pd.DataFrame(XX, columns=col_all)
df['label'] = yy
df.to_csv('./data/szurt_selejtezo/data_all.csv', index=False)
