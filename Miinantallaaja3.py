import pyglet
import random
import haravasto
import time

#sanakirja hiiren painikkeille, jossa avaimet poimittu haravastosta
painikkeet = {
    haravasto.HIIRI_VASEN: "vasen",
    haravasto.HIIRI_KESKI: "keski",
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
    print("Hiiren nappia {} painettiin kohdassa {}, {}".format(painikkeet[painike], x, y))

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
    miinat = 0 #miinojen maara alussa
    for i in range(y-1, y+2): #tarkistetaan loopilla ruudut (4 kpl) valitun x,y ruudun ymparilta
        for j in range(x-1, x+2): #tarkistetaan loopilla ruudut (4 kpl) valitun x,y ruudun ymparilta
            if 0 <= i < len(kentta): #tarkistetaan, etta ollaan huoneen sisalla    
                if 0 <= j < len(kentta[i]): #tarkistetaan, etta ollaan huoneen sisalla    
                    if kentta[i][j] == "x": #jos ruudussa on miina
                        miinat += 1 #lisataan lopputulokseen yksi miina                   
    
    print("Ruutua {},{} ympäröi {} miinaa.".format(i, j, miinat))
    return miinat

def tarkista_voitto(x, y):
    #tarkistaa onko liput samoissa paikoissa kuin miinat
    if set(tila["liput"]) == set(tila["miinat"]):
        print("Voitit pelin")
        print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))
        piirra_kentta()

def sijoita_lippu(x, y):
	# Tarkistaa onko ruutu tyhjä
	if tila["kentta2"][y][x] == " ":
		tila["kentta2"][y][x] = "f"
		tila["liput"].append((x, y))
		tarkista_voitto(x, y)
	# Poistaa lipun
	elif tila["kentta2"][y][x] == "f":
		tila["kentta2"][y][x] = " "
		tila["liput"].remove((x, y))
		print(tila["liput"])
	else:
		print("Ei voi asettaa lippua")

	piirra_kentta()

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    haravasto.tyhjaa_ikkuna()
    haravasto.aloita_ruutujen_piirto()
    for k, rivi in enumerate(tila["kentta"]):
        for l, ruutu in enumerate(rivi):
            haravasto.lisaa_piirrettava_ruutu(ruutu, l * 40, k * 40)
    haravasto.piirra_ruudut()

def tulvataytto(kentta, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    #kentta2 = tila["kentta2"] #paljastaa kaikki numerot tarkistusta varten
    if kentta[y][x] == "x": #jos ruudussa on miina, palaa loopin alkuun
        return
    else: #muutoin   
        fill = [(x, y)] #tayta ruutu x, y 
        while len(fill) > 0: #tayton tapahtuessa, tee seuraavasti
            x, y = fill.pop() #removes and returns last value from the list or the given index value
            if 0 == laske_numerot(x, y, kentta):
                kentta[y][x] = "0"
            else:
                kentta[y][x] = str(laske_numerot(x, y, kentta))
                continue

            for l in range(max(0, y - 1), min(len(kentta), y + 2)): #kaydaan lapi kaikki sarakkeet
                for k in range(max(0, x - 1), min(len(kentta[0]), x + 2)): #kaydaan lapi kaikki rivit
                    if kentta[l][k] == " ": #jos ruutu on tyhja
                        fill.append((k, l)) #tayta ruutu
                        if kentta[y][x] != "x" and kentta2[y][x] != "f":
                            kentta2[y][x] = kentta[y][x]
                        #miinat = str(laske_numerot(k, l, kentta))
                        #kentta[l][k] = miinat #tayttaa ruudun miinojen maaralla
                        #kentta2[l][k] = miinat             

def tarkista_havio(x, y):
	#tarkistaa onko painetussa kohdassa miina
	if tila["kentta"][y][x] == "x":
		print("Hävisit pelin")
		print("Aikaa kului: {:.2f} sekunttia".format(lopeta_kello()))
		tila["kentta2"] = tila["kentta"]
		piirra_kentta()

def aloita_kello():
	# Aloittaa sekunttikellon
	tila["aloitus"] = time.time()

def lopeta_kello():
	# Lopettaa sekunttikellon
	loppuaika = time.time()
	total = loppuaika - tila["aloitus"]
	return total

def avaa_ruutu(x, y):
    tarkista_havio(x, y)
	#jos on lippu, poistaa sen
    if (x, y) == tila["liput"]:
        tila["liput"].remove((x, y))
        #näytä ruutu
        tila["kentta2"][y][x] = tila["kentta"][y][x] 
        piirra_kentta()

    if tila["kentta2"][y][x] == " ":
        #if int(tila["kentta"][x][y]) > 0:
            #tila["kentta2"][x][y] = tila["kentta"][x][y] 
        #if tila["kentta"][x][y] == "0":
        tulvataytto(kentta, x, y)
        #if tila["kentta"][x][y] != "x" and tila["kentta2"][x][y] != "f":
            #tila["kentta2"][x][y] = tila["kentta"][x][y]    
        #piirra_kentta()       

def main(kentta):
    """
    Luo sovellusikkunan ja asettaa käsittelijäfunktion hiiren klikkauksille.
    Käynnistää sovelluksen.
    """
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(tila["kentta2"] * 40), len(tila["kentta2"][0] * 40)) #luo kentan kokoisen ikkunan
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri) 
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    aloita_kello()
    haravasto.aloita()
    
if __name__ == "__main__":
 
    
    pituus = int(input("Anna kentän leveys: ")) #try/except kentta ei saa olla korkeampi kuin on leveä
    korkeus = int(input("Anna kentän korkeus: "))
    miinat = int(input("Anna miinojen lukumäärä: ")) #jos ei int, sanoo anna kokonaisluku ja nollaa ei saa hyväksyä
    xkoor = int(input("Anna aloituspisteen x-koordinaatti: "))
    ykoor = int(input("Anna aloituspisteen y-koordinaatti: "))
    
    kentta = [] #luodaan kentta
    kentta2 = [] #luodaan toinen kentta, jonka avulla peitetaan miinat
    for rivi in range(korkeus): #korkeus                           
        kentta.append([])
        kentta2.append([])
        for sarake in range(pituus): #leveys
            kentta[-1].append(" ")
            kentta2[-1].append(" ")

    jaljella = [] #lista vapaista ruuduista
    jaljella2 = []
    for x in range(pituus): #leveys
        for y in range(korkeus): #korkeus        
            jaljella.append((x, y)) 
            jaljella2.append((x, y))

    tila["liput"] = []
    tila["kentta"] = kentta
    tila["kentta2"] = kentta2
    
    miinoita(kentta, jaljella, miinat)
    tulvataytto(kentta, xkoor, ykoor)
    main(kentta)