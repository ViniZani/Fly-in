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
        self.current_occupancy = 0

    def __repr__(self):
        return (f"{self.name} {self.x} {self.y}: "
                "[{self.zone} {self.color} {self.max_drones}]")


class Connections:
    "representa cada aresta do grafo, conectando 2 ou mais zonas"
    def __init__(self, target: 'Hub', max_link_capacity: int = 1):
        self.target = target
        self.max_link_capacity = max_link_capacity
        self.current_occupancy = 0

    def __repr__(self):
        return f"{self.target.name} (max_link): {self.max_link_capacity}"


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
    def __init__(self, id: int, start: Hub, path):
        self.id = id
        self.current_zone = start
        self.at_goal = False
        self.path = path
        self.path_index = 0

    def move(self):
        if self.at_goal or self.path_index >= len(self.path) - 1:
            return
        next_hub = self.path[self.path_index + 1]
        conn = None
        for c in self.current_zone.connections:
            if c.target == next_hub:
                conn = c
                break
        if conn and (next_hub.current_occupancy < next_hub.max_drones and
                     conn.current_occupancy < conn.max_link_capacity):
            self.current_zone.current_occupancy -= 1
            conn.current_occupancy += 1
            self.path_index += 1
            self.current_zone = next_hub
            next_hub.current_occupancy += 1
            conn.current_occupancy -= 1
            if self.current_zone == self.path[-1]:
                self.at_goal = True


class Simulation:
    def update_drones(self, list_drones):
        turn_moves = []
        for d in list_drones:
            previous_zone = d.current_zone
            d.move()
            if d.current_zone != previous_zone:
                turn_moves.append(f"{d.id}-{d.current_zone.name}")
                # print(f"{d.id}-{d.current_zone}")
        if turn_moves:
            print(" ".join(turn_moves))
