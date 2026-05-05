import math
from parser_config import Parser
from classes_types import Hub
import sys


class Solver_path:
    pass


def calculate_dist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def dijskra(start, end):
    dist = {}
    dist[start.name] = calculate_dist(start.name,)
    pass


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parser = Parser(sys.argv[1])
        (nb_drones, start_hub, list_hubs,
         end_hub, list_conects) = parser.get_data()
        start_hub = Hub(**start_hub)
        end_hub = Hub(**end_hub)
        print(vars(start_hub))
        print(vars(end_hub))
        # print(list_conects)
        # dijskra(start_hub, end_hub)

        list_class_hubs = {}
        list_class_hubs[start_hub.name] = start_hub
        list_class_hubs[end_hub.name] = end_hub
        for h in list_hubs:
            class_hub = Hub(**h)
            list_class_hubs[class_hub.name] = class_hub
        for i in list_class_hubs:
            print(vars(list_class_hubs[i]))
            # não esta salvando as connections, quero salvar
            # cada connection na lista ex:
            # start_hub.connections -> ['roof1', 'corridorA']
