#!/usr/bin/python
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pprint import pprint
import time
import linuxcnc, hal
import json



#BROKER PROGRAM PATH MULTI TABLE
brokerProg = "brokerProg.json"

#COM CONF
COM_PORT = "/dev/ttyS0"
COM_METHOD= "ascii"
COM_BAUD = 9600
COM_STOPBITS = 1
COM_BSIZE = 7
COM_PARITY = 'E'
UNIT_ADDR = 1

#MEMORY MAPPING
START_ADDR = 2048#M0
S_CNT = 70
B1_OFFS = 20
B1_CNT = 20
B2_OFFS = 60
B2_CNT = 23

plc01 = hal.component("plc01")
#CNC <- PLC
#STATUS INPUT
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
#STATUS OUTPUT
plc01.newpin("S20", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S21", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S22", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S23", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S24", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S25", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S26", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S27", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S28", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S29", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S30", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S31", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S32", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S33", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S34", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S35", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S36", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S37", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S38", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S39", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
#STATUS INPUT
plc01.newpin("S40", hal.HAL_BIT,hal.HAL_OUT) #MPG SEL X
plc01.newpin("S41", hal.HAL_BIT,hal.HAL_OUT) #MPG SEL Y
plc01.newpin("S42", hal.HAL_BIT,hal.HAL_OUT) #MPG SEL Z 
plc01.newpin("S43", hal.HAL_BIT,hal.HAL_OUT) #MPG SEL B
plc01.newpin("S44", hal.HAL_BIT,hal.HAL_OUT) #MPG SEL C
plc01.newpin("S45", hal.HAL_BIT,hal.HAL_OUT) #MPG X1
plc01.newpin("S46", hal.HAL_BIT,hal.HAL_OUT) #MPG X10
plc01.newpin("S47", hal.HAL_BIT,hal.HAL_OUT) #MPG X100
plc01.newpin("S48", hal.HAL_BIT,hal.HAL_OUT) #DHOOD DOWN SENS POS
plc01.newpin("S49", hal.HAL_BIT,hal.HAL_OUT) #DHOOD UP SENS POS
plc01.newpin("S50", hal.HAL_BIT,hal.HAL_OUT) #TOOL DETECTION
plc01.newpin("S51", hal.HAL_BIT,hal.HAL_OUT) #DUSTHOOD UP DETECTION
plc01.newpin("S52", hal.HAL_BIT,hal.HAL_OUT) #CSTART A
plc01.newpin("S53", hal.HAL_BIT,hal.HAL_OUT) #CSTART B
plc01.newpin("S54", hal.HAL_BIT,hal.HAL_OUT) #CSTART C
plc01.newpin("S55", hal.HAL_BIT,hal.HAL_OUT) #CSTART D
plc01.newpin("S56", hal.HAL_BIT,hal.HAL_OUT) #MAG SENSOR POS
plc01.newpin("S57", hal.HAL_BIT,hal.HAL_OUT) #MAG HOMED
plc01.newpin("S58", hal.HAL_BIT,hal.HAL_OUT) #
plc01.newpin("S59", hal.HAL_BIT,hal.HAL_OUT) #
#STATUS OUTPUT
plc01.newpin("S60", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S61", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S62", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S63", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S64", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S65", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S66", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S67", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S68", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S69", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S70", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S71", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S72", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S73", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S74", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S75", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S76", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S77", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S78", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT
plc01.newpin("S79", hal.HAL_BIT,hal.HAL_IN) #REFER TO OUTPUT BIT

#CNC -> PLC
plc01.newpin("B20", hal.HAL_BIT,hal.HAL_IN) #MACHINE RST
plc01.newpin("B21", hal.HAL_BIT,hal.HAL_IN) #MACHINE ON
plc01.newpin("B22", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_ON
plc01.newpin("B23", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_REV
plc01.newpin("B24", hal.HAL_BIT,hal.HAL_IN) #SPINDLE_RST
plc01.newpin("B25", hal.HAL_BIT,hal.HAL_IN) #DRILL-ON
plc01.newpin("B26", hal.HAL_BIT,hal.HAL_IN) #MAG-START
plc01.newpin("B27", hal.HAL_BIT,hal.HAL_IN) #TOOL UNCLAMP
plc01.newpin("B28", hal.HAL_BIT,hal.HAL_IN) #MAG Y-
plc01.newpin("B29", hal.HAL_BIT,hal.HAL_IN) #MAG Y+
plc01.newpin("B30", hal.HAL_BIT,hal.HAL_IN) #DRILL BANK DOWN
plc01.newpin("B31", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE AB
plc01.newpin("B32", hal.HAL_BIT,hal.HAL_IN) #TABLE ENABLE CD
plc01.newpin("B33", hal.HAL_BIT,hal.HAL_IN) #MAG DOR OPEN
plc01.newpin("B34", hal.HAL_BIT,hal.HAL_IN) #DUSTHOOD ARM UP DDOWN
plc01.newpin("B35", hal.HAL_BIT,hal.HAL_IN) #TABLE LOCK AB
plc01.newpin("B36", hal.HAL_BIT,hal.HAL_IN) #TABLE LOCK CD
plc01.newpin("B37", hal.HAL_BIT,hal.HAL_IN) #SON-Y
plc01.newpin("B38", hal.HAL_BIT,hal.HAL_IN) #SON-Z
plc01.newpin("B39", hal.HAL_BIT,hal.HAL_IN) #SON-B

#CNC -> PLC
plc01.newpin("B60", hal.HAL_BIT,hal.HAL_IN) #T101
plc01.newpin("B61", hal.HAL_BIT,hal.HAL_IN) #T102
plc01.newpin("B62", hal.HAL_BIT,hal.HAL_IN) #T104
plc01.newpin("B63", hal.HAL_BIT,hal.HAL_IN) #T105
plc01.newpin("B64", hal.HAL_BIT,hal.HAL_IN) #T106
plc01.newpin("B65", hal.HAL_BIT,hal.HAL_IN) #T107
plc01.newpin("B66", hal.HAL_BIT,hal.HAL_IN) #T108
plc01.newpin("B67", hal.HAL_BIT,hal.HAL_IN) #T109
plc01.newpin("B68", hal.HAL_BIT,hal.HAL_IN) #T110
plc01.newpin("B69", hal.HAL_BIT,hal.HAL_IN) #T111
plc01.newpin("B70", hal.HAL_BIT,hal.HAL_IN) #T112
plc01.newpin("B71", hal.HAL_BIT,hal.HAL_IN) #T5859
plc01.newpin("B72", hal.HAL_BIT,hal.HAL_IN) #T6061
plc01.newpin("B73", hal.HAL_BIT,hal.HAL_IN) #T6263
plc01.newpin("B74", hal.HAL_BIT,hal.HAL_IN) #PDL AB Y SETUP
plc01.newpin("B75", hal.HAL_BIT,hal.HAL_IN) #PDL CD Y SETUP
plc01.newpin("B76", hal.HAL_BIT,hal.HAL_IN) #BAR AB SETUP
plc01.newpin("B77", hal.HAL_BIT,hal.HAL_IN) #BAR CD SETUP
plc01.newpin("B78", hal.HAL_BIT,hal.HAL_IN) #SON-C
plc01.newpin("B79", hal.HAL_BIT,hal.HAL_IN) #SON-X

plc01.newpin("B80", hal.HAL_BIT,hal.HAL_IN) #LOCK TABLE AB
plc01.newpin("B81", hal.HAL_BIT,hal.HAL_IN) #LOCK TABLE CD
plc01.newpin("B82", hal.HAL_BIT,hal.HAL_IN) #HOME MAG

#DATA CNC->PLC
plc01.newpin("D201", hal.HAL_U32,hal.HAL_IN) #MAG INDEX COM
plc01.newpin("D201F", hal.HAL_FLOAT,hal.HAL_IN) #MAG INDEX COM

#DATA PLC->CNC
plc01.newpin("E200F", hal.HAL_FLOAT,hal.HAL_OUT) #MAG INDEX COM
plc01.newpin("E201F", hal.HAL_FLOAT,hal.HAL_OUT) #MAG INDEX COM

#internal signal
plc01.newpin("cstart", hal.HAL_BIT,hal.HAL_OUT) #CYCLE START
plc01.newpin("program-is-run", hal.HAL_BIT,hal.HAL_IN) #PROGRAM RUN FLAGS

#alarmCode
plc01.newpin("E01", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E02", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E03", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E04", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E05", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E06", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E07", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E08", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E09", hal.HAL_BIT,hal.HAL_OUT)
plc01.newpin("E010", hal.HAL_BIT,hal.HAL_OUT)

client= ModbusClient(method = COM_METHOD, port=COM_PORT, stopbits = COM_STOPBITS, bytesize = COM_BSIZE, parity = COM_PARITY, baudrate= COM_BAUD)
connection = client.connect()

time.sleep(2)
plc01.ready()
regs = client.read_holding_registers(4297, 1, unit=1)
plc01['D201'] = regs.registers[0]

class table:

	#DATUM T1
	datum_x1 = 533.917
	datum_y1 = -790.665

	#DATUM T2
	datum_x2 = 533.917 + 2350.
	datum_y2 = -790.665

	def __init__(self):	
		self.ab_state = 0
		self.cd_state = 0
		self.s = linuxcnc.stat()
		self.c = linuxcnc.command()
		self.queue = [] #means no job at all
		self.currJob = 0
		self.lastRun = False
	def jsonReader(self,filename=brokerProg):
		data = None
		with open(filename,"r") as f_read:
			data = json.load(f_read)
			
		if data is None:
			return None
	
		return data
	
	def prepare_ab(self):
		if (plc01['S16'] is True) and (self.ab_state is 0):
			if((plc01['S52'] is True) or (plc01['S53'] is True)):
				param = self.jsonReader()
				self.queue.append(['t1',param['table_1_info']['filename']])
				self.ab_state = 1		 
	
	def prepare_cd(self):
		if (plc01['S17'] is True) and (self.cd_state is 0):
			if((plc01['S54'] is True) or (plc01['S55'] is True)):
				param = self.jsonReader()
				self.queue.append(['t2',param['table_2_info']['filename']])
				self.cd_state = 1		 
		
	def double_table(self, runFlag):
		#SCAN TABLE 1
		if (plc01['B31'] is True):
			self.prepare_ab()
		#SCAN TABLE 2	
		if (plc01['B32'] is True):
			self.prepare_cd()
		

		if len(self.queue) != 0 and runFlag is False and self.currJob == 0:
			prog = self.queue[0]
			print("load Program :")
			print(prog[1])
			print("Table :")
			print(prog[0])

			self.c.program_open(prog[1])
			self.c.reset_interpreter()
			
			if prog[0] == "t1":
				mdi_str = "G10 L2 P1 X" + str(self.datum_x1) + " Y" + str(self.datum_y1)
				print(mdi_str)
				self.c.mdi(mdi_str)
				self.c.wait_complete()
				self.c.program_open(prog[1])
				self.c.reset_interpreter()
				self.c.mode(linuxcnc.MODE_AUTO)
				self.c.wait_complete()
				self.c.auto(linuxcnc.AUTO_RUN,0)
				self.ab_state=2
				self.currJob=1
			if prog[0] == "t2":
				mdi_str = "G10 L2 P1 X" + str(self.datum_x2) + " Y" + str(self.datum_y2)
				print(mdi_str)
				self.c.mdi(mdi_str)
				self.c.mode(linuxcnc.MODE_AUTO)
				self.c.program_open(prog[1])
				self.c.reset_interpreter()
				self.c.auto(linuxcnc.AUTO_RUN,0)
				self.cd_state=2 
				self.currJob=2				
			self.queue.remove(prog)
			return True,self.currJob 

		if self.lastRun is True and runFlag is False:
			if self.ab_state==2 and self.currJob==1:
				self.ab_state=0
				self.currJob==0
			if self.cd_state==2 and self.currJob==2:
				self.ab_state=0
				self.currJob==0

		self.lastRun = runFlag
		return False,self.currJob 
		
							


def syncPlc():
	#=========================READ BIT===============================
	result= client.read_discrete_inputs(START_ADDR,S_CNT,unit= UNIT_ADDR)
	#print(result.bits)
#	if hasattr(result, 'bits'):
#		print ("connection err")
#		return -1
	for x in range(0, S_CNT):
		plc01['S' + str(x)] = result.bits[x]
	
	#=========================WRITE BIT===============================
	pinout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for x in range(0, B1_CNT):
		pinout[x] = plc01['B' + str(B1_OFFS + x)]
	client.write_coils(START_ADDR + B1_OFFS,pinout,unit=UNIT_ADDR)
	pinout = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	for x in range(0, B2_CNT):
		pinout[x] = plc01['B' + str(B2_OFFS + x)]
	client.write_coils(START_ADDR + B2_OFFS,pinout,unit=UNIT_ADDR)
	
	#====================READ HOLDING REGS================
	regs = client.read_holding_registers(4296, 2, unit=UNIT_ADDR)
#	if hasattr(regs, 'registers'):
#		print ("connection err")
#		return -1

	plc01['E200F'] = float(regs.registers[0])
	plc01['E201F'] = float(regs.registers[1])
	#====================WRITE HOLDING REGS===============
	client.write_register(4297, int(plc01['D201F']), unit=UNIT_ADDR)
	return 0

def alarm_event():
	plc01['E01'] = plc01['S1']

if __name__ == "__main__":
	tb = table()
	while True:
		try:
			syncPlc()
			alarm_event()
			#cstart,curr_table = tb.double_table(plc01['program-is-run'])	
						
		except KeyboardInterrupt:
			print("Connection was closed")
			client.close()
