import sys
from parser_config import Parser
from classes_types import Hub, Graph, Drone, Simulation
from pathfind_algorithm import Solver_path
from graphic_interface.app import App


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

    # Calls the Solver path class, and check which algo to use
        print([conn.target.name for conn in start_hub.connections])
        algo = Solver_path
        is_weigthed = False
        for k in list_class_hubs:
            if list_class_hubs[k].zone == 'restricted':
                is_weigthed = True
                break

        if is_weigthed is True:
            print("USANDO DIJKSTRA")
            all_paths = algo.dijkstra(list_class_hubs, start_hub, end_hub)
        else:
            print("USANDO BFS")
            all_paths = algo.bfs(list_class_hubs, start_hub, end_hub)
        print(all_paths)

        list_drones = []
        for d in range(1, nb_drones+1):
            drone = Drone(f"D{d}", start_hub, all_paths)
            path = all_paths[(d - 1) % len(all_paths)]
            drone = Drone(f"D{d}", start_hub, path)
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
