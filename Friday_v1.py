import speech_recognition as sr
import os
from playsound import playsound
import webbrowser
import random

speech=sr.Recognizer()

# Dictionaries for functions
greeting_dict = {'hey':'hey','hi':'hi','hello':'hello'}
open_launch_dict ={'open':'open','launch':'launch'}
social_media_dict={'youtube':'https://www.youtube.com/','vaccine':'https://www.cowin.gov.in/','instagram':'https://www.instagram.com/','linkedin':'https://www.linkedin.com/','gmail':'https://mail.google.com/mail/u/0/#inbox','intranet':'https://intranet.cb.amrita.edu/','sign':'https://cms.cb.amrita.edu/login','manage':'https://aumscb.amrita.edu/cas/login?service=https%3A%2F%2Faumscb.amrita.edu%2Faums%2FJsp%2FCore_Common%2Findex.jsp','office':'https://www.office.com/?auth=2'}
google_searches_dict={'what':'what','why':'why','who':'who','which':'which','when':'when'}
control_dict={'get':'get','turn':'turn','start':'start'}

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


if __name__ == '__main__':
        playsound('mp3/mp3_friday_greeting.mp3')
        while True:

            voice_note = read_voice_cmd().lower()
            print ('cmd:{}'.format(voice_note))
            if is_valid_note(greeting_dict,voice_note):
                print("In Greeting...")
                play_sound(mp3_greeting_list)
                continue
            elif is_valid_note(open_launch_dict,voice_note):
                print("In Open...")
                play_sound(mp3_open_launch_list)
                if(is_valid_note(social_media_dict,voice_note)):
                    key=voice_note.split(' ')[1]
                    webbrowser.open(social_media_dict.get(key))
                else:
                    os.system('explorer C:\\"{}"'.format(voice_note.replace('open ','').replace('launch ','')))
                continue
            elif is_valid_google_search(voice_note):
                print("in google search...")
                play_sound(mp3_google_searches_list)
                webbrowser.open('https://www.google.co.in/search?q={}'.format(voice_note))
                continue

            elif 'thank you' in voice_note:
                 play_sound(mp3_thankyou_list)
                 continue

            elif 'bye' in voice_note or 'goodbye' in voice_note or 'by' in voice_note:
                playsound('mp3/mp3_friday_bye.mp3')
            exit()


