import customtkinter as ctk  # type: ignore
from PIL import Image, ImageTk

ctk.set_appearance_mode('dark')


class App(ctk.CTk):
    def __init__(self, simulator):
        super().__init__()

        # Main Window Config
        self.title('Fly-In: Drones Solver System')
        self.geometry('12000x8000')
        self.bind('<Configure>', self.on_window_resize)
        self.simulator = simulator
        self.animating = False

        # Grid responsiveness
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

        # Canvas
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

        # Menu Title
        self.label_menu = ctk.CTkLabel(
            self.menu_control,
            text="Drones Controls Menu",
            font=("Arial", 20, "bold")
        )
        self.label_menu.pack(pady=20)

        # Status Frame (unified, from Code 1)
        self.status_frame = ctk.CTkFrame(
            self.menu_control,
            fg_color="gray25",
            corner_radius=5
        )
        self.status_frame.pack(padx=10, pady=10, fill="x")

        ctk.CTkLabel(
            self.status_frame,
            text="Status View",
            font=("Arial", 19, "bold")
        ).pack(pady=(10, 5), padx=10)

        # Total Drones
        self.label_total_drones = ctk.CTkLabel(
            self.status_frame,
            text="Total Drones: 0",
            font=("Arial", 13, "bold")
        )
        self.label_total_drones.pack(pady=5, padx=10)

        # Total Turns
        self.current_turn = 0
        self.label_turns = ctk.CTkLabel(
            self.status_frame,
            text=f"Total Turns: {self.current_turn}",
            font=("Arial", 13, "bold")
        )
        self.label_turns.pack(pady=5, padx=10)

        # Drones Arrived
        self.current_arrived = 0
        self.label_arrived = ctk.CTkLabel(
            self.status_frame,
            text=f"Drones Arrived at goal: {self.current_arrived}",
            font=("Arial", 13, "bold")
        )
        self.label_arrived.pack(pady=(5, 10), padx=10)

        # Start button
        self.btn_start = ctk.CTkButton(
            self.menu_control,
            text="> Solver Path Simulation",
            command=self.on_start_click
        )
        self.btn_start.pack(pady=10, padx=10, fill="x")

        # Canvas bindings
        self.canvas_graph.bind('<Button-1>', self.catch_click)
        self.canvas_graph.bind('<Configure>', self.on_canvas_resize)

        # Reset button
        self.btn_reset = ctk.CTkButton(
            self.menu_control,
            text="Reset Simulation",
            fg_color="#c0392b",
            hover_color="#a93226",
            command=self.on_reset_click
        )
        self.btn_reset.pack(pady=10, padx=10, fill="x")

        self.log_frame = ctk.CTkFrame(
            self.menu_control,
            fg_color="gray25",
            corner_radius=5
        )
        self.log_frame.pack(padx=10, pady=10, fill="x")

    # ==== Button Logic ====

    def on_start_click(self):
        pass

    def catch_click(self, event):
        print(f"Posição no Canvas: x={event.x}, y={event.y}")

    def on_reset_click(self) -> None:
        self.simulation_running = False
        self.current_turn = 0
        self.label_turns.configure(text="Total Turns: 0")
        self.label_arrived.configure(text="Drones Arrived at goal: 0")

        drones = self.current_drones_list
        start_node = self.start_hub_ref
        points = self.graph_points_ref

        # Reset hub occupancies
        for hub in self.list_class_hubs_ref.values():
            hub.current_occupancy = 0
        for hub in self.list_class_hubs_ref.values():
            for conn in hub.connections:
                conn.current_occupancy = 0

        # Reset drones
        x_start, y_start = points[start_node.name]
        for i, drone in enumerate(drones):
            drone.current_zone = start_node
            drone.at_goal = False
            drone.path = self.all_paths_ref[self.original_path_indices[i]]
            drone.path_index = 0
            drone.turns_in_transit = 0
            drone.turns_stopped = 0
            drone.reserved_hub = None
            drone.reserved_conn = None
            self.canvas_graph.coords(drone.canvas_id, x_start, y_start)

        print("\n==Reseted Simulation==\n")

    # ==== Canvas Elements ====

    def create_vertex(self, x1, y1, x2, y2, cor="gray"):
        """Desenha uma linha entre dois pontos"""
        self.canvas_graph.create_line(x1, y1, x2, y2,
                                      fill=cor, width=2, dash=(4, 4))

    def create_hub(self, x, y, nome, fill_color="#1f6aa5"):
        """Desenha um círculo representando um Hub"""
        r = 25
        self.canvas_graph.create_oval(
            x-r, y-r, x+r, y+r,
            fill=fill_color, outline="white", width=2
        )
        self.canvas_graph.create_text(
            x, y+45, text=nome, fill="#191c1f",
            font=("Arial", 10, "bold")
        )

    def update_info(self, list_drones):
        self.label_total_drones.configure(
            text=f"Total Drones: {len(list_drones)}"
        )

    def draw_graph(self, list_class_hubs, list_drones, start_hub, all_paths):
        """Cria o grafo no canvas"""
        self.list_class_hubs_ref = list_class_hubs
        self.list_drones_ref = list_drones
        self.canvas_graph.delete('all')

        width = self.canvas_graph.winfo_width()
        height = self.canvas_graph.winfo_height()
        if width <= 1 or height <= 1:
            width = 800
            height = 600

        for drone in list_drones:
            if hasattr(drone, 'canvas_id'):
                drone.canvas_id = None

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
        for drone in list_drones:
            x, y = graph_points[drone.current_zone.name]
            drone.canvas_id = self.canvas_graph.create_image(
                x, y, image=self.drone_img)
        self.original_path_indices = [
            (d - 1) % len(all_paths)
            for d in range(1, len(list_drones) + 1)
        ]
        self.all_paths_ref = all_paths

        self.current_drones_list = list_drones
        self.start_hub_ref = start_hub
        self.graph_points_ref = graph_points

        return graph_points

    # ==== Resize Methods ====

    def on_canvas_resize(self, event):
        """Reorganiza os elementos ao redimensionar o canvas"""
        if hasattr(self, 'list_class_hubs_ref') and self.list_class_hubs_ref:
            self.draw_graph(self.list_class_hubs_ref,
                            self.list_drones_ref, self.start_hub_ref,
                            self.all_paths_ref)

    def on_window_resize(self, event=None):
        """Chamado quando a janela é redimensionada (com debounce)"""
        if hasattr(self, '_resize_job'):
            self.after_cancel(self._resize_job)
        self._resize_job = self.after(100, self.redraw_graph)

    def redraw_graph(self):
        """Redesenha todo o grafo com as novas dimensões"""
        if hasattr(self, 'list_class_hubs_ref') and self.list_class_hubs_ref:
            # Redesenha o grafo com as dimensões atuais do canvas
            self.draw_graph(
                self.list_class_hubs_ref,
                self.current_drones_list,
                self.start_hub_ref, self.all_paths_ref
            )
        self.update_info(self.current_drones_list)

    # ==== Animation Logic ====

    def lerp(self, inicio, fim, t):
        """Calcula o valor interpolado entre duas coordenadas"""
        return inicio + (fim - inicio) * t

    def animate(self, list_drones, graph_points,
                simulator, list_class_hubs, all_paths) -> None:
        """Atualiza o status turno a turno e anima os drones"""
        current_points = getattr(self, 'graph_points_ref', graph_points)

        all_arrived = all(d.at_goal for d in list_drones)
        drones_at_goal = 0
        for d in list_drones:
            if d.at_goal:
                drones_at_goal += 1
        self.label_arrived.configure(
            text=f"Drones Arrived at goal: {drones_at_goal}"
        )

        if not all_arrived:
            posicoes_iniciais = {
                drone.id: current_points[drone.current_zone.name]
                for drone in list_drones
            }

            simulator.update_drones(list_drones, all_paths)
            self.current_turn += 1
            self.label_turns.configure(
                text=f"Total Turns: {self.current_turn}"
            )

            total_frames = 20
            self.interpolate_drone_movement(
                list_drones, posicoes_iniciais, current_points,
                step=1, max_steps=total_frames,
                callback=lambda: self.animate(list_drones, graph_points,
                                              simulator, list_class_hubs,
                                              self.all_paths_ref)
            )

    def interpolate_drone_movement(self, list_drones, posicoes_iniciais,
                                   graph_points, step, max_steps,
                                   callback) -> None:
        """Move os drones quadro a quadro entre os Hubs"""
        if step <= max_steps:
            t = step / max_steps

            for drone in list_drones:
                x_inicio, y_inicio = posicoes_iniciais[drone.id]
                x_fim, y_fim = graph_points[drone.current_zone.name]
                current_x = self.lerp(x_inicio, x_fim, t)
                current_y = self.lerp(y_inicio, y_fim, t)
                self.canvas_graph.coords(drone.canvas_id, current_x, current_y)

            self.after(16, self.interpolate_drone_movement,
                       list_drones, posicoes_iniciais, graph_points,
                       step + 1, max_steps, callback)
        else:
            self.after(600, callback)
