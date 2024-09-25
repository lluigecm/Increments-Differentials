import PySimpleGUI as sg
from Inc_Diff import calc_diff, calc_inc


class GUI:

    def __init__(self):
        # Tudo que estiver dentro da janela
        self.layout = [[sg.Text("Inisira a função:", size=15)],
                    [sg.InputText()],
                    [sg.Button('Calcular Incremento', size=(18,10)), sg.Button('Calcular Diferencial', size=(18,10))]]

        # Cria a janela
        self.window = sg.Window('Incrementos e Diferenciais', self.layout, size=(350,120), resizable=False)

        self.catch_events(self.window)

    def catch_events(self, window):
        while True:
            event, values = window.read()

            # if user closes window or clicks cancel
            if event == sg.WIN_CLOSED:
                break

            if event == 'Calcular Incremento':
                calc_inc(values[0])

            if event == 'Calcular Diferencial':
                calc_diff(values[0])

        window.close()