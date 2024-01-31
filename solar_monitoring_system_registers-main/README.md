# solar_monitoring_system_registers
This repository holds the code that simply sets up the data reading of the Renogy Wanderer Solar Charge controller. It sets up the baud rate, stop bits, etc.. Also, reads the registers and displays the data of the registers. 

Contributors:
Ryan Anderson (ryananderson@lewisu.edu)

Renogy Wanderer Solar Controller Registers
|0x00A|Controller voltage rating|Volts|
|0x00A|Controller current rating|Amps|
|0x00B|Controller discharge current rating|Amps|
|0x00B|Controller type||
|0x00C - 0x013|Controller model name||
|0x014 - 0x015|Controller software version||
|0x016 - 0x017|Controller hardware version||
|0x018 - 0x019|Controller serial number||
|0x01A|Controller MODBUS address|
|0x100|Battery Capacity|Percent|
|0x101|Battery Voltage|Volts|
|0x102|Battery Charge Current|Amps|
|0x103|Battery Temperature|Celcius|
|0x103|Controller Temperature|Celcius|
|0x104|Load Voltage|Volts|
|0x105|Load Current|Amps|
|0x106|Load Power|Watts|

**************************************
|0x107|Solar Panel (PV) Voltage|Volts|  
|0x108|Solar Panel (PV) Current|Amps|   
|0x109|Solar Panel (PV) Power|Watts|    
**************************************

|0x10B|Min Battery Voltage Today|Volts|
|0x10C|Min Battery Voltage Today|Volts|
|0x10D|Max Charge Current Today|Amps|
|0x10E|Max Discharge Current Today|Amps|
|0x10F|Max Charge Power Today|Watts|
|0x110|Max Discharge Power Today|Watts|
|0x111|Charge Amp/Hrs Today|Amp Hours|
|0x112|Discharge Amp/Hrs Today|Amp Hours|
|0x113|Charge Watt/Hrs Today|Watt Hours|
|0x114|Discharge Watt/Hrs Today|Watt Hours|
|0x115|Controller Uptime|Days|
|0x116|Total Battery Over-charges|Count|
|0x117|Total Battery Full Charges|Count|




error from raspberry pi:
Failed to send the data: 400


error from server:
SyntaxError: Unexpected token " in JSON at position 0
    at JSON.parse (<anonymous>)
    at createStrictSyntaxError (/home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/body-parser/lib/types/json.js:160:10)
    at parse (/home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/body-parser/lib/types/json.js:83:15)
    at /home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/body-parser/lib/read.js:128:18
    at AsyncResource.runInAsyncScope (async_hooks.js:190:9)
    at invokeCallback (/home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/raw-body/index.js:231:16)
    at done (/home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/raw-body/index.js:220:7)
    at IncomingMessage.onEnd (/home/pi/solar panel/Solar-Monitoring-System-Local/node_modules/express/node_modules/raw-body/index.js:280:7)
    at IncomingMessage.emit (events.js:314:20)
    at endReadableNT (_stream_readable.js:1241:12)



    new error:
    Traceback (most recent call last):
  File "/home/pi/solar_monitoring_system_registers/register_reading.py", line 234, in <module>
    json_dict = json.load(json_data)
  File "/usr/lib/python3.9/json/__init__.py", line 293, in load
    return loads(fp.read(),
AttributeError: 'str' object has no attribute 'read'
