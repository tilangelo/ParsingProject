from tkinter import PhotoImage
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import threading
import requests
from bs4 import BeautifulSoup as bs
from time import sleep
import pandas as pd
import csv

# Конфигурации для кастомткинтер
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# Глобальные переменные
loading_label = None
gif_frames = []
gif_index = 0


# Закрытие и открытие окон
def close_old_window():
    app.destroy()
    open_new_window([])


def close_old_window2():
    app.destroy()
    open_new_window2([])


def long_running_task_remi():
    def remiPars():
        mf = open("GetPars3.txt", "w", encoding="utf-8")
        give = []
        pgNum = 5
        for ttt in range(pgNum):
            sleep(0.1)
            URL_TEMPLATE = "https://remi.ru/news/?PAGEN_1=" + str(ttt + 1)
            r = requests.get(URL_TEMPLATE)
            soup = bs(r.text, "html.parser")
            div_names = soup.find_all('div', class_='news__item__header')

            for name in div_names:
                ass = name.a
                if "цена" in ass.text:
                    url_more = ass.get('href')
                    URL_TEMPLATE1 = "https://remi.ru" + url_more
                    r1 = requests.get(URL_TEMPLATE1)
                    soup1 = bs(r1.text, "html.parser")
                    per = soup1.find_all('div', class_='news-detail')
                    for names in per:
                        strr = names.find_all('p')
                        dvss = names.find_all('div')
                        spns = names.find_all('span')

                        for tftf in strr:
                            vau = tftf.text
                            if "✓" in vau:
                                give.append(vau)
                        for ttf in dvss:
                            viu = ttf.text
                            if "✓" in viu:
                                give.append(viu)
                        for pps in spns:
                            vsp = pps.text
                            if "✓" in vsp:
                                give.append(vsp)

        for el in give:
            mf.write(str(el))
            mf.write('\n')

        mf.close()

        # Убираем лишние строки
        with open('GetPars3.txt', encoding='utf-8') as f:
            lines = f.readlines()
            non_empty_lines = (line for line in lines if not line.isspace())
            newnew = list(non_empty_lines)

            with open('finish.txt', 'w', encoding='utf-8') as n_f:
                for i in range(len(newnew)):
                    if "✓" in newnew[i]:
                        n_f.writelines(newnew[i])

    t1 = threading.Thread(target=remiPars, args=())
    t1.start()
    t1.join()

    with open('finish.txt', 'r', encoding="utf-8") as file:
        lst1 = file.readlines()

    df1 = pd.DataFrame(lst1)
    df1.to_csv('dataRemi.csv')

    file = open('dataRemi.csv', encoding="utf-8")
    reader = csv.reader(file)
    data = list(reader)

    del (data[0][0])

    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = data[i][j].rpartition('р.')[0]

    while ['', ''] in data:
        data.remove(['', ''])

    data.pop(0)

    return data


def long_running_task_perekrestok():
    def perekrPars():
        mf = open("GetParsPerekr.txt", "w", encoding="utf-8")
        give = []
        URL_TEMPLATE = "https://www.perekrestok.ru/cat/d?append=1&page=1"
        r = requests.get(URL_TEMPLATE)
        soup = bs(r.text, "html.parser")
        div_names = soup.find_all('div', class_='product-card__content')
        for name in div_names:
            sleep(0.1)
            thisShit = ""
            titleWrapper = name.find_next('div', class_='product-card__title-wrapper')
            title = titleWrapper.div
            ttt = title.text
            thisShit += ttt
            control = name.find_next('div', class_='product-card__control')
            price = control.find_next('div', class_='product-card__price')
            nextdv = price.find_next()
            priceNew = nextdv.find_next('div', class_='price-new')
            needed = priceNew.text
            for x in range(0, 2):
                needed = needed.replace(needed[-1], "")
            for x in range(0, 4):
                needed = needed.replace(needed[0], "")
            thisShit += ". " + needed + " руб"
            give.append(thisShit)

        for el in give:
            mf.write(str(el))
            mf.write('\n')

    t2 = threading.Thread(target=perekrPars, args=())
    t2.start()
    t2.join()

    lst2 = []
    with open('GetParsPerekr.txt', 'r', encoding="utf-8") as file:
        lst2 = file.readlines()

    df2 = pd.DataFrame(lst2)
    df2.to_csv('dataPerekr.csv')

    file2 = open('dataPerekr.csv', encoding="utf-8")
    reader2 = csv.reader(file2)
    data2 = list(reader2)
    del (data2[0][0])
    data2.pop(0)

    return data2


# Открытие новых окон
def open_new_window(data2):
    newapp = ctk.CTk()
    newapp.title("")
    newapp.geometry("1200x900+350+70")
    textbox = ctk.CTkTextbox(newapp, height=900, width=1200, font=("Segoe UI", 14))
    textbox.insert('end', list_to_string(data2))
    textbox.pack(expand=True)
    textbox.configure(state="disabled")

    newapp.mainloop()


def open_new_window2(data):
    newapp = ctk.CTk()
    newapp.title("")
    newapp.geometry("1200x900+350+70")
    textbox = ctk.CTkTextbox(newapp, height=900, width=1200, font=("Segoe UI", 14))
    textbox.insert('end', list_to_string(data))
    textbox.pack(expand=True)
    textbox.configure(state="disabled")

    newapp.mainloop()


# Анимация гиф
def animate_gif(gif_path):
    global gif_frames, gif_index
    gif = Image.open(gif_path)
    gif_frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]
    gif_index = 0
    update_gif_frame()


def update_gif_frame():
    global gif_index
    if loading_label and gif_frames:
        loading_label.configure(image=gif_frames[gif_index], text="")
        gif_index = (gif_index + 1) % len(gif_frames)
        app.after(100, update_gif_frame)


def show_loading_gif():
    global loading_label
    loading_label = ctk.CTkLabel(app)
    loading_label.place(relx=0.5, rely=0.5, anchor="center")
    animate_gif("loading-green-loading.gif")


def hide_loading_gif():
    global loading_label
    if loading_label:
        loading_label.destroy()
        loading_label = None


def run_task_remi():
    show_loading_gif()
    threading.Thread(target=task_wrapper_remi).start()


def task_wrapper_remi():
    data = long_running_task_remi()
    app.after(0, hide_loading_gif)
    open_new_window(data)


def run_task_perekrestok():
    show_loading_gif()
    threading.Thread(target=task_wrapper_perekrestok).start()


def task_wrapper_perekrestok():
    data = long_running_task_perekrestok()
    app.after(0, hide_loading_gif)
    open_new_window2(data)


# Строка из списка
def list_to_string(data):
    result = ""
    for sublist in data:
        result += "".join(sublist) + "\n"
    return result


# Основное окно
app = ctk.CTk()
app.geometry("800x550+500+250")
app.title("")
app.resizable(width=False, height=False)

image1 = PhotoImage(file="logo-label.png")
image2 = PhotoImage(file="remi-logo-2017.png")

button1 = ctk.CTkButton(master=app, image=image1, text="", command=run_task_perekrestok, corner_radius=24, height=120,
                        width=100)
button1.place(anchor='center', relx=0.5, rely=0.25)
button2 = ctk.CTkButton(master=app, image=image2, text="", command=run_task_remi, corner_radius=24, height=120,
                        width=100)
button2.place(anchor='center', relx=0.5, rely=0.65)

app.mainloop()