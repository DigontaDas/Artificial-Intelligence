import heapq
def p_input(filename):
    a_list = {} #connection er value store kortese each cities er (adjacency list)
    h_value = {}  #estimated distance from each city to bucharest store kortese (heuristics value stores)
    with open(filename, "r") as file:
        lines = file.readlines()
    for i in lines:
        parts = i.strip().split() #proti line splits hocche
        
        if len(parts) < 2: #ekhane 2 deya cause 2 er theke choto length er gula ke empty dhortesi
            continue # Skip kortese empty lines gula
        city = parts[0]  #extract kortese city name
        h = int(parts[1])  #heuristic value gula extract kortese bucharest porjonto value ta
        h_value[city] = h
        print(h_value)
        a_list[city] = [] #neighbors gular jonno empty list initialize kortese
        
        for j in range(2, len(parts), 2): #adjacency list diye iterate kore and neighbor ar distance store kore
            neighbor = parts[j]  # City gula connect kortese neighbor er sathe
            distance = int(parts[j+1]) #neighbor er distance 
            a_list[city].append((neighbor, distance)) #adjacency list e store kortese
    return a_list, h_value
def a_star_search(graph, h_value, start_node, goal_node):
    open_set = []
    heapq.heappush(open_set, (h_value[start_node], 0, start_node, [start_node]))  #priority queue store kortese
    g_costs = {start_node: 0} # Store kortese shortest path costs g(n) to nodes
    while open_set: #search korte thake jotokhon priority queue empty na
        
        f_value, actual_cost, current_node, path = heapq.heappop(open_set) # lowest cost node remove kore
        
        
        if current_node == goal_node:
            return path, actual_cost #goal reach hoile path and actual cost return kore
        
        for neighbor_node, cost in graph[current_node]: #loop chole proti city te ghurar jonno
            new_actual_cost = actual_cost + cost  # actual cost neighbor e reach korte
            new_f = new_actual_cost + h_value[neighbor_node]  # estimated total cost neighbor diye gele according to A* er shutro 
            
            
            if neighbor_node not in g_costs or new_actual_cost < g_costs[neighbor_node]: #neighbor_node not in g_costs liksi first time visit korle neighbor ke ,ar new_actual_cost < g_costs[neighbor_node] ei part ta liksi cause shorter path tar jonno
                g_costs[neighbor_node] = new_actual_cost #cost update kortese to reach neighbor
                #priority queue te push kore updated path ta
                heapq.heappush(open_set, (new_f, new_actual_cost, neighbor_node, path + [neighbor_node]))
    
    return None, None #queue jodi empty hoi tahole kono valid path nai


file = "Input file.txt" 
# shudhu ei graph - A dictionary where keys are city names and values are lists of (neighbor, distance) pairs
graph, h_value = p_input(file) 
start, goal = input("Start node: "), "Bucharest"

#jodi bucharest theke keo bucharest e jaite chai
if start == goal: 
    print(f"Path: {start}")
    print("Total distance: 0 km")
    exit() #statement theke ber howar jonno
path, total_distance = a_star_search(graph, h_value, start, goal)

#join and output print korar jonno
if path:
    print("Path:", " -> ".join(path))
    print("Total distance:", total_distance, "km")
else:
    print("NO PATH FOUND")
