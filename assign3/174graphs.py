from collections import defaultdict		#Using default dictionaries; if a key is not found in the dictionary a new entry is created.

def ReadInputGraph(filename):			#This function reads the input graph from input file. The input file contains edges in the input graph.
    graph = defaultdict(set)			#Using default dictionary; Graph object initialized as empty dictionary set.
    with open(filename) as data_file:	#input file opened
        for line in data_file:			#for loop to raed each line in input file
            a, b = line.rstrip().split(' ')	#Extract the 2 numbers on each line in input file and save in variables a and b.
            a, b = int(a), int(b)		#Convert into integers
            graph[a].add(b)				#add in graph

    for i in range(1, len(graph.keys()) + 1):	#traverse all nodes for incoming egde
        if i not in set(graph.keys()):			#if not available(empty)
            graph[i] = set()					#initialize as empty set

    return dict(graph)							#return the graph set

def getBFS(graph, source):					#get BFS from source node
    visitedNodes, queue = set(), [source]	#define another set for visited nodes and queue for future nodes
    while queue:							#traverse the queue to check if nodes are available to visit
        node = queue.pop(0)					#remove first node in queue
        if node not in visitedNodes:		#if node not visited
            visitedNodes.add(node)			#mark as visited; add in visited nodes set
            queue.extend(graph[node] - visitedNodes)	# Add outgoing connections to queue (except visitedNodes)
    return visitedNodes						#return set

def getBFSedges(graph, source, destination):	#This function finds the shortest path from source node to destination node
    queue = [(source, [source])]				#let queue be a tuple with values : source node, source path[edges]
    while queue:								#traverse queue using while loop(while queue is not empty)
        (node, path) = queue.pop(0)				#remove first node in queue set
        for next in graph[node] - set(path):	#traverse the graph using for loop to check nodes not in visited nodes set
            if next == destination:				#while traversing, if destination node is achieved
                return path + [next]			#return path(set of edges)
            else:
                queue.append((next, path + [next]))	#else add current node to path set of nodes and continue
    return [source]								#if queue set is empty(return only the source node)

def timeDFS(graph, startVertex):				#This function is used to calculate the traverse time
    visitedNodes = set()						#initialize visitednodes, count and timeToTraverse variables
    count = [0]
    timeToTraverse = defaultdict(dict)

    def traverse(vertex):
        visitedNodes.add(vertex)
        count[0] += 1
        timeToTraverse[vertex]['discovery'] = count[0]

        for next_vertex in graph[vertex]:		#traverse graph set using for loop
            if next_vertex not in visitedNodes:	#if next vertex is not visited
                traverse(next_vertex)			#visit

        count[0] += 1							#increment count variable
        timeToTraverse[vertex]['finish'] = count[0]	#only one vertex

    traverse(startVertex)
    return timeToTraverse						#return value

def treeDFS(graph, startVertex):
    visitedNodes = set()						#initialize variables
    tree = []

    def compute_tree(vertex):
        visitedNodes.add(vertex)
        for next_vertex in graph[vertex]:
            if next_vertex not in visitedNodes:
                tree.append((vertex, next_vertex))
                compute_tree(next_vertex)

    compute_tree(startVertex)					#only one vertex
    return tree									#return value

def getDFSedges(tree, graph, order):			#This function is used to get the DFS for the given input graphs
    tree_graph = defaultdict(set)				#Using default dictionary; graphTree object initialized as empty dictionary set.
    for (n1, n2) in tree:						#traverse tree
        tree_graph[n1].add(n2)					#add node

    def getNext(node):							#This function gets next node
        for child in tree_graph[node]:
            yield child
            for grandchild in getNext(child):
                yield grandchild

    back = []									#initialize empty arrays to find egdes
    forward = []
    cross = []

    descends = defaultdict(set)					#Using default dictionary; descend object initialized as empty dictionary set.
    for n1 in graph.keys():						#traverse graph
        descents = getNext(n1)					#get next node
        for i in descents:
            descends[n1].add(i)					#add next node
        for n2 in descends[n1]:
            if n1 in graph[n2]:
                back.append((n2, n1))
            if n2 in graph[n1] and (n1, n2) not in tree:	#check if node not in tree
                forward.append((n1, n2))		#find forward nodes
                        

    for n1 in graph.keys():						#traverse graph using for loop
        for n2 in graph[n1]:
            if n1 not in descends[n2] and n2 not in descends[n1]:
                cross.append((n1, n2))    		#find cross nodes            
        
    return back, forward, cross					#return values

def orderInDFS(graph, startVertex):				#This function is used to compute order in DFS
    visitedNodes = set()						#initialization
    order = [startVertex]

    def CalculateOrder(vertex):					#This function is used to compute the topological order
        visitedNodes.add(vertex)
        for next_vertex in graph[vertex]:
            if next_vertex not in visitedNodes:
                order.append(next_vertex)
                CalculateOrder(next_vertex)

    CalculateOrder(startVertex)					#only one vertex
    return order								#return value


def getBFSOutput(graph_input, graph_output):	#This function generates an output file containing the requred BFS
    graph = ReadInputGraph(graph_input)			#Read file with input graph
    with open(graph_output, 'w') as output_file:	#write the output file
        output_file.write('Vertex: Distance [Path]\n')	#Write the line on top of the output file as in the given required output
        for node in range(1, len(graph.keys()) + 1):	#traverse the graph(for each node in graph)
            paths = getBFSedges(graph, 1, node)	#find the shortest path from source node to the current node
            if paths:							#if path is available
                output_file.write(str(node) + ' : ')			#return the node
                output_file.write(str(len(paths) - 1) + ' ')	#return the distance(number of edges(no. of nodes-1))
                output_file.write(str(paths) + '\n')	#return shortest path

def getDFSOutput(graph_input, graph_output):			#This function generates an output file containing the requred DFS
    graph = ReadInputGraph(graph_input)					#Read file with input graph
    with open(graph_output, 'w') as output_file:		#write the output file
        for node in range(1, len(graph.keys()) + 1):	#traverse the graph(for each node in graph)
            times = timeDFS(graph, 1)					#find the shortest path from source node to the current node
            output_file.write("Discover/Finish: "+str(node)+" : ")	#return discover/finish time
            if 'discovery' not in times[node]:
                output_file.write('None None\n')
            else:
                output_file.write(str(times[node]['discovery'])+' '+str(times[node]['finish'])+'\n')
        tree = treeDFS(graph, 1)
        output_file.write("Tree: "+str(tree)+'\n')		#return tree edges
        order = orderInDFS(graph, 1)        
        back, forward, cross = getDFSedges(tree, graph, order)
        output_file.write("Back: "+str(back)+'\n')		#return back edges from nodes
        output_file.write("Forward: "+str(forward)+'\n')#return forward edges from nodes
        output_file.write("Cross: "+str(cross)+'\n')	#return cross edges from nodes
        output_file.write("Vertices in topological order: "+str(order)+'\n')#return the vertices in topological order

if __name__ == "__main__":										#main, to call from command line
    getBFSOutput("data_1.txt", "BFS_output_graph1.txt")			#Process input file for graph 1 and generate output for its bfs
    getBFSOutput("data_2.txt", "BFS_output_graph2.txt")			#Process input file for graph 2 and generate output for its bfs
    getBFSOutput("data_3.txt", "BFS_output_graph3.txt")			#Process input file for graph 3 and generate output for its bfs

    getDFSOutput("data_1.txt", "DFS_output_graph1.txt")			#Process input file for graph 1 and generate output for its dfs
    getDFSOutput("data_2.txt", "DFS_output_graph2.txt")			#Process input file for graph 2 and generate output for its dfs
    getDFSOutput("data_3.txt", "DFS_output_graph3.txt")			#Process input file for graph 3 and generate output for its dfs
