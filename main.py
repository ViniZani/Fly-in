from parser_config import Parser
from classes_types import Hub, Graph, Drone
import sys
from graphic_interface.app import App


if __name__ == "__main__":
    # try:
    if len(sys.argv) == 2:
        parser = Parser(sys.argv[1])
        (nb_drones, start_hub, list_hubs,
         end_hub, list_conects) = parser.get_data()
        start_hub = Hub(**start_hub)
        end_hub = Hub(**end_hub)

        list_class_hubs = {}
        list_class_hubs[start_hub.name] = start_hub
        list_class_hubs[end_hub.name] = end_hub
        for h in list_hubs:
            class_hub = Hub(**h)
            list_class_hubs[class_hub.name] = class_hub

        graph = Graph(list_class_hubs, start_hub, end_hub)
        for c in list_conects:
            graph.add_connection(
                list_class_hubs[c['a']],
                list_class_hubs[c['b']],
                c['max_link_capacity'] or 1)

        list_drones = []
        for d in range(1, nb_drones+1):
            drone = Drone(f"D{d}", start_hub)
            list_drones.append(drone)
        app = App()
        app.after(100, lambda: app.draw_graph(list_class_hubs,
                                              list_drones, start_hub))
        app.after(100, lambda: app.update_info(list_drones))
        # app.desenhar_grafo_exemplo()
        app.mainloop()
    # except Exception:
        # print("Must have contain one txt")
