from nicegui import ui
from mqtt_client import mqtt_start
from state import sensor_state, initialise_sensor_state


cards = {}
chart= None

import threading
from db_worker import db_worker, get_today

threading.Thread(target=db_worker, daemon=True).start()

def refresh():

    for sensor in range(1, 4):
        values = sensor_state[sensor]

        if not values:
            continue

        cards[sensor]["moisture"].set_value(values["moisture"])

        cards[sensor]["temp"].set_text(
            f'{values["temperature"]:.1f} °C'
        )

        cards[sensor]["battery"].set_text(
            f'{values["battery"]:.0f}%'
        )

        cards[sensor]["last_seen"].set_text(
            f'{values["last_seen"]}'
        )

        chart.options['series'][sensor-1]['data'].append([values['last_seen'], values['moisture']])


def initialise_chart():

    chart_data = get_today()
    chart.options['series'][0]['data']=chart_data[1]
    chart.options['series'][1]['data']=chart_data[2]
    chart.options['series'][2]['data']=chart_data[3]
    chart.update()

ui.label("Soil Monitor").classes("text-h3")


with ui.column().classes("w-full"):

    with ui.row().classes("w-full justify-around"):
        for sensor in range(1, 4):

            with ui.card():
                ui.label(f"Sensor {sensor}")
                gauge = ui.circular_progress(
                    show_value=True,
                    value=0,
                    min=0,
                    max=100
                ).props("size=120px")

                temp = ui.label("--")

                battery = ui.label("--")

                last_seen = ui.label("--")

                cards[sensor] = {
                    "moisture": gauge,
                    "temp": temp,
                    "battery": battery,
                    "last_seen": last_seen
                }

        chart = (
            ui.echart({
                        'xAxis': {
                            'type': 'time'
                        },
                        'yAxis': {
                            'type': 'value'
                        },
                        'legend': {'textStyle': {'color': 'gray'}},
                        'series': [
                            {
                                'type': 'line',
                                'smooth': True,
                                'data': [],
                                'name':'Sensor 1'
                            },
                                 {
                                'type': 'line',
                                'smooth': True,
                                'data': [],
                                'name':'Sensor 2'
                            },
                                 {
                                'type': 'line',
                                'smooth': True,
                                'data': [],
                                'name':'Sensor 3'
                            }
                        ]
                        })
                            .classes("w-full")
                            .style("height:400px")
                        )

ui.timer(1.0, refresh)
initialise_sensor_state()
initialise_chart()
mqtt_start()
ui.run()

