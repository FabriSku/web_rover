import socket  ,time  , math , os,urequests   #, serial, pygame
#from pygame.locals import *
#from ntptime import settime
import ntptime
import utime
from sys import exit
#import androidhelper
import json
import ujson
import uselect as select
#from wsgiref.simple_server import make_server
#from pygame import Surface
#import time
#import wsgiref
#pygame.init()
import network , gc 
from machine import I2C, Pin
from machine import RTC
import ssd1306
import socket
import usocket
import machine

from machine import Pin, PWM ,ADC
import servo
import socket  ,time  , math , os  #, serial, pygame
#from pygame.locals import *
from sys import exit
#import androidhelper
import json
#from wsgiref.simple_server import make_server
#from pygame import Surface
#import time
#import wsgiref
#pygame.init()
import network , gc 
from machine import I2C, Pin
import ssd1306
import socket
import usocket
import machine
import  urequests

from machine import Pin, PWM ,ADC
#import servo_ori1
import servo


import usocket as socket
import uselect as select




#dati x connessione
LOCAL_ADDR = "192.168.1.32", 80
#TRACK_LOCAL_ADDR = "192.168.1.2", 5005
#



#---------------------------------------------------------------asegnazione pin
#global message,canale
#Setup PINS
#LED0 = machine.Pin(14, machine.Pin.OUT)
#LED2 = machine.Pin(27, machine.Pin.OUT)
in3= Pin(13, Pin.OUT)
in4 = Pin(27, Pin.OUT)
p25 = machine.Pin(25)



in1= Pin(12, Pin.OUT)
in2 = Pin(14, Pin.OUT)
p26 = machine.Pin(26)

in5 = Pin(5, Pin.OUT)
in18 = Pin(18 ,Pin.OUT)
p17 = machine.Pin(17)


# in4.value(1)
# p26 = machine.Pin(25)
# servo = machine.PWM((p26) ,freq=50)#,duty=40)
# servo.duty(int(300))

#---------------------variabli velita uty pwm

vel400=400
vel800=800


#------------------------------------settaggio schermo oled 128x64??
rst = Pin(16, Pin.OUT)
rst.value(1)
scl = Pin(15, Pin.OUT, Pin.PULL_UP)
sda = Pin(4, Pin.OUT, Pin.PULL_UP)
i2c = I2C(scl=scl, sda=sda, freq=450000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.ifconfig(('192.168.1.32','255.255.255.0','192.168.1.1','85.37.17.17'))#[0]
        sta_if.connect('TIM-28391995', 'casapiccia66acasapiccia66a')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    #IPaddr= sta_if.ifconfig()[0]
    oled.text(sta_if.ifconfig()[0], 10, 35)
    oled.text('La Faglia', 10, 50)
    oled.show()

do_connect()



def do_something_else():   
#The other script to be executed besides of the blocking socket
    url = "http://worldtimeapi.org/api/timezone/Europe/Rome" #http://worldtimeapi.org/timezone/Europe/Rome" # see http://worldtimeapi.org/timezones
    web_query_delay = 60000 # interval time of web JSON query
    retry_delay = 5000 # interval time of retry after a failed Web query
    rtc=RTC()
    # set timer
    update_time = utime.ticks_ms() - web_query_delay
    #settime()
    tempo=utime.localtime()
    print((str(tempo)))
    
#     oled.text(str(tempo), 10, 50)
#     oled.show()
   # while True:
        # query and get web JSON every web_query_delay ms
    if utime.ticks_ms() - update_time >= web_query_delay:
    
        # HTTP GET data
        response_tempo = urequests.get(url)
    
        if response_tempo.status_code == 200: # query success
        
            print("JSON response:\n", response_tempo.text)
            
            # parse JSON
            parsed = response_tempo.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[0:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))
            #if minute ==31:
                #Client_handler(LEDON0=6)
                #LED2.value(1)
                #print (("LED0 value="),LED0.value())
            # update internal RTC
            rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
            update_time = utime.ticks_ms()
            print("RTC updated\n")
   
        else: # query failed, retry retry_delay ms later
            update_time = utime.ticks_ms() - web_query_delay + retry_delay
        
    # generate formated date/time strings from internal RTC
    date_str = "Date: {2:02d}/{1:02d}/{0:4d}".format(*rtc.datetime())  
    time_str = "Time: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())

    # update SSD1306 OLED display
    oled.fill(0)
    oled.text("ESP32 WebClock", 0, 5)
    oled.text(date_str, 0, 25)
    oled.text(time_str, 0, 45)
    oled.show()
    
    utime.sleep(0.1)
    
#-----------------------------class motor----------
# class motor():
#      def __init__(self,Ena,In1,In2):
#         self.Ena = Ena
#         self.In1 = In1
#         self.In2 = In2
#         GPIO.setup(self.Ena,GPIO.OUT)
#         GPIO.setup(self.In1,GPIO.OUT)
#         GPIO.setup(self.In2,GPIO.OUT)
#         self.pwm = GPIO.PWM(self.Ena, 100)
#         self.pwm.start(0)
#     def moveF(self,x=100,t=0):
#         self.pwm.ChangeDutyCycle(x)
#         GPIO.output(self.In1,GPIO.HIGH)
#         GPIO.output(self.In2,GPIO.LOW)
#         sleep(t)
#     def moveB(self,x=100,t=0):
#         self.pwm.ChangeDutyCycle(x)
#         GPIO.output(self.In1,GPIO.LOW)
#         GPIO.output(self.In2,GPIO.HIGH)
#         sleep(t)
#     def stop(self,t=0):
#         self.pwm.ChangeDutyCycle(0)
#         sleep(t)
#  
# motor1 = motor(2,3,4)
# while True:
#     
#     motor1.moveF(30,2)
#     motor1.stop(1) 
#     motor1.moveB(t=2)
#     motor1.stop(1)
#-------------------------------------------

class Root :
    
    def controllo(self,client_obj):
        
    #Do this when there's a socket connection
        request = conn.recv(1024)
        print("Content = %s" % str(request))   
        request = str(request)
        header=str
        value_string=str
        pos1 =0
        pos2 =0
        
        # Get slider Values
    #     slider = urequests.get('http://192.68.1.32')
    # #    print (('slider'),slider.status_code)
    #     # Change duty cycle
    #     in3.value(1)
    #     in4.value(0)
    #     in1.value(1)
    #     in2.value(0)
    #     servo = machine.PWM((p25) ,freq=50)#,duty=205)     
    #     servo.duty(int(slder))
    #     servo = machine.PWM((p26) ,freq=50)#,duty=77)
    #     servo.duty(int(slider))
    #     

        
        LEDON0 = request.find('/?LED=ON0')
        LEDOFF0 = request.find('/?LED=OFF0')
        LEDON2 = request.find('/?LED=ON2')
        LEDOFF2 = request.find('/?LED=OFF2')
        
        
        vel400ON0 = request.find('/?vel400=ON0')
        #vel400OFF0 = request.find('/?vel400=OFF0')
        vel800ON2 = request.find('/?vel800=ON2')
        #vel800OFF2 = request.find('/?vel800=OFF2')

#         header=request.find('/?vol=')
#         print (('header'),header)
#         if header >0:
#             pos1="="
#             pos2 ="&"
            #value_string = header(str(pos1)+1, str(pos2))

    #     vel3    = request.find({},5,7)
    #     print (('vel3'),vel3)
        #time.sleep(2)
        #print("Data: " + str(LEDON0))
        #print("Data2: " + str(LEDOFF0))
    #     if vel400ON0 == 6:
    #         velduty=400
    #     if vel800ON2 == 6:
    #         velduty=800
        
    #-----------------------------------------------------


        



        
    #-----------------------------------------------------
        if LEDON0 == -1 and vel800ON2 == 6 :
            
            velduty=800
            
            print('TURN LED0 ON')
            in3.value(1)
            in4.value(0)
            in1.value(1)
            in2.value(0)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)     
            servo.duty(int(velduty))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(velduty))
            print (("LEDOFF0"),LEDOFF0)
            print (("LEDON2"),LEDON2)
            print (("LEDOFF2"),LEDOFF2)
            print (("vel800ON2"),vel800ON2)
            print (("vel400ON"),vel400ON0)
            
        
        if LEDON0 == -1 and vel400ON0 == 6 :
            velduty=400
            
            print('TURN LED0 ON')
            in3.value(1)
            in4.value(0)
            in1.value(1)
            in2.value(0)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)     
            servo.duty(int(velduty))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(velduty))
            print (("LEDOFF0"),LEDOFF0)
            print (("LEDON2"),LEDON2)
            print (("LEDOFF2"),LEDOFF2)
            print (("vel800ON2"),vel800ON2)
            print (("vel400ON"),vel400ON0)
                
        
            
       
                
    #     if LEDON0 == 6 :#and vel800ON2 == 6:
    #             velduty=800
    #         
    #             print('TURN LED0 ON')
    #             in3.value(1)
    #             in4.value(0)
    #             in1.value(1)
    #             in2.value(0)
    #             servo = machine.PWM((p25) ,freq=50)#,duty=205)
    #             servo.duty(int(velduty))
    #             servo = machine.PWM((p26) ,freq=50)#,duty=77)
    #             servo.duty(int(velduty))
            
        if LEDOFF0 == 6 :        
            print('TURN LED0 OFF')
            in3.value(0)
            in4.value(0)
            in1.value(0)
            in2.value(0)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)
            servo.duty(int(1))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(0))
            
            
            
        if LEDON2 == -1 and vel800ON2==6:
            velduty=800
            print('TURN LED2 ON')
            in3.value(0)
            in4.value(1)
            in1.value(0)
            in2.value(1)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)
            
            servo.duty(int(velduty))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(velduty))
            
            
        if LEDON2 == -1 and vel400ON0==6:
            velduty=400
            print('TURN LED2 ON')
            in3.value(0)
            in4.value(1)
            in1.value(0)
            in2.value(1)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)        
            servo.duty(int(velduty))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(velduty))
            
        if LEDOFF2 == 6:
            print('TURN LED2 OFF')
            in3.value(0)
            in4.value(0)
            in1.value(0)
            in2.value(0)
            servo = machine.PWM((p25) ,freq=50)#,duty=205)
            servo.duty(int(1))
            servo = machine.PWM((p26) ,freq=50)#,duty=77)
            servo.duty(int(0))
            
            
        split_req= str(request.partition("value=")[2].partition("&")[0] )
        str_split_req=str(split_req)
        if str_split_req=="" :
            str_split_req=0
        print(("str_split_req"),str_split_req)
        self.int_split_req=int(str_split_req)
        #self.int_split_req=int_split_req
        
        self.split_nid= str(request.partition("value_")[2].partition("=")[0] )
        print(("self.split_nid= "),self.split_nid)
        
        self.split_req_b= str(request.partition("value_B=")[2].partition("&")[0] )
        print(("tipo e valore di self.split_req_b"),type(self.split_req_b),self.split_req_b)
        #self.str_split_req_b=str(self.split_req_b)
        
        
        
        if self.split_nid !="B" or self.split_nid =="":
            self.split_req_b=0
            self.split_nid="B"
            
            
            #pass
#             str_split_req_b=33
        #print(("str_split_req_b"),self.str_split_req_b)
        self.int_split_req_b=int(self.split_req_b)
        
        def scale_value_pos(value, in_min, in_max, out_min, out_max):
                        scaled_value_pos = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_pos              
        self.d3_pos = scale_value_pos(self.int_split_req, float(0),float(500), 0,1023) #(30/20), (30/10))
        print (('-------D3-pos----'),self.d3_pos)
        
        
        def scale_value_neg(value, in_min, in_max, out_min, out_max):
                        scaled_value_neg = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_neg              
        self.d3_neg = scale_value_neg(self.int_split_req, float(-500),float(0), 1023,0) #(30/20), (30/10))
        print (('-------D3-neg----'),self.d3_neg)
        
              
        
        
        if self.int_split_req =="" or self.int_split_req > 0 :#or vel400ON0 ==6 :             
                self.sottr_int=(int(self.d3_pos))#-self.int_split_req_b)
                #print(("d3_nid_sembra fisso"),self.d3_nid)
                print(("sottr_int____"),self.sottr_int)
                in3.value(1)
                in4.value(0)
                in1.value(1)
                in2.value(0)
                servo = machine.PWM((p25) ,freq=50)#,duty=205)     
                servo.duty(self.sottr_int)
                servo = machine.PWM((p26) ,freq=50)#,duty=77)          
                servo.duty(self.sottr_int)
                oled.text((str(split_req)), 70, 30)
                oled.show()
                
                
        if self.int_split_req =="" or self.int_split_req < 0:
            
                
                
                in3.value(0)
                in4.value(1)
                in1.value(0)
                in2.value(1)
                servo = machine.PWM((p25) ,freq=50)#,duty=205)     
                servo.duty(int(self.d3_neg))
                servo = machine.PWM((p26) ,freq=50)#,duty=77)          
                servo.duty(int(self.d3_neg))
                oled.text((str(split_req)), 70, 30)
                oled.show()         
                
                #R.web_page()

        if self.split_nid =="B" :
             def scale_value_pos(value, in_min, in_max, out_min, out_max):
                        scaled_value_pos = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_pos              
             self.d3_pos = scale_value_pos(self.int_split_req, float(0),float(500), 0,1023) #(30/20), (30/10))
             print (('-------D3-pos----'),self.d3_pos)
        
             def scale_value_neg(value, in_min, in_max, out_min, out_max):
                        scaled_value_neg = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_neg              
             self.d3_neg = scale_value_neg(self.int_split_req, float(-500),float(0), 1023,0) #(30/20), (30/10))
             print (('-------D3-neg----'),self.d3_neg)
        
        
             if self.int_split_req =="" or self.int_split_req > 0 :#or vel400ON0 ==6 :             
                    self.sottr_int=(int(self.d3_pos)-self.int_split_req_b)
                    #print(("d3_nid_sembra fisso"),self.d3_nid)
                    print(("sottr_int____"),self.sottr_int)
                    in3.value(1)
                    in4.value(0)
                    in1.value(1)
                    in2.value(0)
                    servo = machine.PWM((p25) ,freq=50)#,duty=205)     
                    servo.duty(self.sottr_int)
                    servo = machine.PWM((p26) ,freq=50)#,duty=77)          
                    servo.duty(self.sottr_int)
                    oled.text((str(split_req)), 70, 30)
                    oled.show()
                    
                    
             if self.int_split_req =="" or self.int_split_req < 0:
                
                    
                    
                    in3.value(0)
                    in4.value(1)
                    in1.value(0)
                    in2.value(1)
                    servo = machine.PWM((p25) ,freq=50)#,duty=205)     
                    servo.duty(int(self.d3_neg))
                    servo = machine.PWM((p26) ,freq=50)#,duty=77)          
                    servo.duty(int(self.d3_neg))
                    oled.text((str(split_req)), 70, 30)
                    oled.show()         



#---------------------------------------------------
        #if self.split_nid == "B"  :  #int_value_req > 0 and
                
#         def scale_value_nid(value, in_min, in_max, out_min, out_max):
#                   scaled_value_nid = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#                   return scaled_value_nid
#            
#         self.d3_nid = scale_value_nid(self.int_split_req_b, float(0),float(500), 20,150) #(30/20), (30/10))
#         print (('-------D3 NID-----'),self.split_nid,self.d3_nid)

        def scale_value_pos(value, in_min, in_max, out_min, out_max):
                        scaled_value_pos = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_pos              
        self.d3_pos = scale_value_pos(self.int_split_req, float(0),float(500), 0,1023) #(30/20), (30/10))
        print (('-------D3-pos----'),self.d3_pos)
        
        
        def scale_value_neg(value, in_min, in_max, out_min, out_max):
                        scaled_value_neg = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                        return scaled_value_neg              
        self.d3_neg = scale_value_neg(self.int_split_req, float(-500),float(0), 1023,0) #(30/20), (30/10))
        print (('-------D3-neg----'),self.d3_neg)
        
              
        
        
                  
        self.sottr_int=(int(self.d3_pos))#-self.int_split_req_b)
        #print(("d3_nid_sembra fisso"),self.d3_nid)
        print(("sottr_int____"),self.sottr_int)
        in3.value(1)
        in4.value(0)
        in1.value(1)
        in2.value(0)
        servo = machine.PWM((p25) ,freq=50)#,duty=205)     
        servo.duty(self.sottr_int)
        servo = machine.PWM((p26) ,freq=50)#,duty=77)          
        servo.duty(self.sottr_int)
        oled.text((str(split_req)), 70, 30)
        oled.show()
    #             in18.value(0)
        #         in1.value(1)
        #         in2.value(0)
        servo = machine.PWM((p17) ,freq=100)#,duty=205)     
        servo.duty(int(self.int_split_req_b))    #self.d3_nid
    #         servo = machine.PWM((p26) ,freq=50)#,duty=77)          
    #         servo.duty(int(d3))
        oled.text((str(split_req)), 70, 30)
        oled.show()
#         return self.split_nid
#         return self.int_split_req
        #return   (int(self.d3_nid)) 
  #----------------------------------------------------------------------      
        
        
        response = R.web_page()          
        conn.send('HTTP/1.1 200 OK\n')          
        conn.send('Content-Type: text/html\n')           
        conn.send('Connection: close\n\n')           
        conn.sendall(response)
        conn.close()
        
        

    #----------------------------------------------------
    #'---------------------test rele 3108--------------
    #rboard1 = Pin(14, Pin.OUT)
    #rboard1.value(1)
    #-----------------------------------------------

    #led = Pin(14, Pin.OUT)
    #led.value(1)
    #--------------------------------------------

# 
#     #dati x connessione
#     LOCAL_ADDR = "192.168.1.32", 80
#     #TRACK_LOCAL_ADDR = "192.168.1.2", 5005
#     #



    oled.fill(0)
    def web_page(self):
        #print(("Client_handler.int_split_req"),Client_handler.int_split_req)
        
        if in3.value() == 1 or self.int_split_req >0 :#or self.controllo(self.int_split_req) > 0  :
            #self.int_split_req
            gpio_state_0="ON"
            statopin13="ON"
            #self.controllo()
            print(("-----------self.int_split_req"),self.int_split_req)
            #Client_handler(int_split_req)
            #print((" CLIENT  HANDLER   int_split_req"),int_split_req)
        else:
            gpio_state_0="OFF"
            statopin13="OFF"
            
        if in4.value() == 1 or self.int_split_req < 0 :
            gpio_state_2="ON"
            statopin27="ON"
        else:
            gpio_state_2="OFF"
            statopin27="OFF"
        if in1.value() == 1 :
            statopin14="ON"
    #         gpio_state_0="ON"
        else:
            statopin14="OFF"
    #         gpio_state_0="OFF"
    #         
        if in2.value() == 1 :
            statopin12="ON"
    #         gpio_state_2="ON"
        else:
            statopin12="OFF"
            
            
            
    #         gpio_state_2="OFF
        #<meta http-equiv="refresh" content="1" />    
        html = """<!DOCTYPE html>
        <html>

        
        <head>
       
 <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,">

<style>
*
{
	box-sizing: border-box;
}
body
{
	margin: 0px;
	padding: 0px;
	font-family: monospace;
}
.row
{
	display: inline-flex;
	clear: both;
}
.columnLateral
{
  float: left;
  width: 15%;
  min-width: 300px;
}
.columnCentral
{
  float: left;
  width: 70%;
  min-width: 300px;
}
#joy2Div
{
	width:200px;
	height:200px;
	margin:50px
}

#joystick
{
	border: 1px solid #0000FF;
}
		</style>
        
  
<script src="http://petgarage.it/joy.js"></script>
<script src="http://petgarage.it/joy.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>
<meta http-equiv="Content-Type" content="text/html;
<body>
	
		<!-- Example of two JoyStick integrated in the page structure -->
		 
		<div class="row">
			<div class="columnLateral">
			
	<form action="/" >	
            <p><h2>Position: <span id="servoPos"></p></h2>
            <p><h2>Position_1: <span id="servoPos1"  ></p></h2>
            <p><h2>X : <span id="servoPosX"  ></p></h2>
            
            
            <div id="joy1Div" style="width:200px;height:200px;margin:50px;border:1px ,solid #000000,  onchange="servo(this.value)">
            
            Posizione X:<input type="text" id="joy1PosizioneXid"  min="50" max="150"  name="Xpos"  onchange="servo(this.value)"> <br>
            STO CAZZO<input type="range"  min="-511" max="511" class="slider" id="servo1" onchange="servo(this.value)"><br> 
            
            
            Posizione Y:<input id="joy1PosizioneY" type="text"><br>
            Direzione:<input id="joy1Direzione" type="text"><br>
            X :<input id="joy1X_id" name="joy1X_id"  type="range"  onchange="servo(this.value)" ><br>
            Y :<input id="joy1Y" type="text" ><br>
            
	    </div>
		</form>	
	

		<script>
// Create JoyStick object into the DIV 'joy1Div'
var joy1Param = { "title": "joystick", "autoReturnToCenter": false };
var Joy1 = new JoyStick('joy1Div' , joy1Param ,  onchange="servo(this.value)");

var joy1InputPosX = document.getElementById("joy1PosizioneXid");
setInterval(function(){ joy1InputPosX.value=Joy1.GetPosX();
var servoP = document.getElementById("servoPos");
servoP.innerHTML=joy1PosizioneXid.value; 
joy1InputPosX.onchange = function() {
        joy1InputPosX.value = this.value;
         servoP.innerHTML = this.value;
        };  
         function servo (servoP)     {
          $.get("/?value="+ servoP +"&");
          {Connection: close};
          } } );
  
  
var joy1X = document.getElementById("joy1X_id");
var x = setInterval(function() { joy1X.value=Joy1.GetPosX();})
function servo (x) {





      
   
          $.post("/?value=" + x + "&");
          {Connection: close};
            };   
    
    

    function servo (e)  {
    var joy1X = document.getElementById("joy1X_id");
    setInterval(function(){ joy1X.value=Joy1.GetPosX();
    
          $.post("test_l298_manuale_2_class_test6_OK_I_2.py" ,"/?value="+ e +"&");
          {Connection: close};
          }  ) } ;

   
   
   
   
   
$(document).ready(function(){
  $("joy1X_id").change(function(){
    var txt = $("Joy1.GetPosX()");{
    function servo (txt)     {
    $.get("test_l298_manuale_2_class_test6_OK_I_2.py" ,"/?value="+ txt +"&");
          {Connection: close};
          } } } )})
     

      
        



var servoP1 = document.getElementById("servoPos1");
 
        var slider = document.getElementById("servo1");
        var servoP1 = document.getElementById("servoPos1");
        servoP1.innerHTML = slider.value;
        slider.oninput = function() {
          slider.value = this.value;
          servoP1.innerHTML = this.value;
        };
        
        function servo(pos) {
          $.get("/?value=" + pos+ "&");
          {Connection: close};
        };


//----------------------------
var joy1InputPosY = document.getElementById("joy1PosizioneY");
var joy1Direzione = document.getElementById("joy1Direzione");

var joy1Y = document.getElementById("joy1Y");



        






setInterval(function(){ joy1InputPosY.value=Joy1.GetPosY(); } );
setInterval(function(){ joy1Direzione.value=Joy1.GetDir(); } );
setInterval(function(){ joy1Y.value=Joy1.GetY(); });





          









        
		
        
   


// Create JoyStick object into the DIV 'joy2Div'
var joy2Param = { "title": "joystick2", "autoReturnToCenter": false };
var Joy2 = new JoyStick('joy2Div', joy2Param);

var joy2IinputPosX = document.getElementById("joy2PosizioneX");
var joy2InputPosY = document.getElementById("joy2PosizioneY");
var joy2Direzione = document.getElementById("joy2Direzione");
var joy2X = document.getElementById("joy2X");
var joy2Y = document.getElementById("joy2Y");

setInterval(function(){ joy2IinputPosX.value=Joy2.GetPosX(); }, 50);
setInterval(function(){ joy2InputPosY.value=Joy2.GetPosY(); }, 50);
setInterval(function(){ joy2Direzione.value=Joy2.GetDir(); }, 50);
setInterval(function(){ joy2X.value=Joy2.GetX(); }, 50);
setInterval(function(){ joy2Y.value=Joy2.GetY(); }, 50);

var joy3Param = { "title": "joystick3" };
var Joy3 = new JoyStick('joy3Div', joy3Param);

var joy3IinputPosX = document.getElementById("joy3PosizioneX");
var joy3InputPosY = document.getElementById("joy3PosizioneY");
var joy3Direzione = document.getElementById("joy3Direzione");
var joy3X = document.getElementById("joy3X");
var joy3Y = document.getElementById("joy3Y");






              
</script>
	

</body>
    


        </html>
        """
        #return self.int_split_req
        return html
        


R=Root()
#print(("valore int_split_req con classe"),R.controllo(int_split_req))









# #Setup PINS
# LED0 = machine.Pin(14, machine.Pin.OUT)
# LED2 = machine.Pin(27, machine.Pin.OUT)

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(0)
s.bind(('', 80))
s.listen(5)
while True:
    #def tempo():
    #try:
       
        #tempo()
    #except:

            
            
        r, w, err = select.select ((s,), (), (), 1)
        if r:
            for readable in r:
                conn, addr = s.accept()
                print("Got a connection from %s" % str(addr))
                try:
                    R.controllo(conn)
                except OSError as e:
                        pass
#         LED2.value(1)
#         time.sleep(1)
        do_something_else()        



#while True:
    
#     in3= Pin(13, Pin.OUT)
#     in3.value(1)
#     in4 = Pin(27, Pin.OUT)
#     in4.value(0)
#     p26 = machine.Pin(25)
#     servo = machine.PWM((p26) ,freq=50)#,duty=205)
#     
#     servo.duty(int(500))
#     time.sleep(2)
#     in3= Pin(13, Pin.OUT)
#     in3.value(0)
#     in4 = Pin(27, Pin.OUT)
#     in4.value(1)
#     p26 = machine.Pin(25)
#     servo = machine.PWM((p26) ,freq=50)#,duty=40)
#     servo.duty(int(300))
#     time.sleep(2)
#     oled.text('se move?', 10, 50)
#     oled.show()
#------------------------------------------------------------------------------






# def scale_value3(value, in_min, in_max, out_min, out_max):
#       scaled_value3 = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
#       return scaled_value3
#     
# d3 = scale_value3(messageint3, float(0),float(15), 512,1023) #(30/20), (30/10))
# if d3>549 and d3<749:
#     d3=649
#     time.sleep(0.02)
#     servo.duty(int(d3))
#     print (("d3="),float(d3))
#     #time.sleep(0.02)
#     oled.text((str(int(d3))), 70, 30)
#     oled.show()
# 
# else:
#     d3 = scale_value3(messageint3, float(0), float(15), 512,1023) #(30/20), (30/10))
#     #time.sleep(0.02)
#     #print (("d2="),float(d2))
#     servo.duty(int(d3))
#     #time.sleep(0.02)
#     print (("d3="),float(d3))
#     oled.text((str(int(d3))), 70, 30)
#     oled.show()
