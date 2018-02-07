'''
This code implements the branch-and-bound algorithm for minimum vertex cover problem
'''

import heapq
import time
import os
import networkx as nx

class BnB(object):
    def __init__(self):
        pass
        
    def greedy_approximation_VC(self, G):
        '''
        Greedy approximation algorithm for vertex cover
        '''
        appro_vertex_cover, edges_covered = set(), set()

        for u, v in G.edges_iter():
            if not ((u, v) in edges_covered or (v, u) in edges_covered):
                appro_vertex_cover.update((u, v))
                for temp_u, temp_v in G.edges([u, v]):
                    edge = (temp_u, temp_v) if temp_u <= temp_v else (temp_v, temp_u)
                    edges_covered.add(edge)
        return appro_vertex_cover

    def get_childGraph(self, vertex, parent_graph):
        '''
        Get remaining graph by removing the vertex and all adjacent edges from parent_graph
        '''
        #child_graph = parent_graph.copy()      # slow step
        #child_graph.remove_node(vertex)
        parent_graph.remove_node(vertex)
        return parent_graph

    def vertex_with_maxDeg(self, marked_vertex, G):
        '''
        Get vertex with the maximum degree among unmarked vertex
        '''
        remaining_nodes = set(G.nodes()) - set(marked_vertex)
        nodes_deg_dict = G.degree(remaining_nodes)
        vertex = max(nodes_deg_dict, key=lambda key: nodes_deg_dict[key])
        return vertex

    def get_minimumVC(self, G, cutoff, sol, trace):
        '''
        Get minimum vertex cover of G and write results to sol and trace
        '''
        trace_output = open(trace, 'w')
        start_time = time.time()

        minVC_list = self.greedy_approximation_VC(G)
        minVC_val = len(minVC_list)
        ini_lowbnd = minVC_val / 2

        runtime = time.time() - start_time
        trace_output.write('{:.2f},{}\n'.format(runtime, minVC_val))

        allnodes_set = set(G.nodes())
        minPQ_subpbms = []
        heapq.heappush(minPQ_subpbms, (G.number_of_edges(), [set(), set(), ini_lowbnd]))

        while len(minPQ_subpbms) > 0:
            subpbm = heapq.heappop(minPQ_subpbms)

            parent_marked_vtx, parent_VC, parent_lowbnd = subpbm[1]
            parent_graph = G.subgraph(allnodes_set - parent_VC)

            vtx_maxDeg = self.vertex_with_maxDeg(parent_marked_vtx, parent_graph)
            #assert(vtx_maxDeg > 0)

            # Right branch: vtx_maxDeg is NOT selected but is still marked
            right_child_marked_vtx = set(parent_marked_vtx)
            right_child_marked_vtx.add(vtx_maxDeg)
            right_child_VC = set(parent_VC)
            right_lowbnd = parent_lowbnd

            unmarked_vtx = allnodes_set - right_child_marked_vtx
            unmarked_vtx_length = len(unmarked_vtx)

            if unmarked_vtx_length > 0 and set(parent_graph.neighbors(vtx_maxDeg)) <= unmarked_vtx:
                if right_lowbnd < minVC_val:
                    heapq.heappush(minPQ_subpbms, (parent_graph.number_of_edges(), \
                                   [right_child_marked_vtx, right_child_VC, right_lowbnd]))

            # Left branch: vtx_maxDeg is selected and marked
            left_child_marked_vtx = set(right_child_marked_vtx)
            left_child_VC = set(parent_VC)
            left_child_VC.add(vtx_maxDeg)
            left_child_graph = self.get_childGraph(vtx_maxDeg, parent_graph)

            if left_child_graph.number_of_edges() == 0:     # A vertex cover is found
                if len(left_child_VC) < minVC_val:
                    minVC_list = left_child_VC
                    minVC_val = len(left_child_VC)

                    runtime = time.time() - start_time
                    trace_output.write('{:.2f},{}\n'.format(runtime, minVC_val))

            elif unmarked_vtx_length > 0:
                left_lowbnd = len(left_child_VC) + len(self.greedy_approximation_VC(left_child_graph)) / 2
                if left_lowbnd < minVC_val:
                    heapq.heappush(minPQ_subpbms, (left_child_graph.number_of_edges(), \
                                   [left_child_marked_vtx, left_child_VC, left_lowbnd]))

            runtime = time.time() - start_time
            if runtime > cutoff:
                print 'Program terminated as cutoff time is reached'
                break

        trace_output.close()
        with open(sol, 'w') as f:
            f.write('{}\n'.format(minVC_val))
            result = sorted(list(minVC_list))
            for item in result[:-1]:
                f.write('{},'.format(item))
            f.write('{}'.format(result[-1]))

        return minVC_val, minVC_list

def test(filename):
    G = read_graph('./Data/{}'.format(filename))
    prefix = filename.split('.')[0]

    start_time =  time.time()
    minVC_BnB = BnB()
    minVC_val, minVC_list = minVC_BnB.get_minimumVC(G, cutoff=5*60,
                                sol='./test/{}.sol'.format(prefix),
                                trace='./test/{}.trace'.format(prefix))
    runtime = time.time() - start_time

    assert(minVC_check(minVC_list, G))
    print 'Minimum Vertex Cover for {}: {}'.format(prefix, minVC_val)
    print 'Elapsed Time for {}s: {}'.format(prefix, runtime)
    print

if __name__ == '__main__':
    from BnBHelperFuns import read_graph, minVC_check
    '''
    datafile_dir = './Data/'
    datafiles = [f for f in os.listdir(datafile_dir) \
                         if os.path.isfile(os.path.join(datafile_dir, f))]
    for datafile in datafiles:
        print 'Running BnB for {}'.format(datafile)
        test(datafile)
    '''
    test('netscience.graph')