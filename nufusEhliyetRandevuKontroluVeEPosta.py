import ePostaYolla

import requests
from bs4 import BeautifulSoup as bs
import os
import time
import datetime
from base64 import b64decode
import webbrowser



def sayfaAc(bsSayfa):
    filename = "asd.html"
    # write the file
    open(filename, "w").write(bsSayfa.text)
    # open in the default browser
    webbrowser.open(filename)

def main():
    sayfaURL = r"https://randevu.nvi.gov.tr/default/index?type=2"
    requestURL = r"https://randevu.nvi.gov.tr/Controller/public/ProcessAppointmentStep1"


    with requests.Session() as oturum:
        bsSayfaMuhteva = bs(oturum.get(sayfaURL).content, "html.parser")
        token = bsSayfaMuhteva.find("input", {"name":"__RequestVerificationToken"}).attrs["value"]
        
        resim = bsSayfaMuhteva.find("img", {"class":"pull-right CaptchaImage"}).attrs["src"]

        header, encoded = resim.split(",", 1)
        data = b64decode(encoded)
        with open("capcak.png", "wb") as f:
            f.write(data)

        
        capcka = ePostaYolla.capkaYollaVeCevabiDon("capcak.png")
        while capcka == "tekra":
            capcka = ePostaYolla.capkaYollaVeCevabiDon("capcak.png")
        
        if capcka:


            randevuPostBilgileri = {
                "__RequestVerificationToken": token,
                "appointmentType": 2,
                "passportType": "",
                "FirstName": "isim",
                "LastName": "soyisim",
                "IdentityNo": "tckimlikno",
                "BirthDay": "dogumgunu",
                "BirthMonth": "ay",
                "BirthYear": "yil",
                "MobilePhone": "telefon",
                "CaptchaCode": capcka
            }
            oturum.post(requestURL, randevuPostBilgileri)
            time.sleep(1)

            oturum.get("https://randevu.nvi.gov.tr/default/step1")
            time.sleep(1)

            bsSehirSayfasiMuhteva = bs(oturum.get("https://randevu.nvi.gov.tr/default/step2").content, "html.parser")

            tokenSehirSayfasi = bsSehirSayfasiMuhteva.find("input", {"name":"__RequestVerificationToken"}).attrs["value"]
            sehirPostBilgileri = {
                "__RequestVerificationToken": tokenSehirSayfasi,
                "citySearch": "",
                "CityId": 6,
                "directorateSearch": ""
            }
            cevabp = oturum.post("https://randevu.nvi.gov.tr/default/step2", sehirPostBilgileri)
            sincaninIndeksi = cevabp.text.find("Sincan")
            cevabp = cevabp.text[sincaninIndeksi:]
            cevabp = cevabp[:cevabp.find("%")+10]
            ePostaYolla.stringYolla(cevabp)

#4 saatte bir kontrol yapma       
i = 0
while i < 3:
    main()
    time.sleep(60*60*4)