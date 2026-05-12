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
        queue = []
        all_paths = []
        queue.append((start_hub, [start_hub], {start_hub}))
        for hub, path, visited in queue:
            for conect in hub.connections:
                neig = conect.target
                if neig.zone == 'blocked':
                    continue
                if neig.name == end_hub.name:
                    all_paths.append(path + [neig])
                elif neig not in visited:
                    new_visited = visited.copy()
                    new_visited.add(neig)
                    queue.append((neig, path + [neig], new_visited))
        return all_paths

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
        # for k in list_class_hubs:
        #    print("o i é", list_class_hubs[k])
        #    if list_class_hubs[k].zone != 'normal':
        #        path = algo.dijska
        #    else:
        all_paths = algo.bfs(list_class_hubs, start_hub, end_hub)
        print(all_paths)

        list_drones = []
        for d in range(1, nb_drones+1):
            drone = Drone(f"D{d}", start_hub, all_paths)
            caminho = all_paths[(d - 1) % len(all_paths)]
            drone = Drone(f"D{d}", start_hub, caminho)
            list_drones.append(drone)

        simulator = Simulation()
    # Initialize the Graphic visualization
    app = App()

    def start():
        graph_points = app.draw_graph(list_class_hubs, list_drones, start_hub)
        app.update_info(list_drones)
        app.btn_start.configure(
            command=lambda: app.animate(list_drones, graph_points, simulator)
        )

    app.after(100, start)
    app.mainloop()
