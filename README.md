# KERÄILYKORTTISOVELLUS

Sovelluksen 9. sunnuntain deadline: https://kerailykorttisovellus-final.herokuapp.com/

Sovelluksessa on valmiina järjestelmänvalvojan tunnukset seuraavasti: käyttäjänimi = admin , salasana = adminpassword 

Keräilykorttisovelluksella on kaksi käyttäjää, peruskäyttäjä sekä ylläpitäjä. Sovelluksen tarkoituksena on tarjota käyttäjilleen palvelu, jossa voi hankkia, katsella ja vaihtaa erilaisia keräilykortteja.

## Toteutetut ominaisuudet

- järjestelmä pitää kirjaa eri keräilykorteista, joilla on nimi, elementti, harvinaisuustaso (Kulta - Hopea - Pronssi), kuvaus, sekä ID
- peruskäyttäjä voi luoda tilin ja kirjautua sinne
- ylläpitäjä (admin) voi tarkastella olemassaolevia keräilykortteja sekä lisätä niitä järjestelmään
- Sovellys järjestää korttien vaihtamisen ja yksityisviestit eri käyttäjien välillä
- Tilin luonnin yhteydessä käyttäjälle myönnetään 5 sovelluksen sisäistä kolikkoa
- Käyttäjä tarkistaa kolikkomääränsä sekä hankkia sovelluskolikoita syöttämällä järjestelmään oikean 9-merkkisen koodin
- Käyttäjä voi ostaa satunnaisen keräilykortin 1 kolikolla.
- Käyttäjä lukea ylläpitäjän ilmoituksia
- Ylläpitäjä poistaa keräilykortteja
- kirjoittaa ilmoituksia ja viestejä muille käyttäjille
- Lisätä järjestelmään uusia kolikkokoodeja

## Suunnitellut ominaisuudet

#### Itse järjestelmä:

- pitää kirjaa käyttäjistä sekä heidän tiedoistaan, kuten lähetettyjen viestien määrästä ja heidän omistamistaan sovelluksen sisäisistä hyödykkeist

#### Peruskäyttäjä voi:


- vaihtoehtoisesti kolikoita saa 1kpl per 20 vaihtoa ja/tai yksityisviestiä
- tarkistaa vaihtopyynnöt muilta käyttäjiltä
- tarkastella muiden käyttäjien keräilykortteja 
- ostaa 3 kolikolla satunnaisen kortin niin, että kaikista yleisempien korttien saamismahdollisuus puolittuu
- katsella yksittäisten omistamiensa keräilykorttien tietoja tekstuaalisessa muodossa
- katsella tilastoja omistamistaan korteista, kuten harvinaisten korttien määrä, duplikaatit sekä prosenttiosuus siitä, kuinka lähellä on kaikkien korttien keräämistä
- lähettää muille käyttäjille vaihtopyyntöjä sekä yksityisviestejä


#### Ylläpitäjä voi:

- tarkastella käyttäjiä sekä heidän tietojaan
- deaktivoida kenen tahansa käyttäjän tilin
- tarkastella kolikkokoodeja (mahdollista myöntämistä varten?)
- antaa ja poistaa käyttäjille/ltä kolikoita sekä kortteja mielivaltaisesti
