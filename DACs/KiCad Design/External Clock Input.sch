EESchema Schematic File Version 2
LIBS:Schematic-rescue
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:DACLib
LIBS:Schematic-cache
EELAYER 25 0
EELAYER END
$Descr USLegal 14000 8500
encoding utf-8
Sheet 3 4
Title "External Clock Input"
Date "2017-03-19"
Rev "000"
Comp "Ye Group"
Comment1 "Designed By: Jacob Scott"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L BNC P11
U 1 1 58D06166
P 1100 2200
F 0 "P11" H 1110 2320 50  0000 C CNN
F 1 "Ext. Clock IN" V 1200 2100 50  0000 C CNN
F 2 "Connectors:SMA_THT_Jack_Straight" H 1100 2200 50  0001 C CNN
F 3 "" H 1100 2200 50  0000 C CNN
	1    1100 2200
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR0110
U 1 1 58D061C7
P 1100 2450
F 0 "#PWR0110" H 1100 2200 50  0001 C CNN
F 1 "GNDD" H 1100 2300 50  0000 C CNN
F 2 "" H 1100 2450 50  0000 C CNN
F 3 "" H 1100 2450 50  0000 C CNN
	1    1100 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1100 2400 1100 2450
$Comp
L LTC6957-3 U23
U 1 1 58D215C1
P 2200 1300
F 0 "U23" H 1850 1500 60  0000 C CNN
F 1 "LTC6957-3" H 2800 1500 60  0000 C CNN
F 2 "KiCad_DAC_Specific:LTC6957HMS-3" H 2200 1300 60  0001 C CNN
F 3 "" H 2200 1300 60  0001 C CNN
	1    2200 1300
	1    0    0    -1  
$EndComp
$Comp
L R_Small R8
U 1 1 58D217E8
P 1100 1950
F 0 "R8" H 1130 1970 50  0000 L CNN
F 1 "50" H 1130 1910 50  0000 L CNN
F 2 "Resistors_SMD:R_0805_HandSoldering" H 1100 1950 50  0001 C CNN
F 3 "" H 1100 1950 50  0000 C CNN
	1    1100 1950
	0    -1   -1   0   
$EndComp
$Comp
L C_Small C86
U 1 1 58D21855
P 1550 1800
F 0 "C86" H 1560 1870 50  0000 L CNN
F 1 "10nF" H 1560 1720 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1550 1800 50  0001 C CNN
F 3 "" H 1550 1800 50  0000 C CNN
	1    1550 1800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1600 1650 1550 1650
Wire Wire Line
	1550 1650 1550 1700
Wire Wire Line
	1200 1950 1550 1950
Wire Wire Line
	1550 1900 1550 2000
Connection ~ 1550 1950
$Comp
L GNDD #PWR0111
U 1 1 58D218A7
P 1550 2000
F 0 "#PWR0111" H 1550 1750 50  0001 C CNN
F 1 "GNDD" H 1550 1850 50  0000 C CNN
F 2 "" H 1550 2000 50  0000 C CNN
F 3 "" H 1550 2000 50  0000 C CNN
	1    1550 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	1500 850  1500 1350
$Comp
L +3.3V #PWR0112
U 1 1 58D2562A
P 1500 850
F 0 "#PWR0112" H 1500 700 50  0001 C CNN
F 1 "+3.3V" H 1500 990 50  0000 C CNN
F 2 "" H 1500 850 50  0000 C CNN
F 3 "" H 1500 850 50  0000 C CNN
	1    1500 850 
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR0113
U 1 1 58D258C2
P 1150 1300
F 0 "#PWR0113" H 1150 1050 50  0001 C CNN
F 1 "GNDD" H 1150 1150 50  0000 C CNN
F 2 "" H 1150 1300 50  0000 C CNN
F 3 "" H 1150 1300 50  0000 C CNN
	1    1150 1300
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR0114
U 1 1 58D25F4D
P 2200 2000
F 0 "#PWR0114" H 2200 1750 50  0001 C CNN
F 1 "GNDD" H 2200 1850 50  0000 C CNN
F 2 "" H 2200 2000 50  0000 C CNN
F 3 "" H 2200 2000 50  0000 C CNN
	1    2200 2000
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR0115
U 1 1 58D25F69
P 3150 2000
F 0 "#PWR0115" H 3150 1750 50  0001 C CNN
F 1 "GNDD" H 3150 1850 50  0000 C CNN
F 2 "" H 3150 2000 50  0000 C CNN
F 3 "" H 3150 2000 50  0000 C CNN
	1    3150 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 1700 3150 1700
Wire Wire Line
	3150 1700 3150 2000
Wire Wire Line
	800  2200 950  2200
Wire Wire Line
	800  1850 800  2200
Wire Wire Line
	800  1950 1000 1950
Connection ~ 800  1950
$Comp
L C_Small C85
U 1 1 58D267C3
P 800 1750
F 0 "C85" H 810 1820 50  0000 L CNN
F 1 "10nF" H 810 1670 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 800 1750 50  0001 C CNN
F 3 "" H 800 1750 50  0000 C CNN
	1    800  1750
	1    0    0    -1  
$EndComp
$Comp
L D_Small D1
U 1 1 58D268D5
P 1350 1100
F 0 "D1" H 1300 1180 50  0000 L CNN
F 1 "1n4148" H 1200 1025 50  0000 L CNN
F 2 "Diodes_SMD:D_0805" V 1350 1100 50  0001 C CNN
F 3 "" V 1350 1100 50  0000 C CNN
	1    1350 1100
	0    1    1    0   
$EndComp
$Comp
L D_Small D2
U 1 1 58D26922
P 1350 1800
F 0 "D2" H 1300 1880 50  0000 L CNN
F 1 "1n4148" H 1200 1720 50  0000 L CNN
F 2 "Diodes_SMD:D_0805" V 1350 1800 50  0001 C CNN
F 3 "" V 1350 1800 50  0000 C CNN
	1    1350 1800
	0    1    1    0   
$EndComp
Wire Wire Line
	1150 1250 1600 1250
Wire Wire Line
	800  1550 1600 1550
Wire Wire Line
	1350 1200 1350 1700
Wire Wire Line
	800  1550 800  1650
Connection ~ 1350 1550
Wire Wire Line
	1350 1900 1350 1950
Connection ~ 1350 1950
Wire Wire Line
	1150 1200 1150 1300
Wire Wire Line
	2200 900  2200 950 
Wire Wire Line
	1150 900  2350 900 
Connection ~ 1500 900 
Wire Wire Line
	1500 1350 1600 1350
Wire Wire Line
	1350 900  1350 1000
$Comp
L GNDD #PWR0116
U 1 1 58D2A27F
P 2650 850
F 0 "#PWR0116" H 2650 600 50  0001 C CNN
F 1 "GNDD" H 2650 700 50  0000 C CNN
F 2 "" H 2650 850 50  0000 C CNN
F 3 "" H 2650 850 50  0000 C CNN
	1    2650 850 
	1    0    0    -1  
$EndComp
Wire Wire Line
	2500 950  2500 800 
Wire Wire Line
	2500 800  2650 800 
Wire Wire Line
	2650 800  2650 850 
Wire Wire Line
	2500 2000 2500 2050
Wire Wire Line
	2500 2050 2650 2050
Wire Wire Line
	2650 2050 2650 2000
$Comp
L +3.3V #PWR0117
U 1 1 58D2A4D7
P 2650 2000
F 0 "#PWR0117" H 2650 1850 50  0001 C CNN
F 1 "+3.3V" H 2650 2140 50  0000 C CNN
F 2 "" H 2650 2000 50  0000 C CNN
F 3 "" H 2650 2000 50  0000 C CNN
	1    2650 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 1350 3450 1350
$Comp
L Jumper JP1
U 1 1 58D2C41C
P 3750 1350
F 0 "JP1" H 3750 1500 50  0000 C CNN
F 1 "Jumper" H 3750 1270 50  0000 C CNN
F 2 "Connectors:PINHEAD1-2" H 3750 1350 50  0001 C CNN
F 3 "" H 3750 1350 50  0000 C CNN
	1    3750 1350
	1    0    0    -1  
$EndComp
Wire Wire Line
	4050 1350 4250 1350
Wire Wire Line
	1150 900  1150 1000
Connection ~ 1350 900 
Connection ~ 1150 1250
$Comp
L C_Small C84
U 1 1 58D2CC9A
P 1150 1100
F 0 "C84" H 1160 1170 50  0000 L CNN
F 1 "0.1uF" H 1160 1020 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1150 1100 50  0001 C CNN
F 3 "" H 1150 1100 50  0000 C CNN
	1    1150 1100
	-1   0    0    1   
$EndComp
Text HLabel 4250 1350 2    60   Output ~ 0
CLK
NoConn ~ 3100 1550
Wire Wire Line
	2350 900  2350 950 
Connection ~ 2200 900 
$EndSCHEMATC
