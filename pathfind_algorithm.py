import math
from parser_config import Parser
from classes_types import Hub, Graph, Drone, Simulation
import sys
from graphic_interface.app import App


class Solver_path:
    pass

    def bfs(list_class_hubs, start_hub, end_hub) -> list:
        """começa no start
        pra cada hub da fila, percorre o hub.connections
        se o vizinho (em conn.target nao for visitado, add na fila)"""
        visited = set()
        queue = []
        visited.add(start_hub)
        queue.append((start_hub, [start_hub]))
        for hub, path in queue:
            for conect in hub.connections:
                neig = conect.target
                if neig.name == end_hub.name:
                    return path + [neig]
                if neig not in visited:
                    visited.add(neig)
                    queue.append((neig, path + [neig]))

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
        end_hub.max_drones = 10*nb_drones
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
        # for i in list_class_hubs:
            # print(vars(list_class_hubs[i]))

    # Calls the Solver path objtc
        print([conn.target.name for conn in start_hub.connections])
        algo = Solver_path
        # for i in list_class_hubs:
        #   if i.zone = 'normal':
        #       algo.dijska
        #   else:
        path = algo.bfs(list_class_hubs, start_hub, end_hub)
        print([h.name for h in path])

        list_drones = []
        for d in range(1, nb_drones+1):
            drone = Drone(f"D{d}", start_hub, path)
            list_drones.append(drone)

        simulator = Simulation()
        # for i in range(len(path)):
        #   simulator.update_drones(list_drones)
    app = App()

    def start():
        graph_points = app.draw_graph(list_class_hubs, list_drones, start_hub)
        app.update_info(list_drones)
        app.btn_start.configure(
            command=lambda: app.animate(list_drones, graph_points, simulator)
        )

    app.after(100, start)
    app.mainloop()
