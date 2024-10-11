from PySimpleGUI import Window, Text, Button, InputText, WIN_CLOSED
from Inc_Diff import calc_diff, calc_inc


class GUI:
    """
    Classe GUI para criar uma interface gráfica de usuário para calcular incrementos e diferenciais de uma função.

    Métodos
    -------
    __init__():
        Inicializa a interface gráfica com os componentes necessários.

    catch_events(window):
        Captura e trata os eventos da janela, executando as funções de cálculo de incremento e diferencial conforme necessário.

    Atributos
    ---------
    layout : list
        Lista de listas que define o layout da janela, incluindo texto, campos de entrada e botões.

    window : PySimpleGUI.Window
        Objeto da janela principal da interface gráfica.
    """
    def __init__(self):
        # Tudo que estiver dentro da janela
        self.layout = [[Text("Insira a expressão da função de duas ou três variáveis:", size=40)],
                    [InputText()],
                    [Button('Calcular Incremento', size=(18,10)),
                     Button('Calcular Diferencial', size=(18,10))]]

        # Cria a janela
        self.window = Window('Incrementos e Diferenciais', self.layout, size=(350,120), resizable=False)

        self.catch_events(self.window)

    def catch_events(self, window):
        while True:
            event, values = window.read()

            if event == WIN_CLOSED:
                break

            if event == 'Calcular Incremento':
                calc_inc(values[0])

            if event == 'Calcular Diferencial':
                calc_diff(values[0])

        window.close()