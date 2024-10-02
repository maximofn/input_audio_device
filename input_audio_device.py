#!/usr/bin/env python3
import signal
import gi
gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3, GLib
from gi.repository import Gtk as gtk
import os
import subprocess
import webbrowser
import time
import argparse

APPINDICATOR_ID = 'Audio_input_devices'

PATH = os.path.dirname(os.path.realpath(__file__))
ICON_PATH = os.path.abspath(f"{PATH}/microphone.png")

actual_time_menu_item = None
number_of_devices_in_menu = 0
input_audio_devices_items = []

def main(debug=False):
    audio_input_devices_indicator = AppIndicator3.Indicator.new(APPINDICATOR_ID, ICON_PATH, AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
    audio_input_devices_indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    if debug: print("\n Input audio devices:")
    audio_input_devices_indicator.set_menu(build_menu())

    # Get CPU info
    GLib.timeout_add_seconds(1, update_input_audio_devices, audio_input_devices_indicator, debug)

    GLib.MainLoop().run()

def open_repo_link(_):
    webbrowser.open('https://github.com/maximofn/input_audio_device')

def buy_me_a_coffe(_):
    webbrowser.open('https://www.buymeacoffee.com/maximofn')

def change_input_device(item, output_device_id):
    subprocess.run(["pactl", "set-default-source", output_device_id])

def build_menu(debug=False):
    global actual_time_menu_item
    global number_of_devices_in_menu
    global input_audio_devices_items

    menu = gtk.Menu()

    item_input_devices_title = gtk.MenuItem(label='Input devices')
    menu.append(item_input_devices_title)

    input_devices = get_input_audio_devices(debug)
    input_audio_devices_items = []
    active_input_audio_device = get_active_input_audio_device(debug)
    for input_device in input_devices:
        if 'Name' in input_device.keys():
            key_name = 'Name'
        elif 'Nombre' in input_device.keys():
            key_name = 'Nombre'
        if 'Description' in input_device.keys():
            key_description = 'Description'
        elif 'Descripción' in input_device.keys():
            key_description = 'Descripción'
        elif 'Descripcion' in input_device.keys():
            key_description = 'Descripcion'
        if input_device[key_name] in active_input_audio_device:
            input_device_item = gtk.MenuItem(label=f"\t(active) {input_device[key_description]}")
        else:
            input_device_item = gtk.MenuItem(label=f"\t{input_device[key_description]}")
        input_device_item.connect('activate', change_input_device, input_device['id'])
        menu.append(input_device_item)
        input_audio_devices_items.append(input_device_item)
    number_of_devices_in_menu = len(input_devices)

    horizontal_separator1 = gtk.SeparatorMenuItem()
    menu.append(horizontal_separator1)

    actual_time_menu_item = gtk.MenuItem(label=time.strftime("%H:%M:%S"))
    menu.append(actual_time_menu_item)

    horizontal_separator2 = gtk.SeparatorMenuItem()
    menu.append(horizontal_separator2)

    item_repo = gtk.MenuItem(label='Repository')
    item_repo.connect('activate', open_repo_link)
    menu.append(item_repo)

    item_buy_me_a_coffe = gtk.MenuItem(label='Buy me a coffe')
    item_buy_me_a_coffe.connect('activate', buy_me_a_coffe)
    menu.append(item_buy_me_a_coffe)

    horizontal_separator3 = gtk.SeparatorMenuItem()
    menu.append(horizontal_separator3)

    item_quit = gtk.MenuItem(label='Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)

    menu.show_all()
    return menu

def update_menu(indicator, input_devices, debug=False):
    actual_time_menu_item.set_label(time.strftime("%H:%M:%S"))

    # If the number of devices has changed, update the menu
    if len (input_devices) != number_of_devices_in_menu:
        indicator.set_menu(build_menu(debug))

    # If the number of devices has not changed, update the devices
    else:
        active_input_audio_device = get_active_input_audio_device(debug)
        for number_input_device, input_device in enumerate(input_devices):
            if 'Name' in input_device.keys():
                key_name = 'Name'
            elif 'Nombre' in input_device.keys():
                key_name = 'Nombre'
            if 'Description' in input_device.keys():
                key_description = 'Description'
            elif 'Descripción' in input_device.keys():
                key_description = 'Descripción'
            elif 'Descripcion' in input_device.keys():
                key_description = 'Descripcion'
            if input_device[key_name].strip() in active_input_audio_device.strip():
                input_audio_devices_items[number_input_device].set_label(f"\t(active) {input_device[key_description]}")
            else:
                input_audio_devices_items[number_input_device].set_label(f"\t{input_device[key_description]}")

def update_input_audio_devices(indicator, debug=False):
    if debug: print("\n Input audio devices:")
    input_devices = get_input_audio_devices(debug)
    update_menu(indicator, input_devices, debug)

    return True

def get_active_input_audio_device(debug=False):
    # Get output audio devices
    result = subprocess.run(["pactl", "info"], capture_output=True, text=True)
    if result:
        active_input_audio_device = result.stdout
        if len(active_input_audio_device) > 0:
            for lines in result.stdout.split("\n"):
                if "Default Source:" in lines or "Fuente por defecto:" in lines:
                    active_input_audio_device = lines.split(":")[1].strip()
                    return active_input_audio_device
    
    result = subprocess.run(["pactl", "list", "sources"], capture_output=True, text=True)
    if result:
        output = result.stdout
        active_input_audio_device = None
        for i, line in enumerate(output.split("\n")):
            if "State" in line or "Estado" in line:
                state = line.split(":")[1].strip()
                print(line)
                print(output.split("\n")[i + 1])
                if state == "IDLE":
                    active_input_audio_device = output.split("\n")[i + 1].split(":")[1].strip()
                    print(f"active_input_audio_device: {active_input_audio_device}")
                    return active_input_audio_device
    return None

def get_input_audio_devices(debug=False):
    # Get output audio devices
    result = subprocess.run(["pactl", "list", "sources"], capture_output=True, text=True)
    if result:
        output = result.stdout
        input_devices = []
        input_device = None
        for number_line, line in enumerate(output.split("\n")):
            if "Source #" in line or "Fuente #" in line:
                if input_device:
                    input_devices.append(input_device)
                input_device = {"id": line.split("#")[1]}
                properties = 0
                ports = 0
                formats = 0
                activate_port = 0
            elif "Properties:" in line:
                properties = 1
                ports = 0
                formats = 0
                activate_port = 0
                input_device["properties"] = {}
            elif "Ports:" in line:
                properties = 0
                ports = 1
                formats = 0
                activate_port = 0
                input_device["ports"] = {}
            elif "Formats:" in line:
                properties = 0
                ports = 0
                formats = 1
                activate_port = 0
                input_device["formats"] = {}
            elif "Active Port:" in line:
                properties = 0
                ports = 0
                formats = 0
                activate_port = 1
                input_device["active_port"] = {}
            else:
                key = line.split(":")[0].strip()
                if "balance" in key:
                    key = "balance"
                    value = line.split("balance")[1]
                else:
                    value = line.split(":")[1:]

                # if value is a list, join it
                if type(value) == list:
                    value = "".join(value).strip()
                else:
                    value = value.strip()

                if properties:
                    input_device["properties"][key] = value
                elif ports:
                    input_device["ports"][key] = value
                elif formats:
                    if key != "":
                        input_device["formats"][key] = value
                elif activate_port:
                    input_device["active_port"][key] = value
                else:
                    input_device[key] = value
            
            if number_line == len(output.split("\n")) - 1:
                input_devices.append(input_device)
                
    return input_devices

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Input audio device')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()
    debug = args.debug

    signal.signal(signal.SIGINT, signal.SIG_DFL) # Allow the program to be terminated with Ctrl+C
    main(debug)
