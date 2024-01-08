'''

This code reads and processes the data from a Renogy Wanderer Charge controller. 

'''
# pip3 install pyserial
# pip3 install minimalmodbus
import minimalmodbus
import serial
import sys,os,io
import time 
import json
import requests
from datetime import date

#debug = False
#sleepTime = 10

# battery type. our battery is a 'sealed' battery. This is for the charge controller to use. 
BATTERY_TYPE = {
    1: 'open', 
    2: 'sealed',
    3: 'gel',
    4: 'lithium',
    5: 'customized'
}

# charging state. also used by the charge controller 
CHARGING_STATE = {
    0: 'deactivated',
    1: 'activated',
    2: 'mppt',
    3: 'equalizing',
    4: 'boost',
    5: 'floating',
    6: 'current limiting' 
}

# diagnositcs
#print(minimalmodbus._get_diagnostic_string())

# function to read and print the register data to the console.
def read_registers():
    data = {}
    json_data = {}
    try:
        # this might change depending on if the com port is changed
        # ls /dev/tty* should be anything that ends in USB
        device_name = '/dev/ttyUSB0'

        # charge controller config. Most of the values are from the charge controllers documentation others were from trial and error.
        renogy = minimalmodbus.Instrument(device_name, 1) # this 1 value could change. it might also be 255. But it worked with 1 for us
        renogy.serial.baudrate = 9600
        renogy.serial.bytesize = 8
        renogy.serial.parity = serial.PARITY_NONE
        renogy.serial.stopbits = 1
        renogy.serial.timeout = 2
        # renogy.debug = debug

        # max system voltage and amps
        max_system_register = renogy.read_register(0x00A)
        max_voltage = max_system_register >> 8
        max_current = max_system_register & 0x00ff
        print("MAX Sys Voltage:", float(max_voltage), "V")
        print("MAX Sys Amps:", float(max_current), "A")

        # max discharge and system type
        max_discharge = renogy.read_register(0x00B)
        max_d = max_discharge >> 8
        prod_type = max_discharge & 0x00ff
        print("Max Discharge:", float(max_discharge), "A")
        print("System Type:", prod_type, "00=controller 1=inverter")

        # Battery Capacity
        battery_capacity = renogy.read_register(0x100)
        print("Battery Capacity:", float(battery_capacity), "%")

        # Battery voltage
        battery_voltage = renogy.read_register(0x101)
        battery_voltage = battery_voltage / 10
        print("Battery Voltage:", float(battery_voltage), "V")

        # Charge in Amps
        charge_amps = renogy.read_register(0x102)
        print("Charging Amp:", float(charge_amps/100), "A")

        # Controller Temperature (C)
        controller_temp_register = renogy.read_register(0x103)
        controller_temp_bits = controller_temp_register >> 8
        temp_val = controller_temp_bits & 0x0ff
        sign = controller_temp_bits >> 7
        device_temp = -(temp_val - 128) if sign == 1 else temp_val
        print("Controller Temperature:", float(device_temp), "C")

        # Load Voltage (V)
        load_voltage = renogy.read_register(0x104)
        print("Load Voltage:", load_voltage, "V")

        # Load Current (A)
        load_current = renogy.read_register(0x105)
        print("Load Current:", load_current, "A")

        # Load Power (W)
        load_power = renogy.read_register(0x106)
        print("Load Power:", load_power, "W")

        # Solar Panel (PV) Voltage
        solar_voltage_register = renogy.read_register(0x107)
        print("PV Voltage:", float(solar_voltage_register/10), "V")

        # Solar Panel (PV) Amps
        solar_current_register = renogy.read_register(0x108)
        print("PV Current:", float(solar_current_register/100), "A")
 
        # Solar Panel (PV) Power
        solar_power = renogy.read_register(0x109)
        print("PV Power:", solar_power, "W")

        # Max Battery Voltage Today
        max_battery_voltage_today = renogy.read_register(0x10B)
        print("Battery Max Voltage Today:", float(max_battery_voltage_today)/10, "V")

        # Min Battery Voltage Today
        min_battery_voltage_today = renogy.read_register(0x10C)
        print("Battery Min Voltage Today:", float(min_battery_voltage_today)/10, "V")

        # Max Charge Current Today
        max_charge_current_today = renogy.read_register(0x10D)
        print("Max Charge Current Today:", float(max_charge_current_today)/10, "A")

        # Max Discharge Current Today
        max_discharge_current_today = renogy.read_register(0x10E)
        print("Max Discharge Current Today:", float(max_discharge_current_today)/10, "A")

        # Max Charge Power Today
        max_charge_power_today = renogy.read_register(0x10F)
        print("Max Charge Power Today:", float(max_charge_power_today)/1, "W")

        # Max Discharge Power Today
        max_discharge_power_today = renogy.read_register(0x110)
        print("Todays Max Discharge Power:", float(max_discharge_power_today)/1, "W")

        # Max Charge Amp/Hrs Today
        max_chargeamp_today = renogy.read_register(0x111)
        print("Todays Max Charge Amp Hours:", float(max_chargeamp_today)/1, "A/H")

        # Max Discharge Amp/Hrs Today
        max_dischargeamp_today = renogy.read_register(0x112)
        print("Todays Max Discharge Amp Hours:", float(max_dischargeamp_today)/1, "A/H")

        # Charge Power Today
        power_today = renogy.read_register(0x113)
        print("Todays Power Generated:", float(power_today)/10, "W/H")

        # Discharge Power Today
        discharge_today = renogy.read_register(0x114)
        print("Todays Power Consumed:", float(discharge_today)/10, "W/H")

        # Controller Uptime (Days)
        controller_uptime = renogy.read_register(0x115)
        print("Uptime:", controller_uptime, "Days")

        # Total Battery Over Charges
        battery_overcharge_total = renogy.read_register(0x116)
        print("Battery Over-Charges:", battery_overcharge_total)

        # Total Battery Full Charges
        battery_fullcharge_total = renogy.read_register(0x117)
        print("Battery Full Charges:", battery_fullcharge_total)

        # Charging State
        charging_state_register = renogy.read_register(0x120)
        charge_state_num = charging_state_register & 0x00ff
        charge_state = CHARGING_STATE.get(charge_state_num)
        print("Charge State:", charge_state_num, charge_state)

        # Battery Type
        battery_type_register = renogy.read_register(0xE004)
        battery_type = BATTERY_TYPE.get(battery_type_register)
        print("Battery Type:", battery_type)

        # puts all the data in dictionary
        data["Max System Voltage"] = float(max_voltage)
        data["Max System Amps"] = float(max_current)
        data["Max Discharge"] = float(max_discharge)
        data["System Type"] = prod_type
        data["Battery Capacity"] = float(battery_capacity)
        data["Battery Voltage"] = float(battery_voltage)
        data["Charging Amps"] = float(charge_amps/10)
        data["Controller Temperature"] = float(device_temp)
        data["Load Voltage"] = float(load_voltage)
        data["Load Current"] = float(load_current)
        data["Load Power"] = float(load_power)
        data["PV Voltage"] = float(solar_voltage_register/10)
        data["PV Current"] = float(solar_current_register/100)
        data["PV Power"] = float(solar_power)
        data["Battery Max Voltage Today"] = float(max_battery_voltage_today)/10
        data["Battery Min Voltage Today"] = float(min_battery_voltage_today)/10
        data["Max Charge Current Today"] = float(max_charge_current_today)/10
        data["Max Discharge Current Today"] = float(max_discharge_current_today)/10
        data["Max Charge Power Today"] = float(max_charge_power_today)/1
        data["Todays Max Discharge Power"] = float(max_discharge_power_today)/1
        data["Todays Max Charge Amp Hours"] = float(max_chargeamp_today)/1
        data["Todays Max Discharge Amp Hours"] = float(max_dischargeamp_today)/1
        data["Todays Power Generated"] = float(power_today)/10
        data["Todays Power Consumed"] = float(discharge_today)/10
        data["Uptime"] = float(controller_uptime)
        data["Battery Over-Charges"] = float(battery_overcharge_total)
        data["Battery Full Charges"] = float(battery_fullcharge_total)
        data["Charge State Number"] = charge_state_num
        data["Charging State"] = charge_state
        data["Battery Type"] = battery_type

        # add time stamp (date time library)

        json_data = json.dumps(data, indent=3)

    except IOError:
        print("Failed to read from the controller")

    return json_data

# writes the data to json file
def write_json_file(json_data, filename="solar_panel_data.json"):
    with open(filename, 'w') as json_file:
        json_file.write(json_data)

          

# infintely runs the program and prints the data every 30 seconds.
while True:
    json_data = read_registers()
    write_json_file(json_data)
    # website url
    server_url = "http://localhost:3000/data"
    try:
        # make sure its json.loads and not json.load
        json_dict = json.loads(json_data)
        response = requests.post(server_url, json=json_dict)
        
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occured: {e}")
    time.sleep(30)
