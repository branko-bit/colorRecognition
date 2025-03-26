import cv2
import numpy as np
import time
from collections import Counter

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj):
    obraz = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
    barve = obraz.reshape(-1, 3)#visina*sirina*3
    
    #doloci najpogostejso barvo
    najpogostejse_barve = Counter(map(tuple, barve))#zato gre v map ker counter nemore prebrati numpy arraya
    najpogostejsa_barva = najpogostejse_barve.most_common(1)[0][0]#[0]da nedobim vsega sam barvo

    #upostevanje tolerance
    toleranca = np.array([20, 20, 20])
    spodnja_meja = np.array(najpogostejsa_barva) - toleranca
    zgornja_meja = np.array(najpogostejsa_barva) + toleranca
    
    #preprica se da so barve znotraj pravih mej
    spodnja_meja = np.clip(spodnja_meja, 0, 255)
    zgornja_meja = np.clip(zgornja_meja, 0, 255)

    #tu imam testno samo da vidim katere barve so bile zaznane
    def prikazi_barvo(barva, ime_okna):
        barva_slike = np.zeros((100, 100, 3), dtype=np.uint8) #100x100 + BGR
        barva_slike[:] = barva #vse piksle nastavi
        cv2.imshow(ime_okna, barva_slike)
    
    prikazi_barvo(spodnja_meja, 'Spodnja meja')
    prikazi_barvo(zgornja_meja, 'Zgornja meja')
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return (spodnja_meja, zgornja_meja)

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

    if slika is not None:
        barva_koze = doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj)
    else:
        print("Slika ni bila zajeta.")
        return

    return

if __name__ == "__main__":
    main()