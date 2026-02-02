Run with:

```
processor revokeAndAnonymize --conf certs.asice --params processor.asice

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
Tööriista parameetrite allkirja andmise aeg on 01.02.2026 19:53
Tööriista parameetrite allkiri on korrektne ja kehtiv

E-valimiskasti kontrollsumma laadimine failist 'out-2/KOV_2025-bb-2.json.sha256sum.asice'
E-valimiskasti kontrollsumma on laaditud
E-valimiskasti kontrollsumma allkirja kontrollimine
E-valimiskasti kontrollsumma allkirja on andnud MÄRT PÕDER
E-valimiskasti kontrollsumma allkirja andmise aeg on 02.02.2026 03:31
E-valimiskasti kontrollsumma allkiri on korrektne ja kehtiv
E-valimiskasti kontrollsumma arvutamine failist 'out-2/KOV_2025-bb-2.json'
E-valimiskasti arvutatud kontrollsumma klapib allkirjastatud kontrollsummaga

E-valimiskasti laadimine failist 'out-2/KOV_2025-bb-2.json'
E-valimiskast on laaditud
E-valimiskasti liigi kontrollimine
E-valimiskasti liik on "Korduvhäältest puhastatud korrektsete sedelitega e-valimiskast"
E-valimiskastis on 4 kvalifitseerimiseks sobivat häält

Ringkondade nimekirja laadimine failist 'districts.asice'
Ringkondade nimekirja allkirja kontrollimine
Ringkondade nimekirja allkirja on andnud MÄRT PÕDER
Ringkondade nimekirja allkirja andmise aeg on 01.02.2026 11:24
Ringkondade nimekirja allkiri on korrektne ja kehtiv
Ringkondade nimekiri on laaditud
Ringkondade nimekirjas on 1 ringkonda
Valimiste identifikaator on KOV_2025

Rakendan tühistus-/ennistusnimekirju

E-valimiskasti liik on "Topelthääletajate häältest puhastatud e-valimiskast"
E-valimiskastis on 4 kvalifitseerimiseks sobivat häält

Väljastan e-hääletanute nimekirja
Väljundfail: out-4/KOV_2025-ivoterlist.json

Väljastan tühistamiste ja ennistamiste aruande
Väljundfail: out-4/KOV_2025-revocation-report.csv

Väljastan tühistamiste ja ennistamiste aruande
Väljundfail: out-4/KOV_2025-revocation-report.csv.anonymous

Väljastan Log2 failid

Väljastan Log3 failid
Väljundfail: out-4/KOV_2025.question-KOV_2025.anonymize.log3

Anonümiseerin e-valimiskasti

Anonüümistatud e-valimiskasti salvestamine faili out-4/KOV_2025-bb-4.json
Anonüümistatud e-valimiskast on salvestatud
E-valimiskasti kontrollsumma salvestamine faili out-4/KOV_2025-bb-4.json.sha256sum
E-valimiskasti kontrollsumma on salvestatud
Töötlemisrakendus lõpetas töö ilma vigadeta

```

Optionally:

```
auditor integrity --conf certs.asice --params auditor.integrity.asice
```

Produces:

```
SLF4J(I): Connected with provider of type [ch.qos.logback.classic.spi.LogbackServiceProvider]
Konfiguratsiooni laadimine failist certs.asice
Konfiguratsiooni allkirja kontrollimine
Konfiguratsiooni allkirja on andnud MÄRT PÕDER
Konfiguratsiooni allkirja andmise aeg on 01.02.2026 03:52
Konfiguratsiooni allkiri on korrektne ja kehtiv

Tööriista parameetrite laadimine failist auditor.integrity.asice
Tööriista parameetrite allkirja kontrollimine
Tööriista parameetrite allkirja on andnud MÄRT PÕDER
Tööriista parameetrite allkirja andmise aeg on 01.02.2026 20:23
Tööriista parameetrite allkiri on korrektne ja kehtiv

E-valimiskasti laadimine failist 'votes.zip'
100% [..................................................] 32 / 32
E-valimiskast laaditud

Anonüümitud e-valimiskasti laadimine failist 'out-4/KOV_2025-bb-4.json'
Anonüümitud e-hääled laaditud

E-valimiskasti verifitseerimise logifail: out-2/KOV_2025.question-KOV_2025.check.log1
Korduvhäälte tühistamise logifail: out-2/KOV_2025.question-KOV_2025.squash.log2
Topelthäälte tühistamise logifail: out-4/KOV_2025.question-KOV_2025.revoke.log2
E-häälte anonüümimise logifail: out-4/KOV_2025.question-KOV_2025.anonymize.log3
E-valimiskasti töötlemisvigade raport: out-2/ballotbox_errors.txt

Vastuvõetud häälte seas on korduvaid krüptogramme

E-valimiskasti verifitseerimise logid on terviklikud: ei

Auditirakendus lõpetas töö ilma vigadeta

```

And optionally without `abort_early`:

```
auditor integrity --conf certs.asice --params auditor.integrity_force.asice
```

Produces:

```
SLF4J(I): Connected with provider of type [ch.qos.logback.classic.spi.LogbackServiceProvider]
Konfiguratsiooni laadimine failist certs.asice
Konfiguratsiooni allkirja kontrollimine
Konfiguratsiooni allkirja on andnud MÄRT PÕDER
Konfiguratsiooni allkirja andmise aeg on 01.02.2026 03:52
Konfiguratsiooni allkiri on korrektne ja kehtiv

Tööriista parameetrite laadimine failist auditor.integrity_force.asice
Tööriista parameetrite allkirja kontrollimine
Tööriista parameetrite allkirja on andnud MÄRT PÕDER
Tööriista parameetrite allkirja andmise aeg on 01.02.2026 20:22
Tööriista parameetrite allkiri on korrektne ja kehtiv

E-valimiskasti laadimine failist 'votes.zip'
100% [..................................................] 32 / 32
E-valimiskast laaditud

Anonüümitud e-valimiskasti laadimine failist 'out-4/KOV_2025-bb-4.json'
Anonüümitud e-hääled laaditud

E-valimiskasti verifitseerimise logifail: out-2/KOV_2025.question-KOV_2025.check.log1
Korduvhäälte tühistamise logifail: out-2/KOV_2025.question-KOV_2025.squash.log2
Topelthäälte tühistamise logifail: out-4/KOV_2025.question-KOV_2025.revoke.log2
E-häälte anonüümimise logifail: out-4/KOV_2025.question-KOV_2025.anonymize.log3
E-valimiskasti töötlemisvigade raport: out-2/ballotbox_errors.txt

Vastuvõetud häälte seas on korduvaid krüptogramme

E-valimiskasti verifitseerimise logid on terviklikud: ei
Anonüümimise logi klapib anonüümitud e-valimiskastiga: jah
Tühistuslogid klapivad e-valimiskastidega: jah

Auditirakendus lõpetas töö ilma vigadeta

```

And previously:

```
rm -r out-*
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
Tööriista parameetrite allkirja andmise aeg on 01.02.2026 19:53
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
Kogumisteenus andis e-valimiskasti koosseisus üle 32 häält
E-valimiskasti andmetervikluse kontrollimine
100% [..................................................] 32 / 32
E-valimiskastis sisalduvad andmed on terviklikud
E-valimiskastis on 32 kvalifitseerimiseks sobivat häält
E-valimiskastis sisalduvate häälte digiallkirja vormingule vastavuse kontrollimine
 46% [.......................                           ] 15 / 32
Viga valija *******0298 hääle **************735+0300 töötlemisel: Registreerimispäringu vastuse nonss pole koguja võtmega allkirjastatud registreerimispäringu sisu
 50% [.........................                         ] 16 / 32
Viga valija *******5216 hääle **************042+0300 töötlemisel: Hääletamise aeg '2025-09-30T07:35:20Z' on varasem valimiste algusajast '2025-10-13T03:00:00Z'
 56% [............................                      ] 18 / 32
Viga valija *******2719 hääle **************312+0300 töötlemisel: Häälel on vigane allkiri: Invalid signed container: *******2719/**************312+0300.bdoc
 68% [..................................                ] 22 / 32
Viga valija *******4710 hääle **************436+0300 töötlemisel: Hääletamise aeg '2025-09-30T07:50:08Z' on varasem valimiste algusajast '2025-10-13T03:00:00Z'
 71% [....................................              ] 23 / 32
Viga valija *******4710 hääle **************279+0300 töötlemisel: Hääletamise aeg '2025-09-30T07:57:45Z' on varasem valimiste algusajast '2025-10-13T03:00:00Z'
 81% [.........................................         ] 26 / 32
Viga valija *******2719 hääle **************255+0300 töötlemisel: Häälel on vigane allkiri: Invalid signed container: *******2719/**************255+0300.bdoc
 93% [...............................................   ] 30 / 32
Viga valija *******2724 hääle **************328+0300 töötlemisel: Registreerimispäringu vastus pole unikaalne
100% [..................................................] 32 / 32
Viga valija *******2724 hääle **************352+0300 töötlemisel: Registreerimispäringu vastus pole unikaalne
100% [..................................................] 32 / 32
Viga valija *******2724 hääle **************568+0300 töötlemisel: Registreerimispäringu vastus pole unikaalne
100% [..................................................] 32 / 32
Viga valija *******2724 hääle **************641+0300 töötlemisel: Registreerimispäringu vastus pole unikaalne
100% [..................................................] 32 / 32
Viga valija *******2724 hääle **************737+0300 töötlemisel: Registreerimispäringu vastus pole unikaalne
100% [..................................................] 32 / 32
E-valimiskastis sisalduvate häälte koguarv: 32
E-valimiskastis sisalduvate korrektse allkirjaga häälte arv: 21
E-valimiskastis sisalduvate vigase allkirjaga häälte arv: 11

*****************************************************************************
*                           !!! HOIATUS !!!                                 *
*                                                                           *
* Rakenduse sisendandmetest puuduvad registreerimisandmed.                  *
* Ei saa kontrollida kõikide registreeritud häälte olemasolu! Häälele       *
* vastava registreerimispäringu puudumist ignoreeritakse.                   *
*****************************************************************************

Grupeerin e-hääli valijate järgi
100% [..................................................] 21 / 21
E-valimiskastis sisalduvate kontrollitud häälte koguarv: 21
E-valimiskasti töötlemisel esines vigu. Vigade raport asub failis out-2/ballotbox_errors.txt.

Väljastan Log1 failid
Väljundfail: out-2/KOV_2025.question-KOV_2025.check.log1

Eemaldan korduvad hääled

E-valimiskasti liik on "Korduvhäältest puhastatud e-valimiskast"
E-valimiskastis on 4 kvalifitseerimiseks sobivat häält

Kontrollin krüptogrammide korrektsust
100% [..................................................] 4 / 4

E-valimiskasti liik on "Korduvhäältest puhastatud korrektsete sedelitega e-valimiskast"
E-valimiskastis on 4 kvalifitseerimiseks sobivat häält

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
