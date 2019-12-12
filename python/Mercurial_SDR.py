#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
import subprocess
import shlex
import serial
#from math import pi, sin
#import argparse

from gnuradio import gr

class Mercurial_SDR(gr.sync_block):
    """
    docstring for block Mercurial_SDR
    """
    def __init__(self, modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key):
        gr.sync_block.__init__(self,
            name="Mercurial_SDR",
            in_sig=[numpy.float32],
            out_sig="")
#            out_sig=[numpy.float32])

        # subprocess.call('icepll')

        #ser = serial.Serial('/dev/pts/13')  # open serial port
        #print(ser.name)         # check which port was really used
        #ser.write(b'hello')     # write a string
        #ser.close()             # close port
        #ser.baudrate = 9600
        #print(ser.baudrate)
        # subprocess.call(['echo', 'sin invocar shell\n'])
        #self.modulation = modulation_key
        #print(self.modulation)
        #print("MOD")

        syntethize = True

        modulation  = modulation_key;
        modulation_psk  = psk_key;
        parameter01 = 1;
        parameter02 = 255;
        parameter03 = 8;
        parameter04 = 4;

        try:
            f = open("check_syn","r")
            rl = f.readline()
            current = "{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key)
            
            if (rl == current):
                syntethize = False
            else:
              f.close()
              f = open("check_syn","w+")
              f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key))

                

        except:
            print("Debug EXCEPT")

            f = open("check_syn","w+")
            f.write("{}{}{}{}{}{}{}{}".format(modulation_key,psk_key,fc_key,fs_key,clk_key,pammethod_key,pamtype_key,duty_key))
            f.close()

     #  HDL code
         #.PARAMETER01    (`PARAMETER01),
         #.PARAMETER02    (`PARAMETER02),
         #.PARAMETER03    (`PARAMETER03),
         #.PARAMETER04    (`PARAMETER04)

         #/*  AM_CLKS_PER_PWM_STEP    1
         # *  AM_PWM_STEP_PER_SAMPLE  255
         # *  AM_BITS_PER_SAMPLE      8
         # *  AM_REPEATED_SAMPLE      30
         # */

         #/*  AM_CLKS_PER_PWM_STEP    1
         # *  AM_PWM_STEP_PER_SAMPLE  255
         # *  AM_BITS_PER_SAMPLE      8
         # *  AM_REPEATED_SAMPLE      30
         # */

         #/*  PSK_CLKS_PER_BIT        4
         # *  PSK_BITS_PER_SYMBOL     4
         # *
         # *  PSK_REPEATED_SAMPLE     30
         # */
 
         #/*  PAM_CLKS_SAMPLING_FREQ  1200
         # *  PAM_CLKS_PER_BCLK       12
         # *  PAM_DATA_LENGHT         24
         # *  
         # */

        if(syntethize == True): 

            if(modulation == "am"):
                parameter04 = numpy.round(clk_key/fs_key);
                print("AM");
    
            elif(modulation =="ook"):
                parameter02 = 2;
                print("OOK");
    
            elif(modulation =="pam"):
                parameter02 = 0;
                parameter03 = 24;                               # bits del dac
                print("PAM");
    
            elif(psk_key =="bpsk"):
                parameter01 = clk_key;
                parameter02 = 2;
                parameter04 = numpy.round(clk_key/fs_key);
                print("BPSK");
    
    
    
            elif(psk_key =="qpsk"):
                parameter01 = clk_key;
                parameter02 = 4;
                parameter04 = numpy.round(clk_key/fs_key);
                print("QPSK");
    
            elif(psk_key =="8psk"):
                parameter01 = clk_key;
                parameter02 = 8;
                parameter04 = numpy.round(clk_key/fs_key);
                print("8PSK");
    
    
            self.modulatorParametersGenerator(parameter01, parameter02, parameter03,parameter04)
            self.programFPGA("../../syn", "all", modulation)


#        data = [6 0]#, 3, 9, 12] 

        self.tty = serial.Serial('/dev/ttyUSB1')
        


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # for i in range(45):
        b = numpy.uint8(in0*128-128)
        self.tty.write(b.tobytes())
        # print(type(in0),  " | ", in0)
        # out = output_items[0]
        # # <+signal processing here+>
        # out[:] = in0
        # tty.write(input_items)
        #return

        return len(input_items[0])


    def set_modulation(self, modulation_key):
        self.modulation = modulation_key
        print("Modulacion seleccionada:")
        print(self.modulation)

    ####
    # programFPGA
    #
    # This function runs the Makefile to make the synthesys, place and route and
    # programmation of the FPGA
    ####
    def programFPGA(self, pathMakefileHDL, target, modulator):
        subprocess.call(['make', '-C', pathMakefileHDL,'clean'])
        subprocess.call(['make', '-C', pathMakefileHDL, target, 'MOD=' + modulator])

    ####
    # modulatorParametersGenerator
    #
    # Used to write the necessary defines to build every modulator
    ####
    def modulatorParametersGenerator(self, parameter01, parameter02, parameter03,parameter04):
        # open file and write header
        f = open("../../inc/module_params.v","w+")
        f.write("`ifndef __PROJECT_CONFIG_V\n`define __PROJECT_CONFIG_V\n\n")
        f.write("`define PARAMETER01 %d\n" % parameter01)
        f.write("`define PARAMETER02 %d\n" % parameter02)
        f.write("`define PARAMETER03 %d\n" % parameter03)
        f.write("`define PARAMETER04 %d\n" % parameter04)
        f.write("\n`endif")
        f.close()



