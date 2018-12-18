#!/usr/bin/python
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pprint import pprint
import time
import linuxcnc, hal

START_ADDR = 2048#M0
S_CNT = 40
B_CNT = 20
plc01 = hal.component("plc01")
#CNC <- PLC
plc01.newpin("S0", hal.HAL_BIT,hal.HAL_OUT) #PLC READY
plc01.newpin("S1", hal.HAL_BIT,hal.HAL_OUT) #EXT STOP
plc01.newpin("S2", hal.HAL_BIT,hal.HAL_OUT) #ALARM 
plc01.newpin("S3", hal.HAL_BIT,hal.HAL_OUT) #PLC_BUSY
plc01.newpin("S4", hal.HAL_BIT,hal.HAL_OUT) #SPINDLE ON SPD
plc01.newpin("S5", hal.HAL_BIT,hal.HAL_OUT) #SPINDLE ZERO
plc01.newpin("S6", hal.HAL_BIT,hal.HAL_OUT) #OT-X
plc01.newpin("S7", hal.HAL_BIT,hal.HAL_OUT) #OT-Y
plc01.newpin("S8", hal.HAL_BIT,hal.HAL_OUT) #OT-Z
plc01.newpin("S9", hal.HAL_BIT,hal.HAL_OUT) #OT-B
plc01.newpin("S10", hal.HAL_BIT,hal.HAL_OUT) #OT-C
plc01.newpin("S11", hal.HAL_BIT,hal.HAL_OUT) #MAG-READY
plc01.newpin("S12", hal.HAL_BIT,hal.HAL_OUT) #MAG-ON-POS
plc01.newpin("S13", hal.HAL_BIT,hal.HAL_OUT) #SPINDLE UNLOCK
plc01.newpin("S14", hal.HAL_BIT,hal.HAL_OUT) #DRILL-BANK-DOWN
plc01.newpin("S15", hal.HAL_BIT,hal.HAL_OUT) #DRILL-BANK-UP
plc01.newpin("S16", hal.HAL_BIT,hal.HAL_OUT) #TBL-AB-READY
plc01.newpin("S17", hal.HAL_BIT,hal.HAL_OUT) #TBL-CD-READY
plc01.newpin("S18", hal.HAL_BIT,hal.HAL_OUT) #MAG-OPENED
plc01.newpin("S19", hal.HAL_BIT,hal.HAL_OUT) #MAG-SLIDE-ON-POS

#STATUS BIT
plc01.newpin("S20", hal.HAL_BIT,hal.HAL_IN) #MACHINE RST
plc01.newpin("S21", hal.HAL_BIT,hal.HAL_IN) #MACHINE ON
plc01.newpin("S22", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_ON
plc01.newpin("S23", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_REV
plc01.newpin("S24", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_RST
plc01.newpin("S25", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S26", hal.HAL_BIT,hal.HAL_IN) #MAG-START
plc01.newpin("S27", hal.HAL_BIT,hal.HAL_IN) #TOOL UNCLAMP
plc01.newpin("S28", hal.HAL_BIT,hal.HAL_IN) #MAG Y-
plc01.newpin("S29", hal.HAL_BIT,hal.HAL_IN) #MAG Y+
plc01.newpin("S30", hal.HAL_BIT,hal.HAL_IN) #DRILL BANK DOWN
plc01.newpin("S31", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE AB
plc01.newpin("S32", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE CD
plc01.newpin("S33", hal.HAL_BIT,hal.HAL_IN) #mag open
plc01.newpin("S34", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S35", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S36", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S37", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S38", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("S39", hal.HAL_BIT,hal.HAL_IN) #


#CNC -> PLC
plc01.newpin("B20", hal.HAL_BIT,hal.HAL_IN) #MACHINE RST
plc01.newpin("B21", hal.HAL_BIT,hal.HAL_IN) #MACHINE ON
plc01.newpin("B22", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_ON
plc01.newpin("B23", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_REV
plc01.newpin("B24", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_RST
plc01.newpin("B25", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B26", hal.HAL_BIT,hal.HAL_IN) #MAG-START
plc01.newpin("B27", hal.HAL_BIT,hal.HAL_IN) #TOOL UNCLAMP
plc01.newpin("B28", hal.HAL_BIT,hal.HAL_IN) #MAG Y-
plc01.newpin("B29", hal.HAL_BIT,hal.HAL_IN) #MAG Y+
plc01.newpin("B30", hal.HAL_BIT,hal.HAL_IN) #DRILL BANK DOWN
plc01.newpin("B31", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE AB
plc01.newpin("B32", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE CD
plc01.newpin("B33", hal.HAL_BIT,hal.HAL_IN) #mag open
plc01.newpin("B34", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B35", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B36", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B37", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B38", hal.HAL_BIT,hal.HAL_IN) #
plc01.newpin("B39", hal.HAL_BIT,hal.HAL_IN) #


#DATA CNC->PLC
plc01.newpin("D201", hal.HAL_U32,hal.HAL_IN) #MAG INDEX COM
plc01.newpin("D201F", hal.HAL_FLOAT,hal.HAL_IN) #MAG INDEX COM

#DATA PLC->CNC
plc01.newpin("E200F", hal.HAL_FLOAT,hal.HAL_OUT) #MAG INDEX COM
plc01.newpin("E201F", hal.HAL_FLOAT,hal.HAL_OUT) #MAG INDEX COM



client= ModbusClient(method = "ascii", port="/dev/ttyS0", stopbits = 1, bytesize = 7, parity = 'E', baudrate= 9600)
connection = client.connect()

print(B_CNT)
pinout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
register = [0,0,0,0,0,0,0,0]

time.sleep(2)
plc01.ready()
regs = client.read_holding_registers(4297, 1, unit=1)
plc01['D201'] = regs.registers[0]

def syncPlc():
	result= client.read_discrete_inputs(START_ADDR,S_CNT,unit= 1)
	#print(result.bits)
#	if hasattr(result, 'bits'):
#		print ("connection err")
#		return -1
	for x in range(0, S_CNT):
		plc01['S' + str(x)] = result.bits[x]
	for x in range(0, B_CNT):
		pinout[x] = plc01['B' + str((S_CNT/2) + x)]
	client.write_coils(START_ADDR+(S_CNT/2),pinout,unit=1)
		
	regs = client.read_holding_registers(4296, 2, unit=1)
#	if hasattr(regs, 'registers'):
#		print ("connection err")
#		return -1

	plc01['E200F'] = float(regs.registers[0])
	plc01['E201F'] = float(regs.registers[1])

	client.write_register(4297, int(plc01['D201F']), unit=1)
	#print(int(plc01['E201F']))
	
	#time.sleep(1)
	return 0

if __name__ == "__main__":
	while True:
		try:
			syncPlc()	
		except KeyboardInterrupt:
			print("Connection was closed")
			client.close()
