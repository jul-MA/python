# Raspberry's monitoring information on a 16 x 2 LCD screen
# Display the disk usage, RAM usage, CPU usage and temperature
# Bar charts and KPI's to visualize the information

# import lib
import I2C_LCD_driver
from time import sleep, strftime, time
from gpiozero import CPUTemperature, DiskUsage
import Adafruit_DHT
import psutil
import subprocess
import math


# init variables
mylcd = I2C_LCD_driver.lcd()
cpu = CPUTemperature(min_temp=20, max_temp=100)
cpuTempCurr = 0
cpuUsageCurr = 0
disk = 0
ram = 0
i = 0
symbol = ''
lstUsage = []
displayDuration = 2
symbolsTable = [   
		# arrow up
		[   0x04, 0x0E, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00],
		# arrow down
		[   0x1F, 0x0E, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00],
		# square
		[   0x0E, 0x0E, 0x0E, 0x00, 0x00, 0x00, 0x00, 0x00],
]


# display a small barchart with goal / max value
def displaySmallBar(row, value):
	for i in range (0, 6):
		if i * 17 > value:
			symbol = '.'
		else:
			symbol = chr(255)
		
		mylcd.lcd_display_string(symbol, row, i + 9)		

		
# display the screen for a number of defined seconds
def screenDisplay():
	sleep(displayDuration)
	mylcd.lcd_clear()

	
# format and display the disk usage value on the first row	
def showDiskUsageMini(disk):
	mylcd.lcd_display_string('DSK: {:.0f}%'.format(disk), 1, 0)
	mylcd.lcd_display_string('[', 1, 8)
	mylcd.lcd_display_string(']', 1, 15)
	
	displaySmallBar(1, disk)
	
	screenDisplay()

	
# format and display the RAM usage value on the second row	
def showRAMUsageMini(ram):
	mylcd.lcd_display_string('RAM: {:.0f}%'.format(ram), 2, 0)
	mylcd.lcd_display_string('[', 2, 8)
	mylcd.lcd_display_string(']', 2, 15)
	
	displaySmallBar(2, ram)

	
# from https://github.com/donthideyourfeelings/rpimon
def getCommandOutput(cmd):
    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    return stdout.decode('utf-8')

	
# from https://github.com/donthideyourfeelings/rpimon	
def getUsernameHostname():
    cmd = "whoami"
    cmd2 = "hostname"

    username = getCommandOutput(cmd).replace("\n", "")
    hostname = getCommandOutput(cmd2).replace("\n", "")
	
    return username + "@" + hostname

	
# get the kpi variation symbol based on the current value and the previous value. Symbols recorded into the array symbolsTable	
def getSymbolIndex(currVal, prevVal): 
	if currVal > prevVal:
		symbolIndex = 0
	elif currVal < prevVal:
		symbolIndex = 1
	else:
		symbolIndex = 2
	
	return symbolIndex

	
# represent the last 16 CPU usage values as a bar chart	
def showCPUChart(cpuUsageCurr):
	bars = [
		# 1 bar
		[ 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1F],
		# 2 bars
		[ 0x00,0x00,0x00,0x00,0x00,0x00,0x1F,0x1F],
		# 3 bars
		[ 0x00,0x00,0x00,0x00,0x00,0x1F,0x1F,0x1F],
		# 4 bars
		[ 0x00,0x00,0x00,0x00,0x1F,0x1F,0x1F,0x1F],
		# 5 bars
		[ 0x00,0x00,0x00,0x1F,0x1F,0x1F,0x1F,0x1F],
		# 6 bars
		[ 0x00,0x00,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F],
		# 7 bars
		[ 0x00,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F],
		# 8 bars
		[ 0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F,0x1F],
	]
	
	mylcd.lcd_load_custom_chars(bars)
	mylcd.lcd_display_string("CPU Usage: ", 1,0)
	mylcd.lcd_display_string("{:.1f}%".format(cpuUsageCurr), 1,11)
	
	for j in range (0, len(lstUsage)):
		val = int(math.trunc(lstUsage[j] / 10))
		mylcd.lcd_display_string(chr(val), 2, j)
		
	screenDisplay()
		

# display information related to the device 
def showMainInfo():
	mylcd.lcd_display_string(getUsernameHostname(),1, 2)
	mylcd.lcd_display_string(strftime("%d/%m %H:%M"),2, 2)
	screenDisplay()
	

# format and display the CPU usage and temperature values plus a symbol based on the variation between the current and the previous values
def showCPUInfo(cpuTempCurr, cpuTempPrev, cpuUsageCurr, cpuUsagePrev):
	mylcd.lcd_load_custom_chars(symbolsTable)
	mylcd.lcd_display_string("CPU",1, 6)
	mylcd.lcd_display_string("{:.1f}%".format(cpuUsageCurr),2, 0 if cpuUsageCurr >= 10 else 1)
	mylcd.lcd_display_string("{:04.1f}C".format(cpuTempCurr),2, 9)
	mylcd.lcd_display_string(chr(getSymbolIndex(cpuUsageCurr, cpuUsagePrev)), 2, 5)
	mylcd.lcd_display_string(chr(getSymbolIndex(cpuTempCurr, cpuTempPrev)), 2, 14)
	screenDisplay()	

	
# main
mylcd.lcd_clear()
if __name__ == '__main__':
    try:
        while True:
			print("-----")
			
			# get data
			cpuTempPrev = cpuTempCurr
			cpuTempCurr = cpu.temperature
			cpuUsagePrev = cpuUsageCurr
			cpuUsageCurr = psutil.cpu_percent()
			disk = DiskUsage()
			ram = psutil.virtual_memory()[2]
			
			# data stored to generate the CPU's barchart
			lstUsage.append(cpuUsageCurr)

			# display the screens
			showMainInfo()
			showCPUInfo(cpuTempCurr, cpuTempPrev, cpuUsageCurr, cpuUsagePrev)
			showCPUChart(cpuUsageCurr)
			showRAMUsageMini(ram)	
			showDiskUsageMini(disk.usage)	
			
			# loop / CPU's barchart reset everything 16 steps (LCD screen size)
			if i > 15:
				i = 0
				del lstUsage [:]
				mylcd.lcd_clear()
			else:
				i = i + 1
			
		
    except KeyboardInterrupt:
        print("Off")
        mylcd.lcd_clear()
        mylcd.backlight(0)