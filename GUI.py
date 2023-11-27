import PySimpleGUI as sg
from binancerequest2 import analysis


button_size = (7, 1)


layout = [
    [
        sg.Button("START", size=button_size, font=("Helvetica", 30, "bold"),  pad=(4, 5), key='-START-', button_color=("black", "green")),
        sg.Button("EXIT", size=button_size, font=("Helvetica", 30, "bold"), pad=(4, 5), key='-EXIT-', button_color=("black", "red"))
    ],
    [
        [sg.Button("INSTRUCTION", size=(15, 1), font=("Helvetica", 30, "bold"), key='-INSTRUCTION-', button_color=("black", "orange"), pad=(5, 3))],
    ]
]


window = sg.Window("Binance Trading Bots", layout, background_color="#4a4a4a", finalize=True)
active_window = 'main'

# Create a function to create and show a new empty window
def create_start_window():
    start_layout = [
        [
            [sg.Text("Choose trading bot parameters", background_color="#4a4a4a", font=("Helvetica", 23, "bold"), pad=(0, 0))],

            [sg.Text(("Select grid type:"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.Combo(['Futures grid', 'Spot grid'], key='-GRID-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Select time unit of measure:"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.Combo(['Months', 'Days', 'Hours', 'Minutes', 'Seconds'], key='-UNIT-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Minimum time (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-MITIME-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Maximum time (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-MATIME-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Text(("Select data set size (number):"), background_color="#4a4a4a", font=("Helvetica", 25))],
            [sg.InputText([], key='-SIZE-', size=(14, 1), font=("Helvetica", 20))],

            [sg.Button('START ANALYSIS', size=(28, 1), font=("Helvetica", 20), key='-SUBMIT-', button_color=("black", "green"))],
            [sg.Button("BACK TO MAIN MENU", size=(28, 1), font=("Helvetica", 20), key='-BACK-', button_color=("black", "orange"))],

        ]
    ]

    start_window = sg.Window("Binance Trading Bots", start_layout, background_color="#4a4a4a", finalize=True)

    while True:
        start_event, start_values = start_window.read()

        if start_event in (sg.WIN_CLOSED, '-BACK-'):
            start_window.close()
            return_to_main_window()

        if active_window == 'main':
            break

        if start_event == sg.WIN_CLOSED:
            break

        if start_event == '-SUBMIT-':
            selected_gridtype = start_values['-GRID-']
            selected_unit = start_values['-UNIT-']
            selected_mitime = start_values['-MITIME-']
            selected_matime = start_values['-MATIME-']
            selected_size = start_values['-SIZE-']

            data = analysis(selected_gridtype, selected_unit, selected_mitime, selected_matime, selected_size)
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
                [sg.Table(values=table_data, headings=table_headings, num_rows=20, background_color="#4a4a4a", font=("Helvetica", 15, "bold"), auto_size_columns=False, justification='center', key='-TABLE-')],
                [sg.Button("BACK TO MAIN MENU", size=(46, 1), font=("Helvetica", 20), key='-OK-', button_color=("black", "orange"))]

            ]
            hello_window = sg.Window("Selected Parameters", hello_layout, finalize=True, background_color="#4a4a4a")

            while True:
                hello_event, hello_values = hello_window.read()

                if hello_event == sg.WIN_CLOSED or hello_event == '-OK-':
                    hello_window.close()
                    break

    start_window.close()

# Create a function to create and show the instruction window
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

    instruction_window = sg.Window("Instruction", instruction_layout, finalize=True, background_color="#4a4a4a")

    while True:
        instruction_event, instruction_values = instruction_window.read()

        if instruction_event == sg.WIN_CLOSED:
            break

        if instruction_event == '-BACK-':
            instruction_window.close()
            return_to_main_window()

# Create a function to return to the main window
def return_to_main_window():
    global active_window
    active_window = 'main'
    window.un_hide()

# Create an event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break

    if event == '-START-':
        active_window = 'start'
        window.hide()
        create_start_window()

    if event == '-INSTRUCTION-':
        active_window = 'instruction'
        create_instruction_window()

window.close()
