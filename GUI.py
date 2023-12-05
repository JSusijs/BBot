import PySimpleGUI as sg
from binancerequest2 import analysis, chart
import matplotlib
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import linregress
import numpy as np

matplotlib.use('TkAgg')
button_size = (7, 1)

def create_main_window():
    layout = [
        [
            sg.Button("START", size=button_size, font=("Helvetica", 30, "bold"), pad=(4, 5), key='-START-', button_color=("black", "green")),
            sg.Button("EXIT", size=button_size, font=("Helvetica", 30, "bold"), pad=(4, 5), key='-EXIT-', button_color=("black", "red"))
        ],
        [
            [sg.Button("INSTRUCTION", size=(15, 1), font=("Helvetica", 30, "bold"), key='-INSTRUCTION-', button_color=("black", "orange"), pad=(5, 3))],
        ]
    ]

    return sg.Window("Binance Trading Bots", layout, background_color="#4a4a4a", finalize=True)

def create_start_window():
    start_layout = [
        [
            [sg.Text("Choose trading bot parameters", background_color="#4a4a4a", font=("Helvetica", 23, "bold"), pad=(0, 0))],

            [sg.Text(("Select grid type:"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.Combo(['Futures grid', 'Spot grid'], key='-GRID-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Select time unit of measure:"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.Combo(['Months', 'Days', 'Hours', 'Minutes', 'Seconds'], key='-UNIT-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Minimum time (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-MITIME-', size=(15, 1), font=("Helvetica", 20))],

            [sg.Text(("Maximum time (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-MATIME-', size=(15, 1), font=("Helvetica", 20))],

            [sg.Text(("Select data set size (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-SIZE-', size=(15, 1), font=("Helvetica", 20))],

            [sg.Button('START ANALYSIS', size=(28, 1), font=("Helvetica", 20), key='-SUBMIT-', button_color=("black", "green"))],
            [sg.Button("BACK TO MAIN MENU", size=(28, 1), font=("Helvetica", 20), key='-BACK-', button_color=("black", "orange"))],

        ]
    ]

    return sg.Window("Binance Trading Bots", start_layout, background_color="#4a4a4a", finalize=True)

def create_instruction_window():
    instruction_layout = [
        [sg.Text("Welcome to user manual for Binance Trading Bots application", background_color="#4a4a4a", font=("Helvetica", 30, "bold"))],

        [sg.Text((""), background_color="#4a4a4a")],

        [sg.Text("•Disclaimer•", text_color=("Red"), background_color="#4a4a4a", font=("Helvetica", 30, "bold"))],
        [sg.Text("The Binance Trading Bots application is not liable for:", text_color=("Red"), background_color="#4a4a4a", font=("Helvetica", 20, "bold"))],
        [sg.Text("Any financial losses during or after the use of the program", text_color=("Red"), background_color="#4a4a4a", font=("Helvetica", 20, "bold"))],
        [sg.Text("Injuries suffered during or after the use of the program", text_color=("Red"), background_color="#4a4a4a", font=("Helvetica", 20, "bold"))],
        [sg.Text("•Disclaimer•", text_color=("Red"), background_color="#4a4a4a", font=("Helvetica", 30, "bold"))],

        [sg.Text((""), background_color="#4a4a4a")],

        [sg.Text("Instructions", background_color="#4a4a4a", font=("Helvetica", 30, "bold"))],
        [sg.Text("1.", background_color="#4a4a4a", font=("Helvetica", 20))],
        [sg.Text("2.", background_color="#4a4a4a", font=("Helvetica", 20))],
        [sg.Text("3.", background_color="#4a4a4a", font=("Helvetica", 20))],
        [sg.Text("4.", background_color="#4a4a4a", font=("Helvetica", 20))],
        [sg.Text("5.", background_color="#4a4a4a", font=("Helvetica", 20))],
    ]

    return sg.Window("Instruction", instruction_layout, finalize=True, background_color="#4a4a4a")

def show_row_details(row_data, x, y):
    sg.theme('DarkGrey1')  # Choose a theme (optional)

    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    x1 = np.linspace(0, len(x), len(y))
    y1 = linregress(x, y).slope * x1 + linregress(x, y).intercept
    fig.add_subplot(111).plot(x, y)
    #fig.subplot(x1, y1, ':')

    def draw_figure(canvasg, figure):
        tkcanvas2 = FigureCanvasTkAgg(figure, canvasg)
        tkcanvas2.draw()
        tkcanvas2.get_tk_widget().pack(side='top', fill='both', expand=1)
        return tkcanvas2

    # Create PySimpleGUI layout
    popup_layout = [
        [sg.Text(f"Symbol: {row_data['symbol']}")],
        [sg.Text(f"Strategy ID: {row_data['strategyId']}")],
        [sg.Text(f"Runtime: {row_data['runningTime']}")],
        [sg.Text(f"ROI: {row_data['roi']}")],
        [sg.Text(f"Coef: {row_data['coef']}")],
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('OK', size=(15, 1), button_color=("black", "orange"), key='OK_BUTTON')]
    ]

    popup_window = sg.Window('Row Details', popup_layout, grab_anywhere=True, finalize=True)
    tkcanvas = draw_figure(popup_window['-CANVAS-'].TKCanvas, fig)

    while True:
        event, values = popup_window.read()

        if event == sg.WIN_CLOSED or event == 'OK_BUTTON':
            break

    popup_window.close()

main_window = create_main_window()

while True:
    event, values = main_window.read()

    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break

    if event == '-START-':
        active_window = 'start'
        main_window.hide()
        start_window = create_start_window()

        while True:
            start_event, start_values = start_window.read()

            if start_event in (sg.WIN_CLOSED, '-BACK-'):
                start_window.close()
                main_window.un_hide()
                break

            if start_event == '-SUBMIT-':
                selected_gridtype = start_values['-GRID-']
                selected_unit = start_values['-UNIT-']
                selected_mitime = start_values['-MITIME-']
                selected_matime = start_values['-MATIME-']
                selected_size = start_values['-SIZE-']

                datarecieve = analysis(selected_gridtype, selected_unit, selected_mitime, selected_matime, selected_size)
                data = datarecieve[0]
                graphs = datarecieve[1]
                table_data = []
                for i in range(0, len(data)):
                    row_data = [data[i]['symbol'], data[i]['strategyId'], data[i]['runningTime'], data[i]['roi'], data[i]['coef']]
                    table_data.insert(i, row_data)

                table_headings = ['Symbol', 'strategyID', 'Runtime', 'ROI', 'Coef']

                start_window.close()
                hello_layout = [
                    [sg.Text(f"Selected Grid Type: {selected_gridtype}", background_color="#4a4a4a", font=("Helvetica", 26, "bold"))],
                    [sg.Text(f"Selected Time Unit: {selected_unit}", background_color="#4a4a4a", font=("Helvetica", 26, "bold"))],
                    [sg.Text(f"Selected Minimum Time: {selected_mitime}", background_color="#4a4a4a", font=("Helvetica", 26, "bold"))],
                    [sg.Text(f"Selected Maximum Time: {selected_matime}", background_color="#4a4a4a", font=("Helvetica", 26, "bold"))],
                    [sg.Text(f"Selected Date Set Size: {selected_size}", background_color="#4a4a4a", font=("Helvetica", 26, "bold"))],
                    [sg.Table(values=table_data, headings=table_headings, num_rows=20, background_color="#4a4a4a", font=("Helvetica", 15, "bold"), auto_size_columns=False, justification='center', key='-TABLE-', enable_events=True)],
                    [sg.Button("BACK TO MAIN MENU", size=(46, 1), font=("Helvetica", 20), key='-OK-', button_color=("black", "orange"))]
                ]
                hello_window = sg.Window("Selected Parameters", hello_layout, finalize=True, background_color="#4a4a4a")

                while True:
                    hello_event, hello_values = hello_window.read()

                    if hello_event == sg.WIN_CLOSED or hello_event == '-OK-':
                        hello_window.close()
                        main_window.un_hide()
                        break

                    graphfound = False
                    g_x = [0]
                    g_y = [0]
                    if hello_event == '-TABLE-':
                        selected_row = hello_values['-TABLE-'][0]
                        if selected_row:
                            for i in range(0, len(graphs)):
                                if graphs[i][0] == data[selected_row]['strategyId']:
                                    #chart(graphs[i][1], graphs[i][2])
                                    g_x = graphs[i][1]
                                    g_y = graphs[i][2]
                                    graphfound = True
                                    break
                            if not graphfound:
                                print('error: graph not found')
                            show_row_details(data[selected_row],g_x,g_y)


    if event == '-INSTRUCTION-':
        active_window = 'instruction'
        instruction_window = create_instruction_window()

        while True:
            instruction_event, instruction_values = instruction_window.read()

            if instruction_event == sg.WIN_CLOSED:
                instruction_window.close()
                main_window.un_hide()
                break

main_window.close()
