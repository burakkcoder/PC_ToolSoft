from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import platform
import psutil
import subprocess
import webbrowser as wb
import random

# Parlaklık
import screen_brightness_control as pct

# Ses
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Hava Durumu
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# Saat
from time import strftime

# Takvim
from tkcalendar import *

# Google
import pyautogui

root = Tk()
root.title("PC-ToolSoft")
root.geometry("850x500+300+170")
root.resizable(False, False)
root.configure(bg="#292e2e")

# Icon
tool_icon_png = PhotoImage(file="images/tool_icon.png")
root.iconphoto(False, tool_icon_png)

# Gövde
body = Frame(root, width=900, height=600, bg="#d6d6d6")
body.pack(padx=20, pady=20)

#####SOL BÖLÜM#####
sol_bolum = Frame(body, width=310, height=435, bg="#f4f5f5",
                  highlightbackground="#adacb1", highlightthickness=1)
sol_bolum.place(x=10, y=10)

hp_png = PhotoImage(file="images/hp.png")
hp = Label(sol_bolum, image=hp_png, background="#f4f5f5")
hp.place(x=5, y=0)

sistemim = platform.uname()
# İşlemci Bilgileri Sığdırma


def sigdir(islemci):
    islemci = sistemim.processor
    try:
        islemci = f"{islemci[:28]} ..."
        return islemci
    except:
        return islemci


l1 = Label(sol_bolum, text=sistemim.node, bg="#f4f5f5", font=(
    "Acumin Variable Concept", 15, "bold"), justify="center")
l1.place(x=20, y=210)
l2 = Label(sol_bolum, text=f"Versiyon:{sistemim.version}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 8, "bold"), justify="center")
l2.place(x=20, y=250)
l3 = Label(sol_bolum, text=f"Sistem : {sistemim.system}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 8, "bold"), justify="center")
l3.place(x=20, y=290)
l4 = Label(sol_bolum, text=f"Kullanılabilir RAM : {round(psutil.virtual_memory().total / 1000000000, 2)} GB",
           bg="#f4f5f5", font=("Acumin Variable Concept", 8, "bold"), justify="center")
l4.place(x=20, y=330)
l5 = Label(sol_bolum, text=f"İşlemci : {sigdir(sistemim.processor)}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 8, "bold"), justify="center")
l5.place(x=20, y=370)

#####SAĞ BÖLÜM#####
sag_bolum = Frame(body, width=470, height=230, bg="#f4f5f5",
                  highlightbackground="#adacb1", highlightthickness=1)
sag_bolum.place(x=330, y=10)

sistem = Label(sag_bolum, text="Sistem", font=(
    "Acumin Variable Concept", 15), bg="#f4f5f5")
sistem.place(x=10, y=10)

# Batarya


def batarya_bilgileri():
    global batarya_png
    global batarya_lbl

    batarya = psutil.sensors_battery()
    yuzde = batarya.percent

    lbl.config(text=f"{yuzde}%")
    if batarya.power_plugged:
        durum = "Bağlı"
    else:
        durum = "Bağlı Değil"
    lbl_priz.config(text=f"Priz : {durum}")

    batarya_lbl = Label(sag_bolum, background="#f4f5f5")
    batarya_lbl.place(x=15, y=50)

    lbl.after(1000, batarya_bilgileri)

    if batarya.power_plugged:
        durum = "Bağlı"
        batarya_png = PhotoImage(file="images/şarj.png")
        batarya_lbl.config(image=batarya_png)
    else:
        durum = "Bağlı Değil"
        batarya_png = PhotoImage(file="images/fullşarj.png")
        batarya_lbl.config(image=batarya_png)


lbl = Label(sag_bolum, font=(
    "Acumin Variable Concept", 25, "bold"), bg="#f4f5f5")
lbl.place(x=180, y=50)
lbl_priz = Label(sag_bolum, font=("Acumin Variable Concept", 10), bg="#f4f5f5")
lbl_priz.place(x=20, y=120)
lbl_zaman = Label(sag_bolum, font=(
    "Acumin Variable Concept", 15), bg="#f4f5f5")
lbl_zaman.place(x=180, y=100)

# Hoparlör
lbl_hoparlor = Label(sag_bolum, text="Hoparlör : ",
                     font=("arial", 10, "bold"), bg="#f4f5f5")
lbl_hoparlor.place(x=10, y=150)

anlik_ses_duzeyi = tk.DoubleVar()


def simdiki_ses_duzeyi():
    return "{:.2f}".format(anlik_ses_duzeyi.get())


def ses_degistir(event):
    cihaz = AudioUtilities.GetSpeakers()
    arayuz = cihaz.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    ses = cast(arayuz, POINTER(IAudioEndpointVolume))
    ses.SetMasterVolumeLevel(-float(simdiki_ses_duzeyi()), None)


stil = ttk.Style()
stil.configure("TScale", background="#f4f5f5")
ses = ttk.Scale(sag_bolum, from_=25, to=0, orient="horizontal",
                command=ses_degistir, variable=anlik_ses_duzeyi)
ses.place(x=90, y=150)
ses.set(20)

# Parlaklık
lbl_parlaklik = Label(sag_bolum, text="Parlaklık",
                      font=("arial", 10, "bold"), bg="#f4f5f5")
lbl_parlaklik.place(x=10, y=190)

anlik_parlaklik = tk.DoubleVar()


def simdiki_parlaklik():
    return "{:.2f}".format(anlik_parlaklik.get())


def parlaklik_degistir(event):
    pct.set_brightness(simdiki_parlaklik())


parlaklik = ttk.Scale(sag_bolum, from_=0, to=100, orient="horizontal",
                      command=parlaklik_degistir, variable=anlik_parlaklik)
parlaklik.place(x=90, y=190)

#####UYGULAMA FONKSİYONLARI#####

#HAVA DURUMU#


def hava_durumu():
    hava_uygulama = Toplevel()
    hava_uygulama.title("Hava Durumu")
    hava_uygulama.geometry("900x500+300+200")
    hava_uygulama.resizable(False, False)

    def hava_durumunu_getir():
        try:
            sehir = yazi_alani.get()

            yer_bulucu = Nominatim(user_agent="havaDurumu")
            lokasyon = yer_bulucu.geocode(sehir)

            obje = TimezoneFinder()
            sonuc = obje.timezone_at(
                lng=lokasyon.longitude, lat=lokasyon.latitude)

            konum = pytz.timezone(sonuc)
            yerel_zaman = datetime.now(konum)
            zaman = yerel_zaman.strftime('%H:%M')
            saat.config(text=zaman)
            baslik.config(text="YEREL SAAT")

            # Hava Durumu
            api_key = "caa39983056377866ffffccd4779da5b"
            api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
                sehir + "&appid=" + api_key + "&lang=tr"

            json_data = requests.get(api).json()
            tanim = json_data["weather"][0]["description"].title()
            sicaklik = int(json_data["main"]["temp"] - 273.15)
            basinc = json_data["main"]["pressure"]
            nem = json_data["main"]["humidity"]
            ruzgar = json_data["wind"]["speed"]

            s.config(text=(sicaklik, "°"))
            r.config(text=(ruzgar, "km/sa"))
            n.config(text=("%", nem))
            t.config(text=tanim)
            b.config(text=(basinc, "hPa"))

        except Exception as e:
            messagebox.showerror("Hava Durumu", "Geçersiz Giriş!")

    # Icon
    havadurumu_icon = PhotoImage(file="images/havadurumu.png")
    hava_uygulama.iconphoto(False, havadurumu_icon)

    # Arama Kutusu
    arama_kutusu_png = PhotoImage(file="images/search.png")
    arama_kutusu = Label(hava_uygulama, image=arama_kutusu_png)
    arama_kutusu.place(x=20, y=20)

    yazi_alani = tk.Entry(hava_uygulama, justify="center", width=17, font=(
        "poppins", 25, "bold"), bg="#404040", border=0, fg="white")
    yazi_alani.place(x=50, y=35)
    yazi_alani.focus()

    arama_iconu_png = PhotoImage(file="images/search_icon.png")
    arama_iconu = Button(hava_uygulama, image=arama_iconu_png, borderwidth=0,
                         cursor="hand2", bg="#404040", command=hava_durumunu_getir)
    arama_iconu.place(x=400, y=34)

    # Logo
    logo_png = PhotoImage(file="images/logo.png")
    logo = Label(hava_uygulama, image=logo_png)
    logo.place(x=150, y=100)

    # Alt Alan
    alt_alan_png = PhotoImage(file="images/box.png")
    alt_alan = Label(hava_uygulama, image=alt_alan_png)
    alt_alan.pack(padx=5, pady=5, side=BOTTOM)

    # Zaman
    baslik = Label(hava_uygulama, font=("arial", 15, "bold"))
    baslik.place(x=30, y=100)
    saat = Label(hava_uygulama, font=("Helvetica", 20))
    saat.place(x=30, y=130)

    # Alt Alan Labels
    label1 = Label(hava_uygulama, text="RÜZGAR", font=(
        "Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
    label1.place(x=130, y=400)
    label2 = Label(hava_uygulama, text="NEM", font=(
        "Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
    label2.place(x=320, y=400)
    label3 = Label(hava_uygulama, text="DURUM", font=(
        "Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
    label3.place(x=470, y=400)
    label4 = Label(hava_uygulama, text="BASINÇ", font=(
        "Helvetica", 15, "bold"), fg="white", bg="#1ab5ef")
    label4.place(x=680, y=400)

    s = Label(hava_uygulama, font=("arial", 70, "bold"), fg="#ee666d")
    s.place(x=415, y=150)
    r = Label(hava_uygulama, text="...", font=(
        "arial", 10, "bold"), bg="#1ab5ef")
    r.place(x=130, y=430)
    n = Label(hava_uygulama, text="...", font=(
        "arial", 10, "bold"), bg="#1ab5ef")
    n.place(x=320, y=430)
    t = Label(hava_uygulama, text="...", font=(
        "arial", 10, "bold"), bg="#1ab5ef")
    t.place(x=470, y=430)
    b = Label(hava_uygulama, text="...", font=(
        "arial", 10, "bold"), bg="#1ab5ef")
    b.place(x=680, y=430)

    hava_uygulama.mainloop()

#SAAT#


def saat_func():
    saat_uygulamasi = Toplevel()
    saat_uygulamasi.geometry("850x110+300+10")
    saat_uygulamasi.title("Saat")
    saat_uygulamasi.configure(bg="#292e2e")
    saat_uygulamasi.resizable(False, False)

    # Icon
    saat_icon = PhotoImage(file="images/saat.png")
    saat_uygulamasi.iconphoto(False, saat_icon)

    def saat_():
        saatt = strftime("%H:%M:%S")
        lbl.config(text=saatt)
        lbl.after(1000, saat_)

    lbl = Label(saat_uygulamasi, font=("digital-7", 50, "bold"),
                width=20, bg="#f4f5f5", fg="#292e2e")
    lbl.pack(anchor="center", pady=20)

    saat_()
    saat_uygulamasi.mainloop()

#TAKVİM#


def takvim_func():
    takvim_uygulamasi = Toplevel()
    takvim_uygulamasi.geometry("300x300+-10+10")
    takvim_uygulamasi.title("Takvim")
    takvim_uygulamasi.configure(bg="#292e2e")
    takvim_uygulamasi.resizable(False, False)

    # Icon
    takvim_icon = PhotoImage(file="images/takvim.png")
    takvim_uygulamasi.iconphoto(False, takvim_icon)

    takvimim = Calendar(takvim_uygulamasi, setmode="day",
                        date_pattern="d/m/yy")
    takvimim.pack(padx=15, pady=35)

    takvim_uygulamasi.mainloop()


#MOD#
mod_butonu = True


def mod():
    global mod_butonu
    if mod_butonu:
        sol_bolum.config(bg="#292e2e")
        hp.config(bg="#292e2e")
        l1.config(bg="#292e2e", fg="#d6d6d6")
        l2.config(bg="#292e2e", fg="#d6d6d6")
        l3.config(bg="#292e2e", fg="#d6d6d6")
        l4.config(bg="#292e2e", fg="#d6d6d6")
        l5.config(bg="#292e2e", fg="#d6d6d6")

        alt_sag_bolum.config(bg="#292e2e")
        uygulamalar.config(bg="#292e2e", fg="#d6d6d6")
        havadurumu.config(bg="#292e2e")
        saat.config(bg="#292e2e")
        takvim.config(bg="#292e2e")
        gecemodu.config(bg="#292e2e")
        kizmabirader.config(bg="#292e2e")
        kamera.config(bg="#292e2e")
        dosyalar.config(bg="#292e2e")
        google.config(bg="#292e2e")
        kapat.config(bg="#292e2e")

        mod_butonu = False
    else:
        sol_bolum.config(bg="#f4f5f5")
        hp.config(bg="#f4f5f5")
        l1.config(bg="#f4f5f5", fg="#292e2e")
        l2.config(bg="#f4f5f5", fg="#292e2e")
        l3.config(bg="#f4f5f5", fg="#292e2e")
        l4.config(bg="#f4f5f5", fg="#292e2e")
        l5.config(bg="#f4f5f5", fg="#292e2e")

        alt_sag_bolum.config(bg="#f4f5f5")
        uygulamalar.config(bg="#f4f5f5", fg="#292e2e")
        havadurumu.config(bg="#f4f5f5")
        saat.config(bg="#f4f5f5")
        takvim.config(bg="#f4f5f5")
        gecemodu.config(bg="#f4f5f5")
        kizmabirader.config(bg="#f4f5f5")
        kamera.config(bg="#f4f5f5")
        dosyalar.config(bg="#f4f5f5")
        google.config(bg="#f4f5f5")
        kapat.config(bg="#f4f5f5")

        mod_butonu = True

#KIZMABİRADER#


def oyun():
    kizmabirader_uygulamasi = Toplevel()
    kizmabirader_uygulamasi.geometry("350x500+1170+170")
    kizmabirader_uygulamasi.title("Kızma Birader")
    kizmabirader_uygulamasi.configure(bg="#dee2e5")
    kizmabirader_uygulamasi.resizable(False, False)

    # Icon
    kizmabirader_icon = PhotoImage(file="images/kızmabirader.png")
    kizmabirader_uygulamasi.iconphoto(False, kizmabirader_icon)

    kizmabirader_img = PhotoImage(file="images/kızmabirader2.png")
    Label(kizmabirader_uygulamasi, image=kizmabirader_img).pack()

    label = Label(kizmabirader_uygulamasi, text="", font=("times", 150))

    def zarAt():
        zar = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685", ]
        label.config(
            text=f"{random.choice(zar)}{random.choice(zar)}", fg="#29232e")
        label.pack()

    buton_img = PhotoImage(file="images/zar_at.png")
    buton = Button(kizmabirader_uygulamasi, image=buton_img,
                   bg="#dee2e5", command=zarAt)
    buton.pack(padx=10, pady=10)

    kizmabirader_uygulamasi.mainloop()

#EKRAN ALINTISI#


def ekranAlintisi():
    root.iconify()

    ekran_alintisi = pyautogui.screenshot()
    dosya_yolu = filedialog.asksaveasfilename(defaultextension = ".png")
    ekran_alintisi.save(dosya_yolu)

#DOSYALAR - GOOGLE - INSTAGRAM - KAPAT#


def dosya():
    subprocess.Popen(r"explorer /select,'C:\path\of\folder\file'")


def chrome():
    wb.register("chrome", None)
    wb.open("https://www.google.com.tr/")


def insta():
    wb.register("chrome", None)
    wb.open("https://www.instagram.com/bburakcode/")


def pencereyiKapat():
    root.destroy()


#####SAĞ ALT BÖLÜM#####
alt_sag_bolum = Frame(body, width=470, height=190, bg="#f4f5f5",
                      highlightbackground="#adacb1", highlightthickness=1)
alt_sag_bolum.place(x=330, y=255)

uygulamalar = Label(alt_sag_bolum, text="Uygulamalar", font=(
    "Acumin Variable Concept", 15), bg="#f4f5f5")
uygulamalar.place(x=10, y=10)

havadurumu_png = PhotoImage(file="images/havadurumu.png")
havadurumu = Button(alt_sag_bolum, image=havadurumu_png,
                    bd=0, command=hava_durumu)
havadurumu.place(x=15, y=50)

saat_png = PhotoImage(file="images/saat.png")
saat = Button(alt_sag_bolum, image=saat_png, bd=0, command=saat_func)
saat.place(x=100, y=50)

takvim_png = PhotoImage(file="images/takvim.png")
takvim = Button(alt_sag_bolum, image=takvim_png, bd=0, command=takvim_func)
takvim.place(x=185, y=50)

gecemodu_png = PhotoImage(file="images/gecemodu.png")
gecemodu = Button(alt_sag_bolum, image=gecemodu_png, bd=0, command=mod)
gecemodu.place(x=270, y=50)

kizmabirader_png = PhotoImage(file="images/kızmabirader.png")
kizmabirader = Button(
    alt_sag_bolum, image=kizmabirader_png, bd=0, command=oyun)
kizmabirader.place(x=355, y=50)

kamera_png = PhotoImage(file="images/kamera.png")
kamera = Button(alt_sag_bolum, image=kamera_png, bd=0, command=ekranAlintisi)
kamera.place(x=15, y=120)

dosyalar_png = PhotoImage(file="images/dosyalar.png")
dosyalar = Button(alt_sag_bolum, image=dosyalar_png, bd=0, command=dosya)
dosyalar.place(x=100, y=120)

google_png = PhotoImage(file="images/google.png")
google = Button(alt_sag_bolum, image=google_png, bd=0, command=chrome)
google.place(x=185, y=120)

instagram_png = PhotoImage(file="images/instagram.png")
instagram = Button(alt_sag_bolum, image=instagram_png, bd=0, command=insta)
instagram.place(x=270, y=120)

kapat_png = PhotoImage(file="images/kapat.png")
kapat = Button(alt_sag_bolum, image=kapat_png, bd=0, command=pencereyiKapat)
kapat.place(x=355, y=120)

batarya_bilgileri()
root.mainloop()
