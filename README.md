# Agvysta: atnaujinto dizaino demo

Demonstracinė **agvysta.lt** svetainės versija. Turinys yra originalus (perkeltas iš agvysta.lt), nuotraukos yra originalios įmonės nuotraukos, papildomai naudojami Pexels video. Kryptis: **subtilu, modernu, šiuolaikiška**.

## Peržiūra

- **Gyva versija:** <https://arvydastry.github.io/agvysta/> (GitHub Pages iš saugyklos <https://github.com/arvydastry/agvysta> `main` šakos šaknies). Atnaujinimas: `python3 build.py && python3 tools/check.py`, tada `git add -A && git commit -m "..." && git push`; Pages persigeneruoja per ~1 min. Failas `.nojekyll` reikalingas, kad Pages neapdorotų failų Jekyll.
- `python3 serve.py` ir atverti <http://localhost:8140/> (`.claude/launch.json` sukonfigūruotas, serverio pavadinimas `agvysta`).
- `?static=1` prie adreso išjungia judesį ir video (rodomi plakatai): patogu ekrano nuotraukoms.
- Visi puslapiai turi `noindex, nofollow`. Užklausos forma demonstracinė: tikrina laukus, bet duomenų niekur nesiunčia. EN / RU perjungikliai rodo pranešimą.

## Kryptis

**Dizaino perskaitymas:** B2B inžinerinių tinklų rangovas (generaliniai rangovai, vystytojai, institucijos). Kalba rami ir tiksli, daug realių faktų iš projektų sąrašo, jokio triukšmo.

| | Senoji svetainė (2014) | Demo |
|---|---|---|
| Fonas | balta / pilka, jQuery slankiklis | šviesus vėsus `#F2F3F1`, baltos plokštumos, tamsi poraštė |
| Akcentas | `#0079BE` | ta pati firminė mėlyna `#0079BE` (vienintelis akcentas), rašalas `#0E1A22` |
| Šriftai | Open Sans | **Archivo** (kintamas): tekstas 100 %, antraštės 112,5 % pločio (atkartoja platų AGVYSTA logotipą), žodinis ženklas 125 %; lietuviški rašmenys patikrinti (latin-ext) |
| Hero | 6 nuotraukų slankiklis, vienas šūkis | viso ekrano drono video (smėlis, vandens kanalas, pušynas), šūkis „Jūsų ateities projektų partneris“ išlaikytas, apačioje 4 paslaugų juosta kaip senojoje svetainėje |
| Logotipas | PNG 243×73 | perpieštas vektoriškai (SVG): žiedas su trimis bangomis + „AGVYSTA“. **Prieš paleidimą reikia originalaus vektorinio logotipo iš kliento.** |
| Formos | – | medija, kortelės, laukeliai 6 px; mygtukai, filtrai ir žymos pill |

### Judesys (santūrus, visur motyvuotas)

- Hero antraštė iškyla eilutėmis, video lėtai išryškėja; video valdymo mygtukas (pauzė / paleisti, WCAG 2.2.2).
- Turinys atsiranda slenkant (IntersectionObserver, be `scroll` klausytojų), faktų skaičiai prasisuka.
- Paslaugų rodyklė: užvedus pelę ant paslaugos, dešinėje lipniame rėmelyje keičiasi video (mobiliajame rodomi plakatai).
- Video kraunami ir groja tik matomoje srityje, paslėpus kortelę sustoja.
- „Apie mus“ laiko juosta: vamzdžio linija užsipildo slenkant (CSS scroll-driven animation, kur palaikoma).
- Esant `prefers-reduced-motion` viskas rodoma iš karto, video neautomatiniai.

## v2: UX/UI patobulinimai (prieš šablonišką „AI“ stilių)

- **Mažiau šabloniškumo:** pašalintas mono šriftas ir „01, 02…“ numeracija visur, išskyrus 4 paslaugas; „Visi projektai —“ nuorodos su rodykle; jokių stiklinių žymų ir skaičių „pilulių“ ant nuotraukų.
- **Vienas veiksmo pavadinimas:** „Pateikti užklausą“ antraštėje, hero, paslaugose ir kontaktų bloke; antraštėje telefono numeris (nuo 1320 px).
- **Paslaugų meniu** su miniatiūromis ir trumpu aprašymu.
- **Įvadas:** teiginys + faktai 2×2 (2005, 50 000+ m, 150+, 3 sertifikuotos sistemos).
- **Paslaugų rodyklė:** prie kiekvienos paslaugos tikras projektų ir nuotraukų skaičius.
- **„Sąlygos“** (vienintelis tamsus blokas): 5 sąlygos (šlapi gruntai, dideli gyliai, ankštos sąlygos, įšalo laužymas, perėjimai), pasirinkus keičiasi originali nuotrauka arba video.
- **Atrinkti projektai:** tempimas pele, progreso juosta, nuotraukų skaičius metaduomenyse.
- **„Ilgiausios paklotos trasos“:** reitinguotos juostos pagal tikrus ilgius iš projektų sąrašo (8 objektai, iš viso 36 005 m 15 objektų).
- **Sertifikatai** išsiskleidžia vėduokle, užvedus pakyla.
- **Kontaktų blokas** be video: biuras, direktorius ir statybų vadovas su tiesioginiais telefonais.
- **Paslaugų puslapiai:** po hero tikri skaičiai (projektų sąraše, pirmasis objektas, nuotraukos), telefonas šalia užklausos.
- **Projektai:** filtrai dviem eilutėmis, jungiklis „Su nuotraukomis“, „Išvalyti filtrus“; mobiliajame juosta nelipni, paieška per visą plotį.
- **Nuotraukų peržiūra:** miniatiūrų juosta.

## v3: užsakovų logotipai ir kalbų vėliavėlės

- Po hero: juosta „Tarp mūsų užsakovų“ su 13 užsakovų logotipų (vienspalviai, lėtai slenka, sustoja užvedus pelę; esant „mažiau judesio“ nustatymui stovi ir slenkama ranka). Šaltiniai: [`docs/logotipai.md`](docs/logotipai.md).
- Meniu: LT / EN / RU vėliavėlės (tik dizainas, vertimų nėra; paspaudus EN ar RU rodomas pranešimas). Mobiliajame meniu vėliavėlės su kalbų pavadinimais.

## v4: gylis ir parallax

Visi efektai yra CSS scroll-driven animations (`animation-timeline: view()`): be JS `scroll` klausytojų, animuojamos tik `translate`, `scale` ir `opacity`. Veikia Chrome, Edge ir Safari 26+; kitur viskas tiesiog statiška. Esant „mažiau judesio“ nustatymui niekas nejuda.

- **Hero:** video slenka lėčiau nei puslapis, antraštė ir tekstas kyla ir blunka, paslaugų juosta išnyksta; antraštė tampa vientisa praslinkus ketvirtadalį hero.
- **Vaizdas rėmelyje** (`.px-in`): projektų kortelės, „Sąlygos“, paslaugų galerijos, paslaugų ir karjeros hero video, kontaktų nuotrauka.
- **Sluoksniai skirtingais greičiais** (`.px`, `--par`): faktai, sertifikatų vėduoklė (gilesni lapai juda daugiau), „Apie mus“ koliažas, sertifikatai „Apie mus“, karjeros nuotraukų juosta (banga).
- **Įplaukimas iš gylio** (`.rise`): paslaugų video rėmelis, „Sąlygos“ vaizdas, kontaktų blokas.
- **Vidinių puslapių hero** video slenkant „nugrimzta“ (mažėja ir lėtėja).
- **„Ilgiausios paklotos trasos“:** fone didelis kontūrinis „36 005 m“, slenkantis horizontaliai.
- Telefone parallax amplitudė perpus mažesnė (`--pk: .5`).

## v5: hero iš originalių nuotraukų, užsakovų sienelė

- **Hero:** vietoj Pexels video lėta originalių agvysta.lt projektų nuotraukų kaita (4 didelės raiškos nuotraukos: Aukštaičių g. 10, Linkmenų g. 22 ×2, Verkių g. 29), švelnus priartinimas, keičiasi kas 6,5 s, sustoja kai hero nematomas; pauzės mygtukas apačioje dešinėje. Nuotraukos `assets/img/agvysta/hero/h1-h4` (2400 ir 1280 px).
- **„Užsakovai, kuriems dirbome“:** visų 36 užsakovų sienelė. 16 su logotipais (vienspalviai), kitiems 20 rodomas pavadinimas su teisine forma; kiekvienoje plytelėje objektų skaičius. Logotipų šaltiniai: [`docs/logotipai.md`](docs/logotipai.md).

## v6: naujas hero ir Archivo šriftas

Sprendimas parinktas darbo eiga (workflow): 4 šriftų poros su patikrintu lietuviškų raidžių palaikymu, 3 hero kryptys su prototipais, 3 vertintojai (stilius, AI šabloniškumas, techninė kokybė), tada kritinė peržiūra su 18 patvirtintų ir ištaisytų radinių.

- **Šriftas:** Archivo (Google Fonts, kintamas `wdth 100..125`, `wght 300..800`). Antraštės (`--display`, `--wide: 112.5%`), tekstas 100 %, logotipo žodis 125 % / 800. Atsarginiai šriftai sulyginti metrikomis (mažiau šokinėja kraunantis).
- **Hero „įrėmintas skydas“:** nuotraukų skydas atitrauktas nuo lango krašto (12 px, telefone 8 px), suapvalintas; dešiniame apatiniame kampe puslapio spalvos išpjova su 4 paslaugomis (lygiuota su 1360 px tinkleliu ir antraštės mygtuku). Istorijų tipo progreso juosta (mygtukai = navigacija), pauzė, po juosta dabartinės nuotraukos objektas (adresas, darbai ir metai, užsakovas). Kiekvienai nuotraukai savas tamsinimo stiprumas (`tone` faile `content/site.json`), kontrastas patikrintas pikseliais visose 4 nuotraukose.
- **Judesys:** nuotrauka įsislenka „užuolaida“ iš kairės, lėtas priartinimas; slenkant tekstas kyla greičiau, nuotrauka lėčiau, skydas šiek tiek tolsta. Kitos nuotraukos kraunamos tik po pirmosios, po vieną.
- **Pataisyta peržiūroje:** antraštė dabar tampa vientisa slenkant pele (anksčiau stebėtojas niekada nesuveikdavo), telefone turinys toliau nuo skydo krašto, projektų puslapis telefone nebeplatėja (perjungiklio klaida), meniu atidarius puslapis už jo neaktyvus (`inert`), baltas fokuso žiedas virš nuotraukų, kontrasto ir tipografijos smulkmenos (našlaitės, nedalomi tarpai prie „g.“, „ISO 9001“), „Spec. paslaugos“ pervadinta „Specialiosios paslaugos“.

## v7: spalvota logotipų juosta, naujas įvadas

- **Logotipų juosta po hero:** be užrašo (tik `aria-label`), spalvoti logotipai (`assets/img/klientai/spalvoti/`, balti elementai perdažyti tamsiai, kad matytųsi šviesiame fone), begalinė juosta per visą lango plotį, sustoja užvedus pelę. Ramaus režimo atveju juosta stovi ir slenkama ranka.
- **Įvadas „Įrengiame lauko vandentiekio...“:** ramus redakcinis blokas ant 4 stulpelių tinklelio (tų pačių kaip faktų). Kairiame stulpelyje nuoroda „Apie įmonę“ (telefone po teiginiu), per kitus tris teiginys įprasto pločio Archivo, 400 storio. Slenkant teiginys „įsigeria“: iš pradžių jis blyškus (`--pre`), raidės minkšta banga tamsėja, kol teksto viršus slenka nuo ~88 % iki ~30 % ekrano aukščio (dydžiai `--s`, `--e`, `--w` faile `style.css`). Ant blyškaus pagrindinio teksto uždėta `aria-hidden`, `inert` kopija, todėl ekrano skaitytuvai, žymėjimas, paieška ir vertimas veikia įprastai; kopijos eilutės laužomos ten pat, kur pagrindinio teksto. Tamsėjimą po žodį įjungia `data-read="word"` faile `templates/index.html`. Faktai po teiginiu: virš kiekvieno plona linija, kuri slenkant iš eilės užsipildo mėlyna, o skaičius iškyla. Iki 900 px faktai 2 × 2. Peržiūrėjus būsena užrakinama (grįžtant niekas nebejuda). Judesys valdomas CSS `animation-timeline: view()`, kitur IntersectionObserver; ramiame režime iškart galutinis vaizdas.
- **„Užsakovai, kuriems dirbome“:** vietoje statiškos sienelės trys per visą plotį slenkančios eilutės po 12 užsakovų (1 ir 3 slenka į kairę, 2 į dešinę), be rėmelių: vienspalviai logotipai ir pavadinimai (be teisinės formos) laisvai plaukia, kraštai išblunka. Sustoja užvedus pelę ant eilutės, paspaudus mygtuką šalia pastabos ir kai yra už ekrano ribų. Ekrano skaitytuvui paslėptas visų 36 užsakovų sąrašas (pagal objektų skaičių); be JS ir ramiame režime visi užsakovai vienu ramiu centruotu bloku. Eilutes sudaro `client_rows()` faile `build.py` (logotipai ir pavadinimai paskirstomi tolygiai).

## Puslapiai

Puslapių adresai (slug) **tokie pat kaip senojoje svetainėje** (SEO).

| Puslapis | Failas | Turinys |
|---|---|---|
| Pradžia | `index.html` | video hero, įmonės teiginys ir 4 faktai, interaktyvi paslaugų rodyklė, „Sąlygos“, atrinktų projektų karuselė, ilgiausios trasos, sertifikatai, užsakovai, kontaktų blokas |
| 4 paslaugos | `lauko-inzineriniu-tinklu-montavimas.html`, `siurbliniu-...-montavimas.html`, `zemes-darbai-ir-gerbuvio-darbai-2.html`, `spec-paslaugos-...-isalo-lauzymas.html` | hero su video, „Ką atliekame“ (originalūs punktai), originalių nuotraukų galerija su peržiūra (36 / 15 / 8 / 16), susiję projektai (pirmiausia su nuotraukomis), kitos paslaugos |
| Projektai | `projektai.html` | 8 vykdomi + 55 atlikti projektai, sugrupuoti pagal metus; filtrai (būsena, paslauga, paieška be diakritikų, „su nuotraukomis“), galerijos. `?k=tinklai|siurblines|zemes|spec` ir `?b=vykdomi|atlikti` atidaro su filtru |
| Apie mus | `apie-mus.html` | Dirbame / Esame, „Galime“ (9 punktai, 3 grupės), laiko juosta iš tikrų projektų (2005-šiandien), kokybės, aplinkosaugos ir DSS politika (`#kokybes-politika`, buvęs `kokybes-politika.html`), sertifikatai |
| Karjera | `karjera.html` | originalus tekstas, „Ką žadame komandai“ (iš kokybės politikos), nuotraukų juosta |
| Kontaktai | `kontaktai.html` | telefonas, el. paštas (kopijavimas), adresas, OpenStreetMap žemėlapis, rekvizitai, 4 darbuotojų kontaktai, užklausos forma |
| Duomenų apsauga | `duomenu-apsauga.html` | originalus privatumo ir slapukų politikos tekstas |

### Turinio pakeitimai (redakciniai, ne prasmės)

- Projektų pavadinimų klaidos pataisytos („mokslninių“, „Daugiafukcinis“, „sandėlys“, sulipę žodžiai), užsakovų pavadinimai suvienodinti (UAB „Lakaja“, ne UAB "LAKAJA").
- Privataus asmens vardas projektų sąraše pakeistas į „Privatus užsakovas“.
- Ilgieji brūkšniai pakeisti trumpais arba sakinys perrašytas be jų (demo tipografinė taisyklė).
- Telefonai pateikti tarptautiniu formatu (+370 ...).
- Nauji trumpi tekstai (hero paantraštė, sekcijų antraštės, CTA) sudaryti tik iš originalaus turinio faktų.

## Struktūra ir generavimas

```
build.py                 # python3 build.py -> sugeneruoja visus *.html (reikia jinja2, Pillow)
tools/prepare.py         # content/projektai-raw.json -> content/projektai.json (valymas, kategorijos, metai, ilgiai)
tools/check.py           # statinė patikra: nuorodos, inkarai, failai, h1, alt, ilgieji brūkšniai, iCloud
tools/shot.py            # ekrano nuotrauka headless Chrome: python3 tools/shot.py <url> 1440 7600 out.png 1900
tools/hydrate.sh         # parsiunčia iCloud iškeltus failus atgal į diską (žr. žemiau)
templates/               # base, _macros, po vieną šabloną puslapiui
content/site.json        # įmonė, paslaugos, faktai, apie, kokybė, karjera, darbuotojai
content/projektai*.json  # 63 projektai (originalūs ir sutvarkyti)
assets/css/style.css     # dizaino sistema
assets/js/main.js        # elgsena (vanilla JS)
assets/img/agvysta/      # 140 originalių agvysta.lt nuotraukų, WebP 1600 ir 800 px (~30 MB)
assets/video/            # 6 Pexels video + plakatai (žr. docs/pexels-credits.md)
_originals/              # originalūs nuotraukų failai iš agvysta.lt (~50 MB, .gitignore)
```

Darbo eiga: pakeisti `content/*.json` arba `templates/*`, tada `python3 build.py && python3 tools/check.py`.

## Svarbu: iCloud Drive

Projektas yra `~/Documents` (iCloud Drive), o diske laisvos vietos ~5 %. macOS tokiu atveju iškelia failus į debesį („dataless“), ir vietinis serveris juos grąžina tuščius (dingsta nuotraukos ar video). Sprendimai: Finder'yje ant `Agvysta` aplanko pasirinkti **Keep Downloaded** arba atlaisvinti vietos diske. Laikinai padeda `sh tools/hydrate.sh`; `tools/check.py` tokius failus parodo.

## Prieš paleidžiant

- Originalus logotipas vektoriniu formatu.
- Naujesnės objektų nuotraukos (dabartinės 2009-2014 m., kompaktinio fotoaparato kokybės).
- Atnaujinti projektų sąrašą (paskutiniai įrašai 2018 m.) ir patikslinti, ar 50 000 m / 150+ objektų skaičiai vis dar aktualūs.
- EN ir RU versijos, tikras formos siuntimas, slapukų juosta.
