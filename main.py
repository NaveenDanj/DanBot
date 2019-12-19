import playsound
import speech_recognition as sr
from gtts import gTTS
import json
import random
import os

r = sr.Recognizer()

class Bot:


    def __init__(self):
        self.name = None
        self.data_path = None
        self.config_path = None



    def listen(self , text):
        words = self.pre_processing_text(text)
        return self.choose_question(text)

    def reply(self , text):

        tts = gTTS(text = text , lang = 'en')
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)


    def train(self):
        end_code = '<<end>>'

        qs = []
        wl = []

        while(True):
            raw_text_feed = raw_input("Enter your Question: ")

            if(raw_text_feed == end_code):
                break
            else:
                raw_words = self.pre_processing_text(raw_text_feed)
                qs.append(raw_text_feed)
                wl.append(raw_words)



        ans = []

        while(True):
            ans_str = raw_input("Enter your sample answers: ")

            if(ans_str == end_code):
                break

            else:

                word_list = self.pre_processing_text(ans_str)
                ans.append(ans_str)

        
        json = self.read_data()

        obj = {
            "question":{
                "raw_feed":qs,
                "raw_word_list":wl
            },

            "answer":{
                "answers":ans
            }
        }

        json['questions'].append(obj)

        self.write_data(json)


    def read_data(self):
        data = None
        with open('data.json') as json_file:
            data = json.load(json_file)

        return data



    def write_data(self , data):
        with open(self.data_path , "w") as write_file:
            json.dump(data, write_file)


    def set_path(self , path):
        self.data_path = path

    def choose_question(self , text_feed):

        json = self.read_data()
        word_list = self.pre_processing_text(text_feed)

        index = None
        max_score  = 0

        for i in range(len(json['questions'])):
            count = 0
            for j in word_list:
                for k in json['questions'][i]['question']["raw_word_list"]:
                    for l in k:
                        if j == l:
                            count += 1
            if count > max_score:
                max_score = count
                index = i


        if index == None:
            return "Sorry...I don't Understand that properly!"
        else:
            elem = random.randint(0 , len(json['questions'][index]['answer']["answers"]))
            return json['questions'][index]['answer']["answers"][elem]



    def pre_processing_text(self , text):
        text = text.lower()
        text = text.replace("." , "")
        text = text.replace("?" , "")
        text = text.replace("!" , "")
        text = text.replace("'" , "")
        words = text.split(" ")

        return words

    def run_bot(self):
        end_code = "<<exit>>"

        while(True):
            text_feed = raw_input("You: ")

            if text_feed == end_code:
                break
            else:
                ans = self.listen(text_feed)
                print("DanBot: " ,ans)
                self.reply(ans)
                os.remove("voice.mp3")






bot = Bot()
bot.data_path = 'data.json'
# bot.train()
bot.run_bot()
