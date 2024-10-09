from PySimpleGUI import popup_error, Text, Button, WINDOW_CLOSED, Input, Window, Canvas, popup_yes_no
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from re import findall, sub
from matplotlib.pyplot import subplots
from sympy import symbols, diff, latex, simplify
from time import time

def verify_error(f : str):
    """
    Verifica se a expressão fornecida é válida.
    Args:
        f (str): A expressão a ser verificada.
    Returns:
        bool: Retorna True se a expressão for válida, caso contrário, retorna False.
    A função realiza as seguintes verificações:
    1. Verifica se a expressão é nula ou vazia.
    2. Verifica se o número de parênteses de abertura é igual ao número de parênteses de fechamento.
    3. Verifica se a expressão contém entre 2 e 3 variáveis distintas (excluindo sin, cos e tan).
    Em caso de erro, uma mensagem de erro é exibida através da função `popup_error`.
    """
    if f is None or len(f) == 0:
        popup_error('Expressão Inválida', 'Insira um valor válido para a expressão!', auto_close=True, auto_close_duration=5)
        return False

    if (len(findall('[(]', f)) != len(findall('[)]', f))):
        popup_error('Expressão Inválida', 'Insira uma expressão válida!', auto_close=True, auto_close_duration=5)
        return False

    func = sub(r'(sin|cos|tan)', '', f)
    func = sorted(list(set(findall(r'[a-z]', func))))

    if len(func) > 3 or len(func) < 2:
        popup_error('Expressão Inválida', 'Insira uma expressão com 2 ou 3 variáveis!', auto_close=True, auto_close_duration=5)
        return False

    return True

def calc_diff(f : str = None):
    """
    Calcula a diferença de uma função dada.
    Args:
        f (str, opcional): A função em formato de string. Pode conter variáveis e funções trigonométricas como 'sin', 'cos' e 'tan'.
    Retorna:
        None: A função não retorna nenhum valor diretamente. Ela chama outras funções para calcular a diferença dependendo do número de variáveis encontradas na string fornecida.
    Notas:
        - Se a função fornecida não passar na verificação de erro, a execução será interrompida.
        - A função identifica as variáveis presentes na string fornecida, removendo quaisquer funções trigonométricas.
        - Dependendo do número de variáveis identificadas (2 ou 3), a função chama `calc_diff_2` ou `calc_diff_3` respectivamente para realizar o cálculo da diferença.
    """
    if not verify_error(f):
        return

    vars = sub(r'(sin|cos|tan)', '', f)
    vars = findall(r'[a-z]', vars)
    vars = sorted(list(set(vars)))

    if len(vars) == 2:
        calc_diff_2(f, vars)

    if len(vars) == 3:
        calc_diff_3(f, vars)

def calc_diff_2(f : str, vars : list):
    """
    Calcula a diferencial de uma função de duas variáveis e, opcionalmente, avalia a diferencial em pontos específicos.
    Parâmetros:
    f (str): A função em formato de string, onde '^' representa a potência.
    vars (list): Lista contendo duas variáveis da função.
    Retorna:
    None
    O fluxo da função é o seguinte:
    1. Simplifica a função fornecida.
    2. Calcula as derivadas parciais da função em relação às variáveis fornecidas.
    3. Monta a expressão da diferencial total.
    4. Solicita ao usuário os valores iniciais das variáveis e os incrementos diferenciais.
    5. Se solicitado, avalia a diferencial nos pontos fornecidos e exibe o resultado em formato LaTeX.
    """
    function = simplify(sub(r'\^', '**', f))

    var_dx, var_dy = symbols("d"+vars[0]), symbols("d"+vars[1])

    x, y, dx, dy = symbols(f'{vars[0]} {vars[1]} {var_dx} {var_dy}')

    df_dx = diff(function, x)
    df_dy = diff(function, y)

    df = dx * df_dx + dy * df_dy

    def inpt_initial_values():
        layout = [
            [Text(f'Valor de {vars[0]}0:'), Input(key='x0')],
            [Text(f'Valor de {vars[1]}0:'), Input(key='y0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    def inpt_diff_values():
        layout = [
            [Text(f'Valor de d{vars[0]}:'), Input(key='dx')],
            [Text(f'Valor de d{vars[1]}:'), Input(key='dy')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

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
        f'\n\n${vars[0]}_0$ = ${x0:.2f}$\t${vars[1]}_0$ = ${y0:.2f}$'
        f'\n$d{vars[0]}$ = ${diffx:.2f}$\t$d{vars[1]}$ = ${diffy:.2f}$\n\n'
        f'\n$D_f$ = ${latex(df)}$'
        f'\n\n$D_f$ = ${df_total:.2f}$'
    )

    plot_eq(equacao_latex, 'Diferencial de Função com duas variáveis')

def calc_diff_3(f : str, vars : list):
    """
    Calcula a diferencial de uma função de três variáveis e, opcionalmente, avalia a diferencial em pontos específicos.
    Args:
        f (str): A função em formato de string, onde os expoentes são representados por '^'.
        vars (list): Lista contendo os nomes das variáveis da função.
    Returns:
        None: A função não retorna um valor, mas exibe uma janela gráfica com a diferencial da função e, se solicitado, 
        o valor funcional da diferencial em pontos específicos.
    A função realiza os seguintes passos:
    1. Substitui os expoentes na string da função para o formato Python.
    2. Calcula as derivadas parciais da função em relação a cada variável.
    3. Monta a expressão da diferencial total.
    4. Solicita ao usuário os valores iniciais das variáveis e os incrementos diferenciais através de janelas gráficas.
    5. Se solicitado, calcula o valor funcional da diferencial nos pontos fornecidos.
    6. Exibe a expressão da diferencial e, se aplicável, o valor funcional da diferencial em uma janela gráfica.
    Nota:
        - A função utiliza a biblioteca SymPy para manipulação simbólica e PySimpleGUI para as interfaces gráficas.
        - A função assume que a lista 'vars' contém exatamente três variáveis.
    """
    function = sub(r'\^', '**', f)

    var_dx, var_dy, var_dz = symbols("d"+vars[0]), symbols("d"+vars[1]), symbols("d"+vars[2])

    x, y, z = symbols(f'{vars[0]} {vars[1]} {vars[2]}')
    dx, dy, dz = symbols(f'{var_dx} {var_dy} {var_dz}')

    df_dx = diff(function, x)
    df_dy = diff(function, y)
    df_dz = diff(function, z)

    df = df_dx * dx + df_dy * dy + df_dz * dz

    def inpt_initial_values():
        layout = [
            [Text(f'Valor de {vars[0]}0:'), Input(key='x0')],
            [Text(f'Valor de {vars[1]}0:'), Input(key='y0')],
            [Text(f'Valor de {vars[2]}0:'), Input(key='z0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    def inpt_diff_values():
        layout = [
            [Text(f'Valor de d{vars[0]}:'), Input(key='dx')],
            [Text(f'Valor de d{vars[1]}:'), Input(key='dy')],
            [Text(f'Valor de d{vars[2]}:'), Input(key='dz')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    resp = popup_yes_no("Calcular valor funcional da diferencial?")

    if resp == "No":
        equacao_latex = (
            f'Diferencial da função f({vars[0]},{vars[1]},{vars[2]}) = ${f}$'
            f'\n\n$D_f$ = ${latex(df)}$\n'
        )

        plot_eq(equacao_latex, 'Diferencial de Função com três variáveis')
        return

    vars_values = [inpt_initial_values()]
    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == '') or (vars_values[0]['z0'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_diff_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == '') or (vars_values[1]['dz'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    x0, y0, z0, diffx, diffy, diffz = (simplify(vars_values[0]["x0"]), simplify(vars_values[0]["y0"]),
                                simplify(vars_values[0]["z0"]), simplify(vars_values[1]["dx"]),
                                simplify(vars_values[1]["dy"]), simplify(vars_values[1]["dz"]))

    df_total = simplify(df.subs({x: x0, y: y0, z: z0, dx: diffx, dy: diffy, dz: diffz}))

    equacao_latex = (
        f'Diferencial da função f({vars[0]},{vars[1]},{vars[2]}) = ${f}$'
        f'\n\n${vars[0]}_0$ = {x0}\t${vars[1]}_0$ = {y0}\t${vars[2]}_0$ = {z0}'
        f'\n$d{vars[0]}$ = ${diffx:.2f}$\t$d{vars[1]}$ = ${diffy:.2f}$\t$d{vars[2]}$ = ${diffz:.2f}$\n\n'
        f'\n$D_f$ = ${latex(df)}$'
        f'\n\n$D_f$ = ${df_total:.2f}$'
    )

    plot_eq(equacao_latex, 'Diferencial de Função com três variáveis')

def calc_inc(f : str = None):
    """
    Calcula a incrementação diferencial de uma função.
    Args:
        f (str): A função em formato de string. A função deve conter variáveis
                    representadas por letras e pode incluir funções trigonométricas
                    como 'sin', 'cos' e 'tan'.
    Returns:
        None: A função não retorna nenhum valor. Se houver um erro na verificação
                da função, a execução é interrompida.
    A função identifica as variáveis presentes na string da função fornecida,
    remove as funções trigonométricas e ordena as variáveis em ordem alfabética.
    Dependendo do número de variáveis identificadas (2 ou 3), a função chama
    `calc_inc_2` ou `calc_inc_3` para realizar o cálculo da incrementação diferencial.
    """
    if not verify_error(f):
        return

    vars = sub(r'(sin|cos|tan)', '', f)
    vars = findall(r'[a-z]', vars)
    vars = sorted(list(set(vars)))

    if len(vars) == 2:
        calc_inc_2(f, vars)

    if len(vars) == 3:
        calc_inc_3(f, vars)

def calc_inc_2(f : str, vars : list):
    """
    Calcula o incremento de uma função de duas variáveis.
    Parâmetros:
    f (str): A função em formato de string.
    vars (list): Lista contendo os nomes das variáveis.
    Retorna:
    None. Exibe uma janela com o resultado do incremento da função.
    O cálculo envolve:
    1. Simplificação da função fornecida.
    2. Solicitação dos valores iniciais das variáveis através de uma interface gráfica.
    3. Solicitação dos valores de incremento das variáveis através de uma interface gráfica.
    4. Cálculo do valor inicial da função com os valores fornecidos.
    5. Cálculo do valor final da função após aplicar os incrementos.
    6. Cálculo do incremento da função e exibição do resultado em formato LaTeX.
    Observações:
    - Se os valores fornecidos forem inválidos, uma mensagem de erro será exibida.
    - A função utiliza a biblioteca SymPy para simplificação e substituição de variáveis.
    - A interface gráfica é construída utilizando a biblioteca PySimpleGUI.
    """
    function = simplify(sub(r'\^', '**', f))

    x, y = symbols(f'{vars[0]} {vars[1]}')

    def inpt_initial_values():
        layout = [
            [Text(f'Valor de {vars[0]}0:'), Input(key='x0')],
            [Text(f'Valor de {vars[1]}0:'), Input(key='y0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    def inpt_delta_values():
        layout = [
            [Text(f'Valor de Δ{vars[0]}:'), Input(key='dx')],
            [Text(f'Valor de Δ{vars[1]}:'), Input(key='dy')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

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

    delta_f = round((final_f - init_f), 2)
    equacao_latex = (
        'Incremento de f('+vars[0]+','+vars[1]+') = $'+f+'$'
        '\n $'+vars[0]+'_0$ = $'+str(vars_values[0]["x0"])+'$\t$'+vars[1]+'_0$ = $'+str(vars_values[0]["y0"])+'$'
        '\n $Δ'+vars[0]+'$ = $'+str(vars_values[1]["dx"])+'$\t$Δ'+vars[1]+'$ = $'+str(vars_values[1]["dy"])+'$'
        '\n\n Δf = $'+str(delta_f)+'$'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 2 Variaveis')

def calc_inc_3(f : str, vars : list):
    """
    Calcula o incremento de uma função de três variáveis.
    Parâmetros:
    f (str): A função em formato de string, onde os expoentes são representados por '^'.
    vars (list): Lista contendo os nomes das variáveis da função.
    Retorna:
    None. Exibe uma janela com o resultado do incremento da função.
    O cálculo envolve:
    1. Simplificação da função fornecida.
    2. Solicitação dos valores iniciais das variáveis através de uma interface gráfica.
    3. Solicitação dos valores dos incrementos das variáveis através de uma interface gráfica.
    4. Cálculo do valor inicial da função com os valores fornecidos.
    5. Cálculo do valor final da função com os valores incrementados.
    6. Cálculo do incremento da função.
    7. Exibição do resultado em formato LaTeX.
    Observações:
    - Se os valores fornecidos forem inválidos, uma mensagem de erro será exibida.
    - A função utiliza a biblioteca SymPy para simplificação e substituição de variáveis.
    - A interface gráfica é construída utilizando a biblioteca PySimpleGUI.
    """
    function = simplify(sub(r'\^', '**', f))

    x, y, z, dx, dy, dz = symbols(f'{vars[0]} {vars[1]} {vars[2]} Δ{vars[0]} Δ{vars[1]} Δ{vars[2]}')

    def inpt_initial_values():
        layout = [
            [Text(f'Valor de {vars[0]}0:'), Input(key='x0')],
            [Text(f'Valor de {vars[1]}0:'), Input(key='y0')],
            [Text(f'Valor de {vars[2]}0:'), Input(key='z0')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    def inpt_delta_values():
        layout = [
            [Text(f'Valor de Δ{vars[0]}:'), Input(key='dx')],
            [Text(f'Valor de Δ{vars[1]}:'), Input(key='dy')],
            [Text(f'Valor de Δ{vars[2]}:'), Input(key='dz')],
            [Button('OK'), Button('Cancelar')]
        ]

        window = Window('Pontos Iniciais', layout)

        while True:
            event, values = window.read()

            if event == WINDOW_CLOSED or event == 'Cancelar':
                break

            if values == '':
                popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
                return

            if event == 'OK':
                break
        window.close()
        return values

    vars_values = [inpt_initial_values()]

    if (vars_values[0]['x0'] == '') or (vars_values[0]['y0'] == '') or (vars_values[0]['z0'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    vars_values.append(inpt_delta_values())
    if (vars_values[1]['dx'] == '') or (vars_values[1]['dy'] == '') or (vars_values[1]['dz'] == ''):
        popup_error('Error', 'Valor Inválido', auto_close=True, auto_close_duration=3)
        return

    delta_x, delta_y, delta_z = (simplify(vars_values[1]["dx"]) + simplify(vars_values[0]["x0"]),
                                 simplify(vars_values[1]["dy"]) + simplify(vars_values[0]["y0"]),
                                 simplify(vars_values[1]["dz"]) + simplify(vars_values[0]["z0"]))

    init_f = function.subs({x: vars_values[0]["x0"], y: vars_values[0]["y0"], z: vars_values[0]['z0']})
    final_f = function.subs({x: delta_x, y: delta_y, z: delta_z})

    delta_f = round((final_f - init_f), 2)

    equacao_latex = (
        'Incremento de f('+vars[0]+','+vars[1]+','+vars[2]+') = $'+f+'$'
        '\n $'+vars[0]+'_0$ = $'+str(vars_values[0]["x0"])+'$\t$'+vars[1]+'_0$ = $'+str(vars_values[0]["y0"])+'$\t$'+vars[2]+'_0$ = $'+str(vars_values[0]["z0"])+'$'
        '\n $Δ'+vars[0]+'$ = $'+str(vars_values[1]["dx"])+'$\t$Δ'+vars[1]+'$ = $'+str(vars_values[1]["dy"])+'$\t$Δ'+vars[2]+'$ = $'+str(vars_values[1]["dz"])+'$'
        '\n\n Δf = $'+str(delta_f)+'$'
    )
    plot_eq(equacao_latex, 'Incremento de Função com 3 Variaveis')


def plot_eq(equacao_latex, title):
    """
    Plota uma equação LaTeX em uma janela PySimpleGUI redimensionável.
    Args:
        equacao_latex (str): A equação em formato LaTeX a ser exibida.
        title (str): O título da janela PySimpleGUI.
    Detalhes:
        - A função cria uma figura Matplotlib e insere a equação LaTeX no centro.
        - A janela PySimpleGUI é criada com um Canvas que exibe a figura Matplotlib.
        - O Canvas é redimensionado automaticamente quando a janela é redimensionada.
        - A função mantém a janela aberta até que o evento de fechamento seja acionado.
    Exemplo:
        plot_eq(r"E=mc^2", "Equação de Einstein")
    """
    font_size = max(15 - len(equacao_latex) // 20, 14)

    figura, ax = subplots()
    ax.text(0.5, 0.5, f"{equacao_latex}", horizontalalignment='center',
            verticalalignment='baseline', fontsize=font_size)
    ax.axis('off')  # Desliga os eixos para focar na equação

    # Desenha no PySimpleGUI
    layout = [[Canvas(key='canvas', expand_x=True, expand_y=True)]]

    window = Window(title, layout, finalize=True, auto_size_text=True, resizable=True)

    # Conecta o Canvas do Matplotlib ao PySimpleGUI
    canvas_elem = window['canvas']
    canvas = FigureCanvasTkAgg(figura, canvas_elem.TKCanvas)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

    last_size = (window.size[0], window.size[1])
    last_resize_time = time()

    # Redimensiona o Canvas do Matplotlib junto com a janela
    def resize_canvas(event):
        nonlocal last_size, last_resize_time
        current_time = time()
        if (event.width, event.height) != last_size and (current_time - last_resize_time) > 0.1:
            last_size = (event.width, event.height)
            last_resize_time = current_time
            canvas.get_tk_widget().config(width=event.width, height=event.height)
            figura.set_size_inches(event.width / figura.dpi, event.height / figura.dpi)
            canvas.draw()

    canvas_elem.TKCanvas.bind("<Configure>", resize_canvas)

    while True:
        event, _ = window.read()

        if event == WINDOW_CLOSED:
            break

    window.close()