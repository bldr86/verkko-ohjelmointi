# verkko-ohjelmointi

## Harjoitus 1: HTTP asiakas, TCP palvelin ja TCP asiakas 

- harj1.py: Yksinkertainen HTTP-asiakas.
- harj2_server.py: TCP palvelin joka kaiuttaa asiakkaan lähettämän tekstin takaisin, sillä muutoksella että palvelin lisää tekstin eteen nimen (laita oma nimesi) joka on erotettu ; -merkillä kaiutettavasta tekstistä.
- harj3_client.py: TCP asiakas joka lähettää yhden teksti string:in palvelimelle ja joka vastaanottaa palvelimen kaiuttaman viestin sekä osaa erottaa nimen ja tekstin toisistaan ja tulostaa ne erillisenä näyttöön.

## Harjoitus 2: SMTP Asiakas

- harj4_client.py: Yksinkertainen SMTP client joka tukee komentoja: HELO, QUIT, MAIL FROM, RCPT TO ja DATA

## Harjoitus 3: UDP Chat asiakas ja palvelin

- harj6_UDPServer.py: UDP palvelin joka kaiuttaa asiakkaan lähettämän tekstin kaikille asiakkaille jotka ovat palvelimelle paketin lähettäneet ennen ko. asiakasta.
- harj7_UDPClient_multiplat.py: Chat-asiakas joka toimii windowsilla ja unix-pohjaisissa. Pystyy vastaanottamaan ja lähettämään viestejä.

## Harjoitus 4: Peliprotokollan asiakas

- harj8_peliasiakas.py: Ottaa yhteyden UDP:llä pelipalvelimeen. Pelin tarkoituksena on arvata oikea numero moninpelissä, missä palvelin arpoo numeron ja ilmoittaa voittajan

## Harjoitus 5: Peliprotokollan palvelin - EI VALMIS VIELÄ

- harj10_pelipalvelin.py: Osaa tällä hetkellä käsitellä asiakkaiden join viestit ja kuitata ACK 201, 202 ja 203

