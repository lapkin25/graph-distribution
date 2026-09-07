import pandas as pd
import numpy as np
import networkx as nx

def dict_to_list(centralities, nodes_list):
    values = []
    for v in nodes_list:
        values.append(centralities[v])
    return values

def calc_ranking(values_pd, method="ascending"):
    argsort = list(np.argsort(values_pd.to_numpy()))
    if method != "descending":
        argsort = argsort[::-1]
    ranking = []
    for i, val in enumerate(argsort):
        ranking.append(argsort.index(i) + 1)
    return ranking

def compute_centralities(G, nodes_list):
#    def compute_column(values):
#        values_list = pd.Series(dict_to_list(values, nodes_list))
#        return values_list, calc_ranking(values)
    df = pd.DataFrame()
 #   df['degree'], df['degree_rank'] = compute_column(nx.degree_centrality(G))

    df['degree'] = dict_to_list(nx.degree_centrality(G), nodes_list)
    df['degree_rank'] = calc_ranking(df['degree'])

    df['closeness'] = dict_to_list(nx.closeness_centrality(G), nodes_list)
    df['closeness_rank'] = calc_ranking(df['closeness'])

    #df['eigenvector'] = dict_to_list(nx.eigenvector_centrality(G), nodes_list)
    #df['eigenvector_rank'] = calc_ranking(df['eigenvector'])

    df['current_flow_closeness'] = dict_to_list(nx.current_flow_closeness_centrality(G), nodes_list)
    df['current_flow_closeness_rank'] = calc_ranking(df['current_flow_closeness'])

    df['betweenness'] = dict_to_list(nx.current_flow_betweenness_centrality(G), nodes_list)
    df['betweenness_rank'] = calc_ranking(df['betweenness'])

    df['current_flow_betweenness'] = dict_to_list(nx.current_flow_betweenness_centrality(G), nodes_list)
    df['current_flow_betweenness_rank'] = calc_ranking(df['current_flow_betweenness'])

    df['communicability_betweenness_centrality'] = dict_to_list(nx.communicability_betweenness_centrality(G), nodes_list)
    df['communicability_betweenness_centrality_rank'] = calc_ranking(df['communicability_betweenness_centrality'])

    df['load'] = dict_to_list(nx.load_centrality(G), nodes_list)
    df['load_rank'] = calc_ranking(df['load'])

    df['subgraph'] = dict_to_list(nx.subgraph_centrality(G), nodes_list)
    df['subgraph_rank'] = calc_ranking(df['subgraph'])

    df['harmonic'] = dict_to_list(nx.harmonic_centrality(G), nodes_list)
    df['harmonic_rank'] = calc_ranking(df['harmonic'])

#    df['dispersion'] = dict_to_list(nx.dispersion(G), nodes_list)
#    df['dispersion_rank'] = calc_ranking(df['dispersion'])

    df['laplacian'] = dict_to_list(nx.laplacian_centrality(G), nodes_list)
    df['laplacian_rank'] = calc_ranking(df['laplacian'])

    return df
