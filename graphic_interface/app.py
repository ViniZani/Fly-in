import customtkinter as ctk
from PIL import Image, ImageTk

ctk.set_appearance_mode('dark')


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Main Windown Config
        self.title('Fly-In: Drones Solver System')
        self.geometry('1200x800')

        # Configurando a responsividade (Grid)
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Graph's Frame (Left Side)
        self.graph_display = ctk.CTkFrame(self, corner_radius=10)
        self.graph_display.grid(row=0, column=0,
                                padx=20, pady=20, sticky="nsew")
        img = Image.open("graphic_interface/drone_2d.webp").resize((40, 40))
        self.drone_img = ImageTk.PhotoImage(img)

        # Canvas pad
        self.canvas_graph = ctk.CTkCanvas(
            self.graph_display,
            background="#e1d9c3",
            highlightthickness=0
        )
        self.canvas_graph.pack(fill='both', expand=True, padx=10, pady=10)

        # Control's Frame (Right Side)
        self.menu_control = ctk.CTkFrame(self, width=250, corner_radius=10)
        self.menu_control.grid(row=0, column=1,
                               padx=(0, 20), pady=20, sticky="nsew")

        # Menu's Title
        self.label_menu = ctk.CTkLabel(
            self.menu_control,
            text="Drones Controls Menu",
            font=("Arial", 20, "bold")
        )
        # Data's Menu objtects
        self.label_menu.pack(pady=20)
        self.total_drones_frame = ctk.CTkFrame(
            self.menu_control,
            fg_color="gray25",
            corner_radius=5)
        self.total_drones_frame.pack(padx=10, pady=10, fill="x")

        self.label_total_drones = ctk.CTkLabel(
            self.total_drones_frame,
            text="Total Drones: 0",
            font=("Arial", 13, "bold"))
        self.label_total_drones.pack(pady=10, padx=10)

        # Total Turns Count
        self.turns_frame = ctk.CTkFrame(
            self.menu_control,
            fg_color="gray25",
            corner_radius=5)
        self.turns_frame.pack(padx=10, pady=10, fill="x")

        self.current_turn = 0
        self.label_turns = ctk.CTkLabel(
            self.turns_frame,
            text=f"Total Turns: {self.current_turn}",
            font=("Arial", 13, "bold"),
        )
        self.label_turns.pack(pady=10, padx=10)

        # Initialize animattion bottom
        self.btn_start = ctk.CTkButton(
            self.menu_control,
            text="> Solver Path Simulation",
            command=self.on_start_click
            )
        self.btn_start.pack(pady=10, padx=10, fill="x")
        # Catch mouse click (for debug)
        self.canvas_graph.bind('<Button-1>', self.catch_click)

        # Restart animation bottom
        self.btn_reset = ctk.CTkButton(
            self.menu_control,
            text="Reset Simulation",
            fg_color="#c0392b",
            hover_color="#a93226",
            command=self.on_reset_click
        )
        self.btn_reset.pack(pady=10, padx=10, fill="x")

        # Count Arrived Drones
        self.arrived_drones_frame = ctk.CTkFrame(
            self.menu_control,
            fg_color="gray25",
            corner_radius=5)
        self.arrived_drones_frame.pack(padx=10, pady=10, fill="x")

        self.current_arrived = 0
        self.label_arrived = ctk.CTkLabel(
            self.arrived_drones_frame,
            text=f"Drones Arrived at goal: {self.current_arrived}",
            font=("Arial", 13, "bold"),
        )
        self.label_arrived.pack(pady=10, padx=10)

    # Click logic botom
    def on_start_click(self):
        pass

    def catch_click(self, event):
        print(f"Posição no Canvas: x={event.x}, y={event.y}")

    def on_reset_click(self):
        """if not hasattr(self, 'current_drones_list'):
            print("Nenhuma simulação para resetar.")
            return"""

        self.simulation_running = False

        self.current_turn = 0
        self.label_turns.configure(text="Total Turns: 0")
        if hasattr(self, 'label_arrived'):
            self.label_arrived.configure(text="Drones Arrived at goal: 0")

        drones = self.current_drones_list
        start_node = self.start_hub_ref
        points = self.graph_points_ref

        x_start, y_start = points[start_node.name]

        for drone in drones:
            drone.current_zone = start_node
            drone.at_goal = False
            self.canvas_graph.coords(drone.canvas_id, x_start, y_start)

        print("Reseted Simulation.")

    # Create Canvas Elements
    def create_vertex(self, x1, y1, x2, y2, cor="gray"):
        """ Desenha uma linha entre dois pontos """
        self.canvas_graph.create_line(x1, y1, x2, y2,
                                      fill=cor, width=2, dash=(4, 4))

    def create_hub(self, x, y, nome, fill_color="#1f6aa5"):
        """ Desenha um círculo representando um Hub """
        r = 25

        self.canvas_graph.create_oval(
            x-r, y-r, x+r, y+r,
            fill=fill_color, outline="white", width=2
        )
        self.canvas_graph.create_text(
            x, y+45, text=nome, fill="#191c1f",
            font=("Arial", 10, "bold")
        )
        """if nome == 'goal':
            self.canvas_graph.create_text(
                x, y+65, text="Drones occuped: 0", fill="#191c1f",
                font=("Arial", 10, "bold")
            )"""

    def update_info(self, list_drones):
        self.label_total_drones.configure(text="Total Drones:"
                                          f"{len(list_drones)}")

    def draw_graph(self, list_class_hubs, list_drones, start_hub):
        self.canvas_graph.delete('all')
        graph_points = {}
        all_x = [hub.x for hub in list_class_hubs.values()]
        all_y = [hub.y for hub in list_class_hubs.values()]
        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)

        padding_x = 70
        padding_y = 70
        width = self.canvas_graph.winfo_width()
        height = self.canvas_graph.winfo_height()
        centro_y = height / 2
        zero_x = padding_x
        area_x = width - 2 * padding_x
        area_y = height - 2 * padding_y

        # Eixos
        self.canvas_graph.create_line(zero_x, centro_y, width - padding_x,
                                      centro_y, fill="#b2bec3",
                                      width=2, arrow='last')
        self.canvas_graph.create_line(zero_x, padding_y, zero_x,
                                      height - padding_y, fill="#b2bec3",
                                      width=2, arrow='last')

        # Normalization
        for name, hub in list_class_hubs.items():
            x_abs_max = max(abs(x_max), abs(x_min)) or 1
            y_abs_max = max(abs(y_max), abs(y_min)) or 1
            x_scale = area_x / x_abs_max
            y_scale = (area_y / 2) / y_abs_max
            x_normal = zero_x + hub.x * x_scale
            y_normal = centro_y - hub.y * y_scale
            graph_points[name] = (x_normal, y_normal)

        # Connections
        for name, hub in list_class_hubs.items():
            x1, y1 = graph_points[name]
            for conn in hub.connections:
                x2, y2 = graph_points[conn.target.name]
                self.create_vertex(x1, y1, x2, y2)

        # Hubs
        for name, (x, y) in graph_points.items():
            self.create_hub(x, y, name,
                            list_class_hubs[name].color or "#1f6aa5")

        # Drones
        x_start, y_start = graph_points[start_hub.name]
        for drone in list_drones:
            x, y = graph_points[drone.current_zone.name]
            drone.canvas_id = self.canvas_graph.create_image(
                x, y, image=self.drone_img)
        self.current_drones_list = list_drones
        self.start_hub_ref = start_hub
        self.graph_points_ref = graph_points
        return graph_points

    def animate(self, list_drones, graph_points, simulator, list_class_hubs, all_paths):
        # To see what is going on each turn
        # for drone in list_drones:
        #    print(f"{drone.id}: {drone.current_zone.name} at_goal={drone.at_goal}") # noqa
        # print(f"D3 path: {[h.name for h in list_drones[2].path]}")
        # print(f"D6 path: {[h.name for h in list_drones[5].path]}")
        # print(f"D8 path: {[h.name for h in list_drones[7].path]}")
        # print(f"waiting_area3 occupancy: {list_class_hubs['waiting_area3'].current_occupancy}")
        # Draw the current position
        for drone in list_drones:
            x, y = graph_points[drone.current_zone.name]
            self.canvas_graph.coords(drone.canvas_id, x, y)
        # Moves to the next turn
        all_arrived = all(d.at_goal for d in list_drones)
        drones_at_goal = sum(1 for d in list_drones if d.at_goal)
        self.label_arrived.configure(
            text=f"Drones Arrived at goal: {drones_at_goal}"
        )
        if not all_arrived:
            simulator.update_drones(list_drones, all_paths)
            # if list_class_hubs and 'exit_point' in list_class_hubs:
            #    print(f"exit_point: {list_class_hubs['exit_point'].current_occupancy}") # noqa
            self.current_turn += 1
            self.label_turns.configure(text="Total Turns:"
                                       f"{self.current_turn}")
            self.after(500, lambda: self.animate(
                list_drones, graph_points, simulator, list_class_hubs, all_paths
            ))
