from parser_config import Parser
from classes_types import Hub, Connections
import sys
# from graphic_interface import ...


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
        for c in list_conects:
            hub_a = list_class_hubs[c['a']]
            hub_b = list_class_hubs[c['b']]
            conec_for_b = Connections(
             target=hub_b,
             max_link_capacity=c['max_link_capacity'])
            hub_a.connections.append(conec_for_b)
            conec_for_a = Connections(
                target=hub_a,
                max_link_capacity=c['max_link_capacity'])
            hub_b.connections.append(conec_for_a)
    # except Exception:
        # print("Must have contain one txt")
