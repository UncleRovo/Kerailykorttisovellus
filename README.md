# KERÄILYKORTTISOVELLUS

Keräilykorttisovelluksella on kaksi käyttäjää, peruskäyttäjä sekä ylläpitäjä. Sovelluksen tarkoituksena on tarjota käyttäjilleen palvelu, jossa voi hankkia, katsella ja vaihtaa erilaisia keräilykortteja.

## Suunnitellut ominaisuudet

#### Itse järjestelmä:

- pitää tietokantaa eri keräilykorteista, joilla on nimi, elementti, harvinaisuustaso (1 - 3), kuvaus, sekä ID.
- pitää kirjaa käyttäjistä sekä heidän tiedoistaan, kuten lähetettyjen viestien määrästä ja heidän omistamistaan sovelluksen sisäisistä hyödykkeistä
- järjestää korttien vaihtamisen ja yksityisviestit eri käyttäjien välillä

#### Peruskäyttäjä voi:

- luoda tilin ja kirjautua sinne. Tilin luonnin yhteydessä käyttäjälle myönnetään 5 sovelluksen sisäistä kolikkoa
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
- tarkastella jokaista mahdollista keräilykorttia
- poistaa ja lisätä eri keräilykortteja
- tarkastella kolikkokoodeja (mahdollista myöntämistä varten?)
- antaa ja poistaa käyttäjille/ltä kolikoita sekä kortteja mielivaltaisesti
