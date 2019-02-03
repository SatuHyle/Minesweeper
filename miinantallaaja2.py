import pyglet
import random
import haravasto

#sanakirja hiiren painikkeille, jossa avaimet poimittu haravastosta
painikkeet = {
    haravasto.HIIRI_VASEN: "vasen",
    haravasto.HIIRI_KESKI: "keski",
    haravasto.HIIRI_OIKEA: "oikea"
    }

#sanakirja, johon tallentuu kentan tilanne
tila = {
    "kentta": None,
    "kentta2": None
    }

def kasittele_hiiri(x, y, painike, muokkaus):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin.
    """
    print("Hiiren nappia {} painettiin kohdassa {}, {}".format(painikkeet[painike], x, y))

def miinoita(kentta, ruudut, miinat):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    for i, j in random.sample(ruudut, miinat):
        kentta[j][i] = "x"
        
def sijoita_numerot(x, y, kentta):
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

def tulvataytto(kentta, x, y):
    """
    Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten, että
    täyttö aloitetaan annetusta x, y -pisteestä.
    """
    kentta2 = tila["kentta2"] #paljastaa kaikki numerot vaikkei saisi
    if kentta[y][x] == "x": #jos ruudussa on miina, palaa loopin alkuun
        return
    else:    
        fill = [(x, y)] #tayta ruutu x, y 
        while fill: #tayton tapahtuessa, tee seuraavasti
            x, y = fill.pop() #removes and returns last value from the list or the given index value
            for l in range(max(0, y - 1), min(len(kentta), y + 2)): #kaydaan lapi kaikki sarakkeet
                for k in range(max(0, x - 1), min(len(kentta[0]), x + 2)): #kaydaan lapi kaikki rivit
                    if kentta[l][k] == " ": #jos ruutu on tyhja
                        fill.append((k, l)) #tayta ruutu
                        miinat = str(sijoita_numerot(k, l, kentta))
                        kentta[l][k] = miinat #tayttaa ruudun miinojen maaralla
                        kentta2[l][k] = miinat
def main(kentta):
    """
    Luo sovellusikkunan ja asettaa käsittelijäfunktion hiiren klikkauksille.
    Käynnistää sovelluksen.
    """
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(kentta[0])*40, len(kentta*40)) #luo kentan kokoisen ikkunan
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri) 
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aloita()
    
if __name__ == "__main__":
 
    
    kokox = int(input("Anna kentän leveys: ")) #try/except kentta ei saa olla korkeampi kuin on leveä
    kokoy = int(input("Anna kentän korkeus: "))
    miinat = int(input("Anna miinojen lukumäärä: ")) #jos ei int, sanoo anna kokonaisluku ja nollaa ei saa hyväksyä
    xkoor = int(input("Anna aloituspisteen x-koordinaatti: "))
    ykoor = int(input("Anna aloituspisteen y-koordinaatti: "))
    
    kentta = [] #luodaan kentta
    kentta2 = [] #luodaan toinen kentta, jonka avulla peitetaan miinat
    for rivi in range(kokoy): #korkeus                           
        kentta.append([])
        kentta2.append([])
        for sarake in range(kokox): #leveys
            kentta[-1].append(" ")
            kentta2[-1].append(" ")

    jaljella = [] #lista vapaista ruuduista
    jaljella2 = []
    for x in range(kokox): #leveys
        for y in range(kokoy): #korkeus        
            jaljella.append((x, y)) 
            jaljella2.append((x, y))    
    
    tila["kentta"] = kentta
    tila["kentta2"] = kentta2

    miinoita(kentta, jaljella, miinat)
    tulvataytto(kentta, xkoor, ykoor)
    main(kentta)