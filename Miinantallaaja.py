import random
import time
import pyglet
import haravasto


#sanakirja hiiren painikkeille, jossa avaimet poimittu haravastosta
painikkeet = {
    haravasto.HIIRI_VASEN: "vasen",
    haravasto.HIIRI_KESKI: "keski",\
    haravasto.HIIRI_OIKEA: "oikea"
    }

#sanakirja, johon tallentuu kentan tilanne
tila = {
    "kentta": None,
    "kentta2": None,
    "liput": None,
    "miinat": None,
    "aloitus": None
    }

def kasittele_hiiri(x, y, painike, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
    """

    x = int(x / 40)
    y = int(y / 40)
    if painike == haravasto.HIIRI_VASEN:
        avaa_ruutu(x, y)
    elif painike == haravasto.HIIRI_OIKEA:
        sijoita_lippu(x, y)
    #print("Hiiren nappia {} painettiin kohdassa {}, {}".format(painikkeet[painike], x, y))

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """

    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()
    for k, rivi in enumerate(tila["kentta2"]):
        for l, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, l * 40, k * 40)
    haravasto.piirra_ruudut()

def miinoita(kentta, ruudut, miinat):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """

    miinojen_maara = []
    for i, j in random.sample(ruudut, miinat):
        kentta[j][i] = "x"
        miinojen_maara.append((i, j))
        
    tila["miinat"] = miinojen_maara
    tila["kentta"] = kentta

def laske_numerot(x, y, kentta):
    """
    Asettaa numerot miinojen ympärille
    """

    miinat = 0                              #miinojen maara alussa
    for i in range(y-1, y+2):               #tarkistetaan loopilla ruudut (4 kpl) valitun x,y ruudun ymparilta
        for j in range(x-1, x+2):           #tarkistetaan loopilla ruudut (4 kpl) valitun x,y ruudun ymparilta
            if 0 <= i < len(kentta):        #tarkistetaan, etta ollaan huoneen sisalla
                if 0 <= j < len(kentta[i]): #tarkistetaan, etta ollaan huoneen sisalla
                    if kentta[i][j] == "x": #jos ruudussa on miina
                        miinat += 1         #lisataan lopputulokseen yksi miina
    
    #print("Ruutua {},{} ympäröi {} miinaa.".format(i, j, miinat))
    return miinat

def tulvataytto(kentta, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """

    kentta2 = tila["kentta2"]
    if kentta[y][x] == "x": #jos ruudussa on miina, palaa loopin alkuun
        return
    else:  
        fill = [(x, y)]                                             #tayta ruutu x, y
        fill_lista = [(x, y)]
        while len(fill) > 0:                                        #tayton tapahtuessa, tee seuraavasti
            x, y = fill.pop()
            if laske_numerot(x, y, kentta) == 0:                    #jos koordinaatissa x, y on nolla
                kentta[y][x] = "0"                                  #koordinaatissa on nolla
            else:                                                   #muutoin
                kentta[y][x] = str(laske_numerot(x, y, kentta))     #koordinaatissa on miinojen määrä
                continue
            #tutkitaan kentasta kaikki ruudut ja avataan jos ovat nollia
            for l in range(max(0, y - 1), min(len(kentta), y + 2)):
                for k in range(max(0, x - 1), min(len(kentta[0]), x + 2)):
                    if laske_numerot(k, l, kentta) == 0:
                        if (k, l) not in fill_lista:
                            fill.append((k, l))                     #lista tyhjista ruuduista
                            fill_lista.append((k, l))               #lista tyhjista ruuduista, josta katsotaan ymparoivat numerot

            #tutkitaan ymparoivat numerot, jotta saadaan myos ne auki
            for x, y in fill_lista:
                for l in range(max(0, y - 1), min(len(kentta), y + 2)):
                    for k in range(max(0, x - 1), min(len(kentta[0]), x + 2)):
                        miinat = (laske_numerot(k, l, kentta))
                        kentta2[l][k] = miinat                      #tallennetaan numerot myos kenttaan2, jotta avautuvat
                        kentta[l][k] = miinat

def avaa_ruutu(x, y):

    tarkista_havio(x, y)
    #jos on lippu, poistaa sen
    if (x, y) == tila["liput"]:
        tila["liput"].remove((x, y))
        #näytä ruutu
        tila["kentta2"][y][x] = tila["kentta"][y][x]
        piirra_kentta()

    #pelilogiikka
    if tila["kentta2"][y][x] == " ":
        if laske_numerot(x, y, kentta) > 0:
            kentta[y][x] = str(laske_numerot(x, y, kentta))
            tila["kentta2"][y][x] = tila["kentta"][y][x]
        if laske_numerot(x, y, kentta) == 0:
            tulvataytto(kentta, x, y)
        if tila["kentta"][y][x] != "x" and tila["kentta2"][y][x] != "f":
            tila["kentta2"][y][x] = tila["kentta"][y][x]
    piirra_kentta()

def sijoita_lippu(x, y):

    #tarkistaa onko ruutu tyhjä
    if tila["kentta2"][y][x] == " ":
        tila["kentta2"][y][x] = "f"
        tila["liput"].append((x, y))
        tarkista_voitto(x, y)

    #poistaa lipun
    elif tila["kentta2"][y][x] == "f":
        tila["kentta2"][y][x] = " "
        tila["liput"].remove((x, y))
        print(tila["liput"])
    else:
        print("Ei voi asettaa lippua")

    piirra_kentta()

def tarkista_voitto(x, y):

    #tarkistaa onko liput samoissa paikoissa kuin miinat
    if set(tila["liput"]) == set(tila["miinat"]):
        print("Voitit pelin")
        print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))
        piirra_kentta()


def tarkista_havio(x, y):

    #tarkistaa onko painetussa kohdassa miina
    if tila["kentta"][y][x] == "x":
        print("Hävisit pelin")
        print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))

        #avaa koko kentan pelin paattyessa
        for y, rivi in enumerate(tila["kentta2"]):
            for x, ruutu in enumerate(rivi):
                    if tila["kentta"][y][x] == "x":
                        continue
                    tila["kentta"][y][x] = str(laske_numerot(x, y, kentta))

        tila["kentta2"] = tila["kentta"]
        piirra_kentta()

def aloita_kello():

    #aloittaa sekunttikellon
    tila["aloitus"] = time.time()

def lopeta_kello():

    #lopettaa sekunttikellon
    loppuaika = time.time()
    total = loppuaika - tila["aloitus"]
    return total

def main(kentta):
    """
    Luo sovellusikkunan ja asettaa käsittelijäfunktion hiiren klikkauksille.
    Käynnistää sovelluksen.
    """

    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(tila["kentta2"][1] * 40), len(tila["kentta2"] * 40)) #luo kentan kokoisen ikkunan
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    aloita_kello()
    haravasto.aloita()

if __name__ == "__main__":

    pituus = int(input("Anna kentän leveys: "))
    korkeus = int(input("Anna kentän korkeus: "))
    miinat = int(input("Anna miinojen lukumäärä: "))
    xkoor = int(input("Anna aloituspisteen x-koordinaatti: "))
    ykoor = int(input("Anna aloituspisteen y-koordinaatti: "))
    
    #luodaan kentta ja kentta2
    #kentta2 peittaa kentan, jossa miinat ja numerot
    kentta = []
    kentta2 = []
    for rivi in range(korkeus):
        kentta.append([])
        kentta2.append([])
        for sarake in range(pituus):
            kentta[-1].append(" ")
            kentta2[-1].append(" ")

    #lista vapaista ruuduista
    jaljella = []
    jaljella2 = []
    for x in range(pituus):
        for y in range(korkeus):
            jaljella.append((x, y))
            jaljella2.append((x, y))

    #tallennetaan tilanne sanakirjaan
    tila["liput"] = []
    tila["kentta"] = kentta
    tila["kentta2"] = kentta2
    
    miinoita(kentta, jaljella, miinat)
    tulvataytto(kentta, xkoor, ykoor)
    main(kentta)