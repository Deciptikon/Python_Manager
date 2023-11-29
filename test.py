import pyttsx3
import speech_recognition as sr
import dearpygui.dearpygui as dpg

import subprocess
import pyautogui
import time

#############################################################################

VERSION = '0.1.2'

##############################################################################

# Задержка перед выполнением действия (дайте время для переключения на нужное окно)
time.sleep(5)

# Эмулируем нажатие клавиши (например, клавиши 'A')
#pyautogui.press('A')

##############################################################################
list_program = [['блокнот',     'notepad.exe'],
                ['календарь',   ['start', 'ms-cald:']],
                ['браузер',     ["start", "opera.exe"]]]

def get_path_from_program(program):
    return program[1]

def find_words_right_of(target_word, input_string, num_words=1):
    words = input_string.split()
    index = words.index(target_word) if target_word in words else -1

    if index != -1 and index + num_words < len(words):
        return words[index + 1 : index + num_words + 1]
    else:
        return None

def parse_and_work(text):
    
    if 'открой' in text:
        target = find_words_right_of('открой', text)

        for program in list_program:
            if target in program:
                subprocess.Popen(get_path_from_program(program))            

##############################################################################

engine = pyttsx3.init()
ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
engine.setProperty('voice', ru_voice_id)

#engine.say('привет, это просто тест голоса по русски')
#engine.runAndWait()

###############################################################################

recognizer = sr.Recognizer()

def listen_and_recognize():
    dpg.hide_item('bt_listen')
    with sr.Microphone(device_index=2) as source:
        print("Я вас слушаю...")
        dpg.set_value('txt_area', ".....................")
        
        engine.say("Я вас слушаю...")
        engine.runAndWait()
        dpg.set_value('txt_area', "Скажите что-нибудь...")

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU") #google #sphinx
        print("Вы сказали: ", text)
        dpg.set_value('txt_area', "Вы сказали: " + text)
        engine.say("Вы сказали: " + text)
        engine.runAndWait()
        
        ############################
        #### выполняем действия ####
        ############################



        dpg.show_item('bt_listen')
    except sr.UnknownValueError:
        print("Речь не распознана")
        dpg.set_value('txt_area', "Мне не удалось вас понять.")
        engine.say("Извините, мне не удалось вас понять.")
        engine.runAndWait()

        dpg.show_item('bt_listen')
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания речи: {e}")
        dpg.set_value('txt_area', "Ошибка сервиса распознавания речи.")
        engine.say(f"Произошла ошибка сервиса распознавания речи. Вы можете ознакомиться с подробностями в логах программы.")
        engine.runAndWait()

        dpg.show_item('bt_listen')
    
###########################################################################

dpg.create_context()

with dpg.font_registry():
    with dpg.font("lucon.ttf", 20, default_font=True, id="Default font"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic )
    dpg.bind_font("Default font")

dpg.create_viewport(title="Recognizer " + VERSION, 
                    width=600, height=300, 
                    x_pos=600, y_pos=300)

with dpg.window(label="Main", width=600, height=300):
    dpg.add_text("...", tag='txt_area')
    dpg.add_button(label="Говорить", 
                   width=200, height=80, 
                   pos=[(600-200)/2, 150], 
                   callback=listen_and_recognize, 
                   tag='bt_listen', 
                   filter_key=ord('A'))


dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()




############################################################################