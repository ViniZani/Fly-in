import sys
from typing import Dict, List, Any
from parser_config import Parser
from classes_types import Hub, Graph, Drone, Simulation
from pathfind_algorithm import Solver_path
from graphic_interface.App import App


if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            parser: Parser = Parser(sys.argv[1])
            (nb_drones, start_hub_dict, list_hubs,
             end_hub_dict, list_conects) = parser.get_data()
            if (start_hub_dict is None or end_hub_dict is None
                    or list_conects is None):
                raise ValueError("[ERROR] None of the values can be None")
            start_hub: Hub = Hub(**start_hub_dict)
            end_hub: Hub = Hub(**end_hub_dict)
            end_hub.max_drones = 10 * nb_drones

            list_class_hubs: Dict[str, Hub] = {}
            list_class_hubs[start_hub.name] = start_hub
            list_class_hubs[end_hub.name] = end_hub
            for h in list_hubs:
                class_hub: Hub = Hub(**h)
                list_class_hubs[class_hub.name] = class_hub
            graph: Graph = Graph(list_class_hubs, start_hub, end_hub)
            for c in list_conects:
                graph.add_connection(list_class_hubs[c['a']],
                                     list_class_hubs[c['b']],
                                     c['max_link_capacity'] or 1)
            # for i in list_class_hubs:
                # print(vars(list_class_hubs[i]))

        # Calls the Solver path class, and check which algo to use
            # print([conn.target.name for conn in start_hub.connections])
            algo: type[Solver_path] = Solver_path
            is_weigthed: bool = False
            for k in list_class_hubs:
                if list_class_hubs[k].zone == 'restricted':
                    is_weigthed = True
                    break

            all_paths: List[List[Hub]]
            if is_weigthed is True:
                print("USANDO DIJKSTRA")
                all_paths = algo.dijkstra(start_hub, end_hub)
            else:
                print("USANDO BFS")
                all_paths = algo.bfs(start_hub, end_hub)
            # print(all_paths)

            list_drones: List[Drone] = []
            for d in range(1, nb_drones + 1):
                path: List[Hub] = all_paths[(d - 1) % len(all_paths)]
                drone: Drone = Drone(f"D{d}", start_hub, path)
                list_drones.append(drone)
            exit_hub: Any = list_class_hubs.get('exit_point')
            simulator: Simulation = Simulation()
        else:
            raise ValueError("Please, input only 1 parameter (map)")

        # Initialize the Graphic visualization
        app: App = App()

        def start() -> None:
            graph_points = app.draw_graph(list_class_hubs,
                                          list_drones, start_hub)
            app.update_info(list_drones)
            app.btn_start.configure(
                command=lambda: app.animate(
                    list_drones, graph_points, simulator,
                    list_class_hubs, all_paths
                )
            )

        app.after(100, start)
        app.mainloop()
    except ValueError as e:
        print(e)
