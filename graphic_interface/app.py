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
            text="Controle de Drones",
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

        # Catch mouse click
        self.canvas_graph.bind('<Button-1>', self.capturar_clique)

    def create_vertex(self, x1, y1, x2, y2, cor="gray"):
        """ Desenha uma linha entre dois pontos """
        self.canvas_graph.create_line(x1, y1, x2, y2,
                                      fill=cor, width=2, dash=(4, 4))

    def create_hub(self, x, y, nome, fill_color="#1f6aa5"):
        """ Desenha um círculo representando um Hub """
        r = 15

        self.canvas_graph.create_oval(
            x-r, y-r, x+r, y+r,
            fill=fill_color, outline="white", width=2
        )
        self.canvas_graph.create_text(
            x, y+45, text=nome, fill="#191c1f",
            font=("Arial", 10, "bold")
        )

    def capturar_clique(self, event):
        print(f"Posição no Canvas: x={event.x}, y={event.y}")

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
        x_range = x_max - x_min if x_max != x_min else 1
        y_range = y_max - y_min if y_max != y_min else 1

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
            x_normal = zero_x + (hub.x - x_min) / x_range * area_x
            y_normal = centro_y - (hub.y - y_min) / y_range * (area_y / 2)
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
            self.canvas_graph.create_image(x_start, y_start,
                                           image=self.drone_img)

    """def desenhar_grafo_exemplo(self):
        # Aplica as funções de desenho com os pontos definidos
        # Definição dos pontos (coordenadas para o Canvas)
        start_point = (100, 400)
        ponto_a = (300, 150)
        ponto_b = (300, 650)
        ponto_c = (600, 400)
        ponto_d = (300, 400)
        ponto_f = (600, 650)
        end_point = (900, 100)

        # 1. Desenha as Conexões (Vertex)
        self.create_vertex(*start_point, *ponto_a)
        self.create_vertex(*start_point, *ponto_b)
        self.create_vertex(*start_point, *ponto_d)
        self.create_vertex(*ponto_d, *ponto_b)
        self.create_vertex(*ponto_d, *ponto_f)
        self.create_vertex(*ponto_a, *ponto_c)
        self.create_vertex(*ponto_b, *ponto_f)
        self.create_vertex(*ponto_f, *ponto_c)
        self.create_vertex(*ponto_c, *end_point)

        # 2. Desenha os Hubs
        self.create_hub(*start_point, "Start Hub", "#3ab903")
        self.create_hub(*ponto_a, "Zone 01")
        self.create_hub(*ponto_b, "Zone 02")
        self.create_hub(*ponto_c, "Zone 03")
        self.create_hub(*ponto_d, "Zone 04")
        self.create_hub(*ponto_f, "Zone 05")
        self.create_hub(*end_point, "End hub", "#e67e22")"""
