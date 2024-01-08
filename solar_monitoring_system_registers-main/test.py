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

# infintely runs the program and prints the data every 30 seconds.
json_data= {
            "Max System Voltage": 12.0,
            "Max System Amps": 30.0,
            "Max Discharge": 5120.0,
            "System Type": 0,
            "Battery Capacity": 50.0,
            "Battery Voltage": 12.8,
            "Charging Amps": 0.0,
            "Controller Temperature": 20.0,
            "Load Voltage": 0.0,
            "Load Current": 0.0,
            "Load Power": 0.0,
            "PV Voltage": 8.9,
            "PV Current": 0.0,
            "PV Power": 0.0,
            "Battery Max Voltage Today": 12.7,
            "Battery Min Voltage Today": 12.8,
            "Max Charge Current Today": 0.0,
            "Max Discharge Current Today": 0.0,
            "Max Charge Power Today": 0.0,
            "Todays Max Discharge Power": 0.0,
            "Todays Max Charge Amp Hours": 0.0,
            "Todays Max Discharge Amp Hours": 0.0,
            "Todays Power Generated": 0.0,
            "Todays Power Consumed": 0.0,
            "Uptime": 1.0,
            "Battery Over-Charges": 0.0,
            "Battery Full Charges": 0.0,
            "Charge State Number": 0,
            "Charging State": "deactivated",
            "Battery Type": "sealed"
    }



    

# website url
server_url = "http://localhost:3000/data"

counter = 0
while True:
    try:
        # Make a POST request to the server
        response = requests.post(server_url, json=json_data)

        # Check if the request was successful
        if response.status_code == 200:
            print("Data sent successfully")
        else:
            print(f"Failed to send data: {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the request
        print(f"An error occurred: {e}")
    
    time.sleep(15)
    counter += 15

    # every 24 hours send the today data.
    if counter >= 86400:
        try:
            today_response = requests.post(server_url + "/store", json=json_data)
            if today_response.status_code == 200:
                print("Today Request sent successfully")
            else:
                print(f"Failed to send today request: {today_response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occured during today request: {e}")
        counter = 0 # reset the counter




