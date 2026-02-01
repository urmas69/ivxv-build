Run with:

```
processor checkAndSquash --conf certs.asice --params processor.asice
```

Produces:

```
SLF4J(I): Connected with provider of type [ch.qos.logback.classic.spi.LogbackServiceProvider]
Konfiguratsiooni laadimine failist certs.asice
Konfiguratsiooni allkirja kontrollimine
Konfiguratsiooni allkirja on andnud MÄRT PÕDER
Konfiguratsiooni allkirja andmise aeg on 01.02.2026 03:52
Konfiguratsiooni allkiri on korrektne ja kehtiv

Tööriista parameetrite laadimine failist processor.asice
Tööriista parameetrite allkirja kontrollimine
Tööriista parameetrite allkirja on andnud MÄRT PÕDER
Tööriista parameetrite allkirja andmise aeg on 01.02.2026 15:37
Tööriista parameetrite allkiri on korrektne ja kehtiv

Ringkondade nimekirja laadimine failist 'districts.asice'
Ringkondade nimekirja allkirja kontrollimine
Ringkondade nimekirja allkirja on andnud MÄRT PÕDER
Ringkondade nimekirja allkirja andmise aeg on 01.02.2026 11:24
Ringkondade nimekirja allkiri on korrektne ja kehtiv
Ringkondade nimekiri on laaditud
Ringkondade nimekirjas on 1 ringkonda
Valimiste identifikaator on KOV_2025
*****************************************************************************
*                           !!! HOIATUS !!!                                 *
*                                                                           *
* Rakenduse sisendandmetes puuduvad valijate nimekirjad.                    *
* Ei saa kontrollida valijate hääleõigust valijate nimekirja alusel!        *
* Kasutatakse fiktiivset valija nime '<Valija Nimi>'!                               *
*****************************************************************************

*****************************************************************************
*                           !!! HOIATUS !!!                                 *
*                                                                           *
* Rakenduse sisendandmetest puudub e-valimiskasti allkirjastatud            *
* kontrollsumma. E-valimiskast on tundmatut päritolu! Rakendus kontrollib   *
* e-valimiskasti terviklust, kuid ei väljasta andmeid töötlemisprotsessi    *
* järgmisteks etappideks.                                                   *
*****************************************************************************

E-valimiskasti laadimine failist 'votes.zip'
E-valimiskast on laaditud
E-valimiskasti liigi kontrollimine
E-valimiskasti liik on "Korrastamata e-valimiskast"
Kogumisteenus andis e-valimiskasti koosseisus üle 2 häält
E-valimiskasti andmetervikluse kontrollimine
100% [..................................................] 2 / 2
E-valimiskastis sisalduvad andmed on terviklikud
E-valimiskastis on 2 kvalifitseerimiseks sobivat häält
E-valimiskastis sisalduvate häälte digiallkirja vormingule vastavuse kontrollimine
100% [..................................................] 2 / 2
E-valimiskastis sisalduvate häälte koguarv: 2
E-valimiskastis sisalduvate korrektse allkirjaga häälte arv: 2
E-valimiskastis sisalduvate vigase allkirjaga häälte arv: 0
Kõik e-valimiskastis sisalduvad hääled vastavad digiallkirja vormingule

*****************************************************************************
*                           !!! HOIATUS !!!                                 *
*                                                                           *
* Rakenduse sisendandmetest puuduvad registreerimisandmed.                  *
* Ei saa kontrollida kõikide registreeritud häälte olemasolu! Häälele       *
* vastava registreerimispäringu puudumist ignoreeritakse.                   *
*****************************************************************************

Grupeerin e-hääli valijate järgi
100% [..................................................] 2 / 2
E-valimiskastis sisalduvate kontrollitud häälte koguarv: 2

Väljastan Log1 failid
Väljundfail: out-2/KOV_2025.question-KOV_2025.check.log1

Eemaldan korduvad hääled

E-valimiskasti liik on "Korduvhäältest puhastatud e-valimiskast"
E-valimiskastis on 1 kvalifitseerimiseks sobivat häält

Kontrollin krüptogrammide korrektsust
100% [..................................................] 1 / 1

E-valimiskasti liik on "Korduvhäältest puhastatud korrektsete sedelitega e-valimiskast"
E-valimiskastis on 1 kvalifitseerimiseks sobivat häält

Väljastan e-hääletanute nimekirja
Väljundfail: out-2/KOV_2025-ivoterlist.json
Väljundfail: out-2/KOV_2025-ivoterlist.pdf

Väljastan tühistamiste ja ennistamiste aruande
Väljundfail: out-2/KOV_2025-revocation-report.csv

Väljastan tühistamiste ja ennistamiste aruande
Väljundfail: out-2/KOV_2025-revocation-report.csv.anonymous

Väljastan Log2 failid
Väljundfail: out-2/KOV_2025.question-KOV_2025.squash.log2

Korduvhäältest puhastatud korrektsete sedelitega e-valimiskasti salvestamine faili out-2/KOV_2025-bb-2.json
Korduvhäältest puhastatud korrektsete sedelitega e-valimiskast on salvestatud
E-valimiskasti kontrollsumma salvestamine faili out-2/KOV_2025-bb-2.json.sha256sum
E-valimiskasti kontrollsumma on salvestatud
Töötlemisrakendus lõpetas töö ilma vigadeta

```
