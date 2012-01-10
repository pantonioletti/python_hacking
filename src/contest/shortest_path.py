'''
Created on 26-05-2009

Euler project problem # 16
@author: pantonio
'''
def relax(target, new_node, previous_node):
    ret_val = False
    if (target is not None):
        if (target > new_node + previous_node):
            ret_val = True
    return ret_val

def dijkstra(d_matrix, adj_list, nodes):
    sp = dict()
    source = 0
    sp[source] = 0
    for i in range(nodes):
        children=adj_list[i]
        for j in range(len(children)):
            new_d = sp[i] + d_matrix[i][children[j]]
            d = sp.get(children[j])
            if (d is None):
                sp[children[j]] = new_d
            else:
                if (d < new_d):
                    sp[children[j]] = new_d
    pass
    
def problem17():
        nodes = 16 * 17 / 2
        levels = 16
        dist = [(75,),
              (95, 64,),
              (17, 47, 82,),
              (18, 35, 87, 10,),
              (20, 4, 82, 47, 65,),
              (19, 1, 23, 75, 3, 34,),
              (88, 2, 77, 73, 7, 63, 67,),
              (99, 65, 4, 28, 6, 16, 70, 92,),
              (41, 41, 26, 56, 83, 40, 80, 70, 33,),
              (41, 48, 72, 33, 47, 32, 37, 16, 94, 29,),
              (53, 71, 44, 65, 25, 43, 91, 52, 97, 51, 14,),
              (70, 11, 33, 28, 77, 73, 17, 78, 39, 68, 17, 57,),
              (91, 71, 52, 38, 17, 14, 91, 43, 58, 50, 27, 29, 48,),
              (63, 66, 4, 68, 89, 53, 67, 30, 73, 16, 69, 87, 40, 31,),
              (4, 62, 98, 27, 23, 9, 70, 98, 73, 93, 38, 53, 60, 4, 23,)];


        cur_node = 0
        adj_list = dict()
        dist_matrix = dict()
        # As nodes can be thought as distributed in a pyramid we
        # will iterate through the levels of this pyramid, each
        # level has number 'level' of nodes
        for level in range(levels-1):
            # First exception level 0 has ...... 1 node
            if (level == 0):
                children = []
                dist_matrix[cur_node]=dict()
                children.append(cur_node + 1)
                dist_matrix[cur_node][cur_node + 1]=dist[level][0]
                adj_list[cur_node] = children
                cur_node += 1      
            else:
                # Nodes will be named as its position number in a sequence starting
                # at the edge of the pyramid moving from left to right, at the end of
                # level continuing on the next level
                children = []
                dist_matrix[cur_node]=dict()
                cur_next_level_node = int((level*(level+1)/2)+1)
                dist_counter = 0
                for node in range(level):
                    children.append(cur_next_level_node)
                    dist_matrix[cur_node][cur_next_level_node]=dist[level][dist_counter]
                    cur_next_level_node += 1
                    dist_counter += 1
                    children.append(cur_next_level_node)
                    dist_matrix[cur_node][cur_next_level_node]=dist[level][dist_counter]
                    adj_list[cur_node] = children
                    cur_node += 1
                    children = []
                    dist_matrix[cur_node]=dict()
                   
        res = dijkstra(dist_matrix, adj_list, cur_node)
        #pass
        

if __name__ == '__main__':
    problem17()