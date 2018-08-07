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
Sheet 4 4
Title "8, 18Bit-DAC, FPGA Controlled"
Date "2017-03-12"
Rev "001"
Comp "Ye Group"
Comment1 "Desined By: Jacob Scott"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L CONN_01X03 P9
U 1 1 58C3543C
P 1000 1750
F 0 "P9" H 1000 1950 50  0000 C CNN
F 1 "CONN_01X03" V 1100 1750 50  0000 C CNN
F 2 "Connectors:PINHEAD1-3" H 1000 1750 50  0001 C CNN
F 3 "" H 1000 1750 50  0000 C CNN
	1    1000 1750
	-1   0    0    -1  
$EndComp
$Comp
L GNDA #PWR0118
U 1 1 58C3555F
P 3250 1900
F 0 "#PWR0118" H 3250 1650 50  0001 C CNN
F 1 "GNDA" H 3250 1750 50  0000 C CNN
F 2 "" H 3250 1900 50  0000 C CNN
F 3 "" H 3250 1900 50  0000 C CNN
	1    3250 1900
	1    0    0    -1  
$EndComp
$Comp
L C_Small C78
U 1 1 58C3557E
P 1400 1450
F 0 "C78" H 1410 1520 50  0000 L CNN
F 1 "0.1uF" H 1410 1370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1400 1450 50  0001 C CNN
F 3 "" H 1400 1450 50  0000 C CNN
	1    1400 1450
	1    0    0    -1  
$EndComp
$Comp
L L_Core_Ferrite L1
U 1 1 58C35630
P 1650 1250
F 0 "L1" V 1600 1250 50  0000 C CNN
F 1 "1k ohm" V 1760 1250 50  0000 C CNN
F 2 "Capacitors_SMD:C_1812_HandSoldering" H 1650 1250 50  0001 C CNN
F 3 "" H 1650 1250 50  0000 C CNN
	1    1650 1250
	0    -1   -1   0   
$EndComp
$Comp
L +15V #PWR0119
U 1 1 58C356EA
P 2000 1200
F 0 "#PWR0119" H 2000 1050 50  0001 C CNN
F 1 "+15V" H 2000 1340 50  0000 C CNN
F 2 "" H 2000 1200 50  0000 C CNN
F 3 "" H 2000 1200 50  0000 C CNN
	1    2000 1200
	1    0    0    -1  
$EndComp
$Comp
L C_Small C80
U 1 1 58C3576B
P 2000 1450
F 0 "C80" H 2010 1520 50  0000 L CNN
F 1 "0.01uF" H 2010 1370 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2000 1450 50  0001 C CNN
F 3 "" H 2000 1450 50  0000 C CNN
	1    2000 1450
	1    0    0    -1  
$EndComp
$Comp
L +3.3V #PWR0120
U 1 1 58C35819
P 2550 950
F 0 "#PWR0120" H 2550 800 50  0001 C CNN
F 1 "+3.3V" H 2550 1090 50  0000 C CNN
F 2 "" H 2550 950 50  0000 C CNN
F 3 "" H 2550 950 50  0000 C CNN
	1    2550 950 
	1    0    0    -1  
$EndComp
$Comp
L C_Small C79
U 1 1 58C3685A
P 1400 2050
F 0 "C79" H 1410 2120 50  0000 L CNN
F 1 "0.1uF" H 1410 1970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 1400 2050 50  0001 C CNN
F 3 "" H 1400 2050 50  0000 C CNN
	1    1400 2050
	1    0    0    1   
$EndComp
$Comp
L L_Core_Ferrite L2
U 1 1 58C36864
P 1650 2250
F 0 "L2" V 1600 2250 50  0000 C CNN
F 1 "1k ohm" V 1760 2250 50  0000 C CNN
F 2 "Capacitors_SMD:C_1812_HandSoldering" H 1650 2250 50  0001 C CNN
F 3 "" H 1650 2250 50  0000 C CNN
	1    1650 2250
	0    -1   1    0   
$EndComp
$Comp
L -15V #PWR142
U 1 1 58C3698F
P 2000 2300
F 0 "#PWR142" H 2000 2400 50  0001 C CNN
F 1 "-15V" H 2000 2450 50  0000 C CNN
F 2 "" H 2000 2300 50  0000 C CNN
F 3 "" H 2000 2300 50  0000 C CNN
	1    2000 2300
	-1   0    0    1   
$EndComp
$Comp
L C_Small C81
U 1 1 58C36872
P 2000 2050
F 0 "C81" H 2010 2120 50  0000 L CNN
F 1 "0.01uF" H 2010 1970 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805_HandSoldering" H 2000 2050 50  0001 C CNN
F 3 "" H 2000 2050 50  0000 C CNN
	1    2000 2050
	1    0    0    1   
$EndComp
Wire Wire Line
	1200 1750 3250 1750
Wire Wire Line
	3250 1750 3250 1900
Wire Wire Line
	1250 1650 1200 1650
Wire Wire Line
	1250 1250 1250 1650
Wire Wire Line
	1250 1250 1500 1250
Wire Wire Line
	1800 1250 2400 1250
Connection ~ 2000 1250
Connection ~ 2000 1750
Wire Wire Line
	2000 1550 2000 1950
Wire Wire Line
	2000 1200 2000 1350
Wire Wire Line
	1200 1850 1250 1850
Wire Wire Line
	1250 2250 1500 2250
Connection ~ 2000 2250
Wire Wire Line
	2000 2300 2000 2150
Wire Wire Line
	2000 2250 1800 2250
Wire Wire Line
	1400 1250 1400 1350
Connection ~ 1400 1250
Wire Wire Line
	1400 1550 1400 1950
Connection ~ 1400 1750
Wire Wire Line
	1400 2150 1400 2250
Connection ~ 1400 2250
Wire Wire Line
	1250 1850 1250 2250
$Comp
L LT1963A U22
U 1 1 58C3FE43
P 3100 1250
F 0 "U22" H 3100 1600 60  0000 C CNN
F 1 "LT1963A" H 3100 1700 60  0000 C CNN
F 2 "TO_SOT_Packages_THT:TO-220-5_Pentawatt_Multiwatt-5_Vertical_StaggeredType1" H 3100 1250 60  0001 C CNN
F 3 "" H 3100 1250 60  0001 C CNN
	1    3100 1250
	0    1    1    0   
$EndComp
Wire Wire Line
	2850 1150 2850 1050
Wire Wire Line
	2850 1050 2900 1050
Connection ~ 2850 1150
Wire Wire Line
	2550 950  2550 1450
Wire Wire Line
	2550 1350 2900 1350
Wire Wire Line
	2550 1450 2900 1450
Connection ~ 2550 1350
Wire Wire Line
	2900 1250 2700 1250
Wire Wire Line
	2700 1250 2700 1750
Connection ~ 2700 1750
$Comp
L CP1_Small C83
U 1 1 58C401D8
P 2850 1600
F 0 "C83" H 2860 1670 50  0000 L CNN
F 1 "10uF" H 2860 1520 50  0000 L CNN
F 2 "Capacitors_Tantalum_SMD:CP_Tantalum_Case-A_EIA-3216-18_Hand" H 2850 1600 50  0001 C CNN
F 3 "" H 2850 1600 50  0000 C CNN
	1    2850 1600
	1    0    0    -1  
$EndComp
$Comp
L CP1_Small C82
U 1 1 58C4021C
P 2400 1600
F 0 "C82" H 2410 1670 50  0000 L CNN
F 1 "10uF" H 2410 1520 50  0000 L CNN
F 2 "Capacitors_Tantalum_SMD:CP_Tantalum_Case-A_EIA-3216-18_Hand" H 2400 1600 50  0001 C CNN
F 3 "" H 2400 1600 50  0000 C CNN
	1    2400 1600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 1150 2400 1150
Connection ~ 2400 1250
Wire Wire Line
	2850 1500 2850 1450
Connection ~ 2850 1450
Wire Wire Line
	2850 1700 2850 1750
Connection ~ 2850 1750
Connection ~ 2400 1750
Wire Wire Line
	2400 1150 2400 1500
Wire Wire Line
	2400 1750 2400 1700
$EndSCHEMATC
