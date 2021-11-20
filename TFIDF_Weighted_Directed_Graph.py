import pandas as pd
import networkx as nx
import numpy as np
import string
import random

'''
This is an implementation of using TF-IDF in the system call graph as coefficients in the pagerank algorithm.
We the TFIDF is added as node attributes
For more details review 
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0211373
'''


## generate random data in edglist form 
def generate_malware_data(n):
  d = []
  for i in range(n):
    a = ''.join(random.choices(string.ascii_letters[:5], k=3))
    b = ''.join(random.choices(string.ascii_letters[:5], k=3))
    w = random.choice(range(10)[1:])
    c = ''.join(random.choices(string.ascii_uppercase[:3], k=3))
    d.append([a,b,w,c])
  return d
  
  
  
def calculate_edgelist_tfidf(d):
    df = pd.DataFrame(d, columns=['n1','n2','w','class'])
    df1 = df[['class', 'n1', 'w']]
    df1.columns = ['class', 'node', 'w']
    df2 = df[['class', 'n2', 'w']]
    df2.columns = ['class', 'node','w']
    dff = pd.concat([df1,df2]).drop_duplicates()

    ## Starting  TFIDF
    dfff = dff.pivot_table(columns = 'node', index='class', values='w')

    ##TF
    dfff.loc['total'] = dfff.count(axis=0)
    ##IDF
    dfff.loc['log_result'] = np.log10((len(dfff)-1)/dfff.loc['total'])

    ##TFIDF
    dffff = dfff*dfff.loc['log_result']
    dffff = dffff.loc[dffff.index[:-2]]

    ## add TFIDF as nodes attributes 
    nodes = []
    for i in dffff.columns:
        for j in dffff.index:
            nodes.append([j,i,dffff.loc[j,i]])

    df_nodes = pd.DataFrame(nodes, columns=['class','node', 'p'])
    df_nodes.dropna(inplace=True)
    df.set_index('class', inplace=True)
    df.sort_index(inplace=True)
    df_nodes.set_index('class',inplace=True)
    return df, df_nodes



## Build graph
def build_graph(df, df_nodes):
    ## We assume there are different malware families  index/class
    ## The keys of the dictionary is the malware family
    Graph={}
    for cl in list(set(list(df.index))):
        dd = [tuple(i) for i in df.loc[cl][['n1', 'n2', 'w']].values]
        G = nx.DiGraph() 
        G.add_weighted_edges_from(dd)
        dict_node = {}
        for i in df_nodes.loc[cl].drop_duplicates().values:
            G.nodes[i[0]]['tfidf'] = i[1] 
        Graph[cl] = G
    return Graph



def main():
    d = generate_malware_data(400)
    df, df_nodes = calculate_edgelist_tfidf(d)
    graph = build_graph(df, df_nodes)
    retrun graph

if __name__ == '__main__':
  main()
