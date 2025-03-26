import cv2
import numpy as np
import time
from collections import Counter

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    return

def zmanjsaj_sliko(slika, sirina, visina):
    return

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    return

def prikazi_skatle(slika, seznam_skatel, sirina_skatle, visina_skatle):
    return

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    return

def zajemi_kalibracijsko_sliko(sirina_kamere, visina_kamere, levo_zg_x, levo_zg_y, desno_sp_x, desno_sp_y):
    kamera = cv2.VideoCapture(0)
    kamera.set(cv2.CAP_PROP_FRAME_WIDTH, sirina_kamere)
    kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, visina_kamere)
    
    while True:
        ret, okvir = kamera.read()
        if not ret:
            break
        
        okvir = cv2.flip(okvir, 1)
        cv2.rectangle(okvir, (levo_zg_x-10, levo_zg_y-10), (desno_sp_x+10, desno_sp_y+10), (0, 255, 0), 1)

        cv2.imshow('Kamera', okvir)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            zajeta_slika = okvir.copy()
            print("Slika zajeta!")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            zajeta_slika = None
            break

    kamera.release()
    cv2.destroyAllWindows()
    
    return zajeta_slika

def main():
    sirina_kamere, visina_kamere = 640, 480
    levo_zgoraj = [int(sirina_kamere / 5)*2, int(visina_kamere / 7)*2]
    desno_spodaj = [int((sirina_kamere / 5)*3), int((visina_kamere / 7)*5)]
    sirina_skatle, visina_skatle = int(sirina_kamere/20), int(visina_kamere/20)

    slika = zajemi_kalibracijsko_sliko(sirina_kamere, visina_kamere, levo_zgoraj[0], levo_zgoraj[1], desno_spodaj[0], desno_spodaj[1])
    return

if __name__ == "__main__":
    main()