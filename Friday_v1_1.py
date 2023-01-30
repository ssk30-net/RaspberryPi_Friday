import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random
#import RPi.GPIO as gpio
#from picamera import PiCamera
import time
import datetime
import weathercom
import json
import pyttsx3 as px
import subprocess
import logging
import valib as va
import requests 
     
speech=sr.Recognizer()



# Sectioning
try:
    engine=px.init() # Engine for text to speech
except ImportError:
    print('Requested Driver not found')
except RuntimeError:
    print('Driver Fails to Initialize')

# Section property of engine
voices=engine.getProperty('voices')

engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') # setting the tts to zira the female voice
# for setting speech rate
rate=engine.getProperty('rate')
engine.setProperty('rate',rate)
# Function for speaking the text given
def speakfromtext_cmd(cmd):
    engine.say(cmd)
    engine.runAndWait()

# Dictionaries for functions
greeting_dict = {'hey':'hey','hi':'hi','hello':'hello'}
open_launch_dict ={'open':'open','launch':'launch'}
social_media_dict={'youtube':'https://www.youtube.com/','vaccine':'https://www.cowin.gov.in/','instagram':'https://www.instagram.com/','linkedin':'https://www.linkedin.com/','gmail':'https://mail.google.com/mail/u/0/#inbox','intranet':'https://intranet.cb.amrita.edu/','sign':'https://cms.cb.amrita.edu/login','manage':'https://aumscb.amrita.edu/cas/login?service=https%3A%2F%2Faumscb.amrita.edu%2Faums%2FJsp%2FCore_Common%2Findex.jsp','office':'https://www.office.com/?auth=2'}
google_searches_dict={'what':'what','why':'why','who':'who','which':'which','when':'when' }
control_dict={'get':'get','turn':'turn','start':'start','open':'open','light':'light','set':'set'}

# List for operations
mp3_greeting_list=['mp3/mp3_friday_greeting_accept_2.mp3','mp3/mp3_friday_greeting_accept.mp3','mp3/mp3_friday_greeting_accept.mp3']
mp3_open_launch_list=['mp3/mp3_friday_open_1.mp3','mp3/mp3_friday_open_2.mp3','mp3/mp3_friday_open_3.mp3']
mp3_google_searches_list=['mp3/mp3_friday_google_search_1.mp3','mp3/mp3_friday_google_search_2.mp3']
mp3_listening_problem_list=['mp3/mp3_friday_listening_problem_1.mp3','mp3/mp3_friday_listening_problem_2.mp3']
mp3_struggling_list=['mp3/mp3_friday_struggling_1.mp3']
mp3_thankyou_list=['mp3/mp3_friday_thankyou_1.mp3']

error_occurence=0

#Function for google seraches
def is_valid_google_search(phrase):
    if (google_searches_dict.get(phrase.split(' ')[0])==phrase.split(' ')[0]):
        return True

# Function for playing sound
def play_sound(mp3_list):
    mp3 = random.choice(mp3_list)
    playsound(mp3)

# Function for reading voice
def read_voice_cmd():
    global voice_text
    voice_text=''
    print("Listening...")
    global error_occurence
    

    try:
        with sr.Microphone() as source:
            audio = speech.listen(source=source, timeout=10, phrase_time_limit=5)
        voice_text=speech.recognize_google(audio)
    except sr.UnknownValueError:
        if error_occurence==0:
            play_sound(mp3_listening_problem_list)
            error_occurence+=1
        elif error_occurence==1:
            play_sound(mp3_struggling_list)
            error_occurence+=1
        pass
    except sr.RequestError:
        print ('Network Error!!')
    except sr.WaitTimeoutError:

        if error_occurence==0:
            play_sound(mp3_listening_problem_list)
            error_occurence+=1
        elif error_occurence==1:
            play_sound(mp3_struggling_list)
            error_occurence+=1
        pass
    return voice_text

# Function for operations
def is_valid_note(greet_dict,voice_note):
    for key,value in greet_dict.items():
        try:
            if value==voice_note.split(' ')[0]:
                return True
                break
            elif key== voice_note.split(' ')[1]:
                return True
                break
        except IndexError:
            pass

    return False
  


    





logger = logging.getLogger('voice assistant')


def process_text(text, pa):
    """
    asking who are you?
    """
    if "who are you" in voice_note:
        speakfromtext_cmd("i am a i voice assistant system")

    """
    asking about weather information.
    """
    """if "weather" in voice_note:
        speakfromtext_cmd("which city")
        time.sleep(5)
        file_name = pa.process(3)
        city = pa.voice_command_processor(file_name)
        logger.info("process_text : City :: " + city)
        try:
            humidity, temp, phrase = weatherReport(city)
            speakfromtext_cmd(
                "currently in " + city + " temperature is " + str(
                    temp) + " degree celsius, " + "humidity is " + str(
                    humidity) + " percent and sky is " + phrase)
            logger.info("currently in " + city + " temperature is " + str(
                temp) + "degree celsius, " + "humidity is " + str(
                humidity) + " percent and sky is " + phrase)
        except KeyError as e:
            speakfromtext_cmd("sorry, i couldn't get the location")"""
 
    

    return "done"

if __name__ == '__main__':
        playsound('mp3/mp3_friday_greeting.mp3')
        while True:
            playsound('mp3/mp3_friday_greeting.mp3')
            voice_note = read_voice_cmd().lower()
            print ('cmd:{}'.format(voice_note))
            if is_valid_note(greeting_dict,voice_note):
                print("In Greeting...")
                play_sound(mp3_greeting_list)

                continue
            elif is_valid_note(open_launch_dict,voice_note):
                print("In Open...")
                play_sound(mp3_open_launch_list)
                speakfromtext_cmd("ok sir")
                if(is_valid_note(social_media_dict,voice_note)):
                    key=voice_note.split(' ')[1]
                    webbrowser.open(social_media_dict.get(key))
                else:
                    os.system('explorer C:\\"{}"'.format(voice_note.replace('open ','').replace('launch ','')))
                continue
            elif is_valid_google_search(voice_note):
                print("in google search...")
                #play_sound(mp3_google_searches_list)
                speakfromtext_cmd("Let me search for you sir")
                webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_note))
                continue
            elif is_valid_note(control_dict,voice_note):
                """"Asking for turning Light control"""
                """if "light off" in voice_note:
                    speakfromtext_cmd('Turning off Light')
                    ledpin=36
                    gpio.setwarnings(False)
                    gpio.setmode(gpio.BOARD)
                    gpio.setup(ledpin,gpio.OUT)
                    #while True:
                    gpio.output(ledpin,False)
                    #time.sleep(30)
                    gpio.cleanup()
                    
                    continue"""

                """if "light on" in voice_note:
                    speakfromtext_cmd("Turning on Light")
                    ledpin=36
                    gpio.setwarnings(False)
                    gpio.setmode(gpio.BOARD)
                    gpio.setup(ledpin,gpio.OUT)
                    #while True:
                    gpio.output(ledpin,True)
                    #time.sleep(30)
                    #gpio.cleanup()
                    
                    continue"""

                """Asking to start camera"""
                """if "camera" in voice_note:
                    speakfromtext_cmd("Starting camera")
                    pi_cam = PiCamera()
                    pi_cam.start_preview(alpha=255)  # Increase Transperancy
                    pi_cam.capture('myimage.png')
                    time.sleep(5)
                    pi_cam.stop_preview()
                    pi_cam.close()
                    continue"""

                """if "alarm" in voice_note:
                    speakfromtext_cmd("The alarm was Set")
                    Buzzer=36
                    gpio.setmode(gpio.BOARD)
                    gpio.setwarnings(False)
                    
                    i=0
                    HOUR=0
                    MINUTE=0
                    gpio.setup(Buzzer,gpio.OUT)
                    
                    a = datetime.datetime.now()
                    b=str(a)
                    splt=b.split(' ')
                    tme=splt[1]
                    hour=tme.split(':')
                    hr=hour[0]
                    minte=hour[1]
                    print (a)
                    print("ENTER THE HOUR IN THE RAILWAY TIME FORMAT")
                    HOUR = int(input('Enter the HOUR to set Alarm'))
                    MINUTE = int(input('Enter the MINUTE to set Alarm'))
                    if ((hr==HOUR)and(minte==MINUTE)):
                            print("Time reachimport requestsed")
                            for i in range (2) :
                                gpio.output(Buzzer, True)
                                #time.sleep(0.5)
                                gpio.output(Buzzer, False)
                                #time.sleep(0.5)
                            var = "Times up!!! Happy Morning Have a Good day"
                            subprocess.call(["sudo", "espeak", var])
                    else:
                        gpio.output(Buzzer, False)
                    continue"""
                if "reboot" in voice_note or "Reboot" in voice_note:
                    speakfromtext_cmd("ok.. rebooting the server")
                    command = "/usr/bin/sudo /sbin/shutdown -r now"
                    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                    continue
                if "climate" in voice_note or "weather" in voice_note:
                    city = input('input the city name')
                    print(city)
                    print('Displaying Weather report for: ' + city)
                    url = 'https://wttr.in/{}'.format(city)
                    res = requests.get(url)
                    print(res.text)
                else:
                    recognized_text=''
                    process=process_text(read_voice_cmd(),voice_note)
                    continue
            elif 'thank you' in voice_note:
                 play_sound(mp3_thankyou_list)
                 continue

            elif 'bye' or 'goodbye' in voice_note:
                playsound('mp3/mp3_friday_bye.mp3')
            exit()


