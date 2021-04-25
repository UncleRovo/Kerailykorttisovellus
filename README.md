# KERÄILYKORTTISOVELLUS

Sovellusta voi testata: https://kerailykorttisovellus.herokuapp.com/
**HUOM! Jos "Luo tunnus" -vaihtoehtoa klikatessa tapahtuu palvelinvirhe,** kokeile kirjautua millä tahansa käyttäjällä (kuten alempana mainitulla admin-käyttäjällä), kirjautua ulos ja luoda tunnusta uudelleen. 

Sovelluksessa on valmiina järjestelmänvalvojan tunnukset seuraavasti: käyttäjänimi = admin , salasana = adminpassword 

Keräilykorttisovelluksella on kaksi käyttäjää, peruskäyttäjä sekä ylläpitäjä. Sovelluksen tarkoituksena on tarjota käyttäjilleen palvelu, jossa voi hankkia, katsella ja vaihtaa erilaisia keräilykortteja.

## Toteutetut ominaisuudet

- järjestelmä pitää kirjaa eri keräilykorteista, joilla on nimi, elementti, harvinaisuustaso (1 - 3), kuvaus, sekä ID.
- peruskäyttäjä voi luoda tilin ja kirjautua sinne
- ylläpitäjä (admin) voi tarkastella olemassaolevia keräilykortteja sekä lisätä niitä järjestelmään

## Suunnitellut ominaisuudet

#### Itse järjestelmä:

- järjestää korttien vaihtamisen ja yksityisviestit eri käyttäjien välillä
- pitää kirjaa käyttäjistä sekä heidän tiedoistaan, kuten lähetettyjen viestien määrästä ja heidän omistamistaan sovelluksen sisäisistä hyödykkeist

#### Peruskäyttäjä voi:

- Tilin luonnin yhteydessä käyttäjälle myönnetään 5 sovelluksen sisäistä kolikkoa
- tarkistaa kolikkomääränsä sekä hankkia sovelluskolikoita syöttämällä järjestelmään oikean 9-merkkisen koodin
- vaihtoehtoisesti kolikoita saa 1kpl per 20 vaihtoa ja/tai yksityisviestiä
- tarkistaa yksityisviestinsä sekä vaihtopyynnöt muilta käyttäjiltä
- tarkastella muiden käyttäjien keräilykortteja
- ostaa satunnaisen keräilykortin 1 kolikolla. 
- ostaa 3 kolikolla satunnaisen kortin niin, että kaikista yleisempien korttien saamismahdollisuus puolittuu
- katsella yksittäisten omistamiensa keräilykorttien tietoja tekstuaalisessa muodossa
- katsella tilastoja omistamistaan korteista, kuten harvinaisten korttien määrä, duplikaatit sekä prosenttiosuus siitä, kuinka lähellä on kaikkien korttien keräämistä
- lähettää muille käyttäjille vaihtopyyntöjä sekä yksityisviestejä
- lukea ylläpitäjän ilmoituksia

#### Ylläpitäjä voi:

- tarkastella käyttäjiä sekä heidän tietojaan
- kirjoittaa ilmoituksia muille käyttäjille sekä poistaa niitä
- deaktivoida kenen tahansa käyttäjän tilin
- lähettää yksityisviestejä
- poistaa keräilykortteja
- tarkastella kolikkokoodeja (mahdollista myöntämistä varten?)
- antaa ja poistaa käyttäjille/ltä kolikoita sekä kortteja mielivaltaisesti
