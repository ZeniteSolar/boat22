EESchema Schematic File Version 4
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 37
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:Battery_Cell BT?
U 1 1 5CCDA0F1
P 2900 2050
AR Path="/5CCDA0F1" Ref="BT?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA0F1" Ref="BT?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA0F1" Ref="BT2401"  Part="1" 
AR Path="/5DC4E327/5CCDA0F1" Ref="BT2501"  Part="1" 
F 0 "BT2501" H 3050 2150 50  0000 L CNN
F 1 "D35" H 3050 2100 50  0000 L CNN
F 2 "" V 2900 2110 50  0001 C CNN
F 3 "~" V 2900 2110 50  0001 C CNN
	1    2900 2050
	1    0    0    -1  
$EndComp
$Comp
L Device:Battery_Cell BT?
U 1 1 5CCDA0F7
P 2900 2550
AR Path="/5CCDA0F7" Ref="BT?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA0F7" Ref="BT?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA0F7" Ref="BT2402"  Part="1" 
AR Path="/5DC4E327/5CCDA0F7" Ref="BT2502"  Part="1" 
F 0 "BT2502" H 3050 2650 50  0000 L CNN
F 1 "D35" H 3050 2600 50  0000 L CNN
F 2 "" V 2900 2610 50  0001 C CNN
F 3 "~" V 2900 2610 50  0001 C CNN
	1    2900 2550
	1    0    0    -1  
$EndComp
$Comp
L Device:Battery_Cell BT?
U 1 1 5CCDA0FD
P 2900 3050
AR Path="/5CCDA0FD" Ref="BT?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA0FD" Ref="BT?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA0FD" Ref="BT2403"  Part="1" 
AR Path="/5DC4E327/5CCDA0FD" Ref="BT2503"  Part="1" 
F 0 "BT2503" H 3050 3150 50  0000 L CNN
F 1 "D35" H 3050 3100 50  0000 L CNN
F 2 "" V 2900 3110 50  0001 C CNN
F 3 "~" V 2900 3110 50  0001 C CNN
	1    2900 3050
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 3150 2900 3300
Wire Wire Line
	2900 1850 2900 1700
$Comp
L Device:Fuse F?
U 1 1 5CCDA105
P 3350 3300
AR Path="/5CCDA105" Ref="F?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA105" Ref="F?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA105" Ref="F2401"  Part="1" 
AR Path="/5DC4E327/5CCDA105" Ref="F2501"  Part="1" 
F 0 "F2501" V 3100 3300 50  0000 C CNN
F 1 "250A" V 3200 3300 50  0000 C CNN
F 2 "" V 3280 3300 50  0001 C CNN
F 3 "~" H 3350 3300 50  0001 C CNN
	1    3350 3300
	0    1    1    0   
$EndComp
Wire Wire Line
	2900 3300 3200 3300
$Comp
L Connector_Generic:Conn_01x01 J?
U 1 1 5CCDA10E
P 4100 1700
AR Path="/5CCDA10E" Ref="J?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA10E" Ref="J?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA10E" Ref="J2401"  Part="1" 
AR Path="/5DC4E327/5CCDA10E" Ref="J2501"  Part="1" 
F 0 "J2501" H 4200 1750 50  0000 L CNN
F 1 "Conn_01x01" H 4200 1650 50  0000 L CNN
F 2 "" H 4100 1700 50  0001 C CNN
F 3 "~" H 4100 1700 50  0001 C CNN
	1    4100 1700
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x01 J?
U 1 1 5CCDA114
P 4100 3300
AR Path="/5CCDA114" Ref="J?"  Part="1" 
AR Path="/5CCD4ED0/5CCDA114" Ref="J?"  Part="1" 
AR Path="/5DC3DF9F/5CCDA114" Ref="J2402"  Part="1" 
AR Path="/5DC4E327/5CCDA114" Ref="J2502"  Part="1" 
F 0 "J2502" H 4200 3350 50  0000 L CNN
F 1 "Conn_01x01" H 4200 3250 50  0000 L CNN
F 2 "" H 4100 3300 50  0001 C CNN
F 3 "~" H 4100 3300 50  0001 C CNN
	1    4100 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	2900 2150 2900 2350
Wire Wire Line
	2900 2650 2900 2850
Text HLabel 3850 1500 1    50   Input ~ 0
Bat+
Text HLabel 3850 3100 1    50   Input ~ 0
Bat-
Wire Wire Line
	3850 1500 3850 1700
Connection ~ 3850 1700
Wire Wire Line
	3850 1700 3900 1700
Wire Wire Line
	3850 3100 3850 3300
Connection ~ 3850 3300
Wire Wire Line
	3850 3300 3900 3300
Wire Wire Line
	3500 3300 3850 3300
Wire Wire Line
	2900 1700 3150 1700
$Comp
L Switch:SW_SPST SW?
U 1 1 5CCDFB7B
P 3350 1700
AR Path="/5CCD4ED0/5CCDFB7B" Ref="SW?"  Part="1" 
AR Path="/5DC3DF9F/5CCDFB7B" Ref="SW2401"  Part="1" 
AR Path="/5DC4E327/5CCDFB7B" Ref="SW2501"  Part="1" 
F 0 "SW2501" H 3350 1950 50  0000 C CNN
F 1 "Battery Switch" H 3350 1850 50  0000 C CNN
F 2 "" H 3350 1700 50  0001 C CNN
F 3 "~" H 3350 1700 50  0001 C CNN
	1    3350 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3550 1700 3850 1700
Text HLabel 1950 3900 0    50   Input ~ 0
Bat_P_Unfused_Out
Text HLabel 1950 4000 0    50   Input ~ 0
Bat_N_UNfused_Out
$EndSCHEMATC
