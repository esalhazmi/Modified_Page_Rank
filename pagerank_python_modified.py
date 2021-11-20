'''
I followed the codes implemented in networkx.
I replaced alpha by tfidf as nodes attributes
'''


def pagerank_python_modified(G):
    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G

    # Create a copy in (right) stochastic form
    W = nx.stochastic_graph(D, weight='weight')
    N = W.number_of_nodes()
    x = dict.fromkeys(W, 1.0 / N)
    p = dict.fromkeys(W, 1.0 / N)
    dangling_weights = p
    dangling_nodes = [n for n in W if W.out_degree(n, weight='weight') == 0.0]

    xlast = x
    x = dict.fromkeys(xlast.keys(), 0)

    ## replace coeffecient (alpha) by tfidf
    danglesum = sum(xlast[n]*G.nodes[n]['tfidf'] for n in dangling_nodes)
    for n in x:
        for _, nbr, wt in W.edges(n, data='weight'):
            ## replace coeffecient (alpha) by tfidf
            x[nbr] += G.nodes[nbr]['tfidf'] * xlast[n] * wt
        ## replace coeffecient (alpha) by tfidf
        x[n] += danglesum * dangling_weights.get(n, 0) + G.nodes[n]['tfidf'] * p.get(n, 0)
    return x

