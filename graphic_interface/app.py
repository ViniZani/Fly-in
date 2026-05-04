import customtkinter as ctk
ctk.set_appearance_mode('dark')

# Creation of main window (graph)
app = ctk.CTk()
app.title('Fly-In: Drones Solver System')
app.geometry('2500x1500')

# Creation of the fiels
label_graph = ctk.CTkLabel(app, text='map.txt', font=('Bold', 30))
label_graph.place(x=942, y=1123)
graph_display = ctk.CTkFrame(master=app, width=1900, height=1100,
                             corner_radius=10)
graph_display.place(x=25, y=10)
graph_display.pack_propagate(False)

canvas_graph = ctk.CTkCanvas(
    graph_display,
    width=1890,
    height=1090,
    background="#e1d9c3",
    highlightthickness=0
)
canvas_graph.pack(fill='both', expand=True)

# Criação das funçõs de funcionalidade
menu_control = ctk.CTkFrame(master=app, width=500, height=1100,
                            corner_radius=10)
menu_control.place(x=2071, y=16)

# OBjetos do Grafo


def create_start_hub(canvas, x, y, nome, cor="#1f6aa5"):
    """ Desenha um círculo representando um drone ou ponto """
    raio = 40
    # O canvas usa coordenadas (x1, y1, x2, y2) para o oval
    canvas.create_oval(x-raio, y-raio, x+raio, y+raio, fill=cor,
                       outline="white", width=2)
    canvas.create_text(x, y+60, text=nome, fill="#191c1f",
                       font=("Arial", 10, "bold"))


def create_hub(canvas, x, y, nome, cor="#1f6aa5"):
    """ Desenha um círculo representando um drone ou ponto """
    raio = 40
    canvas.create_oval(x-raio, y-raio, x+raio, y+raio, fill=cor,
                       outline="white", width=2)
    canvas.create_text(x, y+60, text=nome, fill="#191c1f",
                       font=("Arial", 10, "bold"))


def create_vertex(canvas, x1, y1, x2, y2, cor="gray"):
    """ Desenha uma linha entre dois pontos """
    canvas.create_line(x1, y1, x2, y2, fill=cor, width=2, dash=(4, 4))


def capturar_clique(event):
    print(f"Posição clicada: x={event.x}, y={event.y}")


app.bind('<Button-1>', capturar_clique)

# Título dentro do menu lateral
label_menu = ctk.CTkLabel(menu_control, text="Controle de Drones",
                          font=("Arial", 20, "bold"))
label_menu.pack(pady=20, padx=10)

# View graph
start_point = (100, 545)
ponto_a = (100, 100)
ponto_b = (400, 300)
ponto_c = (700, 150)
end_point = (900, 545)

# Draw Conncections between a-b hubs
create_vertex(canvas_graph, *start_point, *ponto_a)
create_vertex(canvas_graph, *start_point, *ponto_b)
create_vertex(canvas_graph, *ponto_a, *ponto_b)
create_vertex(canvas_graph, *ponto_b, *ponto_c)
create_vertex(canvas_graph, *ponto_c, *end_point)

# Draw Hubs
create_start_hub(canvas_graph, *start_point, "Start Hub", cor="#3ab903")
create_hub(canvas_graph, *ponto_a, "Zone 01")
create_hub(canvas_graph, *ponto_b, "Zone 02")
create_hub(canvas_graph, *ponto_c, "Zone 03")
create_hub(canvas_graph, *end_point, "End hub", cor="#e67e22")

# Initialize the aplication
app.mainloop()
