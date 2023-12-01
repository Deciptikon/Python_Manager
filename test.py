import pyttsx3                      # озвучивание текста
import speech_recognition as sr     # распознование голоса
import dearpygui.dearpygui as dpg   # графический интерфейс

import subprocess                   # открытие программ
import pyautogui                    # манипуляция с мышью и кнопками
import pygetwindow                  # манипуляция с окнами
import time                         # время

#############################################################################

VERSION = '0.1.3'

##############################################################################

# Задержка перед выполнением действия (дайте время для переключения на нужное окно)
time.sleep(5)

# Эмулируем нажатие клавиши (например, клавиши 'A')
#pyautogui.press('A')

##############################################################################
list_action_opened = ['открой',
                      'открыть',
                      'открывай']



list_program = [['блокнот',     'C:\\Windows\\System32\\notepad.exe'],
                ['калькулятор', ''],
                ['браузер',     'C:\\Users\\ASUS\\AppData\\Local\\Programs\\Opera\\launcher.exe']]

def get_path_from_program(program: list) -> (list[str] | str):
    return program[1]

def find_words_right_of(target_words: (list | tuple), input_string: str, num_words: int = 1) -> (list[str] | str | None):
    words = input_string.lower().split()
    print(f'{words=}')
    index = -1
    for target_word in target_words:
        if target_word in words:
            index = words.index(target_word) 

    if index != -1 and index + num_words <= len(words):
        return_words = words[index + 1 : index + num_words + 1]
        print(f'{return_words=}')
        if len(return_words) == 1:
            return return_words[0] 
        else:
            return return_words
    else:
        return None

def parse_and_work(text: str) -> None:
    lower_text = text.lower()
    common_list_action_opened = [action for action in list_action_opened if action in lower_text]
    if len(common_list_action_opened) > 0:
        target = find_words_right_of(list_action_opened, lower_text, num_words=1)
        for program in list_program:
            name, path = program
            subprocess.Popen(get_path_from_program(program)) if name == target else -1
    return None          

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
    subprocess.Popen()
    with sr.Microphone(device_index=2) as source:
        print("Я вас слушаю...")
        dpg.set_value('txt_area', ".....................")
        
        engine.say("Я вас слушаю...")
        engine.runAndWait()
        dpg.set_value('txt_area', "Скажите что-нибудь...")

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU",) #google #sphinx
        print("Вы сказали: ", text)
        dpg.set_value('txt_area', "Вы сказали: " + text)
        engine.say("Вы сказали: " + text)
        engine.runAndWait()
        
        ############################
        #### выполняем действия ####
        ############################

        parse_and_work(text)

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