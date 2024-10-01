from PySimpleGUI import popup_error, Text, Button, WINDOW_CLOSED, Input, Window, Canvas, popup_yes_no, popup_notify
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from re import findall, sub
from matplotlib.pyplot import subplots
from sympy import symbols, diff, latex, simplify


def calc_diff(f : str = None):
    if f is None or len(f) == 0:
        popup_error('Função Inválida', 'Insira um valor válido para a função!', auto_close=True, auto_close_duration=5)
        return
    vars = findall(r'[xyz]', f)
    vars = list(set(vars))

    if len(vars) == 2:
        calc_diff_2(f)

    if len(vars) == 3:
        calc_diff_3(f)

def calc_diff_2(f : str):
    function = simplify(sub(r'\^', '**', f))

    x, y, dx, dy = symbols('x y dx dy')

    df_dx = diff(function, x)
    df_dy = diff(function, y)

    df = dx * df_dx + dy * df_dy

    def inpt_initial_values():
        layout = [
            [Text('Valor inicial de x:'), Input(key='x0')],
            [Text('Valor inicial de y:'), Input(key='y0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    def inpt_diff_values():
        layout = [
            [Text('Valor de dx:'), Input(key='dx')],
            [Text('Valor de dy:'), Input(key='dy')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                window.close()
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    resp = popup_yes_no("Calcular valor funcional da diferencial?")

    if resp == "No":
        equacao_latex =(
            f'Diferencial da função $f(x,y)$ = ${f}$'
            f'\n\n$D_f$ = ${latex(df)}$'
        )

        plot_eq(equacao_latex, 'Diferencial')
        return

    vars_values = [inpt_initial_values()]
    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_diff_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    x0, y0, diffx, diffy = (simplify(vars_values[0]["x0"]), simplify(vars_values[0]["y0"]),
                      simplify(vars_values[1]["dx"]), simplify(vars_values[1]["dy"]))

    df_total = simplify(df.subs({x: x0, y: y0, dx: diffx, dy: diffy}))

    equacao_latex = (
        f'Diferencial da função $f(x,y)$ = ${f}$'
        f'\n\n$x_0$ = {x0}\t$y_0$ = {y0}'
        f'\n$dx$ = {diffx}\t$dy$ = {diffy}\n\n'
        f'\n\n$D_f$ = ${df_total}$'
    )

    plot_eq(equacao_latex, 'Diferencial de Função com duas variáveis')

def calc_diff_3(f : str):
    function = sub(r'\^', '**', f)

    resp = popup_yes_no("Calcular valor funcional da diferencial?")

    if resp == "No":
        x, y, z = symbols('x y z')
        dx, dy, dz = symbols('dx dy dz')

        df_dx = diff(function, x)
        df_dy = diff(function, y)
        df_dz = diff(function, z)

        df = df_dx*dx + df_dy*dy + df_dz*dz

        equacao_latex = (
            f'Diferencial da função f(x,y,z) = ${f}$'
            f'\n\n$D_f$ = ${latex(df)}$\n'
        )

        plot_eq(equacao_latex, 'Diferencial de Função com três variáveis')


def calc_inc(f : str = None):
    if f is None or len(f) == 0:
        popup_error('Função Inválida', 'Insira um valor válido para a função!', auto_close=True, auto_close_duration=5)
        return
    vars = findall(r'[xyz]', f)
    vars = list(set(vars))

    if len(vars) == 2:
        calc_inc_2(f)

    if len(vars) == 3:
        calc_inc_3(f)

def calc_inc_2(f : str):
    function = simplify(sub(r'\^', '**', f))

    x, y, dx, dy = symbols('x y Δx Δy')

    def inpt_initial_values():
        layout = [
            [Text('Valor inicial de x:'), Input(key='x0')],
            [Text('Valor inicial de y:'), Input(key='y0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    def inpt_delta_values():
        layout = [
            [Text('Valor de Δx:'), Input(key='dx')],
            [Text('Valor de Δy:'), Input(key='dy')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                window.close()
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    vars_values = [inpt_initial_values()]

    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_delta_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    delta_x, delta_y = (simplify(vars_values[1]["dx"]) + simplify(vars_values[0]["x0"]),
                        simplify(vars_values[1]["dy"]) + simplify(vars_values[0]["y0"]))

    init_f = function.subs({x: vars_values[0]["x0"], y : vars_values[0]["y0"]})
    final_f = function.subs({x: delta_x, y : delta_y})

    delta_f = final_f - init_f
    equacao_latex = (
        f'Incremento de f(x,y) = ${f}$'
        f'\n$x_0$ = {vars_values[0]["x0"]}\t$y_0$ = {vars_values[0]["y0"]}'
        f'\n$Δx$ = {vars_values[1]["dx"]}\t$Δy$ = {vars_values[1]["dy"]}\n\n'
        f'\n Δf = ${delta_f}$\n'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 2 Variaveis')

def calc_inc_3(f : str):
    function = simplify(sub(r'\^', '**', f))

    x, y, z, dx, dy, dz= symbols('x y z Δx Δy Δz')

    def inpt_initial_values():
        layout = [
            [Text('Valor inicial de x:'), Input(key='x0')],
            [Text('Valor inicial de y:'), Input(key='y0')],
            [Text('Valor inicial de z:'), Input(key='z0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    def inpt_delta_values():
        layout = [
            [Text('Valor de Δx:'), Input(key='dx')],
            [Text('Valor de Δy:'), Input(key='dy')],
            [Text('Valor de Δz:'), Input(key='dz')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            evento, valores = window.read()

            if evento == WINDOW_CLOSED or evento == 'Cancelar':
                window.close()
                break

            if evento == 'OK':
                break
        window.close()
        return valores

    vars_values = [inpt_initial_values()]

    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == '') or (vars_values[0]['z0'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_delta_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == '') or (vars_values[1]['dz'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    delta_x, delta_y, delta_z = (simplify(vars_values[1]["dx"]) + simplify(vars_values[0]["x0"]), simplify(
        vars_values[1]["dy"]) + simplify(vars_values[0]["y0"]),
        simplify(vars_values[1]["dz"]) + simplify(vars_values[0]["z0"]))

    init_f = function.subs({x: vars_values[0]["x0"], y: vars_values[0]["y0"], z: vars_values[0]['z0']})
    final_f = function.subs({x: delta_x, y: delta_y, z: delta_z})

    delta_f = final_f - init_f
    equacao_latex = (
        f'Incremento de f(x,y,z) = ${f}$'
        f'\n $x_0$ = {vars_values[0]["x0"]}\t$y_0$ = {vars_values[0]["y0"]}\t$z_0$ = {vars_values[0]["z0"]}'
        f'\n $Δx$ = {vars_values[1]["dx"]}\t$Δy$ = {vars_values[1]["dy"]}\t$Δz$ ={vars_values[1]["dz"]}'
        f'\n\n Δf = ${delta_f}$'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 3 Variaveis')

def plot_eq(equacao_latex, title):
    """
    Renderiza a equação LaTeX e a exibe em um popup usando Matplotlib e PySimpleGUI
    """
    font_size = max(15 - len(equacao_latex) // 20, 14)

    figura, ax = subplots()
    ax.text(0.5, 0.5, f"{equacao_latex}", horizontalalignment='center',
            verticalalignment='baseline', fontsize=font_size)
    ax.axis('off')  # Desligar os eixos para focar na equação

    # Desenhar no PySimpleGUI
    layout = [[Canvas(key='canvas')]]

    window = Window(title, layout, finalize=True, auto_size_text=True)

    # Conectar o Canvas do Matplotlib ao PySimpleGUI
    canvas_elem = window['canvas']
    canvas = FigureCanvasTkAgg(figura, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack()

    while True:
        evento, _ = window.read()
        if evento == WINDOW_CLOSED:
            break

    window.close()