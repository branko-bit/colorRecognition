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
    return cv2.resize(slika, (sirina, visina))

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    visina, sirina = slika.shape[:2]
    seznam_skatel = []
    #gre cez vsako skatlo na sliki in klice prestej_piksle_z_barvo_koze() za vsako skatlo
    for y in range(0, visina, visina_skatle):
        for x in range(0, sirina, sirina_skatle):
            skatla = slika[y:y + visina_skatle, x:x + sirina_skatle]
            stevilo_pikslov_koze = prestej_piksle_z_barvo_koze(skatla, barva_koze)
            skupno_stevilo_pikslov = skatla.shape[0] * skatla.shape[1] #visina*sirina
            odstotek_koze = stevilo_pikslov_koze / skupno_stevilo_pikslov

            if odstotek_koze >= 0.7:
                seznam_skatel.append(((x, y), stevilo_pikslov_koze))

    return seznam_skatel

def prikazi_skatle(slika, seznam_skatel, sirina_skatle, visina_skatle):
    for (x, y), stevilo_pikslov_koze in seznam_skatel:
        cv2.rectangle(slika, (x, y), (x + sirina_skatle, y + visina_skatle), (0, 255, 0), 2)

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    #prejme posamezno skatlo in presteje piksle ki so znotraj barve koze
    spodnja_meja, zgornja_meja = barva_koze
    maska = cv2.inRange(slika, spodnja_meja, zgornja_meja) #use piksle zntori mej da na 255 ostale na 0
    stevilo_pikslov_koze = cv2.countNonZero(maska)
    return stevilo_pikslov_koze

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

    kamera = cv2.VideoCapture(0)
    kamera.set(cv2.CAP_PROP_FRAME_WIDTH, sirina_kamere)
    kamera.set(cv2.CAP_PROP_FRAME_HEIGHT, visina_kamere)

    frame_count = 0
    start_time = time.time()

    while True:
        ret, okvir = kamera.read()
        if not ret:
            break

        #okvir = zmanjsaj_sliko(okvir, 220, 340)

        frame_count += 1
        end_time = time.time()
        fps = frame_count / (end_time - start_time)

        okvir = cv2.flip(okvir, 1)
        seznam_skatel = obdelaj_sliko_s_skatlami(okvir, sirina_skatle, visina_skatle, barva_koze)

        #stetje fpsa
        cv2.putText(okvir, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        cv2.imshow('Kamera', okvir)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    kamera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()