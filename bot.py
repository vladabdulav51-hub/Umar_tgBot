import os
import requests
import telebot
from bs4 import BeautifulSoup
from telebot import types
#from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
bot=telebot.TeleBot('My token')
pageg=1
pag=[]
name_tre=[]
exect_tre=[]
track_href=[]
major_li1=[]
Error=False
def Dowen_file(urls,fil_names):
    rssp=requests.get(urls)
    with open(fil_names,'wb') as f:
        for chunk in rssp.iter_content(chunk_size=8192):
            f.write(chunk)
        return fil_names
@bot.message_handler(commands=['start'])
def buttons(message):
    markup= types.ReplyKeyboardMarkup()
    btn1=types.KeyboardButton("Почему бот ненаходит музыку?")
    btn2=types.KeyboardButton("/help")
    markup.add(btn1)
    markup.add(btn2)
    #Морозов Блять только попробуй свои арабские символы написать
    bot.send_message(message.chat.id,"Привет я бот чтобы искать и скачивать треки\nПрошу писать на русском и английском.",reply_markup=markup)
@bot.message_handler(content_types=['text'])
def text_command(message):
    global pageg
    global pag
    global name_tre
    global exect_tre
    global track_href
    global major_li1
    pag=[]
    pageg=0
    if message.text=="/help":
        bot.send_message(message.chat.id,"Вот что я могу:\n1. Искать музыку по обрывку названия трека\n2. Cкачивать трек для вас.")
    elif(message.text=="Почему бот ненаходит музыку?") :
        bot.send_message(message.chat.id,"Здраствуй дорогой пользователь! \n приносим наши извенения если бот не может найти музыку \n по вашему запросую.\nРекомендуеые действия\n1. Проверить орфографию запроса.\n2. Попробывать изменить запрос ищите не по названию трека ,а\nпо названию исполнителя или группы.")
    else:
        print(message.text)
        print(message.chat.id)
        id_user=message.chat.id
        id_Admin=5161929113
        id_Morozov=948596905
        if id_Morozov==id_user:
            bot.send_message(message.chat.id,"Морозов не балуйся я все вижу")
            print("Морозов я вижу все!")
        serch_url="https://rus.hitmotop.com/search?q="
        rspon=requests.get(serch_url+message.text)
        bot.send_message(message.chat.id,"Подождите минутку ищу вашу музыку")
        sup=BeautifulSoup(rspon.text,'lxml')
        track_Name = sup.find_all('div',class_='track__title')
        track_Executor = sup.find_all('div',class_='track__desc')
        track_butn=sup.find_all('a',attrs={"data-nopjax": True})
        name_tre=[]
        exect_tre=[]
        track_href=[]
        i=0
        for i in track_Name:
            nam=i.text.strip()
            name_tre.append(nam)
        print(len(name_tre))
        i=0
        for i in track_Executor:
            exect=i.text.strip()
            exect_tre.append(exect)
        i=0
        for i in track_butn:
            track_href.append(i['href'])
        i=0
        for i in range(len(name_tre)):
            pag.append(name_tre[i]+" "+exect_tre[i])
        temp_li=[]
        i=0
        merkuri=types.InlineKeyboardMarkup()
        for i in range(len(pag)):
            bth_fil=types.InlineKeyboardButton(text=pag[i],callback_data=str(i))
            temp_li.append(bth_fil)
        major_li1=[]
        i=0
        for i in range(i,len(temp_li),5):
            major_li1.append(temp_li[i:i+5])
        print(len(major_li1))
        try:
            for i in major_li1[0]:
                merkuri.add(i)
            next_but=types.InlineKeyboardButton(text="Next",callback_data="/next")
            merkuri.add(next_but)
            bot.send_message(message.chat.id,"Мы нашли "+str(len(track_Name))+" треков",reply_markup=merkuri)
        except IndexError:
            bot.send_message(message.chat.id,"Ой произошла ошибка повтрите запрос")
            print('ошибка обработана')


@bot.callback_query_handler(func=lambda call: True)
def bot_butn_clck(call):
    global pageg
    global pag
    global name_tre
    global exect_tre
    global track_href
    global major_li1
    if call.data=="/next":
        if pageg==(len(major_li1)-1):
            merkuri=types.InlineKeyboardMarkup()
            for i in major_li1[pageg]:
                merkuri.add(i)
            dow_but=types.InlineKeyboardButton(text="Down",callback_data="/down")
            merkuri.add(dow_but)
        elif pageg<(len(major_li1)-1):
            pageg=pageg+1
            merkuri=types.InlineKeyboardMarkup()
            for i in major_li1[pageg]:
                merkuri.add(i)
            next_but=types.InlineKeyboardButton(text="Next",callback_data="/next")
            dow_but=types.InlineKeyboardButton(text="Down",callback_data="/down")
            merkuri.add(dow_but,next_but)
        bot.edit_message_reply_markup(call.message.chat.id,message_id=call.message.message_id,reply_markup=merkuri)
    elif call.data=="/down":
        if pageg==0:
            merkuri=types.InlineKeyboardMarkup()
            for i in major_li1[pageg]:
                merkuri.add(i)
            next_but=types.InlineKeyboardButton(text="Next",callback_data="/next")
            merkuri.add(next_but)
        elif pageg>0:
            pageg=pageg-1
            merkuri=types.InlineKeyboardMarkup()
            for i in major_li1[pageg]:
                merkuri.add(i)
            next_but=types.InlineKeyboardButton(text="Next",callback_data="/next")
            dow_but=types.InlineKeyboardButton(text="Down",callback_data="/down")
            merkuri.add(dow_but,next_but)
            bot.edit_message_reply_markup(call.message.chat.id,message_id=call.message.message_id,reply_markup=merkuri)
            bot.send_message(call.message.chat.id,"Ой произошла ошибка повтрите запрос")
    else:
        try:
            num_name=int(call.data)
            print(pag[num_name])
            print(track_href[num_name])
            pons=requests.get(track_href[num_name],stream=True)
            pons.raise_for_status()
            fil_name=track_href[num_name]
            name_fil=fil_name.split("/")[-1]
            print(name_fil)
            tmp="./mus/tmp_"+name_fil
            with open(tmp,"wb") as f:
                for chunk in pons.iter_content(1024):
                    f.write(chunk)
            print(tmp)
            filee=open(tmp,'rb')
            bot.send_message(call.message.chat.id,"Грузим ваш файл вы в очереди")
            bot.send_audio(call.message.chat.id,filee,timeout=500)
            os.remove(tmp)
            filee.close()
        except IndexError:
            bot.send_message(call.message.chat.id,"Повторите запрос произошла ошибка")
            print('ошибка обработана')
bot.polling(none_stop=True)


