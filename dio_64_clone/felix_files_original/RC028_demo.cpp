// RC028_demo.cpp : Defines the entry point for the console application.਍ഀ
//਍ഀ
਍ഀ
#include "stdafx.h"਍ഀ
#include <string>਍ഀ
#include <iostream>਍ഀ
#include <stdio.h>਍ഀ
#include "RC028.h"਍ഀ
#include <windows.h>਍ഀ
#include <chrono>਍ഀ
਍ഀ
using namespace std;਍ഀ
using namespace std::chrono;਍ഀ
਍ഀ
RC028 pattern1(RC028 DIO)਍ഀ
{਍ഀ
	//generate 100, 200, 300, 400, 500 ns pulses on P1.0 and P2.0਍ഀ
	DIO.setPoint(0, 0, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(1, 10, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(2, 20, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(3, 40, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(4, 50, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(5, 80, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(6, 90, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(7, 130, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(8, 140, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(9, 190, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(10, 250, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(11, 0, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	return DIO;਍ഀ
}਍ഀ
਍ഀ
RC028 pattern2(RC028 DIO)਍ഀ
{਍ഀ
	////1s test pattern on P1.0 and P2.0਍ഀ
	DIO.setPoint(0, 0, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(1, 100000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(2, 200000000, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(3, 300000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(4, 400000000, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(5, 500000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(6, 600000000, 1, 1, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(7, 700000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(8, 0, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	return DIO;਍ഀ
}਍ഀ
਍ഀ
RC028 pattern_all(RC028 DIO)਍ഀ
{਍ഀ
	////1s test pattern on P1.0 and P2.0਍ഀ
	DIO.setPoint(0, 0, 255, 255, 255, 255, 255, 255, 255, 255);਍ഀ
	DIO.setPoint(1, 100000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(2, 200000000, 255, 255, 255, 255, 255, 255, 255, 255);਍ഀ
	DIO.setPoint(3, 300000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(4, 400000000, 255, 255, 255, 255, 255, 255, 255, 255);਍ഀ
	DIO.setPoint(5, 500000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(6, 600000000, 255, 255, 255, 255, 255, 255, 255, 255);਍ഀ
	DIO.setPoint(7, 700000000, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	DIO.setPoint(8, 800000000, 255, 255, 255, 255, 255, 255, 255, 255);਍ഀ
	DIO.setPoint(9, 0, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	return DIO;਍ഀ
}਍ഀ
਍ഀ
RC028 patternlong(RC028 DIO)਍ഀ
{਍ഀ
	//full array਍ഀ
	unsigned int end = 2047;਍ഀ
	int time = 0;਍ഀ
	int timeinc = 10;਍ഀ
	int x = 1;਍ഀ
	for (unsigned int i=0;i < end;i++)਍ഀ
	{਍ഀ
		DIO.setPoint(i, time, x, x, 0, 0, 0, 0, 0, 0);਍ഀ
		time += timeinc;਍ഀ
		if (x == 1)਍ഀ
		{਍ഀ
			x = 0;਍ഀ
		}਍ഀ
		else਍ഀ
		{਍ഀ
			x = 1;਍ഀ
		}਍ഀ
	}਍ഀ
	DIO.setPoint(end, 0, 0, 0, 0, 0, 0, 0, 0, 0);਍ഀ
	return DIO;਍ഀ
}਍ഀ
਍ഀ
int main()਍ഀ
{	਍ഀ
	RC028 DIO;਍ഀ
਍ഀ
	DIO = pattern_all(DIO);਍ഀ
਍ഀ
	DIO.connectasync("FT2E722BB"); //This is the serial number of the FTDI chip "FT2E722B" - another B is added to select channel B਍ഀ
਍ഀ
	high_resolution_clock::time_point t1 = high_resolution_clock::now();਍ഀ
	DIO.write();਍ഀ
	high_resolution_clock::time_point t2 = high_resolution_clock::now();਍ഀ
਍ഀ
	auto duration = duration_cast<microseconds>(t2 - t1).count();਍ഀ
਍ഀ
	cout << "Write function took " << duration << " microseconds" << endl;਍ഀ
਍ഀ
	਍ഀ
	DIO.trigger();਍ഀ
	DIO.disconnect();਍ഀ
਍ഀ
	cout << "Finished..." << endl;਍ഀ
਍ഀ
    return 0;਍ഀ
}਍ഀ
਍ഀ
