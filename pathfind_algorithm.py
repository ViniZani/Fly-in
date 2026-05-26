from typing import List, Tuple, Dict, Set
from classes_types import Hub


MAX_PATHS = 20
class Solver_path():
    @staticmethod
    def count_priority(path: List[Hub]) -> int:
        total_priority = 0
        for hub in path:
            if hub.zone == 'priority':
                total_priority += 1
        return total_priority

    @staticmethod
    def bfs(start_hub: Hub, end_hub: Hub) -> List[List[Hub]]:
        queue: List[Tuple[Hub, List[Hub], Set[Hub]]] = []
        all_paths: List[List[Hub]] = []
        queue.append((start_hub, [start_hub], {start_hub}))
        for hub, path, visited in queue:
            if len(all_paths) > MAX_PATHS:
                break
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
        all_paths.sort(
            key=lambda x: Solver_path.count_priority(x),
            reverse=True
        )
        return all_paths

    @staticmethod
    def dijkstra(start_hub: Hub, end_hub: Hub) -> List[List[Hub]]:
        queue: List[Tuple[int, int, Hub, List[Hub], Set[Hub]]] = []
        all_paths: List[Tuple[int, List[Hub]]] = []
        zone_cost: Dict[str, int] = {
            'normal': 1,
            'priority': 1,
            'restricted': 2
        }
        queue.append((0, 0, start_hub, [start_hub], {start_hub}))
        for curr_cost, neg_priority, hub, path, visited in queue:
            if len(all_paths) > MAX_PATHS:
                break
            for conect in hub.connections:
                neig = conect.target
                if neig.zone == 'blocked':
                    continue
                new_cost = curr_cost + zone_cost.get(neig.zone, 1)
                new_priority = neg_priority
                if neig.zone == 'priority':
                    new_priority -= 1
                if neig.name == end_hub.name:
                    all_paths.append((new_cost, path + [neig]))
                elif neig not in visited:
                    new_visited = visited.copy()
                    new_visited.add(neig)
                    queue.append((new_cost, new_priority, neig,
                                  path + [neig], new_visited))
                    queue.sort(key=lambda x: (x[0], x[1]))
        return [p for _, p in all_paths]
