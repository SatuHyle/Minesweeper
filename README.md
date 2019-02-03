# Minesweeper - under development
Course Work

---Course Work Description in Finish---
Seuraavien tarkempien vaatimusten täyttämisen tarkoitus on osoittaa, että opiskelija on oppinut kurssilla käsitellyt asiat.

    * Pelitilanne esitetään pelaajalle ymmärrettävässä muodossa graafisesti
    * Pelaaja pystyy tekemään siirtoja hiirellä; siirtojen sääntöjenmukaisuus tarkistetaan ja laittomat siirrot 
      estetään
    * Peli päättyy kun päättymisehto täyttyy
    * Peli tallentaa tilastoja pelatuista peleistä: vähintään pelin ajankohdan (päivämäärä + kellonaika), keston 
      minuuteissa, keston vuoroissa ja lopputuloksen (voitto tai häviö, kentän koko ja miinojen lukumäärä). Tilastojen 
      kirjoitus ja lukeminen on toteuttu itse (ts. ei käytetä mitään valmista ratkaisua kuten SQLite tai Pickle)
    * Pelissä on alkuvalikko, josta voi valita uuden pelin, lopettamisen ja tilastojen katsomisen - huom! valikko 
      voi olla tekstipohjainen, ainoastaan itse peli-ikkunan tulee olla graafinen.
      
Työjärjestys grafiikan piirtämisessä annetulla kirjastolla (haravasto.py) on kaiken kaikkiaan seuraavanlainen:

    1. lataa peligrafiikat
    2. luo peli-ikkuna
    3. määrittele ja rekisteröi käsittelijäfunktiot
    4. käynnistä peli
