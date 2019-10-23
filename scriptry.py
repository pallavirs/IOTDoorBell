import RPi.GPIO as GPIO
import time
import os
import random
import datetime
import telepot
from subprocess import call
#import encodeimg


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(2,GPIO.OUT)         #LED output pin
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)    

os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/welcome.mp3")

def detect_intruder():
    while True:
        i=GPIO.input(17)
        if i==0:                 #When output from motion sensor is LOW
            print "No intruders",i
            GPIO.output(2,0)  #Turn OFF LED
            time.sleep(0.1)
        elif i==1:               #When output from motion sensor is HIGH
            print "Intruder detected",i
            GPIO.output(2,1)  #Turn ON LED'''
            #call(["fswebcam", "-d", "/dev/video0", "-r", "1280x720", "--no-banner", "./img4.jpg"])
            #print("Loop")
            break
    exec(open("/home/pi/AWS_Cloud/main_code/encodeimg.py").read(),globals())      
    

while True:
    
    input_state=GPIO.input(18)
    if input_state == False:
        print "Alarm Pressed"
        os.system("sudo omxplayer -o local /home/pi/AWS_Cloud/main_code/doorbell.mp3")
        detect_intruder()




#exec(open("encodeimg.py").read(),globals())      
'''bot=telepot.Bot('343511006:AAHmqbNCBDFqdX9wd4dWPzeALoVcFGubFnc')
chat_id=328797460;
print 'Sending Notification to Mobile along with photo...'
bot.sendMessage(chat_id,'someone is knocking your Door')
bot.sendMessage(chat_id,str(datetime.datetime.now()))
bot.sendPhoto(chat_id=chat_id,photo=open('./img4.jpg','rb'))
bot.message_loop(handle)'''












