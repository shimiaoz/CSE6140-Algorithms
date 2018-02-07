import networkx as nx
import time
import os

def read_graph(path_filename):
    '''
    Read graph from file and store as a networkx graph object
    '''
    G = nx.Graph()

    with open(path_filename, 'r') as f:
        graphInfo = f.readline()
        graphInfo = [int(item) for item in graphInfo.split()]
        num_nodes, num_edges = graphInfo[0], graphInfo[1]
        for i, line in enumerate(f, start=1):
            if line.split():
                nodesList = [int(item) for item in line.split()]
                edgesList = [(i, node) for node in nodesList]
                G.add_edges_from(edgesList)
            elif G.number_of_nodes() < num_nodes:   # Dealing with blank lines
                G.add_node(i)
    try:
        assert(num_nodes == G.number_of_nodes() and num_edges == G.number_of_edges())
    except:
        print 'Expected number of nodes and edges: {}, {}'.format(num_nodes, num_edges)
        print 'Actual number of nodes and edges: {}, {}'.format(G.number_of_nodes(), G.number_of_edges())
        raise AssertionError
    return G

def minVC_check(vertex_cover, G):
    graph = G.copy()
    graph.remove_nodes_from(vertex_cover)
    if graph.number_of_edges() == 0:
        return True
    else:
        print 'Remaining graph has {} edges'.format(graph.number_of_edges())
        return False

def greedy_approximation_VC_deprecated(G):
    '''
    Deprecated: Not efficient
    Greedy approximation algorithm for vertex cover
    '''
    appro_vertex_cover = set()
    while G.number_of_edges() > 0:
        u, v = G.edges()[0]
        appro_vertex_cover.update((u, v))
        G.remove_nodes_from([u, v])
    return appro_vertex_cover

if __name__ == '__main__':
    datafile_dir = './Data/'
    datafiles = [f for f in os.listdir(datafile_dir) \
                         if os.path.isfile(os.path.join(datafile_dir, f))]
    for datafile in datafiles:
        start_time = time.time()
        G = read_graph('./Data/{}'.format(datafile))
        runtime = time.time() - start_time
        print '{}: {}'.format(datafile, runtime)