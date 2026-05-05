class Hub:
    "Nó do grafo, representa cada zona onde o drone pode ficar"
    def __init__(self, name: str, x: int, y: int, zone: str = 'normal',
                 color: str = None, max_drones: int = 1):
        self.name = name
        self.x = x
        self.y = y
        self.zone = zone
        self.color = color
        self.max_drones = max_drones
        self.connections: list['Connections'] = []


class Connections:
    "representa cada aresta do grafo, conectando 2 ou mais zonas"
    def __init__(self, target: 'Hub', max_link_capacity: int = 1):
        self.target = target
        self.max_link_capacity = max_link_capacity
        self.current_occupancy = 0


class Graph:
    "Monta o modelo do grafo"
    def __init__(self, graphs_hubs, start_hub, end_hub):
        self.graphs_hubs = graphs_hubs
        self.start = start_hub
        self.end = end_hub

    def add_connection(self, hub_a: Hub, hub_b: Hub, max_link_capacity: int):
        conn_to_b = Connections(target=hub_b,
                                max_link_capacity=max_link_capacity)
        hub_a.connections.append(conn_to_b)
        conn_to_a = Connections(target=hub_a,
                                max_link_capacity=max_link_capacity)
        hub_b.connections.append(conn_to_a)


class Drone:
    def __init__(self, id: int, start: Hub):
        self.id = id
        self.current_zone = start
        self.next_zone = None
        self.at_goal = False
        self.path = []


class Simulation:
    pass
