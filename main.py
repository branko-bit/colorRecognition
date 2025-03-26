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

    #testno izpisovanje da vidim kaksne so dejanske dimenzije...ker ce mi jih kamera ne podpira gre na neke default nastavitve
    actual_width = int(kamera.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(kamera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("Širina: ", actual_width)
    print("Višina: ", actual_height)

    kamera.release()
    cv2.destroyAllWindows()
    
    return 

def main():
    return

if __name__ == "__main__":
    main()