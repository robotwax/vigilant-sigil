# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_dangerously_set_inner_html
import json
import nltk
from nltk.corpus import wordnet as wn

from itertools import chain, product
import itertools
import numpy as nd
import string
import numpy as np
import pandas as pd
import selectarray

app = dash.Dash(__name__)

app.config['suppress_callback_exceptions'] = True

server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
    <head>
    <meta charset="utf-8">

    <title>Vigilant Squares</title>

        {%favicon%}
        {%css%}

    </head>
    <body>
        {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
        
    </footer>
    </body>
</html>
'''

androm='''Name: Andromeda

Abbreviation:	And
Genitive:	Andromedae
Pronunciation:	/ænˈdrɒmɪdə/
Genitive: /ænˈdrɒmɪdiː/

Symbolism	Andromeda, the Chained Woman

Right ascension	23h 25m 48.6945s–02h 39m 32.5149s
Declination	53.1870041°–21.6766376°
Area	722 sq. deg. (19th)

Main stars	16
Bayer/Flamsteed stars	65
Stars with planets	12
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	3
Brightest star	α And (Alpheratz) (2.07m)
Messier objects  3
Meteor showers	Andromedids (Bielids)

Bordering constellations	

    Perseus
    Cassiopeia
    Lacerta
    Pegasus
    Pisces
    Triangulum

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of November.'''

antlia='''Name Antlia

Abbreviation	Ant
Genitive	Antliae
Pronunciation	/ˈæntliə/, genitive /-lii/
Symbolism	the Air Pump

Right ascension	09h 27m 05.1837s–11h 05m 55.0471s[2]
Declination	−24.5425186°–−40.4246216°

Area	239 sq. deg. (62nd)
Main stars	3
Bayer/Flamsteed
stars	9
Stars with planets	2
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	α Ant (4.25m)
Messier objects	0
Meteor showers	None
Bordering
constellations

Hydra
Pyxis
Vela
Centaurus

Visible at latitudes between +45° and −90°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

aquarius = '''Name: Aquarius

Abbreviation	Aqr
Genitive	Aquarii
Pronunciation	/əˈkwɛəriəs/, genitive /əˈkwɛəriaɪ/
Symbolism	the Water-Bearer

Right ascension	20h 38m 19.1706s–23h 56m 23.5355s
Declination	03.3256676°–−24.9040413°
Area	980 sq. deg. (10th)
Main stars	10, 22
Bayer/Flamsteed
stars	97
Stars with planets	12
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	7
Brightest star	β Aqr (Sadalsuud) (2.91m)
Messier objects	3
Meteor showers	March Aquariids
Eta Aquariids
Delta Aquariids
Iota Aquariids
Bordering
constellations

Pisces
Pegasus
Equuleus
Delphinus
Aquila
Capricornus
Piscis Austrinus
Sculptor
Cetus

Visible at latitudes between +65° and −90°.
Best visible at 21:00 (9 p.m.) during the month of October.'''

aquila = '''Name: Aquila

Abbreviation	Aql
Genitive	Aquilae[1]
Pronunciation	/ˈækwɪlə/ Áquila,
occasionally /əˈkwɪlə/;
genitive /ˈækwɪliː/
Symbolism	the Eagle[1]
Right ascension	18h 41m 18.2958s–20h 38m 23.7231s
Declination	18.6882229°–−11.8664360°
Area	652 sq. deg. (22nd)
Main stars	10
Bayer/Flamsteed
stars	65
Stars with planets	9
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	2
Brightest star	Altair (α Aql) (0.76m)
Messier objects	0
Meteor showers	

    June Aquilids
    Epsilon Aquilids

Bordering
constellations	

    Sagitta
    Hercules
    Ophiuchus
    Serpens Cauda
    Scutum
    Sagittarius
    Capricornus
    Aquarius
    Delphinus

Visible at latitudes between +90° and −75°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

aries = '''Name: Aries

Abbreviation	Ari
Genitive	Arietis
Pronunciation	/ˈɛəriːz/, formally /ˈɛəriiːz/; genitive /əˈraɪ.ɪtɪs/
Symbolism	the Ram
Right ascension	01h 46m 37.3761s–03h 29m 42.4003s
Declination	31.2213154°–10.3632069°
Area	441[3] sq. deg. (39th)
Main stars	4, 9
Bayer/Flamsteed
stars	67
Stars with planets	6
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	2
Brightest star	Hamal (2.01m)
Messier objects	0
Meteor showers	

    May Arietids
    Autumn Arietids
    Delta Arietids
    Epsilon Arietids
    Daytime-Arietids
    Aries-Triangulids

Bordering
constellations	

    Perseus
    Triangulum
    Pisces
    Cetus
    Taurus[3]

Visible at latitudes between +90° and −60°.
Best visible at 21:00 (9 p.m.) during the month of December.'''

auriga = '''Name Auriga

Abbreviation	Aur
Genitive	Aurigae
Pronunciation	/ɔːˈraɪɡə/ Auríga genitive /ɔːˈraɪdʒiː/

Symbolism	the Charioteer
Right ascension	04h 37m 54.4293s–07h 30m 56.1899s
Declination	56.1648331°–27.8913116°
Area	657[4] sq. deg. (21st)
Main stars	5, 8
Bayer/Flamsteed
stars	65
Stars with planets	7
Stars brighter than 3.00m	4
Stars within 10.00 pc (32.62 ly)	2
Brightest star	Capella (α Aur) (0.08m)
Messier objects	3[5]
Meteor showers	

    Aurigids
    Delta Aurigids

Bordering
constellations	

    Camelopardalis
    Perseus
    Taurus
    Gemini
    Lynx[6]

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of late February to early March.'''

boo = '''Name Bootes

Abbreviation	Boo
Genitive	Boötis
Pronunciation	/boʊˈoʊtiːz/, genitive /boʊˈoʊtɪs/[1]
Symbolism	The Herdsman
Right ascension	13h 36.1m to 15h 49.3m[2]
Declination	+7.36° to +55.1°[2]
Quadrant	NQ3
Area	907 sq. deg. (13th)
Main stars	7, 15
Bayer/Flamsteed
stars	59
Stars with planets	10
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	3
Brightest star	Arcturus (α Boo) (−0.04m)
Messier objects	0
Meteor showers	

    January Bootids
    June Bootids
    Quadrantids

Bordering
constellations	

    Draco
    Ursa Major
    Canes Venatici
    Coma Berenices
    Virgo
    Serpens Caput
    Corona Borealis
    Hercules

Visible at latitudes between +90° and −50°.
Best visible at 21:00 (9 p.m.) during the month of June.
Other designations: Arctophylax'''

cael = '''Name Caelum

Abbreviation	Cae
Genitive	Caeli[1]
Pronunciation	/ˈsiːləm/, genitive /ˈsiːlaɪ/
Symbolism	the chisel

Right ascension	04h 19.5m to 05h 05.1m[2]
Declination	−27.02° to −48.74°[2]

Quadrant	SQ1
Area	125 sq. deg. (81st)
Main stars	4
Bayer/Flamsteed
stars	8
Stars with planets	1
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α Cae (4.45m)
Messier objects	0
Meteor showers	1
Bordering constellations	

Columba
Lepus
Eridanus
Horologium
Dorado
Pictor

Visible at latitudes between +40° and −90°.
Best visible at 21:00 (9 p.m.) during the month of January. '''

canc = '''Name Cancer

Abbreviation	Cnc[1]
Genitive	Cancri[1]
Pronunciation	/ˈkænsər/,
genitive /ˈkæŋkraɪ/
Symbolism	the Crab
Right ascension	07h 55m 19.7973s–09h 22m 35.0364s[2]
Declination	33.1415138°–6.4700689°[2]
Area	506 sq. deg. (31st)
Main stars	5
Bayer/Flamsteed
stars	76
Stars with planets	10
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	β Cnc (Altarf) (3.53m)
Messier objects	2
Meteor showers	Delta Cancrids
Bordering constellations	

Lynx
Gemini
Canis Minor
Hydra
Leo
Leo Minor (corner)

Visible at latitudes between +90° and −60°.
Best visible at 21:00 (9 p.m.) during the month of March. '''

cane  = '''Name Canes Venatici

Abbreviation	CVn
Genitive	Canum Venaticorum
Pronunciation	/ˈkeɪniːz vɪˈnætɪsaɪ/ Cánes Venátici, genitive /ˈkeɪnəm vɪnætɪˈkɒrəm/
Symbolism	the Hunting Dogs
Right ascension	12h 06.2m to 14h 07.3m
Declination	+27.84° to +52.36°[1]
Quadrant	NQ3
Area	465 sq. deg. (38th)
Main stars	2
Bayer/Flamsteed
stars	21
Stars with planets	4
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	2
Brightest star	Cor Caroli (Asterion) (α CVn) (2.90m)
Messier objects	5
Meteor showers	Canes Venaticids
Bordering constellations

Ursa Major
Boötes
Coma Berenices

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of May. '''

can_maj = '''Name Canis Major

Abbreviation	CMa
Genitive	Canis Majoris
Pronunciation	/ˌkeɪnɪs ˈmeɪdʒər/, genitive /ˈkeɪnɪs məˈdʒɒrɪs/
Symbolism	the greater dog
Right ascension	06h 12.5m to 07h 27.5m[1]
Declination	−11.03° to −33.25°[1]
Quadrant	SQ2
Area	380 sq. deg. (43rd)
Main stars	8
Bayer/Flamsteed
stars	32
Stars with planets	7
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	1
Brightest star	Sirius (α CMa) (−1.46m)
Messier objects	1
Meteor showers	None
Bordering constellations	

    Monoceros
    Lepus
    Columba
    Puppis

Visible at latitudes between +60° and −90°.
Best visible at 21:00 (9 p.m.) during the month of February.'''

can_min = '''Name Canis Minor
Abbreviation 	CMi
Genitive	Canis Minoris

Pronunciation	/ˌkeɪnɪs ˈmaɪnər/, genitive /ˈkeɪnɪs mɪˈnɒrɪs/
Symbolism	The Lesser Dog

Right ascension	07h 06.4m to 08h 11.4m
Declination	13.22° to −0.36°

Quadrant	NQ2
Area	183 sq. deg. (71st)
Main stars	2
Bayer/Flamsteed
stars	14
Stars with planets	1
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	4
Brightest star	Procyon (α CMi) (0.34m)
Messier objects	0
Meteor showers	Canis-Minorids
Bordering
constellations	

    Monoceros
    Gemini
    Cancer
    Hydra

Visible at latitudes between +90° and −75°.
Best visible at 21:00 (9 p.m.) during the month of March.'''

cap = '''Name Capricornus

Abbreviation	Cap
Genitive	Capricorni
Pronunciation	/ˌkæprɪˈkɔːrnəs/, genitive /ˌkæprɪˈkɔːrnaɪ/
Symbolism	the Sea Goat

Right ascension	20h 06m 46.4871s–21h 59m 04.8693s[1]
Declination	−8.4043999°–−27.6914144°[1]

Area	414 sq. deg. (40th)
Main stars	9, 13, 23
Bayer/Flamsteed
stars	49
Stars with planets	5
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	3
Brightest star	δ Cap (Deneb Algedi) (2.85m)
Messier objects	1
Meteor showers	Alpha Capricornids
Chi Capricornids
Sigma Capricornids
Tau Capricornids
Capricorniden-Sagittariids
Bordering
constellations	

Aquarius
Aquila
Sagittarius
Microscopium
Piscis Austrinus

Visible at latitudes between +60° and −90°.
Best visible at 21:00 (9 p.m.) during the month of September.'''

cent = '''Name Centaurus

Abbreviation	Cen
Genitive	Centauri
Pronunciation	/sɛnˈtɔːrəs/, genitive /sɛnˈtɔːraɪ/
Symbolism	the Centaur

Right ascension	11h 05m 20.9415s–15h 03m 11.1071s
Declination	−29.9948788°–−64.6957885°

Area	1060 sq. deg. (9th)
Main stars	11
Bayer/Flamsteed
stars	69
Stars with planets	15
Stars brighter than 3.00m	10
Stars within 10.00 pc (32.62 ly)	8
Brightest star	α Cen (−0.27m)
Messier objects	0
Meteor showers	Alpha Centaurids
Omicron Centaurids
Theta Centaurids
Bordering
constellations	

Antlia
Carina
Circinus
Crux
Hydra
Libra (corner)
Lupus
Musca
Vela

Visible at latitudes between +25° and −90°.
Best visible at 21:00 (9 p.m.) during the month of May.'''

cet = '''Name Cetus

Abbreviation	Cet
Genitive	Ceti
Pronunciation	/ˈsiːtəs/, genitive /ˈsiːtaɪ/
Symbolism	the Whale, Shark, or Sea Monster

Right ascension	00h 26m 22.2486s–03h 23m 47.1487s
Declination	10.5143948°–−24.8725095°

Area	1231 sq. deg. (4th)
Main stars	14
Bayer/Flamsteed
stars	88
Stars with planets	23
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	9
Brightest star	β Cet (Deneb Kaitos)† (2.04m)
Messier objects	1
Meteor showers	October Cetids
Eta Cetids
Omicron Cetids
Bordering
constellations	

Aries
Pisces
Aquarius
Sculptor
Fornax
Eridanus
Taurus

Visible at latitudes between +70° and −90°.
Best visible at 21:00 (9 p.m.) during the month of November.
Note: †Mira (ο Cet) is magnitude 2.0 at its brightest.'''

col = '''Name Columba

Abbreviation	Col
Genitive	Columbae
Pronunciation	/kəˈlʌmbə/,
genitive /kəˈlʌmbiː/
Symbolism	the dove
Right ascension	05h 03m 53.8665s–06h 39m 36.9263s[1]
Declination	−27.0772038°–−43.1116486°[1]
Area	270 sq. deg. (54th)
Main stars	5
Bayer/Flamsteed
stars	18
Stars with planets	1
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α Col (Phact) (2.65m)
Messier objects	0
Meteor showers	None
Bordering
constellations	

Lepus
Caelum
Pictor
Puppis
Canis Major

Visible at latitudes between +45° and −90°.
Best visible at 21:00 (9 p.m.) during the month of February.'''

comab = '''Coma Berenices

Abbreviation	Com
Genitive	Comae Berenices
Pronunciation	/ˈkoʊmə bɛrəˈnaɪsiːz/,
genitive /ˈkoʊmiː/
Symbolism	Berenice's hair
Right ascension	11h 58m 25.0885s–13h 36m 06.9433s[1]
Declination	33.3074303°–13.3040485°[1]
Area	386 sq. deg. (42nd)
Main stars	3
Bayer/Flamsteed
stars	44
Stars with planets	5
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	1
Brightest star	β Com (4.26m)
Messier objects	8
Meteor showers	Coma Berenicids
Bordering
constellations	

Canes Venatici
Ursa Major
Leo
Virgo
Boötes

Visible at latitudes between +90° and −70°.
Best visible at 21:00 (9 p.m.) during the month of May.'''

cor_aus = '''Name Corona Australis

Abbreviation	CrA
Genitive	

    Coronae Australis
    Coronae Austrinae

Pronunciation	/kəˈroʊnə ɔːˈstreɪlɪs/ or /kəˈroʊnə ɔːˈstraɪnə/, genitive /kəˈroʊni/[1][2][3]
Symbolism	The Southern Crown

Right ascension	17h 58m 30.1113s–19h 19m 04.7136s
Declination	−36.7785645°–−45.5163460°

Area	128 sq. deg. (80th)
Main stars	6
Bayer/Flamsteed
stars	14
Stars with planets	2
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α CrA (4.10m)
Messier objects	0
Meteor showers	Corona Australids
Bordering
constellations	

    Sagittarius
    Scorpius
    Ara
    Telescopium

Visible at latitudes between +40° and −90°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

cor_bor='''Name Corona Borealis

Abbreviation	CrB
Genitive	Coronae Borealis
Pronunciation	/kəˈroʊnə ˌbɔːriˈælɪs, -ˌboʊ-, -ˈeɪlɪs/, genitive /kəˈroʊni/
Symbolism	The Northern Crown

Right ascension	15h 16m 03.8205s–16h 25m 07.1526s
Declination	39.7117195°–25.5380573°

Area	179 sq. deg. (73rd)
Main stars	8
Bayer/Flamsteed
stars	24
Stars with planets	5
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α CrB (Alphecca or Gemma) (2.21m)
Messier objects	0
Meteor showers	None
Bordering
constellations	

    Hercules
    Boötes
    Serpens Caput

Visible at latitudes between +90° and −50°.
Best visible at 21:00 (9 p.m.) during the month of July.'''

corv= '''Name Corvus

Abbreviation	 Crv
Genitive	Corvi
Pronunciation	/ˈkɔːrvəs/,
genitive /ˈkɔːrvaɪ/
Symbolism	the Crow/Raven

Right ascension	12h
Declination	−20°

Quadrant	SQ3
Area	184 sq. deg. (70th)
Main stars	4
Bayer/Flamsteed
stars	10
Stars with planets	3
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	1
Brightest star	γ Crv (Gienah) (2.59m)
Messier objects	0
Meteor showers	Corvids
Eta Corvids
Bordering
constellations	

Virgo
Crater
Hydra

Visible at latitudes between +60° and −90°.
Best visible at 21:00 (9 p.m.) during the month of May.'''

crat= '''Name Crater

Abbreviation	Crt
Genitive	Crateris
Pronunciation	/ˈkreɪtər/,
genitive /krəˈtiːrɪs/
Symbolism	the cup

Right ascension	11h
Declination	−16°

Quadrant	SQ2
Area	282 sq. deg. (53rd)
Main stars	4
Bayer/Flamsteed
stars	12
Stars with planets	7
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	δ Crt (Labrum) (3.57m)
Messier objects	0
Meteor showers	Eta Craterids
Bordering
constellations	

Leo
Sextans
Hydra
Corvus
Virgo

Visible at latitudes between +65° and −90°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

cyg= '''Name Cygnus

Abbreviation	Cyg
Genitive	Cygni
Pronunciation	/ˈsɪɡnəs/, genitive /ˈsɪɡnaɪ/
Symbolism	the Swan or Northern Cross

Right ascension	20.62h
Declination	+42.03°

Quadrant	NQ4
Area	804 sq. deg. (16th)
Main stars	9
Bayer/Flamsteed
stars	84
Stars with planets	97
Stars brighter than 3.00m	4
Stars within 10.00 pc (32.62 ly)	1
Brightest star	Deneb (α Cyg) (1.25m)
Messier objects	2
Meteor showers	October Cygnids
Kappa Cygnids
Bordering
constellations	

Cepheus
Draco
Lyra
Vulpecula
Pegasus
Lacerta

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of September.'''

delph= '''Name Delphinus

Abbreviation	Del
Genitive	Delphini
Pronunciation	/dɛlˈfaɪnəs/ Delfínus, genitive /dɛlˈfaɪnaɪ/
Symbolism	(dolphin)

Right ascension	21h
Declination	+10°

Quadrant	NQ4
Area	189 sq. deg. (69th)
Main stars	5
Bayer/Flamsteed
stars	19
Stars with planets	5
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	Rotanev (β Del) (3.63m)
Messier objects	0
Meteor showers	None
Bordering
constellations	

Vulpecula
Sagitta
Aquila
Aquarius
Equuleus
Pegasus

Visible at latitudes between +90° and −70°.
Best visible at 21:00 (9 p.m.) during the month of September.'''

equ= '''Name Equuleus

Abbreviation	Equ
Genitive	Equulei
Pronunciation	/ɪˈkwuːliəs/ Equúleus, genitive /ɪˈkwuːliaɪ/
Symbolism	the pony

Right ascension	21h
Declination	+10°

Quadrant	NQ4
Area	72 sq. deg. (87th)
Main stars	3
Bayer/Flamsteed
stars	10
Stars with planets	2
Stars brighter than 3.00m	None
Stars within 10.00 pc (32.62 ly)	None
Brightest star	α Equ (Kitalpha) (3.92m)
Messier objects	None
Meteor showers	None
Bordering
constellations	

Aquarius
Delphinus
Pegasus

Visible at latitudes between +90° and −80°.
Best visible at 21:00 (9 p.m.) during the month of September.'''

erid= '''Name Eridanus

Abbreviation	Eri
Genitive	Eridani
Pronunciation	/ɪˈrɪdənəs/ Erídanus,
genitive /ɪˈrɪdənaɪ/
Symbolism	the river Eridanus

Right ascension	3.25h
Declination	−29°

Quadrant	SQ1
Area	1138 sq. deg. (6th)
Main stars	24
Bayer/Flamsteed
stars	87
Stars with planets	32
Stars brighter than 3.00m	4
Stars within 10.00 pc (32.62 ly)	13
Brightest star	Achernar (α Eri) (0.46m)
Messier objects	None
Meteor showers	None
Bordering
constellations	

Cetus
Fornax
Phoenix
Hydrus
Tucana (corner)
Horologium
Caelum
Lepus
Orion
Taurus

Visible at latitudes between +32° and −90°.
Best visible at 21:00 (9 p.m.) during the month of December.'''

forn= '''Name Fornax

Abbreviation	For
Genitive	Fornacis
Pronunciation	/ˈfɔːrnæks/, genitive /fɔːrˈneɪsɪs/
Symbolism	the brazier
Right ascension	3h
Declination	−30°
Quadrant	SQ1
Area	398 sq. deg. (41st)
Main stars	2
Bayer/Flamsteed
stars	27
Stars with planets	6
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	α For (3.80m)
Messier objects	None
Meteor showers	None
Bordering
constellations	

Cetus
Sculptor
Phoenix
Eridanus

Visible at latitudes between +50° and −90°.
Best visible at 21:00 (9 p.m.) during the month of December.'''

gem= '''Name Gemini

Abbreviation	Gem
Genitive	Geminorum
Pronunciation	/ˈdʒɛmɪnaɪ/
genitive /ˌdʒɛmɪˈnɒrəm/
Symbolism	the Twins, Castor and Pollux

Right ascension	7h
Declination	+20°

Quadrant	NQ2
Area	514 sq. deg. (30th)
Main stars	8, 17
Bayer/Flamsteed
stars	80
Stars with planets	8
Stars brighter than 3.00m	4
Stars within 10.00 pc (32.62 ly)	4
Brightest star	Pollux (β Gem) (1.15m)
Messier objects	1
Meteor showers	Geminids
Rho Geminids
Bordering
constellations	

Lynx
Auriga
Taurus
Orion
Monoceros
Canis Minor
Cancer

Visible at latitudes between +90° and −60°.
Best visible at 21:00 (9 p.m.) during the month of February.'''

grus= '''Name Grus

Abbreviation	Gru
Genitive	Gruis
Pronunciation	/ˈɡrʌs/, or colloquially /ˈɡruːs/; genitive /ˈɡruːɪs/
Symbolism	the crane

Right ascension	21h 27.4m to 23h 27.1m
Declination	−36.31° to −56.39°

Quadrant	SQ4
Area	366 sq. deg. (45th)
Main stars	8
Bayer/Flamsteed
stars	28
Stars with planets	6
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	1
Brightest star	α Gru (Alnair) (1.73m)
Messier objects	0
Meteor showers	none
Bordering
constellations	

Piscis Austrinus
Microscopium
Indus
Tucana
Phoenix
Sculptor

Visible at latitudes between +34° and −90°.
Best visible at 21:00 (9 p.m.) during the month of October.'''

herc= '''Name Hercules

Abbreviation	Her
genitive = Herculis
Pronunciation	/ˈhɜːrkjʊliːz/, genitive /ˈhɜːrkjʊlɪs/
Symbolism	Heracles

Right ascension	17h
Declination	+30°

Quadrant	NQ3
Area	1225 sq. deg. (5th)
Main stars	14, 22
Bayer/Flamsteed
stars	106
Stars with planets	15
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	9
Brightest star	β Her (Kornephoros) (2.78m)
Messier objects	2
Meteor showers	Tau Herculids
Bordering
constellations

Draco
Boötes
Corona Borealis
Serpens Caput
Ophiuchus
Aquila
Sagitta
Vulpecula
Lyra

Visible at latitudes between +90° and −50°.
Best visible at 21:00 (9 p.m.) during the month of July.'''

hyd= '''Abbreviation	Hya
Genitive	Hydrae
Pronunciation	

    /ˈhaɪdrə/
    genitive /ˈhaɪdriː/

Symbolism	the sea serpent
Right ascension	8h–15h
Declination	−20°
Quadrant	SQ2
Area	1303 sq. deg. (1st)
Main stars	17
Bayer/Flamsteed
stars	75
Stars with planets	18
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	4
Brightest star	Alphard (α Hya) (1.98m)
Messier objects	3
Meteor showers	

    Alpha Hydrids
    Sigma Hydrids

Bordering
constellations	

    Antlia
    Cancer
    Canis Minor
    Centaurus
    Corvus
    Crater
    Leo
    Libra
    Lupus (corner)
    Monoceros
    Puppis
    Pyxis
    Sextans
    Virgo

Visible at latitudes between +54° and −83°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

lac= '''Name Lacerta

Abbreviation	Lac
Genitive	Lacertae
Pronunciation	/læˈkɜːrtə/,
genitive /læˈkɜːrti/
Symbolism	the Lizard

Right ascension	22.5h
Declination	+45°

Quadrant	NQ4
Area	201 sq. deg. (68th)
Main stars	5
Bayer/Flamsteed
stars	17
Stars with planets	12
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	1
Brightest star	α Lac (3.76m)
Messier objects	0
Bordering
constellations

Andromeda
Cassiopeia
Cepheus
Cygnus
Pegasus

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of October.'''

leom= '''Name Leo Minor

Abbreviation	LMi
Genitive	Leonis Minoris
Pronunciation	/ˌliːoʊ ˈmaɪnər/,
genitive /liːˈoʊnɪs mɪˈnɒrɪs/
Symbolism	the lesser Lion
Right ascension	9h 22.4m to 11h 06.5m
Declination	22.84° to 41.43°[1]
Quadrant	NQ2
Area	232 sq. deg. (64th)
Main stars	3
Bayer/Flamsteed
stars	34
Stars with planets	3
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	46 LMi (Praecipua) (3.83m)
Messier objects	0
Meteor showers	Leonis Minorids
Bordering
constellations	Ursa Major
Lynx
Cancer (corner)
Leo
Visible at latitudes between +90° and −45°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

leoz= '''Name Leo

Abbreviation	Leo
Genitive	Leonis
Pronunciation	/ˈliːoʊ/, genitive /liːˈoʊnɪs/
Symbolism	the Lion

Right ascension	11h
Declination	+15°

Quadrant	NQ2
Area	947 sq. deg. (12th)
Main stars	9, 15
Bayer/Flamsteed
stars	92
Stars with planets	13
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	5
Brightest star	Regulus (α Leo) (1.35m)
Messier objects	5
Meteor showers	Leonids
Bordering
constellations

Ursa Major
Leo Minor
Lynx (corner)
Cancer
Hydra
Sextans
Crater
Virgo

Coma Berenices
Visible at latitudes between +90° and −65°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

lep= '''Name Lepus

Abbreviation	Lep
Genitive	Leporis
Pronunciation	/ˈliːpəs/, or colloquially /ˈlɛpəs/; genitive /ˈlɛpərɪs/
Symbolism	the Hare

Right ascension	6h
Declination	−20°

Quadrant	NQ2
Area	290 sq. deg. (51st)
Main stars	8
Bayer/Flamsteed
stars	20
Stars with planets	3
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	3
Brightest star	α Lep (Arneb) (2.58m)
Messier objects	1
Meteor showers	None
Bordering
constellations

Orion
Monoceros
Canis Major
Columba
Caelum
Eridanus

Visible at latitudes between +63° and −90°.
Best visible at 21:00 (9 p.m.) during the month of January.'''

lib= '''Name Libra

Abbreviation	Lib
Genitive	Librae
Pronunciation	/ˈliːbrə/, genitive /ˈliːbriː/
Symbolism	the balance

Right ascension	15h
Declination	−15°

Quadrant	SQ3
Area	538 sq. deg. (29th)
Main stars	4, 6
Bayer/Flamsteed
stars	46
Stars with planets	3
Stars brighter than 3.00m	2
Stars within 10.00 pc (32.62 ly)	5
Brightest star	Zubeneschamali (β Lib) (2.61m)
Messier objects	0
Meteor showers	May Librids
Bordering
constellations

Serpens Caput
Virgo
Hydra
Centaurus (corner)
Lupus
Scorpius
Ophiuchus

Visible at latitudes between +65° and −90°.
Best visible at 21:00 (9 p.m.) during the month of June.'''

lup= '''Name Lupus

Abbreviation	Lup
Genitive	Lupi
Pronunciation	/ˈljuːpəs/, genitive /-paɪ/
Symbolism	The Wolf

Right ascension	Template:15.3
Declination	−45°

Quadrant	SQ3
Area	334 sq. deg. (46th)
Main stars	9
Bayer/Flamsteed
stars	41
Stars with planets	5
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	1
Brightest star	α Lup (Men) (2.30m)
Messier objects	0
Bordering
constellations

Norma
Scorpius
Circinus
Centaurus
Libra
Hydra (corner)

Visible at latitudes between +35° and −90°.
Best visible at 21:00 (9 p.m.) during the month of June.'''

lyn= '''Name  Lynx

Abbreviation	Lyn
Genitive	Lyncis
Pronunciation	/ˈlɪŋks/,
genitive /ˈlɪnsɪs/
Symbolism	the Lynx

Right ascension	8h
Declination	+45°

Quadrant	NQ2
Area	545 sq. deg. (28th)
Main stars	4
Bayer/Flamsteed
stars	42
Stars with planets	6
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	1
Brightest star	α Lyn (3.14m)
Messier objects	0
Meteor showers	Alpha Lyncids
September Lyncids
Bordering
constellations

Ursa Major
Camelopardalis
Auriga
Gemini
Cancer
Leo (corner)
Leo Minor

Visible at latitudes between +90° and −55°.
Best visible at 21:00 (9 p.m.) during the month of March.'''

lyr= '''Name Lyra

Abbreviation	Lyr
Genitive	Lyrae
Pronunciation	/ˈlaɪrə/, genitive /ˈlaɪriː/
Symbolism	Lyre, harp
Right ascension	18h 14m to 19h 28m
Declination	25.66° to 47.71°
Quadrant	NQ4
Area	286 sq. deg. (52nd)
Main stars	5
Bayer/Flamsteed
stars	25
Stars brighter than 3.00m	1 (Vega)
Stars within 10.00 pc (32.62 ly)	3[n 1]
Brightest star	Vega (α Lyr) (0.03m)
Messier objects	2
Meteor showers	Lyrids
June Lyrids
Alpha Lyrids
Bordering
constellations

Draco
Hercules
Vulpecula
Cygnus

Visible at latitudes between +90° and −40°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

micro= '''Name Microscopium

Abbreviation	Mic
Genitive	Microscopii
Pronunciation	/ˌmaɪkrəˈskɒpiəm/, genitive /ˌmaɪkrəˈskɒpiaɪ/
Symbolism	the Microscope

Right ascension	21h
Declination	−36°

Quadrant	SQ4
Area	210 sq. deg. (66th)
Main stars	5
Bayer/Flamsteed
stars	13
Stars with planets	2
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	γ Mic (4.67m)
Messier objects	none
Meteor showers	Microscopids
Bordering
constellations	

    Capricornus
    Sagittarius
    Telescopium
    Indus
    Grus
    Piscis Austrinus

Visible at latitudes between +45° and −90°.
Best visible at 21:00 (9 p.m.) during the month of September.'''

mono= '''Name Monoceros

Abbreviation	Mon
Genitive	Monocerotis
Pronunciation	/məˈnɒsɪrəs/,
genitive /ˌmɒnəsɪˈroʊtɪs/
Symbolism	the Unicorn

Right ascension	7.15h
Declination	−5.74°

Quadrant	NQ2
Area	482 sq. deg. (35th)
Main stars	4
Bayer/Flamsteed
stars	32
Stars with planets	16
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	β Mon (3.76m)
Messier objects	1
Meteor showers	December Monocerids
Alpha Monocerids
Bordering
constellations

Canis Major
Canis Minor
Gemini
Hydra
Lepus
Orion
Puppis

Visible at latitudes between +75° and −90°.
Best visible at 21:00 (9 p.m.) during the month of February.'''

oph= '''Name Ophiuchus

Abbreviation	Oph
Genitive	Ophiuchi
Pronunciation	/ɒfiˈjuːkəs/ Ophiúchus, genitive /ɒfiˈjuːkaɪ/
Symbolism	the serpent-bearer

Right ascension	17h
Declination	−8°

Quadrant	SQ3
Area	948 sq. deg. (11th)
Main stars	10
Bayer/Flamsteed
stars	65
Stars with planets	15
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	11
Brightest star	α Oph (Rasalhague) (2.08m)
Messier objects	7
Meteor showers	Ophiuchids
Northern May Ophiuchids
Southern May Ophiuchids
Theta Ophiuchids
Bordering
constellations

Hercules
Serpens
Libra
Scorpius
Sagittarius
Aquila

Visible at latitudes between +80° and −80°.
Best visible at 21:00 (9 p.m.) during the month of July.'''

Or= '''Name Orion

Abbreviation	Ori
Genitive	Orionis
Pronunciation	/ɒˈraɪ.ən/
Symbolism	Orion, the Hunter

Right ascension	5h
Declination	+5°

Quadrant	NQ1
Area	594 sq. deg. (26th)
Main stars	7
Bayer/Flamsteed
stars	81
Stars with planets	10
Stars brighter than 3.00m	8
Stars within 10.00 pc (32.62 ly)	8
Brightest star	Rigel (β Ori) (0.12m)
Messier objects	3
Meteor showers	Orionids
Chi Orionids
Bordering
constellations

Gemini
Taurus
Eridanus
Lepus
Monoceros

Visible at latitudes between +85° and −75°.
Best visible at 21:00 (9 p.m.) during the month of January.'''

peg= '''Name Pegasus

Abbreviation	Peg
Genitive	Pegasi
Pronunciation	/ˈpɛɡəsəs/,
genitive /ˈpɛɡəsaɪ/
Symbolism	the Winged Horse

Right ascension	21h 12.6m to 00h 14.6m
Declination	+2.33° to +36.61°

Quadrant	NQ4
Area	1121 sq. deg. (7th)
Main stars	9, 17
Bayer/Flamsteed
stars	88
Stars with planets	12
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	3
Brightest star	ε Peg (Enif) (2.38m)
Messier objects	1
Meteor showers	July Pegasids
Bordering
constellations

Andromeda
Lacerta
Cygnus
Vulpecula
Delphinus
Equuleus
Aquarius
Pisces

Visible at latitudes between +90° and −60°.
Best visible at 21:00 (9 p.m.) during the month of October.'''

per= '''Name Perseus

Abbreviation	Per
Genitive	Persei
Pronunciation	/ˈpɜːrsiəs, -sjuːs/;
genitive /-siaɪ/
Symbolism	Perseus

Right ascension	3h
Declination	+45°

Quadrant	NQ1
Area	615 sq. deg. (24th)
Main stars	19
Bayer/Flamsteed
stars	65
Stars with planets	7
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α Per (Mirfak) (1.79m)
Messier objects	2
Meteor showers	Perseids
September Perseids
Bordering
constellations

Aries
Taurus
Auriga
Camelopardalis
Cassiopeia
Andromeda
Triangulum

Visible at latitudes between +90° and −35°.
Best visible at 21:00 (9 p.m.) during the month of December.'''

pisc= '''Name Pisces

Abbreviation	Psc
Genitive	Piscium
Pronunciation	/ˈpaɪsiːz/, genitive /ˈpɪʃiəm/
Symbolism	the Fishes

Right ascension	1h
Declination	+15°

Quadrant	NQ1
Area	889 sq. deg. (14th)
Main stars	18
Bayer/Flamsteed
stars	86
Stars with planets	13
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	8
Brightest star	η Psc (Alpherg) (3.62m)
Messier objects	1
Meteor showers	Piscids
Bordering
constellations	

    Triangulum
    Andromeda
    Pegasus
    Aquarius
    Cetus
    Aries

Visible at latitudes between +90° and −65°.
Best visible at 21:00 (9 p.m.) during the month of November.'''

pisc_aus= '''Name Pisces Austrinus

Abbreviation	PsA
Genitive	Piscis Austrini
Pronunciation	/ˈpaɪsɪs ɒsˈtraɪnəs/ or /ɒsˈtreɪlɪs/, genitive /ˈpaɪsɪs ɒˈstraɪnaɪ/
Symbolism	the Southern Fish

Right ascension	22h
Declination	−30°

Quadrant	SQ4
Area	245 sq. deg. (60th)
Main stars	7
Bayer/Flamsteed
stars	21
Stars with planets	3
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	3
Brightest star	Fomalhaut (α PsA) (1.16m)
Messier objects	0
Meteor showers	?
Bordering
constellations

Capricornus
Microscopium
Grus
Sculptor
Aquarius

Visible at latitudes between +55° and −90°.
Best visible at 21:00 (9 p.m.) during the month of October.'''

pup= '''Name Puppis

Abbreviation	Pup
Genitive	Puppis
Pronunciation	/ˈpʌpɪs/, genitive the same
Symbolism	the Poop Deck

Right ascension	7.5h
Declination	−30°

Quadrant	SQ2
Area	673 sq. deg. (20th)
Main stars	9
Bayer/Flamsteed
stars	76
Stars with planets	6
Stars brighter than 3.00m	1
Stars within 10.00 pc (32.62 ly)	3
Brightest star	ζ Pup (Naos) (2.25m)
Messier objects	3
Meteor showers	Pi Puppids
Zeta Puppids
Puppid-Velids
Bordering
constellations

Monoceros
Pyxis
Vela
Carina
Pictor
Columba
Canis Major
Hydra

Visible at latitudes between +40° and −90°.
Best visible at 21:00 (9 p.m.) during the month of February.'''

pyx= '''Name Pyxis

Abbreviation	Pyx
Genitive	Pyxidis
Pronunciation	/ˈpɪksɪs/, genitive /ˈpɪksɪdɪs/
Symbolism	The compass box

Right ascension	9h
Declination	−30°

Quadrant	SQ2
Area	221 sq. deg. (65th)
Main stars	3
Bayer/Flamsteed
stars	10
Stars with planets	3
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	1
Brightest star	α Pyx (3.68m)
Messier objects	None
Meteor showers	None
Bordering
constellations

Hydra
Puppis
Vela
Antlia

Visible at latitudes between +50° and −90°.
Best visible at 21:00 (9 p.m.) during the month of March.'''

sag= '''Sagitt

Abbreviation	Sge
Genitive	Sagittae
Pronunciation	/səˈdʒɪtə/ Sagítta,
genitive /səˈdʒɪtiː/
Symbolism	the Arrow

Right ascension	19.8333h
Declination	+18.66°

Quadrant	NQ4
Area	80 sq. deg. (86th)
Main stars	4
Bayer/Flamsteed
stars	19
Stars with planets	2
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	1
Brightest star	γ Sge (3.51m)
Messier objects	1
Bordering
constellations

Vulpecula
Hercules
Aquila
Delphinus

Visible at latitudes between +90° and −70°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

sagit= '''Name Sagittarius

Abbreviation	Sgr
Genitive	Sagittarii
Pronunciation	/ˌsædʒɪˈtɛəriəs/,
genitive /-iaɪ/
Symbolism	the Archer

Right ascension	19h
Declination	−25°

Quadrant	SQ4
Area	867 sq. deg. (15th)
Main stars	12, 8
Bayer/Flamsteed
stars	68
Stars with planets	32
Stars brighter than 3.00m	7
Stars within 10.00 pc (32.62 ly)	3
Brightest star	ε Sgr (Kaus Australis) (1.79m)
Messier objects	15
Bordering
constellations	

    Aquila
    Scutum
    Serpens Cauda
    Ophiuchus
    Scorpius
    Corona Australis
    Telescopium
    Indus (corner)
    Microscopium
    Capricornus

Visible at latitudes between +55° and −90°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

sco= '''Name Scorpio

Abbreviation	Sco
Genitive	Scorpii
Pronunciation	/ˈskɔːrpiəs/, genitive /ˈskɔːrpiaɪ/
Symbolism	the Scorpion

Right ascension	16.8875h
Declination	−30.7367°

Quadrant	SQ3
Area	497 sq. deg. (33rd)
Main stars	18
Bayer/Flamsteed
stars	47
Stars with planets	14
Stars brighter than 3.00m	13
Stars within 10.00 pc (32.62 ly)	3
Brightest star	Antares (α Sco) (0.96m)
Messier objects	4
Meteor showers	Alpha Scorpiids
Omega Scorpiids
Bordering
constellations

Sagittarius
Ophiuchus
Libra
Lupus
Norma
Ara
Corona Australis

Visible at latitudes between +40° and −90°.
Best visible at 21:00 (9 p.m.) during the month of July.'''

scul= '''Name Sculptor

Abbreviation	Scl
Genitive	Sculptoris
Pronunciation	/ˈskʌlptər/,
genitive /skəlpˈtɒrɪs/
Symbolism	the Sculptor

Right ascension	0h
Declination	−30°

Quadrant	SQ1
Area	475 sq. deg. (36th)
Main stars	4
Bayer/Flamsteed
stars	18
Stars with planets	6
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	2
Brightest star	α Scl (4.30m)
Messier objects	0
Bordering
constellations	

Cetus
Aquarius
Piscis Austrinus
Grus
Phoenix
Fornax

Visible at latitudes between +50° and −90°.
Best visible at 21:00 (9 p.m.) during the month of November.'''

scut= '''Name Scutus

Abbreviation	Sct
Genitive	Scuti
Pronunciation	/ˈskjuːtəm/,
genitive /ˈskjuːtaɪ/
Symbolism	the Shield

Right ascension	18.7h
Declination	−10°

Quadrant	SQ4
Area	109 sq. deg. (84th)
Main stars	2
Bayer/Flamsteed
stars	7
Stars with planets	1
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	α Scuti (3.85m)
Messier objects	2
Meteor showers	June Scutids
Bordering
constellations	

Aquila
Sagittarius
Serpens Cauda

Visible at latitudes between +80° and −90°.
Best visible at 21:00 (9 p.m.) during the month of August.'''

sext= '''Name Sextus
Abbreviation 	Sex
Genitive	Sextantis, Sextansis
Pronunciation	/ˈsɛkstənz/,
genitive /sɛksˈtæntɪs/
Symbolism	the Sextant

Right ascension	10h
Declination	0°

Quadrant	SQ2
Area	314 sq. deg. (47th)
Main stars	3
Bayer/Flamsteed
stars	28
Stars with planets	5
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	5
Brightest star	α Sex (4.49m)
Messier objects	None
Meteor showers	Sextantids
Bordering
constellations	

Leo
Hydra
Crater

Visible at latitudes between +80° and −90°.
Best visible at 21:00 (9 p.m.) during the month of April.'''

taur= '''Name Taurus

Abbreviation	Tau
Genitive	Tauri
Pronunciation	

    /ˈtɔːrəs/ TOR-əs
    genitive /ˈtɔːraɪ/ TOR-eye[1][3]

Symbolism	the Bull

Right ascension	4.9h
Declination	19°

Quadrant	NQ1
Area	797 sq. deg. (17th)
Main stars	19
Bayer/Flamsteed
stars	132
Stars with planets	9 candidates
Stars brighter than 3.00m	4
Stars within 10.00 pc (32.62 ly)	1
Brightest star	Aldebaran (α Tau) (0.85m)
Messier objects	2
Meteor showers	

    Taurids
    Beta Taurids

Bordering
constellations	

    Auriga
    Perseus
    Aries
    Cetus
    Eridanus
    Orion
    Gemini

Visible at latitudes between +90° and −65°.
Best visible at 21:00 (9 p.m.) during the month of January.'''

tria= '''Name Triangulum

Abbreviation	Tri
Genitive	Trianguli
Pronunciation	/traɪˈæŋɡjʊləm/,
genitive /traɪˈæŋɡjʊlaɪ/
Symbolism	The Triangle

Right ascension	01h 31.3m to 02h 50.4m
Declination	25.60° to 37.35°

Quadrant	NQ1
Area	132 sq. deg. (78th)
Main stars	3
Bayer/Flamsteed
stars	14
Stars with planets	3
Stars brighter than 3.00m	0
Stars within 10.00 pc (32.62 ly)	0
Brightest star	β Tri (3.00m)
Messier objects	1
Meteor showers	None
Bordering
constellations

Andromeda
Pisces
Aries
Perseus

Visible at latitudes between +90° and −60°.
Best visible at 21:00 (9 p.m.) during the month of December.'''

vela= '''Name Vela

Abbreviation	Vel
Genitive	Velorum
Pronunciation	/ˈviːlə/,
genitive /vɪˈloʊrəm/
Symbolism	the Sails

Right ascension	9h
Declination	−50°

Quadrant	SQ2
Area	500 sq. deg. (32nd)
Main stars	5
Bayer/Flamsteed
stars	50
Stars with planets	7
Stars brighter than 3.00m	5
Stars within 10.00 pc (32.62 ly)	3
Brightest star	γ Vel (1.75m)
Messier objects	0
Meteor showers	Delta Velids
Gamma Velids
Puppid-velids
Bordering
constellations

Antlia
Pyxis
Puppis
Carina
Centaurus

Visible at latitudes between +30° and −90°.
Best visible at 21:00 (9 p.m.) during the month of March.'''

virg= '''Name Virgo

Abbreviation	Vir
Genitive	Virginis
Pronunciation	/ˈvɜːrɡoʊ/,
genitive /ˈvɜːrdʒɪns/
Symbolism	the Virgin

Right ascension	13h
Declination	−4°

Quadrant	SQ3
Area	1294 sq. deg. (2nd)
Main stars	9, 15
Bayer/Flamsteed
stars	96
Stars with planets	29
Stars brighter than 3.00m	3
Stars within 10.00 pc (32.62 ly)	10
Brightest star	Spica (α Vir) (0.98m)
Messier objects	11
Meteor showers	Virginids
Mu Virginids
Bordering
constellations

Boötes
Coma Berenices
Leo
Crater
Corvus
Hydra
Libra
Serpens Caput

Visible at latitudes between +80° and −80°.
Best visible at 21:00 (9 p.m.) during the month of May.'''

constellations = {'Andromeda': [94, 294, 425, 566], 'Andromeda1': [225, 380, 475, 495], 'Antlia': [15, 211, 533, 627], 'Antlia1': [492, 266, 151, 438], 'Aquarius': [206, 232, 264, 334, 481], 'Aquarius1': [129, 127, 148, 132, 221], 'Aquila': [83, 209, 391, 219, 526, 524], 'Aquila1': [458, 403, 351, 190, 54, 570], 'Aries': [67, 157, 226, 522, 610, 623],  'Aries1': [466, 415, 232, 351, 428, 473], 'Auriga': [176, 355, 416, 427, 493, 175],  'Auriga1': [247, 211, 318, 253, 504, 434], 'Bootes': [219, 359, 363, 557, 293, 137], 'Bootes1': [49, 103, 294, 464, 375, 214], 'Caelum': [126, 362, 374, 461],  'Caelum1': [90, 172, 415, 576], 'Cancer': [261, 277, 264, 161, 479],  'Cancer1': [27, 243, 342, 532, 613], 'Cane': [569, 371], 'Cane1': [306, 460], 'Canis Major': [120, 216, 248, 366, 522, 278, 527], 'Canis Major1': [538, 443, 369, 157, 198, 517, 555], 'Canis Minor': [292, 466], 'Canis Minor1': [442, 251], 'Columba': [53, 129, 323, 388, 331, 500, 587], 'Columba1': [105, 186, 170, 191, 550, 103, 176], 'Coma-Berenices': [64, 50, 480], 'Coma-Berenices1': [568, 100, 74], 'Corona-Australis': [343, 187, 137, 135, 173, 270, 525], 'Corona-Australis1': [27, 34, 117, 258, 360, 511, 630], 'Corona-Borealis': [188, 286, 372, 438, 532, 588, 530], 'Corona-Borealis1': [367, 505, 541, 528, 503, 373, 272], 'Corvus': [190, 410, 491, 508, 123], 'Corvus1': [60, 131, 462, 588, 493], 'Capricornus': [28, 74, 192, 298, 596, 618, 423, 384, 288, 176, 152, 98], 'Capricornus1': [221, 238, 239, 248, 187, 126, 474, 518, 461, 393, 377, 313], 'Centaurus': [55, 69, 138, 104, 31, 179, 236, 295, 329, 239, 239, 225, 271, 153, 220, 424, 411, 424, 454, 501, 487, 590, 494, 500], 'Centaurus1': [119, 161, 151, 227, 241, 121, 86, 166, 121, 204, 215, 292, 393, 524, 503, 330, 186, 330, 356, 375, 401, 478, 556, 592], 'Cetus': [52, 120, 133, 204, 295 , 385, 437, 514, 598, 320, 295], 'Cetus1': [185, 197, 238,  280,  377,  348,  376,  484,  363, 451, 377], 'Crater': [216, 350, 409, 619, 480, 347, 133, 14], 'Crater1': [19, 73, 250, 423, 624, 384, 413, 365], 'Cygnus': [230, 303, 419, 555, 436, 205, 83], 'Cygnus1': [270, 370, 469, 603, 257, 499, 570], 'Delphinus': [132, 337, 404, 548, 238], 'Delphinus1': [70, 79, 220, 601, 179], 'Equuleus': [245, 488, 173], 'Equuleus1': [55, 30, 596], 'Grus': [76, 64, 257, 473, 176, 237, 326, 423, 483, 579], 'Grus1': [287, 350, 384, 371, 610, 546, 266, 172, 102, 26], 'Eridanus': [157, 158, 196, 213, 236, 295, 323, 354, 360, 386, 476, 486, 468, 439, 403, 374, 344, 314, 243, 238, 261, 273, 326, 325, 344, 370, 414, 446, 438, 444, 446, 475, 471], 'Eridanus1': [104, 66, 70, 47, 47, 83, 147, 138, 114, 114, 118, 218, 238, 259, 235, 231, 242, 247, 298, 305, 340, 335, 363, 375, 403, 435, 417, 422, 450, 503, 544, 559, 623], 'Fornax': [21, 227, 625], 'Fornax1': [263, 404, 303], 'Gemini': [45, 175, 275, 434, 557, 606, 526, 476, 440, 433, 314, 217, 74, 80, 90], 'Gemini1': [102, 106, 150, 280, 339, 338, 401, 503, 583, 595, 399, 359, 292, 200, 177], 'Hercules': [35, 121, 197, 232, 271, 324, 382, 434, 388, 252, 319, 488, 513, 582, 501, 552, 584], 'Hercules1': [446, 437, 334, 330, 360, 390, 411, 313, 218, 201, 60, 180, 122, 72, 299, 462, 499], 'Hydra': [36, 110, 251, 279, 354, 391, 422, 431, 455, 503, 487, 538, 580, 603, 613, 614, 599], 'Hydra1': [435, 392, 452, 438, 330, 340, 312, 316, 333, 293, 234, 212, 187, 211, 211, 194, 184], 'Lacerta': [327, 375, 371, 339, 334, 459], 'Lacerta1': [104, 24, 134, 215, 403, 620], 'Leo Minor': [20, 228, 380, 627], 'Leo Minor1': [310, 241, 295, 244], 'Leo': [610, 575, 476, 461, 217, 48, 519], 'Leo1': [80, 38, 95, 164, 145, 251, 315], 'Lepus': [222, 461, 534, 276], 'Lepus1': [338, 273, 579, 489], 'Libra': [140, 167, 258, 358, 381, 493], 'Libra1': [285, 334, 290, 173, 398, 320], 'Lupus': [125, 291, 297, 411, 485, 339, 342, 289, 223, 87, 49], 'Lupus1': [120, 181, 306, 375, 499, 619, 539, 416, 319, 260, 220], 'Lynx': [61, 74, 160, 308, 497, 532, 626], 'Lynx1': [621, 572, 476, 449, 293, 74, 17], 'Lyra': [275, 342, 312, 245], 'Lyra1': [269, 243, 390, 420], 'Microscopium': [101, 122, 373, 541], 'Microscopium1': [619, 24, 26, 133], 'Monoceros': [469, 513, 435, 562, 311, 533, 610, 14, 159], 'Monoceros1': [105, 157, 143, 216, 321, 455, 442, 374, 506], 'Ophiuchus': [27, 133, 200, 259, 334, 304, 239, 264, 372, 448, 494, 484, 425, 441, 566, 587, 614, 580, 573, 549], 'Ophiuchus1': [243, 324, 400, 461, 465, 570, 234, 143, 180, 264, 331, 343, 408, 479, 238, 215, 165, 105, 74, 104], 'Orion': [184, 142, 188, 223, 317, 321, 365, 334, 402, 418, 260, 293, 312, 511, 534, 537, 530, 516, 494], 'Orion1': [18, 139, 234, 279, 227, 237, 299, 434, 561, 591, 620, 465, 450, 222, 249, 286, 312, 375, 389], 'Pegasus': [16, 58, 267, 264, 331, 350, 471, 566], 'Pegasus1': [373, 165, 191, 383, 429, 449, 511, 451], 'Perseus': [186, 162, 162, 221, 288, 361, 387, 406], 'Perseus1': [619, 530,428, 244, 189, 298, 389, 435], 'Pisces': [213, 190, 204, 145, 98, 41, 108, 143, 230, 274, 426, 486, 524, 559, 528, 480], 'Pisces1': [94, 129, 163, 276, 354, 432, 400, 392, 373, 378, 386, 400, 388, 426, 453, 448], 'Pisces-Austrinus': [31, 171, 396, 614, 625, 250, 84, 54], 'Pisces-Austrinus1': [309, 203, 228, 363, 438, 401, 424, 416], 'Puppis': [189, 239, 264, 302, 313, 328, 366, 479, 415, 363, 318, 210, 193], 'Puppis1': [38, 100, 133, 165, 191, 238, 343, 470, 587, 474, 446, 385, 122], 'Pyxis': [188, 188, 267, 304, 256, 233, 291, 346, 431, 504, 454, 430, 454], 'Pyxis1': [604, 611, 309, 238, 143, 128, 128, 250, 225, 140, 315, 408, 462], 'Pyxis': [231, 391, 463, 538, 580], 'Pyxis1': [38, 136, 150, 461, 597], 'Sagitta': [69, 549], 'Sagitta1': [261, 372], 'Sagittarius': [188, 188, 267, 247, 304, 256, 233, 291, 346, 431, 504, 454, 430, 454], 'Sagittarius1': [604, 611, 309, 264, 238, 143, 128, 128, 250, 225, 140, 315, 408, 462], 'Scorpius': [109, 122, 137, 164, 174, 160, 240, 296, 308, 316, 374, 401, 438, 504, 433, 521, 519], 'Scorpius1': [489, 540, 520, 482, 487, 587, 589, 573, 499, 435, 331, 306, 267, 197, 293, 250, 309], 'Sculptor': [16, 455, 625, 519], 'Sculptor1': [198, 170, 328, 471], 'Scutum': [237, 534, 462, 300], 'Scutum1': [58, 280, 586, 287], 'Sextans': [22, 373, 618], 'Sextans1': [121, 98, 553], 'Taurus':[32, 327, 99, 364, 407, 392, 364], 'Taurus1':[183, 293, 34, 306, 310, 272, 238], 'Triangulum': [49, 225, 572], 'Triangulum1': [178, 84, 595]}


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Magic Sigil Maker', style={'margin-top':55, 'font-size': 80},
            className='six columns'),
            #html.Img(src='/assets/vigil-logo.jpg',
            #className='six columns'),
    ], className = "row"),
    html.Div([
        dcc.Dropdown(
            id='my-dropdown',
            options=[{'label': 'Andromeda', 'value': 'Andromeda'},
                {'label': 'Antlia', 'value': 'Antlia'},
                {'label': 'Aquarius', 'value': 'Aquarius'},
                {'label': 'Aquila', 'value': 'Aquila'},
                {'label': 'Aries', 'value': 'Aries'},
                {'label': 'Auriga', 'value': 'Auriga'},
                {'label': 'Bootes', 'value': 'Bootes'},
                {'label': 'Caelum', 'value': 'Caelum'},
                {'label': 'Cancer', 'value': 'Cancer'},
                {'label': 'Canes', 'value': 'Cane'},
                {'label': 'Canis-Major', 'value': 'Canis Major'},
                {'label': 'Canis-Minor', 'value': 'Canis Minor'},
                {'label': 'Capricornus', 'value': 'Capricornus'},
                {'label': 'Centaurus', 'value': 'Centaurus'},
                {'label': 'Cetus', 'value': 'Cetus'},
                {'label': 'Columba', 'value': 'Columba'},
                {'label': 'Coma-Berenices', 'value': 'Coma-Berenices'},
                {'label': 'Corona-Australis', 'value': 'Corona-Australis'},
                {'label': 'Corona-Borealis', 'value': 'Corona-Borealis'},
                {'label': 'Corvus', 'value': 'Corvus'},
                {'label': 'Crater', 'value': 'Crater'},
                {'label': 'Cygnus', 'value': 'Cygnus'},
                {'label': 'Delphinus', 'value': 'Delphinus'},
                {'label': 'Equuleus', 'value': 'Equuleus'},
                {'label': 'Eridanus', 'value': 'Eridanus'},
                {'label': 'Fornax', 'value': 'Fornax'},
                {'label': 'Gemini-Zodiac', 'value': 'Gemini'},
                {'label': 'Grus', 'value': 'Grus'},
                {'label': 'Hercules', 'value': 'Hercules'},
                {'label': 'Hydra', 'value': 'Hydra'},
                {'label': 'Lacerta', 'value': 'Lacerta'},
                {'label': 'Leo-Minor', 'value': 'Leo Minor'},
                {'label': 'Leo-Zodiac', 'value': 'Leo'},
                {'label': 'Lepus', 'value': 'Lepus'},
                {'label': 'Libra', 'value': 'Libra'},
                {'label': 'Lupus', 'value': 'Lupus'},
                {'label': 'Lynx', 'value': 'Lynx'},
                {'label': 'Lyra', 'value': 'Lyra'},
                {'label': 'Microscopium', 'value': 'Microscopium'},
                {'label': 'Monoceros', 'value': 'Monoceros'},
                {'label': 'Ophiuchus', 'value': 'Ophiuchus'},
                {'label': 'Orion', 'value': 'Orion'},
                {'label': 'Pegasus', 'value': 'Pegasus'},
                {'label': 'Perseus', 'value': 'Perseus'},
                {'label': 'Pisces', 'value': 'Pisces'},
                {'label': 'Piscis-Austrinus', 'value': 'Pisces-Austrinus'},
                {'label': 'Puppis', 'value': 'Puppis'},
                {'label': 'Pyxis', 'value': 'Pyxis'},
                {'label': 'Sagitta', 'value': 'Sagitta'},
                {'label': 'Sagittarius', 'value': 'Sagittarius'},
                {'label': 'Scorpius', 'value': 'Scorpius'},
                {'label': 'Sculptor', 'value': 'Sculptor'},
                {'label': 'Scutum', 'value': 'Scutum'},
                {'label': 'Sextans', 'value': 'Sextans'},
                {'label': 'Taurus', 'value': 'Taurus'},
                {'label': 'Triangulum', 'value': 'Triangulum'},
                {'label': 'Vela', 'value': 'Vela'},
                {'label': 'Virgo', 'value': 'Virgo'}],
            value='Andromeda',
            style={'margin-right': 10},
            ),
    ], className = "row"),
    html.Br(),
    html.Div([
            dcc.Markdown('**Constellation**', className="four columns offset-by-one"),
            dcc.Markdown('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Information**', className="three columns"),
    ], className='row'),
    html.Div([
        html.Div(id='output-container2',
        className="five columns offset-by-one"),
        dcc.Textarea(id='textbox', value=androm, readOnly = True, style={'width': '40%', 'padding-top': 0, 'padding-bottom': 0, 'background-color': '#ffffff', 'border-radius': 1, 'resize': 'none', 'font-family': 'arial', 'size': 14, 'color': 'black', 'margin-top': 0, 'margin-right': 0, 'margin-left': 45},
        className="five columns"),
    ], className='row'),
    html.Div([
    html.Hr(style={'color': '#de3d96'}),
    ], className='row'),
    html.Div([
            html.H2(children='Magic Square Maker', style={'margin-left':50, 'padding-top': -40, 'padding-bottom': 0}),
    ]),
    html.Div([
        html.P('Input any real number between 3 and 37.', style={'margin-left':50, 'color': '#ffffff'}),
        dcc.Input(id='input-1', value=11, style={'margin-left':50}),
    ]),
    html.Br(),
    html.Div([
        html.Div(id='markd-container', style={'margin-left':50}),
    ], className="row"),
    html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='inter-input', style={'display': 'none'}),
    html.Div(id='intermediate-value7', style={'display': 'none'}),
    html.Div([
        html.Div(id='output', style={'margin-left':50, 'position': 'relative'},
        className="eleven columns")
    ], className="row"),
    html.Br(),
    html.Div([
        dcc.Slider(id='slider',
            min=1,
            max=8,
            marks={
                1: {'label': 'Transform 1', 'style': {'color': 'white'}},
                2: {'label': 'Transform 2', 'style': {'color': 'white'}},
                3: {'label': 'Transform 3', 'style': {'color': 'white'}},
                4: {'label': 'Transform 4', 'style': {'color': 'white'}},
                5: {'label': 'Transform 5', 'style': {'color': 'white'}},
                6: {'label': 'Transform 6', 'style': {'color': 'white'}},
                7: {'label': 'Transform 7', 'style': {'color': 'white'}},
                8: {'label': 'Transform 8', 'style': {'color': 'white'}},},
            value=1,
        ),
    ], className="ten columns offset-by-one"),
    html.Div(id='inter-dropd', style={'display': 'none'}),
    html.Div(id='inter-slider', style={'display': 'none'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#de3d96'}),
    html.Div([
            html.H2(children='Magic Spell Maker', style={'margin-left':40, 'padding-top': 0, 'padding-bottom': 0}),
            html.P('Reverse engineer your sigils', style={'margin-left':40, 'padding-top': 0, 'padding-bottom': 0, 'color': '#ffffff'}),
    ], className = "row"),
    html.Div([
        html.P('DECODE', style={'margin-left': 40, 'width': '33%', 'bottom-margin': -30, 'size': 24}, className='four columns'),
        html.P('REVERSE ENGINEER', style={'margin-left': -20, 'width': '30%', 'bottom-margin': -30, 'size': 24}, className='three columns'),
        html.P('DICTIONARY', style={'margin-left': 20, 'width': '30%', 'bottom-margin': -30, 'size': 24}, className='four columns'),
    ], className='row'),
    html.Div([
        html.Button('Shift', id='button-1', n_clicks = 0, style={'width': '10%', 'margin-left': 40, 'color': '#de3d96'}, className='three columns'),
        html.Button('Brute Force', id='button-2', n_clicks = 0, style={'width': '10%', 'margin-left':305, 'text-align': 'center', 'color': '#de3d96'}, className='four columns'),
        html.Button('Results', id='button-3', n_clicks = 0, style={'width': '10%', 'margin-left':305, 'text-align': 'center', 'color': '#de3d96'}, className='four columns'),
    ], className='row'),
    html.Div(id='decode-value', style={'display': 'none'}),
    html.Div(id='inter-btndecode', style={'display': 'none'}),
    html.Br(),
    html.Div(id='intermediate-value6', style={'display': 'none'}),
    html.Div([
        dcc.Textarea(id='textbox-1', readOnly = True, style={'width': '30%',  'height': 2, 'padding-top': 0, 'padding-bottom': 0, 'background-color': '#ffffff', 'border-radius': 1, 'resize': 'none', 'font-family': 'arial', 'size': 14, 'color': 'black', 'margin-top': 0, 'margin-right': 0, 'margin-left': 40},
        className='three columns'),
        dcc.Textarea(id='textbox-2', readOnly = True, rows = 40, style={'width': '30%', 'height': 560, 'padding-top': 0, 'padding-bottom': 0, 'background-color': '#ffffff', 'border-radius': 1, 'resize': 'none', 'font-family': 'arial', 'size': 14, 'color': 'black', 'margin-top': 0, 'margin-right': 0, 'margin-left':20, 'text-align': 'justify'},
        className='four columns'),
        dcc.Textarea(id='textbox-3', readOnly = True, rows = 40, style={'width': '30%', 'height': 240, 'padding-top': 0, 'padding-bottom': 0, 'background-color': '#ffffff', 'border-radius': 1, 'resize': 'none', 'font-family': 'arial', 'size': 14, 'color': 'black', 'margin-top': 0, 'margin-right': 0, 'margin-left':20, 'text-align': 'justify'},
        className='four columns'),
    ], className='row'),    
    html.Div([
        html.Br(),
        html.Hr(),
        html.Br(),
        html.Footer(
            html.Center('Cataphysical Research Society - 2018.' ),
        ),
    ], className = "row"),
    html.Br(),
    ]),
])



@app.callback(dash.dependencies.Output('inter-input', 'children'), [dash.dependencies.Input('input-1', 'value')])
def func(value):
    x2 = int(value)
    with open('x.txt', 'w') as outfile:
        return json.dump(x2, outfile)

@app.callback(dash.dependencies.Output('inter-dropd', 'children'), [dash.dependencies.Input('my-dropdown', 'value')])
def func(value):
    z1 = value
    with open('z1.txt', 'w') as outfile:
        return json.dump(z1, outfile)
        
@app.callback(dash.dependencies.Output('inter-slider', 'children'), [dash.dependencies.Input('slider', 'value')])
def func(slider):
    z2 = slider
    with open('z2.txt', 'w') as outfile:
        return json.dump(z2, outfile)
        
@app.callback(dash.dependencies.Output('inter-btndecode', 'children'), [dash.dependencies.Input('button-1', 'n_clicks')])
def func(button1):
    z4 = button1
    with open('z4.txt', 'w') as outfile:
        return json.dump(z4, outfile)

@app.callback(dash.dependencies.Output('intermediate-value', 'children'), [dash.dependencies.Input('input-1', 'value')])
def func(input1):
    a = int(input1)
    b = a * a
    if a % 2 != 0:
        magic_square4 = np.zeros((a,a), dtype=int)
        n = 1
        i, j = 0, a//2
        while n <= a**2:
            magic_square4[i, j] = n
            n += 1
            newi, newj = (i-1) % a, (j+1)% a
            if magic_square4[newi, newj]:
                i += 1
            else:
                i, j = newi, newj
        magic_square5=magic_square4.tolist()
        with open('magic.txt', 'w') as f:
            return json.dump(magic_square5, f)
    elif a % 4 == 2:
        c = int(a/2)
        c1 = c * c
        def func(a):
            magic_square = np.zeros((c,c), dtype=int)
            n = 1
            i, j = 0, c//2
            while n <= c**2:
                magic_square[i, j] = n
                n += 1
                newi, newj = (i-1) % c, (j+1)% c
                if magic_square[newi, newj]:
                    i += 1
                else:
                    i, j = newi, newj
            return(magic_square)
        r = (func(a))
        f = (c**2)
        e = r + f
        g = r + (f*2)
        h = r + (f*3)
        m = np.concatenate((r, g), axis=1)
        p = np.concatenate((h, e), axis=1)
        mas = np.concatenate((m, p), axis=0)
        bc = a - 6
        mas2 = mas.copy()
        dc = int(bc/4)
        gg = a - dc
        ee = ([-1]*dc)
        for i in ee:
            mas = np.delete(mas, i, 1)
        ff = ([0]*gg)
        for i in ff:
            try:
                mas2 = np.delete(mas2, i, 1)
            except IndexError:
                varr = 5
        xf = np.roll(mas2, c, axis=0)
        px = np.concatenate((mas, xf), axis=1)
        eff = dc + 1
        px2 = px.copy()
        e2 = ([0]*eff)
        eg = a - eff
        for i in e2:
            px = np.delete(px, i, 1)
        ff = ([-1]*eg)
        for i in ff:
            px2 = np.delete(px2, i, 1)
        pxf = np.roll(px2, c, axis=0)
        px1 = np.concatenate((pxf, px), axis=1)
        af = int(c/2)
        ag = af + c
        temp = px1[af,0]
        px1[af,0] = px1[ag,0]
        px1[ag,0] = temp
        temp1 = px1[af, af]
        px1[af, af] = px1[ag, af]
        px1[ag, af] = temp1
        magic_square5=px1.tolist()
        with open('magic.txt', 'w') as f:
            return json.dump(magic_square5, f)
    elif a % 4 == 0:
        z = range(1, b+1)
        c = (list(z))
        d = c[0] + c[-1]
        e = int(a/2)
        e = d * e
        f = int(a/4)
        g = [1, 0, 0, 1]*f
        h = [0, 1, 1, 0]*f
        i = [0, 1, 1, 0]*f
        k = [1, 0, 0, 1]*f
        m = g + h + i + k
        o = m * f
        p = np.array(o).reshape(a, a)
        p[p == 1] = d
        q = np.array(c).reshape(a, a)
        r = p - q
        magic_square = abs(r)
        magic_square5=magic_square.tolist()
        with open('magic.txt', 'w') as f:
            return json.dump(magic_square5, f)

@app.callback(dash.dependencies.Output('intermediate-value7', 'children'), [dash.dependencies.Input('input-1', 'value')])
def func(input1):
    a = int(input1)
    b = a * a
    if a % 2 != 0:
        magic_square4 = np.zeros((a,a), dtype=int)
        n = 1
        i, j = 0, a//2
        while n <= a**2:
            magic_square4[i, j] = n
            n += 1
            newi, newj = (i-1) % a, (j+1)% a
            if magic_square4[newi, newj]:
                i += 1
            else:
                i, j = newi, newj
        magicsum = magic_square4[1].sum().tolist()
        with open('magicsum.txt', 'w') as f:
            return json.dump(magicsum, f)
    elif a % 4 == 2:
        c = int(a/2)
        c1 = c * c
        def func(a):
            magic_square = np.zeros((c,c), dtype=int)
            n = 1
            i, j = 0, c//2
            while n <= c**2:
                magic_square[i, j] = n
                n += 1
                newi, newj = (i-1) % c, (j+1)% c
                if magic_square[newi, newj]:
                    i += 1
                else:
                    i, j = newi, newj
            return(magic_square)
        r = (func(a))
        f = (c**2)
        e = r + f
        g = r + (f*2)
        h = r + (f*3)
        m = np.concatenate((r, g), axis=1)
        p = np.concatenate((h, e), axis=1)
        mas = np.concatenate((m, p), axis=0)
        bc = a - 6
        mas2 = mas.copy()
        dc = int(bc/4)
        gg = a - dc
        ee = ([-1]*dc)
        for i in ee:
            mas = np.delete(mas, i, 1)
        ff = ([0]*gg)
        for i in ff:
            try:
                mas2 = np.delete(mas2, i, 1)
            except IndexError:
                varr = 5
        xf = np.roll(mas2, c, axis=0)
        px = np.concatenate((mas, xf), axis=1)
        eff = dc + 1
        px2 = px.copy()
        e2 = ([0]*eff)
        eg = a - eff
        for i in e2:
            px = np.delete(px, i, 1)
        ff = ([-1]*eg)
        for i in ff:
            px2 = np.delete(px2, i, 1)
        pxf = np.roll(px2, c, axis=0)
        px1 = np.concatenate((pxf, px), axis=1)
        af = int(c/2)
        ag = af + c
        temp = px1[af,0]
        px1[af,0] = px1[ag,0]
        px1[ag,0] = temp
        temp1 = px1[af, af]
        px1[af, af] = px1[ag, af]
        px1[ag, af] = temp1
        magicsum = px1[1].sum().tolist()
        with open('magicsum.txt', 'w') as f:
            return json.dump(magicsum, f)
    elif a % 4 == 0:
        z = range(1, b+1)
        c = (list(z))
        d = c[0] + c[-1]
        e = int(a/2)
        e = d * e
        f = int(a/4)
        g = [1, 0, 0, 1]*f
        h = [0, 1, 1, 0]*f
        i = [0, 1, 1, 0]*f
        k = [1, 0, 0, 1]*f
        m = g + h + i + k
        o = m * f
        p = np.array(o).reshape(a, a)
        p[p == 1] = d
        q = np.array(c).reshape(a, a)
        r = p - q
        magic_square = abs(r)
        magicsum = magic_square[1].sum().tolist()
        with open('magicsum.txt', 'w') as f:
            return json.dump(magicsum, f)

@app.callback(
    dash.dependencies.Output('output-container2', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def update_output(value):
    if value == 'Andromeda':
        return html.Img(src = '/assets/constellations/andromeda.png', style={'width': '100%'})
    elif value == 'Antlia':
        return html.Img(src = '/assets/constellations/antlia.png', style={'width': '100%'})
    elif value == 'Aquarius':
        return html.Img(src = '/assets/constellations/aquarius.png', style={'width': '100%'})
    elif value == 'Aquila':
        return html.Img(src = '/assets/constellations/aquila.png', style={'width': '100%'})
    elif value == 'Aries':
        return html.Img(src = '/assets/constellations/aries.png', style={'width': '100%'})
    elif value == 'Auriga':
        return html.Img(src = '/assets/constellations/auriga.png', style={'width': '100%'})
    elif value == 'Bootes':
        return html.Img(src = '/assets/constellations/bootes.png', style={'width': '100%'})
    elif value == 'Caelum':
        return html.Img(src = '/assets/constellations/caelum.png', style={'width': '100%'})
    elif value == 'Cancer':
        return html.Img(src = '/assets/constellations/cancer.png', style={'width': '100%'})
    elif value == 'Cane':
        return html.Img(src = '/assets/constellations/canes.png', style={'width': '100%'})
    elif value == 'Canis Major':
        return html.Img(src = '/assets/constellations/canis-major.png', style={'width': '100%'})
    elif value == 'Canis Minor':
        return html.Img(src = '/assets/constellations/canis-minor.png', style={'width': '100%'})
    elif value == 'Capricornus':
        return html.Img(src = '/assets/constellations/capricornus.png', style={'width': '100%'})
    elif value == 'Centaurus':
        return html.Img(src = '/assets/constellations/centaurus.png', style={'width': '100%'})
    elif value == 'Cetus':
        return html.Img(src = '/assets/constellations/cetus.png', style={'width': '100%'})
    elif value == 'Columba':
        return html.Img(src = '/assets/constellations/columba.png', style={'width': '100%'})
    elif value == 'Coma-Berenices':
        return html.Img(src = '/assets/constellations/coma-berenices.png	', style={'width': '100%'})
    elif value == 'Corona-Australis':
        return html.Img(src = '/assets/constellations/corona-australis.png	', style={'width': '100%'})
    elif value == 'Corona-Borealis':
        return html.Img(src = '/assets/constellations/corona-borealis.png	', style={'width': '100%'})
    elif value == 'Corvus':
        return html.Img(src = '/assets/constellations/corvus-constellations.png', style={'width': '100%'})
    elif value == 'Crater':
        return html.Img(src = '/assets/constellations/crater-constellations.png', style={'width': '100%'})
    elif value == 'Cygnus':
        return html.Img(src = '/assets/constellations/cygnus-constellations.png', style={'width': '100%'})
    elif value == 'Delphinus':
        return html.Img(src = '/assets/constellations/delphinus-constellations.png', style={'width': '100%'})
    elif value == 'Equuleus':
        return html.Img(src = '/assets/constellations/equuleus-constellations.png', style={'width': '100%'})
    elif value == 'Eridanus':
        return html.Img(src = '/assets/constellations/eridanus-constellations.png', style={'width': '100%'})
    elif value == 'Fornax':
        return html.Img(src = '/assets/constellations/fornax-constellations.png', style={'width': '100%'})
    elif value == 'Gemini':
        return html.Img(src = '/assets/constellations/gemini-zodiac.png	', style={'width': '100%'})
    elif value == 'Grus':
        return html.Img(src = '/assets/constellations/grus-constellations.png	', style={'width': '100%'})
    elif value == 'Hercules':
        return html.Img(src = '/assets/constellations/hercules.png', style={'width': '100%'})
    elif value == 'Hydra':
        return html.Img(src = '/assets/constellations/hydra.png', style={'width': '100%'})
    elif value == 'Lacerta':
        return html.Img(src = '/assets/constellations/lacerta.png', style={'width': '100%'})
    elif value == 'Leo Minor':
        return html.Img(src = '/assets/constellations/leo-minor.png', style={'width': '100%'})
    elif value == 'Leo':
        return html.Img(src = '/assets/constellations/leo-zodiac.png', style={'width': '100%'})
    elif value == 'Lepus':
        return html.Img(src = '/assets/constellations/lepus.png', style={'width': '100%'})
    elif value == 'Libra':
        return html.Img(src = '/assets/constellations/libra.png', style={'width': '100%'})
    elif value == 'Lupus':
        return html.Img(src = '/assets/constellations/lupus.png', style={'width': '100%'})
    elif value == 'Lynx':
        return html.Img(src = '/assets/constellations/lynx.png', style={'width': '100%'})
    elif value == 'Lyra':
        return html.Img(src = '/assets/constellations/lyra.png', style={'width': '100%'})
    elif value == 'Microscopium':
        return html.Img(src = '/assets/constellations/microscopium.png', style={'width': '100%'})
    elif value == 'Monoceros':
        return html.Img(src = '/assets/constellations/monoceros.png', style={'width': '100%'})
    elif value == 'Ophiuchus':
        return html.Img(src = '/assets/constellations/ophiuchus.png', style={'width': '100%'})
    elif value == 'Orion':
        return html.Img(src = '/assets/constellations/orion.png', style={'width': '100%'})
    elif value == 'Pegasus':
        return html.Img(src = '/assets/constellations/pegasus.png', style={'width': '100%'})
    elif value == 'Perseus':
        return html.Img(src = '/assets/constellations/perseus.png', style={'width': '100%'})
    elif value == 'Pisces':
        return html.Img(src = '/assets/constellations/pisces.png', style={'width': '100%'})
    elif value == 'Pisces-Austrinus':
        return html.Img(src = '/assets/constellations/piscis-austrinus.png', style={'width': '100%'})
    elif value == 'Puppis':
        return html.Img(src = '/assets/constellations/puppis.png', style={'width': '100%'})
    elif value == 'Pyxis':
        return html.Img(src = '/assets/constellations/pyxis.png', style={'width': '100%'})
    elif value == 'Sagitta':
        return html.Img(src = '/assets/constellations/sagitta.png', style={'width': '100%'})
    elif value == 'Sagittarius':
        return html.Img(src = '/assets/constellations/sagittarius.png', style={'width': '100%'})
    elif value == 'Scorpius':
        return html.Img(src = '/assets/constellations/scorpius.png', style={'width': '100%'})
    elif value == 'Sculptor':
        return html.Img(src = '/assets/constellations/sculptor.png', style={'width': '100%'})
    elif value == 'Scutum':
        return html.Img(src = '/assets/constellations/scutum.png', style={'width': '100%'})
    elif value == 'Sextans':
        return html.Img(src = '/assets/constellations/sextans.png', style={'width': '100%'})
    elif value == 'Taurus':
        return html.Img(src = '/assets/constellations/taurus.png', style={'width': '100%'})
    elif value == 'Triangulum':
        return html.Img(src = '/assets/constellations/triangulum.png', style={'width': '100%'})
    elif value == 'Vela':
        return html.Img(src = '/assets/constellations/vela.png', style={'width': '100%'})
    elif value == 'Virgo':
        return html.Img(src = '/assets/constellations/virgo.png', style={'width': '100%'})

@app.callback(
    dash.dependencies.Output('textbox', 'value'),
    [dash.dependencies.Input('my-dropdown', 'value')])
def output(value):
    if value == 'Andromeda':
        return androm
    elif value == 'Antlia':
        return antlia
    elif value == 'Aquarius':
        return aquarius
    elif value == 'Aquila':
        return aquila
    elif value == 'Aries':
        return aries
    elif value == 'Auriga':
        return auriga
    elif value == 'Bootes':
    	return boo
    elif value == 'Caelum':
    	return cael
    elif value == 'Cancer':
    	return canc
    elif value == 'Cane':
    	return cane
    elif value == 'Canis Major':
        return can_maj
    elif value == 'Canis Minor':
    	return can_min
    elif value == 'Capricornus':
        return cap
    elif value == 'Centaurus':
    	return cent
    elif value == 'Cetus':
        return cet
    elif value == 'Columba':
        return col
    elif value == 'Coma-Berenices':
        return comab
    elif value == 'Corona-Australis':
        return cor_aus
    elif value == 'Corona-Borealis':
        return cor_bor
    elif value == 'Corvus':
        return corv
    elif value == 'Crater':
        return crat
    elif value == 'Cygnus':
        return cyg
    elif value == 'Delphinus':
        return delph
    elif value == 'Equuleus':
        return equ
    elif value == 'Eridanus':
        return erid
    elif value == 'Fornax':
        return forn
    elif value == 'Gemini':
        return gem
    elif value == 'Grus':
        return grus
    elif value == 'Hercules':
        return herc
    elif value == 'Hydra':
        return hyd
    elif value == 'Lacerta':
        return lac
    elif value == 'Leo Minor':
        return leom
    elif value == 'Leo':
        return leoz
    elif value == 'Lepus':
        return lep
    elif value == 'Libra':
        return lib
    elif value == 'Lupus':
        return lup
    elif value == 'Lynx':
        return lyn
    elif value == 'Lyra':
        return lyr
    elif value == 'Microscopium':
        return micro
    elif value == 'Monoceros':
        return mono
    elif value == 'Ophiuchus':
        return oph
    elif value == 'Orion':
        return Or
    elif value == 'Pegasus':
        return peg
    elif value == 'Perseus':
        return per
    elif value == 'Pisces':
        return pisc
    elif value == 'Pisces-Austrinus':
        return pisc_aus
    elif value == 'Puppis':
        return pup
    elif value == 'Pyxis':
        return pyx
    elif value == 'Sagitta':
        return sag
    elif value == 'Sagittarius':
        return sagit
    elif value == 'Scorpius':
        return sco
    elif value == 'Sculptor':
        return scul
    elif value == 'Scutum':
        return scut
    elif value == 'Sextans':
        return sext
    elif value == 'Taurus':
        return taur
    elif value == 'Triangulum':
        return tria
    elif value == 'Vela':
        return vela
    elif value == 'Virgo':
        return virg

    
@app.callback(
    Output('markd-container', 'children'),
    [Input('input-1', 'value'),
     Input('my-dropdown', 'value'),
     Input('intermediate-value', 'children')])
def on_click(mydropdown, input1, intermediatevalue):
    with open('magicsum.txt') as inFile: 
        try:
            magsum= json.load(inFile)
            return dcc.Markdown('''Constellation: {},
            Magic Square Order: {},
            Magic Number: {}'''.format(input1, mydropdown, magsum))
        except :
            return dcc.Markdown('''Constellation: {},
            Magic Square Order: {},
            Magic Number: No input data'''.format(input1, mydropdown))

@app.callback(dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('inter-btndecode', 'children'),
    dash.dependencies.Input('intermediate-value', 'children'),
    dash.dependencies.Input('inter-input', 'children'),
    dash.dependencies.Input('inter-dropd', 'children'),
    dash.dependencies.Input('inter-slider', 'children')])
def style_table(interbtndecode, intermediatevalue, interinput, interslider, interdropd):
    with open('magic.txt') as json_file:  
        be= json.load(json_file)
        bc = np.array(be)
    with open('z2.txt') as json_file:  
        slider= json.load(json_file)
    with open('z4.txt') as json_file:  
        button1= json.load(json_file)
        neg1= (button1*(-1))
    with open('x.txt') as json_file:  
        input1= json.load(json_file)
        e = int(input1)
        s = int(640/e)
    with open('z1.txt') as json_file:  
        zz= json.load(json_file)
    if e <= 2:
        return html.Table(
                    [html.Tr('That value is out of range')], 
                style={'font-size': 48, 'text-align': 'center', 'vertical-align': 'middle'})
    elif e >= 38:
        return html.Table(
                    [html.Tr('That value is out of range')], 
                style={'font-size': 48, 'text-align': 'center', 'vertical-align': 'middle'})
    else:
        if slider == 1:
            df = np.roll(bc, neg1, axis=1)
        elif slider == 2:
            df = np.flip(bc, 1)
            df = np.roll(df, neg1, axis=1)
        elif slider == 3:
            bd = np.rot90(bc, 2)
            df = np.roll(bd, neg1, axis=1)
        elif slider == 4:
            bd = np.flip(bc, 0)
            df = np.roll(bd, neg1, axis=1)
        elif slider == 5:
            bd = np.rot90(bc, 3)
            df = np.roll(bd, neg1, axis=1)
        elif slider == 6:
            bd = np.rot90(bc, 1)
            df = np.roll(bd, neg1, axis=1)
        elif slider == 7:
            bd = np.rot90(bc, 1)
            be = np.flip(bd, 1)
            df = np.roll(be, neg1, axis=1)
        else:
            bd = np.rot90(bc, 3)
            be = np.flip(bd, 1)
            df = np.roll(be, neg1, axis=1)
        def func20():
            hw1 = constellations["Andromeda"]
            hw2 = constellations["Andromeda1"]
            if zz == 'Andromeda':
                hw1 = hw1
                hw2 = hw2
                return(hw1, hw2)
            elif zz == 'Antlia':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Aquarius':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Aquila':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Aries':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Auriga':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Bootes':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Caelum':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Cancer':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Cane':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Canis Major':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Canis Minor':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Capricornus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Centaurus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Cetus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Columba':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Coma-Berenices':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Corona-Australis':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Corona-Borealis':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Corvus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Crater':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Cygnus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Delphinus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Equuleus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Eridanus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Fornax':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Gemini':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Grus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Hercules':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Hydra':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Lacerta':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Leo Minor':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Leo':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Lepus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Libra':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Lupus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Lynx':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Lyra':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Microscopium':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Monoceros':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Ophiuchus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Orion':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Pegasus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Perseus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Pisces':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Pisces-Austrinus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Puppis':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Pyxis':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Sagitta':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Sagittarius':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Scorpius':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Sculptor':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Scutum':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Sextans':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Taurus':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Triangulum':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Vela':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
            elif zz == 'Virgo':
                hw1 = constellations[zz]
                var = zz +'1'
                hw2 = constellations[var]
                return(hw1, hw2)
        dhg = func20()
        (pos1, pos2) = dhg
        hw1= np.array(pos1)
        hw2= np.array(pos2)
        hw1 = hw1//s
        hw2 = hw2//s
        hw1[hw1 == e] = (e-1)
        hw2[hw2 == e] = (e-1)
        kl = df[np.array(hw2), np.array(hw1)]
        k=[]
        for i in kl:
            k.append(i)
        df = df.tolist()
        df = pd.DataFrame(df)
        def k_color(val):
            if val in k:
                color = "#de3d96"
            else:
                color = "white"
            return "background: %s" % color
        gs = df.style\
            .applymap(k_color)\
            .set_properties(**{'border-color': 'black'})\
            .set_table_styles(
                 [{'selector': '.row_heading',
                   'props': [('display', 'none')]},
                  {'selector': '.blank.level0',
                   'props': [('display', 'none')]}])
        gs=gs.render()
        return dash_dangerously_set_inner_html.DangerouslySetInnerHTML(gs)


@app.callback(
    dash.dependencies.Output('decode-value', 'children'),
    [dash.dependencies.Input('intermediate-value', 'children'),
    dash.dependencies.Input('inter-input', 'children'),
    dash.dependencies.Input('inter-dropd', 'children'),
    dash.dependencies.Input('inter-slider', 'children'),
    dash.dependencies.Input('inter-btndecode', 'children'),])
def func(intermediatevalue, interinput, interdropd, interslider, interbtndecode):
    with open('x.txt') as json_file:  
        x1 = json.load(json_file)
    with open('z1.txt') as json_file:  
        zz = json.load(json_file)
    with open('z2.txt') as json_file:  
        z3 = json.load(json_file)
    with open('z4.txt') as json_file:  
        z5 = json.load(json_file)
        z5 = z5 * -1
        e = int(x1)
        s = int(640/e)
    with open('magic.txt') as json_file:  
        magic_square = json.load(json_file)
    if z3 == 1:
        bd = np.array(magic_square)
    elif z3 == 2:
        bc = np.array(magic_square)
        bd = np.flip(bc, 1)
    elif z3 == 3:
        bc = np.array(magic_square)
        bd = np.rot90(bc, 2)
    elif z3 == 4:
        bc = np.array(magic_square)
        bd = np.flip(bc, 0)
    elif z3 == 5:
        bc = np.array(magic_square)
        bd = np.rot90(bc, 3)
    elif z3 == 6:
        bc = np.array(magic_square)
        bd = np.rot90(bc, 1)
    elif z3 == 7:
        bc = np.array(magic_square)
        be = np.rot90(bc, 1)
        bd = np.flip(be, 1)
    else:
        bc = np.array(magic_square)
        be = np.rot90(bc, 3)
        bd = np.flip(be, 1)
    def func24():
        hw1 = constellations["Andromeda"]
        hw2 = constellations["Andromeda1"]
        if zz == 'Andromeda':
            hw1 = constellations["Andromeda"]
            hw2 = constellations["Andromeda1"]
            return(hw1, hw2)
        elif zz == 'Antlia':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Aquarius':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Aquila':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Aries':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Auriga':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Bootes':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Caelum':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Cancer':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Cane':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Canis Major':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Canis Minor':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Capricornus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Centaurus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Cetus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Columba':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Coma-Berenices':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Corona-Australis':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Corona-Borealis':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Corvus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Crater':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Cygnus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Delphinus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Equuleus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Eridanus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Fornax':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Gemini':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Grus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Hercules':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Hydra':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Lacerta':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Leo Minor':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Leo':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Lepus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Libra':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Lupus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Lynx':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Lyra':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Microscopium':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Monoceros':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Ophiuchus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Orion':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Pegasus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Perseus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Pisces':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Pisces-Austrinus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Puppis':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Pyxis':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Sagitta':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Sagittarius':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Scorpius':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Sculptor':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Scutum':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Sextans':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Taurus':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Triangulum':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Vela':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
        elif zz == 'Virgo':
            hw1 = constellations[zz]
            var = zz +'1'
            hw2 = constellations[var]
            return(hw1, hw2)
    dhg = func24()
    (pos1, pos2) = dhg
    l = (bd % 26)
    l[l == 0] = 26
    k = []
    hw1= np.array(pos1)
    hw2= np.array(pos2)
    hw1 = hw1//s
    hw2 = hw2//s
    hw1[hw1 == e] = (e-1)
    hw2[hw2 == e] = (e-1)
    de = dict(enumerate(string.ascii_uppercase, 1))
    l = np.roll(l, z5, axis=1)
    kl = l[np.array(hw2), np.array(hw1)]
    for i in kl:
        k.append(de[i])
    s = ''.join(k)
    with open('het.txt', 'w') as outfile:
        return json.dump(s, outfile)
 

@app.callback(dash.dependencies.Output('textbox-1', 'value'),
[dash.dependencies.Input('decode-value', 'children'),
dash.dependencies.Input('inter-btndecode', 'children'),
dash.dependencies.Input('inter-input', 'children')])
def update(interinput, interbtndecode, decodevalue):
    with open('x.txt') as json_file:  
        input1= json.load(json_file)
    num = int(input1)
    with open('z4.txt') as json_file:  
        z5 = json.load(json_file)
    mod_num = z5 % num
    with open('het.txt') as json_file:  
        text = json.load(json_file)
    return '{}. {}'.format(mod_num, text)

@app.callback(dash.dependencies.Output('intermediate-value6', 'children'),
[dash.dependencies.Input('decode-value', 'children'),
dash.dependencies.Input('button-2', 'n_clicks')])
def func(interinput, button2):
    if button2 >= 1:
        with open('het.txt') as json_file:  
            xx = json.load(json_file)
            xox=(len(xx))
            if xox == 4:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(6250, 4)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 2:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(2500, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 3:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 5:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(6250, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 6:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=6))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(31250, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 7:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(6250, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 8:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=4))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(1250, 4)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 9:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u', 'e'], repeat=3))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 10:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 10)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 11:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u', 'e'], repeat=6))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(93312, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 12:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u', 'e', 'o', 'a'], repeat=3))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 13:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u', 'e', 'o', 'a'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(65536, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 14:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(6250, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 15:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 10)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 16:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=4))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(1250, 4)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 17:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=5))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(f, 10)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 19:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=6))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(37500, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 20:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=4))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(1000, 5)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 24:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u'], repeat=6))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(31250, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)
            elif xox == 33:
                xx = str(xx)
                xx = (xx.lower())
                a = list(itertools.product(['a', 'e', 'i', 'o', 'u', 'e'], repeat=6))
                c = (len(a))
                y = nd.array(a)
                xy = list(itertools.chain(*a))
                f = int(c)
                q = (xx * f)
                e = zip(q, xy)
                x = list(zip(q, xy))
                merged1 = list(itertools.chain(*x))
                y = nd.array(merged1).reshape(93312, 6)
                h = [(''.join(i)) for i in y]
                h = str(h)
                with open('box2.txt', 'w', encoding="utf-8") as outfile:
                    return json.dump(h, outfile)


@app.callback(dash.dependencies.Output('textbox-2', 'value'), [dash.dependencies.Input('intermediate-value6', 'children')])
def update(intermediatevalue6):
        with open('box2.txt') as json_file:  
            asx = json.load(json_file)
            jj = asx.replace("', '", ", ")
            kc = jj.replace("['", "")
            kc = kc.replace("']", "")
            return(kc)

@app.callback(dash.dependencies.Output('textbox-3', 'value'),
[dash.dependencies.Input('intermediate-value6', 'children'),
dash.dependencies.Input('button-3', 'n_clicks')])
def func(intermediatevalue6, button3):
    if button3 >= 1:
        with open('box2.txt') as json_file:  
            adc = json.load(json_file)
            jj = adc.replace("', '", " ")
            kc = jj.replace("['", "")
            kc = kc.replace("a,", ",")
            kc = kc.replace("e,", ",")
            kc = kc.replace("o,", ",")
            kc = kc.replace("u,", ",")
            kc = kc.replace("i,", ",")
            kc = kc.replace("']", "")
            wrd = nltk.word_tokenize(kc)
            kj=[]
            from nltk.corpus import wordnet
            for i in wrd:
                if wn.synsets(i):
                    kj.append(i)
            skj = str(kj)
            jc = skj.replace(", ", "")
            kc = jc.replace("[", "")
            kc = kc.replace("]", "")
            kc = kc.replace("\''", ", ")
            kc = kc.replace("\'", "")
            klj = (len(kc))
            if klj == 0:
                return 'No results'
            else:
                return (kc)


if __name__ == '__main__':
    app.run_server(debug=True)
