import sympy as sp
import PySimpleGUI as sg
import matplotlib.pyplot as plt
import re
from PySimpleGUI import popup_error
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calc_diff(f : str = None):
    if f is None or len(f) == 0:
        popup_error('Função Inválida', 'Insira um valor válido para a função!', auto_close=True, auto_close_duration=5)
        return
    vars = re.findall(r'[xyz]', f)
    vars = list(set(vars))

    if len(vars) == 2:
        calc_diff_2(f)

    if len(vars) == 3:
        calc_diff_3(f)

def calc_diff_2(f : str):
    function = re.sub(r'\^', '**', f)

    x, y, dx, dy = sp.symbols('x y dx dy')

    df_dx = sp.diff(function, x)
    df_dy = sp.diff(function, y)

    df = dx*df_dx + dy*df_dy

    equacao_latex =(
        f'Diferencial de f(x,y): ${sp.latex(df)}$ \n'
    )

    plot_eq(equacao_latex, 'Diferencial')

def calc_diff_3(f : str):
    function = re.sub(r'\^', '**', f)

    x, y, z = sp.symbols('x y z')
    dx, dy, dz = sp.symbols('dx dy dz')

    df_dx = sp.diff(function, x)
    df_dy = sp.diff(function, y)
    df_dz = sp.diff(function, z)

    df = df_dx*dx + df_dy*dy + df_dz*dz

    equacao_latex = (
        f'Diferencial de f(x,y,z) = ${sp.latex(df)}$\n'
    )

    plot_eq(equacao_latex, 'Diferencial de Função com três variáveis')

def calc_inc(f : str = None):
    if f is None or len(f) == 0:
        popup_error('Função Inválida', 'Insira um valor válido para a função!', auto_close=True, auto_close_duration=5)
        return
    vars = re.findall(r'[xyz]', f)
    vars = list(set(vars))

    if len(vars) == 2:
        calc_inc_2(f)

    if len(vars) == 3:
        calc_inc_3(f)

def calc_inc_2(f : str):
    function = sp.simplify(re.sub(r'\^', '**', f))

    x, y, dx, dy = sp.symbols('x y Δx Δy')

    def inpt_initial_values():
        layout = [
            [sg.Text('Valor inicial de x:'), sg.Input(key='x0')],
            [sg.Text('Valor inicial de y:'), sg.Input(key='y0')],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == sg.WINDOW_CLOSED or evento == 'Cancelar':
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    def inpt_delta_values():
        layout = [
            [sg.Text('Valor de Δx:'), sg.Input(key='dx')],
            [sg.Text('Valor de Δy:'), sg.Input(key='dy')],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == sg.WINDOW_CLOSED or evento == 'Cancelar':
                window.close()
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    vars_values = [inpt_initial_values()]

    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == ''):
        sg.popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_delta_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == ''):
        sg.popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    delta_x, delta_y = (sp.simplify(vars_values[1]["dx"]) + sp.simplify(vars_values[0]["x0"]),
                        sp.simplify(vars_values[1]["dy"]) + sp.simplify(vars_values[0]["y0"]))

    init_f = function.subs({x: vars_values[0]["x0"], y : vars_values[0]["y0"]})
    final_f = function.subs({x: delta_x, y : delta_y})

    delta_f = final_f - init_f
    equacao_latex = (
        f'Incremento de f(x,y)\n Δf = ${delta_f}$\n'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 2 Variaveis')

def calc_inc_3(f : str):
    function = sp.simplify(re.sub(r'\^', '**', f))

    x, y, z, dx, dy, dz= sp.symbols('x y z Δx Δy Δz')

    def inpt_initial_values():
        layout = [
            [sg.Text('Valor inicial de x:'), sg.Input(key='x0')],
            [sg.Text('Valor inicial de y:'), sg.Input(key='y0')],
            [sg.Text('Valor inicial de z:'), sg.Input(key='z0')],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == sg.WINDOW_CLOSED or evento == 'Cancelar':
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    def inpt_delta_values():
        layout = [
            [sg.Text('Valor de Δx:'), sg.Input(key='dx')],
            [sg.Text('Valor de Δy:'), sg.Input(key='dy')],
            [sg.Text('Valor de Δz:'), sg.Input(key='dz')],
            [sg.Button('OK'), sg.Button('Cancelar')]
        ]

        window = sg.Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == sg.WINDOW_CLOSED or evento == 'Cancelar':
                window.close()
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    vars_values = [inpt_initial_values()]

    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == '') or (vars_values[0]['z0'] == ''):
        sg.popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_delta_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == '') or (vars_values[1]['dz'] == ''):
        sg.popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    delta_x, delta_y, delta_z = (sp.simplify(vars_values[1]["dx"]) + sp.simplify(vars_values[0]["x0"]), sp.simplify(
        vars_values[1]["dy"]) + sp.simplify(vars_values[0]["y0"]),
        sp.simplify(vars_values[1]["dz"]) + sp.simplify(vars_values[0]["z0"]))

    init_f = function.subs({x: vars_values[0]["x0"], y: vars_values[0]["y0"], z: vars_values[0]['z0']})
    final_f = function.subs({x: delta_x, y: delta_y, z: delta_z})

    delta_f = final_f - init_f
    equacao_latex = (
        f'Incremento de f(x,y)\n Δf = ${delta_f}$\n'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 3 Variaveis')

def plot_eq(equacao_latex, title):
    """
    Renderiza a equação LaTeX e a exibe em um popup usando Matplotlib e PySimpleGUI
    """
    font_size = max(15 - len(equacao_latex) // 20, 14)

    figura, ax = plt.subplots()
    ax.text(0.5, 0.5, f"{equacao_latex}", horizontalalignment='center', verticalalignment='center', fontsize=font_size)
    ax.axis('off')  # Desligar os eixos para focar na equação

    # Desenhar no PySimpleGUI
    layout = [[sg.Canvas(key='canvas')]]

    window = sg.Window(title, layout, finalize=True, auto_size_text=True)

    # Conectar o Canvas do Matplotlib ao PySimpleGUI
    canvas_elem = window['canvas']
    canvas = FigureCanvasTkAgg(figura, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack()

    while True:
        evento, _ = window.read()
        if evento == sg.WINDOW_CLOSED:
            break

    window.close()