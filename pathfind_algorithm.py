import math
from parser_config import Parser
from classes_types import Hub, Graph
import sys


class Solver_path:
    pass

    def bfs(list_class_hubs):
        """começa no start
        pra cada hub da fila, percorre o hub.connections
        se o vizinho (em conn.target nao for visitado, add na fila)"""
        visited = set()
        queue = []
        path = []
        visited.add(list_class_hubs[start_hub.name])
        queue.append(list_class_hubs[start_hub.name])
        print(f"set: visited: {visited}")
        print(f"Fila: {queue}")
        print(f"len queue {len(queue)}")
        for hub in queue:
            for neig in hub.connections:
                print(neig)
                if neig == list_class_hubs[end_hub.name]:
                    path.append(list_class_hubs[end_hub.name])
                    return path
                if neig not in visited:
                    print("entro ", neig)
                    for i in list_class_hubs:
                        if neig == list_class_hubs[i.name]:
                            queue.append(neig)

    def calculate_dist(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def dijskra(start, end):
        pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parser = Parser(sys.argv[1])
        (nb_drones, start_hub, list_hubs,
         end_hub, list_conects) = parser.get_data()
        start_hub = Hub(**start_hub)
        end_hub = Hub(**end_hub)
        # dijskra(start_hub, end_hub)

        list_class_hubs = {}
        list_class_hubs[start_hub.name] = start_hub
        list_class_hubs[end_hub.name] = end_hub
        for h in list_hubs:
            class_hub = Hub(**h)
            list_class_hubs[class_hub.name] = class_hub
        graph = Graph(list_class_hubs, start_hub, end_hub)
        for c in list_conects:
            graph.add_connection(list_class_hubs[c['a']],
                                 list_class_hubs[c['b']],
                                 c['max_link_capacity'] or 1)
        for i in list_class_hubs:
            print(vars(list_class_hubs[i]))

    # Calls the Solver path objtc
        algo = Solver_path
        # for i in list_class_hubs:
        #   if i.zone = 'normal':
        #       algo.dijska
        #   else:
        algo.bfs(list_class_hubs)
