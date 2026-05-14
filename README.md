# Fly-In

*This project has been created as part of the 42 curriculum by vzani-st.*

---

## Description
**Fly-In** is a project focused on solver Drone System using Pathfinder Algos with robustness logical validation to find the best way to move all drones from the start zone at the goal. It explores fundamental concepts of Graph Theory, algorithms, and data structures, offering an interactive command-window interface for visualization and a command-line with the steps.

## Instructions

### Installation
The project uses a `Makefile` to facilitate setup across different operating systems. It is recommended to use a Python 3.10+ environment.

```bash
# Creates the virtual environment and installs dependencies (customtkinter, Pillow, flake8, mypy)
make install
```
### Execution
To run the program using a map file:

```bash
# In Linux/macOS
$FILE=<name_from_your_map.txt>
make run
```

### Code Quality (Linting)
To verify that the code follows PEP8 standards and static typing:

```bash
make lint           # Basic verification
make lint-strict    # Strict verification with Mypy
```

### Configuration Map's File Description
The program reads a file (e.g., map_easy.txt) in a specific format. The following fields are mandatory:
- The first line defines the number of drones using nb_drones: <number>.
- Zone definition on each line using type prefixes:
    * start_hub: <name> <x> <y> [metadata] marks the starting zone.
    * end_hub: <name> <x> <y> [metadata] marks the end zone.
    * hub: <name> <x> <y> [metadata] defines a regular zone.
    * The connection syntax forbids dashes in zone names (see below).
- All metadata is optional and enclosed in brackets [...] with default values:
    * zone=<type> (default: normal)
    * color=<value> (default: none)
    * max_drones=<number> (default: 1) - Maximum drones that can occupy this zone simultaneously

    * Tags inside brackets can appear in any order

- Zone types:
    * normal - Standard zone with 1 turn movement cost (default)
    * blocked - Inaccessible zone. Drones must not enter or pass through this zone.
  Any path using it is invalid.
    * restricted - A sensitive or dangerous zone. Movement to this zone costs 2
turns.
    * priority - A preferred zone. Movement to this zone costs 1 turn but should
be prioritized in pathfinding.
- Colors:
    * Colors are optional and can be used for visual representation (terminal output
or graphical display).
    * Accepted values for color are any valid single-word strings (e.g., red, blue,
gray). There is no fixed list of allowed colors.
    * When colors are specified, the implementation should provide visual feedback
through colored terminal output or graphical representation.
- Connections are defined using connection: <name1>-<name2> [metadata]:
    * Define a bidirectional connection (edge) between two zones.
    * The connection syntax forbids dashes in zone names.
    * Optional metadata can be specified in brackets [...]:
        * max_link_capacity=<number> (default: 1) - Maximum drones that can
traverse this connection simultaneously
- Comments start with "#" and are ignored.

exemple:
```bash
nb_drones: 5
start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]
connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

## Algorithm Choices
From this project, the aspcet 'restricted' in zones causes a cost in the turns that you will need to arrive at the goal. So, at this point we have 2 scenarios: 1. Thats no resctricted zones and 2. That is at least one restricted zone.

After studing, i found the BFS and Dijskra algos, but the big O help me witch i needed to use. 
### BFS

### Dijskra

##  Visual Representation Feature
For help and enhance the user experience, i chose use the lib Customtkinter, a lib focus on create interative interfaces using an extra window to show the interface. I separate the window in two points. One, bigger, for the representation of the graph, create the hubs, the connections, the drones. and the other, one vertical menu to show important data, like the total numbers of drones, how many drones arrived at the goal, the total of turns the was needed in real time uptaded. And one bottom in this menu to start and reset the animation of the drones moves through the hubs and connections and counting turns.

## Resources
- Wikipedia: Dijskra Algorithm

- Algoritmo do Caminho Mais Curto de Dijkstra | Teoria dos Grafos- https://www.youtube.com/watch?v=pSqmAO-m7Lk&t=28sk

- Algoritmo de Busca em Largura | Caminho Mais Curto | Teoria dos Grafos - https://www.youtube.com/watch?v=oDqjPvD54Ss


- Como Criar uma Interface Gráfica Python c/ CustomTkinter [RÁPIDO]- https://www.youtube.com/watch?v=Px-DgrQ_wjI

- Breadth First Search (BFS): Visualized and Explained - https://www.youtube.com/watch?v=xlVX7dXLS64&t=45s


- 5.1 Graph Traversals - BFS & DFS -Breadth First Search and Depth First Search - https://www.youtube.com/watch?v=pcKY4hjDrxk

### AI Usage
Artificial Intelligence was utilized in this project for the following tasks:

Code Refactoring: Assistance in converting functions to meet rigorous Flake8 and Mypy standards (linting).

Environment Bug Fixing: Diagnosing compatibility errors between Unix Makefiles and Windows PowerShell.

Documentation: Initial structuring of Docstrings following the PEP 257 standard.

Optimization: Used to anwser pontual questions.